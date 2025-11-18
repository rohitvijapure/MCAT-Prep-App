from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from uuid import UUID
import uuid
from app.core.database import get_db
from app.api.deps.auth import get_current_user
from app.models.user import User
from app.models.test import PracticeTest, UserTestAttempt
from app.models.content import Question
from app.schemas.test import (
    QuizCreateRequest,
    PracticeTestResponse,
    TestAttemptResponse,
    TestAttemptStart,
)

router = APIRouter()


@router.post("/quiz/create", response_model=PracticeTestResponse)
async def create_custom_quiz(
    quiz_request: QuizCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a custom quiz based on user preferences"""

    # Query questions based on filters
    query = db.query(Question)

    if quiz_request.mcat_section:
        query = query.filter(Question.mcat_section == quiz_request.mcat_section)
    if quiz_request.topic_ids:
        query = query.filter(Question.topic_id.in_(quiz_request.topic_ids))
    if quiz_request.difficulty_level:
        query = query.filter(Question.difficulty_level == quiz_request.difficulty_level)
    if quiz_request.question_type:
        query = query.filter(Question.question_type == quiz_request.question_type)

    # Get random questions
    questions = query.order_by(func.random()).limit(quiz_request.num_questions).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found matching the criteria")

    # Create practice test
    section_title = quiz_request.mcat_section or "Mixed Sections"
    practice_test = PracticeTest(
        test_type="custom_quiz",
        title=f"Custom Quiz - {section_title}",
        description=f"{len(questions)} questions",
        sections=[
            {
                "section": quiz_request.mcat_section or "mixed",
                "duration_minutes": len(questions) * 2,  # ~2 min per question
                "question_ids": [str(q.id) for q in questions],
            }
        ],
        total_questions=len(questions),
        total_duration_minutes=len(questions) * 2,
    )

    db.add(practice_test)
    db.commit()
    db.refresh(practice_test)

    return practice_test


@router.post("/attempt/start", response_model=TestAttemptResponse)
async def start_test_attempt(
    test_start: TestAttemptStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Start a new test attempt"""

    # Verify practice test exists
    practice_test = (
        db.query(PracticeTest).filter(PracticeTest.id == test_start.practice_test_id).first()
    )
    if not practice_test:
        raise HTTPException(status_code=404, detail="Practice test not found")

    # Create test attempt
    attempt = UserTestAttempt(
        user_id=current_user.id,
        practice_test_id=test_start.practice_test_id,
        total_questions=practice_test.total_questions,
        status="in_progress",
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


@router.get("/attempts", response_model=List[TestAttemptResponse])
async def get_user_test_attempts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all test attempts for current user"""
    attempts = (
        db.query(UserTestAttempt)
        .filter(UserTestAttempt.user_id == current_user.id)
        .order_by(UserTestAttempt.started_at.desc())
        .all()
    )
    return attempts
