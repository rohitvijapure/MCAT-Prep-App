from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class StudyModuleResponse(BaseModel):
    """Schema for study module response"""

    id: int
    title: str
    mcat_section: str
    topic_id: Optional[int]
    content_type: str
    content: Dict[str, Any]
    order_index: Optional[int]
    estimated_time_minutes: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class TopicResponse(BaseModel):
    """Schema for topic response"""

    id: int
    name: str
    mcat_section: str
    description: Optional[str]
    difficulty_level: Optional[int]

    class Config:
        from_attributes = True


class AAMCConceptResponse(BaseModel):
    """Schema for AAMC foundational concept response"""

    id: int
    concept_code: str
    mcat_section: str
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True


class UserStudyProgressResponse(BaseModel):
    """Schema for user study progress response"""

    study_module_id: int
    status: str
    time_spent_seconds: int
    completed_at: Optional[datetime]
    last_accessed_at: datetime

    class Config:
        from_attributes = True
