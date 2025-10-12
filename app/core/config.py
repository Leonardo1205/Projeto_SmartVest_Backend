from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartVest API"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    OAUTH_BASE_URL: str = "http://127.0.0.1:8000"
    FRONTEND_URL: str = "http://localhost:5173"

    CORS_ORIGINS: List[AnyHttpUrl] | List[str] = ["http://localhost:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_csv(cls, v):
        # aceita lista ou string separada por vírgula
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
