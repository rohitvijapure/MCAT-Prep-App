from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class PracticeTest(Base):
    """Practice Test model"""

    __tablename__ = "practice_tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_type = Column(String(50), nullable=False, index=True)  # 'full_length', 'section_test', 'custom_quiz'
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_official_aamc = Column(Boolean, default=False)

    # Test structure
    sections = Column(JSONB, nullable=False)  # Array of section configurations
    total_questions = Column(Integer, nullable=False)
    total_duration_minutes = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<PracticeTest {self.title}>"


class UserTestAttempt(Base):
    """User Test Attempt model"""

    __tablename__ = "user_test_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    practice_test_id = Column(UUID(as_uuid=True), ForeignKey("practice_tests.id"), nullable=False)

    # Attempt metadata
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True, index=True)
    status = Column(String(20), default="in_progress", index=True)  # 'in_progress', 'paused', 'completed', 'abandoned'

    # Scores (calculated after completion)
    total_score = Column(Integer, nullable=True)
    cpbs_score = Column(Integer, nullable=True)
    cars_score = Column(Integer, nullable=True)
    bbls_score = Column(Integer, nullable=True)
    psbb_score = Column(Integer, nullable=True)

    # Performance metrics
    total_correct = Column(Integer, nullable=True)
    total_questions = Column(Integer, nullable=True)
    accuracy_percentage = Column(Integer, nullable=True)
    total_time_spent_seconds = Column(Integer, nullable=True)

    # State preservation for pause/resume
    current_section = Column(Integer, default=0)
    current_question_index = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint("total_score >= 472 AND total_score <= 528 OR total_score IS NULL", name="check_total_score"),
        CheckConstraint("cpbs_score >= 118 AND cpbs_score <= 132 OR cpbs_score IS NULL", name="check_cpbs_score"),
        CheckConstraint("cars_score >= 118 AND cars_score <= 132 OR cars_score IS NULL", name="check_cars_score"),
        CheckConstraint("bbls_score >= 118 AND bbls_score <= 132 OR bbls_score IS NULL", name="check_bbls_score"),
        CheckConstraint("psbb_score >= 118 AND psbb_score <= 132 OR psbb_score IS NULL", name="check_psbb_score"),
    )

    def __repr__(self):
        return f"<UserTestAttempt {self.id} - User {self.user_id}>"


class UserQuestionAttempt(Base):
    """User Question Attempt model - Critical for analytics"""

    __tablename__ = "user_question_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False, index=True)
    test_attempt_id = Column(UUID(as_uuid=True), ForeignKey("user_test_attempts.id"), nullable=True, index=True)

    # Attempt details
    selected_answer = Column(String(1), nullable=False)  # A, B, C, D, or X for omitted
    is_correct = Column(Boolean, nullable=False, index=True)
    time_spent_seconds = Column(Integer, nullable=False)

    # Flagging for review
    is_flagged = Column(Boolean, default=False)
    is_reviewed = Column(Boolean, default=False)

    # Context
    attempt_mode = Column(String(20), nullable=False)  # 'timed', 'untimed', 'review'
    attempted_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Metadata for analytics
    confidence_level = Column(Integer, nullable=True)  # Optional self-rating 1-5
    notes = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("selected_answer IN ('A', 'B', 'C', 'D', 'X')", name="check_selected_answer"),
        CheckConstraint("confidence_level >= 1 AND confidence_level <= 5 OR confidence_level IS NULL", name="check_confidence"),
    )

    def __repr__(self):
        return f"<UserQuestionAttempt {self.id} - User {self.user_id}>"
