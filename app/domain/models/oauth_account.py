from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, UniqueConstraint, ForeignKey
from app.db.base import Base

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    __table_args__ = (UniqueConstraint("provider","provider_user_id", name="uq_provider_pid"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(30), nullable=False)            # 'google'
    provider_user_id = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
