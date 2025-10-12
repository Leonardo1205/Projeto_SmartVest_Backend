from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.api.v1.routes.auth import router as auth_router
from app.db.session import engine
from app.db.base import Base
from app.domain.models import user as _user
from app.domain.models import oauth_account as _oauth
from app.api.v1.routes.oauth_google import router as google_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(google_router, prefix=settings.API_V1_STR)
    app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)

    @app.on_event("startup")
    async def on_startup():
        Base.metadata.create_all(bind=engine)  # em prod, prefira Alembic

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app

app = create_app()
