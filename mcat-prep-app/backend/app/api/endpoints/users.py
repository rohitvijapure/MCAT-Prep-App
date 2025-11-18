from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile"""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.target_mcat_score is not None:
        current_user.target_mcat_score = user_update.target_mcat_score
    if user_update.target_exam_date is not None:
        current_user.target_exam_date = user_update.target_exam_date

    db.commit()
    db.refresh(current_user)
    return current_user
