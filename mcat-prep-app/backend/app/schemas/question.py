from pydantic import BaseModel
from typing import Optional, Dict, List
from uuid import UUID


class QuestionResponse(BaseModel):
    """Schema for question response"""

    id: UUID
    question_type: str
    mcat_section: str
    passage_id: Optional[UUID]
    question_text: str
    question_images: Optional[List[str]]
    options: Dict[str, str]  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    difficulty_level: Optional[int]
    tags: Optional[List[str]]
    estimated_time_seconds: int

    class Config:
        from_attributes = True


class QuestionWithAnswer(QuestionResponse):
    """Schema for question with correct answer and explanation"""

    correct_answer: str
    correct_explanation: str
    incorrect_explanations: Optional[Dict[str, str]]


class QuestionAttempt(BaseModel):
    """Schema for submitting a question attempt"""

    question_id: UUID
    selected_answer: str  # A, B, C, D, or X for omitted
    time_spent_seconds: int
    is_flagged: bool = False
    confidence_level: Optional[int] = None
    test_attempt_id: Optional[UUID] = None
    attempt_mode: str = "timed"  # 'timed', 'untimed', 'review'


class QuestionAttemptResponse(BaseModel):
    """Schema for question attempt response"""

    id: UUID
    question_id: UUID
    is_correct: bool
    selected_answer: str
    correct_answer: str
    correct_explanation: str
    incorrect_explanations: Optional[Dict[str, str]]
    time_spent_seconds: int

    class Config:
        from_attributes = True


class PassageResponse(BaseModel):
    """Schema for passage response"""

    id: UUID
    mcat_section: str
    passage_text: str
    passage_images: Optional[List[str]]

    class Config:
        from_attributes = True
