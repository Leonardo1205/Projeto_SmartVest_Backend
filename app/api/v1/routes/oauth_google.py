# app/api/v1/routes/oauth_google.py
from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token, hash_password
from app.core.config import settings
from app.domain.models.oauth_account import OAuthAccount  # <— importe o modelo

router = APIRouter(tags=["oauth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

repo = UserRepository()
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = f"{settings.OAUTH_BASE_URL}{settings.API_V1_STR}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri, prompt="select_account")

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo:
        resp = await oauth.google.get("userinfo", token=token)
        userinfo = resp.json()

    email = userinfo["email"]
    nickname = (userinfo.get("given_name") or email.split("@")[0])[:60]
    provider_user_id = userinfo["sub"]
    email_verified = bool(userinfo.get("email_verified"))

    # upsert usuário
    user = repo.get_by_email(db, email)
    if not user:
        user = repo.create(
            db,
            nickname=nickname,
            email=email,
            password_hash=hash_password("oauth_google_dummy"),
        )

    # upsert oauth_accounts usando ORM (sem SQL cru)
    oa = (
        db.query(OAuthAccount)
        .filter(
            OAuthAccount.provider == "google",
            OAuthAccount.provider_user_id == provider_user_id,
        )
        .first()
    )
    if not oa:
        oa = OAuthAccount(
            user_id=user.id,
            provider="google",
            provider_user_id=provider_user_id,
            email_verified=email_verified,
        )
        db.add(oa)
    else:
        oa.user_id = user.id
        oa.email_verified = email_verified

    db.commit()

    jwt = create_access_token(sub=str(user.id))
    return RedirectResponse(f"{settings.FRONTEND_URL}/oauth/callback?token={jwt}")
