from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps.auth import get_current_user
from app.models.user import User
from app.models.content import StudyModule, Topic
from app.schemas.study import StudyModuleResponse, TopicResponse

router = APIRouter()


@router.get("/modules", response_model=List[StudyModuleResponse])
async def get_study_modules(
    mcat_section: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all study modules, optionally filtered by MCAT section"""
    query = db.query(StudyModule)
    if mcat_section:
        query = query.filter(StudyModule.mcat_section == mcat_section)
    modules = query.order_by(StudyModule.order_index).all()
    return modules


@router.get("/topics", response_model=List[TopicResponse])
async def get_topics(
    mcat_section: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all topics, optionally filtered by MCAT section"""
    query = db.query(Topic)
    if mcat_section:
        query = query.filter(Topic.mcat_section == mcat_section)
    topics = query.all()
    return topics
