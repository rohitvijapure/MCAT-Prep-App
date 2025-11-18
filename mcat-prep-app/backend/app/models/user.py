from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # NULL if OAuth only
    full_name = Column(String(255), nullable=False)
    target_mcat_score = Column(Integer, nullable=True)
    target_exam_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String(50), default="free")  # free, premium, pro

    def __repr__(self):
        return f"<User {self.email}>"
