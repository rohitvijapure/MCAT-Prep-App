from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class UserCreate(BaseModel):
    """Schema for user registration"""

    email: EmailStr
    password: str
    full_name: str
    target_mcat_score: Optional[int] = None
    target_exam_date: Optional[date] = None


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response"""

    id: UUID
    email: str
    full_name: str
    target_mcat_score: Optional[int]
    target_exam_date: Optional[date]
    subscription_tier: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserUpdate(BaseModel):
    """Schema for updating user profile"""

    full_name: Optional[str] = None
    target_mcat_score: Optional[int] = None
    target_exam_date: Optional[date] = None
