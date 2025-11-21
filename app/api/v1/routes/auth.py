from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import LoginRequest, TokenResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.security import get_current_subject

router = APIRouter(tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

repo = UserRepository()
user_service = UserService(repo)
auth_service = AuthService(repo)

@router.post("/auth/register", response_model=TokenResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = user_service.register(db, payload)
    token = auth_service.authenticate(db, email=user.email, password=payload.password)
    return TokenResponse(access_token=token)

@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.authenticate(db, email=payload.email, password=payload.password)
    return TokenResponse(access_token=token)

@router.get("/auth/me", response_model=UserRead)
def me(sub: str = Depends(get_current_subject), db: Session = Depends(get_db)):
    from app.domain.models.user import User
    user = db.get(User, int(sub))
    return UserRead.model_validate(user, from_attributes=True)
