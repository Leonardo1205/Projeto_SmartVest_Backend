from sqlalchemy.orm import Session
from app.domain.models.user import User

class UserRepository:
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, nickname: str, email: str, password_hash: str) -> User:
        user = User(nickname=nickname, email=email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
