from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, db: Session, *, email: str, password: str) -> str:
        user = self.repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
        return create_access_token(sub=str(user.id))
