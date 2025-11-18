from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Date, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class UserStudyProgress(Base):
    """User Study Progress model"""

    __tablename__ = "user_study_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    study_module_id = Column(Integer, ForeignKey("study_modules.id"), nullable=False)

    status = Column(String(20), default="not_started", index=True)  # 'not_started', 'in_progress', 'completed'
    time_spent_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Engagement metrics
    notes = Column(Text, nullable=True)
    bookmark_position = Column(JSONB, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "study_module_id", name="unique_user_study_module"),
    )

    def __repr__(self):
        return f"<UserStudyProgress User {self.user_id} - Module {self.study_module_id}>"


class UserGoal(Base):
    """User Goal model"""

    __tablename__ = "user_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_type = Column(String(50), nullable=False)  # 'target_score', 'weekly_questions', 'study_hours'
    target_value = Column(Integer, nullable=False)
    current_value = Column(Integer, default=0)
    deadline = Column(Date, nullable=True)
    status = Column(String(20), default="active", index=True)  # 'active', 'completed', 'abandoned'

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<UserGoal {self.goal_type} - User {self.user_id}>"


class ReviewQueue(Base):
    """Review Queue model - Questions flagged for review"""

    __tablename__ = "review_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    priority = Column(Integer, default=0, index=True)  # Higher = more urgent to review
    last_attempt_id = Column(UUID(as_uuid=True), ForeignKey("user_question_attempts.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="unique_user_question_review"),
    )

    def __repr__(self):
        return f"<ReviewQueue User {self.user_id} - Question {self.question_id}>"
