from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class QuizCreateRequest(BaseModel):
    """Schema for creating a custom quiz"""

    mcat_section: Optional[str] = None  # None = all sections
    topic_ids: Optional[List[int]] = None
    difficulty_level: Optional[int] = None
    num_questions: int = 10
    question_type: Optional[str] = None  # 'passage_based', 'standalone', None = mixed


class TestAttemptResponse(BaseModel):
    """Schema for test attempt response"""

    id: UUID
    practice_test_id: UUID
    started_at: datetime
    completed_at: Optional[datetime]
    status: str
    total_score: Optional[int]
    cpbs_score: Optional[int]
    cars_score: Optional[int]
    bbls_score: Optional[int]
    psbb_score: Optional[int]
    total_correct: Optional[int]
    total_questions: Optional[int]
    accuracy_percentage: Optional[int]

    class Config:
        from_attributes = True


class PracticeTestResponse(BaseModel):
    """Schema for practice test response"""

    id: UUID
    test_type: str
    title: str
    description: Optional[str]
    is_official_aamc: bool
    sections: List[Dict[str, Any]]
    total_questions: int
    total_duration_minutes: int

    class Config:
        from_attributes = True


class TestAttemptStart(BaseModel):
    """Schema for starting a test attempt"""

    practice_test_id: UUID


class TestAttemptComplete(BaseModel):
    """Schema for completing a test attempt"""

    test_attempt_id: UUID
