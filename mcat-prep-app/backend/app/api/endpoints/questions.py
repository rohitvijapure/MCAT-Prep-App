from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from uuid import UUID
from app.core.database import get_db
from app.api.deps.auth import get_current_user
from app.models.user import User
from app.models.content import Question, Passage
from app.models.test import UserQuestionAttempt
from app.models.progress import ReviewQueue
from app.schemas.question import (
    QuestionResponse,
    QuestionWithAnswer,
    QuestionAttempt,
    QuestionAttemptResponse,
    PassageResponse,
)

router = APIRouter()


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a question by ID (without answer)"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.get("/", response_model=List[QuestionResponse])
async def get_questions(
    mcat_section: Optional[str] = Query(None),
    topic_id: Optional[int] = Query(None),
    difficulty_level: Optional[int] = Query(None),
    question_type: Optional[str] = Query(None),
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get questions with filters"""
    query = db.query(Question)

    if mcat_section:
        query = query.filter(Question.mcat_section == mcat_section)
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if difficulty_level:
        query = query.filter(Question.difficulty_level == difficulty_level)
    if question_type:
        query = query.filter(Question.question_type == question_type)

    # Random order for quiz generation
    query = query.order_by(func.random())
    questions = query.limit(limit).offset(offset).all()

    return questions


@router.post("/attempt", response_model=QuestionAttemptResponse)
async def submit_question_attempt(
    attempt: QuestionAttempt,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit a question attempt and get immediate feedback"""

    # Get the question
    question = db.query(Question).filter(Question.id == attempt.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if answer is correct
    is_correct = attempt.selected_answer == question.correct_answer

    # Save the attempt
    user_attempt = UserQuestionAttempt(
        user_id=current_user.id,
        question_id=attempt.question_id,
        test_attempt_id=attempt.test_attempt_id,
        selected_answer=attempt.selected_answer,
        is_correct=is_correct,
        time_spent_seconds=attempt.time_spent_seconds,
        is_flagged=attempt.is_flagged,
        attempt_mode=attempt.attempt_mode,
        confidence_level=attempt.confidence_level,
    )

    db.add(user_attempt)

    # Update question statistics
    question.times_answered += 1

    # Add to review queue if incorrect or flagged
    if not is_correct or attempt.is_flagged:
        # Check if already in review queue
        existing_review = (
            db.query(ReviewQueue)
            .filter(
                ReviewQueue.user_id == current_user.id,
                ReviewQueue.question_id == attempt.question_id,
            )
            .first()
        )

        if not existing_review:
            review_item = ReviewQueue(
                user_id=current_user.id,
                question_id=attempt.question_id,
                priority=5 if not is_correct else 3,
                last_attempt_id=user_attempt.id,
            )
            db.add(review_item)
        else:
            # Update priority if question was incorrect
            if not is_correct:
                existing_review.priority = min(existing_review.priority + 1, 10)

    db.commit()
    db.refresh(user_attempt)

    return {
        "id": user_attempt.id,
        "question_id": question.id,
        "is_correct": is_correct,
        "selected_answer": attempt.selected_answer,
        "correct_answer": question.correct_answer,
        "correct_explanation": question.correct_explanation,
        "incorrect_explanations": question.incorrect_explanations,
        "time_spent_seconds": attempt.time_spent_seconds,
    }


@router.get("/passage/{passage_id}", response_model=PassageResponse)
async def get_passage(
    passage_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a passage by ID"""
    passage = db.query(Passage).filter(Passage.id == passage_id).first()
    if not passage:
        raise HTTPException(status_code=404, detail="Passage not found")
    return passage
