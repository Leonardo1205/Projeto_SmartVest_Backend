from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, db: Session, payload: UserCreate) -> UserRead:
        if self.repo.get_by_email(db, payload.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado")
        user = self.repo.create(
            db,
            nickname=payload.nickname,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        return UserRead.model_validate(user, from_attributes=True)
