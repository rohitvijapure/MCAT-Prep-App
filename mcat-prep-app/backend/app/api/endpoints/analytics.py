from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Dict, Any
from app.core.database import get_db
from app.api.deps.auth import get_current_user
from app.models.user import User
from app.models.test import UserQuestionAttempt, UserTestAttempt
from app.models.content import Question, AAMCFoundationalConcept
from app.models.progress import ReviewQueue

router = APIRouter()


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get comprehensive dashboard analytics for current user"""

    # Total questions answered
    total_questions = (
        db.query(func.count(UserQuestionAttempt.id))
        .filter(UserQuestionAttempt.user_id == current_user.id)
        .scalar()
    )

    # Total correct answers
    total_correct = (
        db.query(func.count(UserQuestionAttempt.id))
        .filter(UserQuestionAttempt.user_id == current_user.id, UserQuestionAttempt.is_correct == True)
        .scalar()
    )

    # Overall accuracy
    overall_accuracy = round((total_correct / total_questions * 100), 2) if total_questions > 0 else 0

    # Get latest test attempts with scores
    recent_tests = (
        db.query(UserTestAttempt)
        .filter(
            UserTestAttempt.user_id == current_user.id,
            UserTestAttempt.status == "completed",
        )
        .order_by(UserTestAttempt.completed_at.desc())
        .limit(10)
        .all()
    )

    score_history = [
        {
            "date": test.completed_at.isoformat(),
            "total_score": test.total_score,
            "accuracy": test.accuracy_percentage,
            "cpbs_score": test.cpbs_score,
            "cars_score": test.cars_score,
            "bbls_score": test.bbls_score,
            "psbb_score": test.psbb_score,
        }
        for test in recent_tests
    ]

    # Get concept mastery (simplified version)
    concept_performance = (
        db.query(
            AAMCFoundationalConcept.concept_code,
            AAMCFoundationalConcept.title,
            AAMCFoundationalConcept.mcat_section,
            func.count(UserQuestionAttempt.id).label("total_attempts"),
            func.sum(case((UserQuestionAttempt.is_correct == True, 1), else_=0)).label(
                "correct_attempts"
            ),
        )
        .join(Question, Question.foundational_concept_id == AAMCFoundationalConcept.id)
        .join(UserQuestionAttempt, UserQuestionAttempt.question_id == Question.id)
        .filter(UserQuestionAttempt.user_id == current_user.id)
        .group_by(
            AAMCFoundationalConcept.id,
            AAMCFoundationalConcept.concept_code,
            AAMCFoundationalConcept.title,
            AAMCFoundationalConcept.mcat_section,
        )
        .all()
    )

    concept_mastery = []
    for concept in concept_performance:
        accuracy = (
            round((concept.correct_attempts / concept.total_attempts * 100), 2)
            if concept.total_attempts > 0
            else 0
        )
        proficiency = "green" if accuracy >= 80 else "yellow" if accuracy >= 60 else "red"
        concept_mastery.append(
            {
                "concept_code": concept.concept_code,
                "title": concept.title,
                "mcat_section": concept.mcat_section,
                "accuracy": accuracy,
                "proficiency": proficiency,
                "total_attempts": concept.total_attempts,
            }
        )

    # Review queue count
    review_queue_count = (
        db.query(func.count(ReviewQueue.id))
        .filter(ReviewQueue.user_id == current_user.id)
        .scalar()
    )

    return {
        "user": {
            "name": current_user.full_name,
            "target_score": current_user.target_mcat_score,
            "exam_date": current_user.target_exam_date.isoformat()
            if current_user.target_exam_date
            else None,
        },
        "summary": {
            "total_questions_answered": total_questions or 0,
            "total_correct": total_correct or 0,
            "overall_accuracy": overall_accuracy,
            "review_queue_count": review_queue_count or 0,
        },
        "score_history": score_history,
        "concept_mastery": concept_mastery,
    }


@router.get("/review-queue")
async def get_review_queue(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get questions in review queue"""
    review_items = (
        db.query(ReviewQueue)
        .filter(ReviewQueue.user_id == current_user.id)
        .order_by(ReviewQueue.priority.desc())
        .limit(50)
        .all()
    )

    return {"review_queue": [{"question_id": str(item.question_id), "priority": item.priority} for item in review_items]}
