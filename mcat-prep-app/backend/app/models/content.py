from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, ARRAY, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class AAMCFoundationalConcept(Base):
    """AAMC Foundational Concepts model"""

    __tablename__ = "aamc_foundational_concepts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    concept_code = Column(String(10), unique=True, nullable=False)  # e.g., '1A', '7C'
    mcat_section = Column(String(10), nullable=False, index=True)  # CPBS, CARS, BBLS, PSBB
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_concept_id = Column(Integer, ForeignKey("aamc_foundational_concepts.id"), nullable=True)

    def __repr__(self):
        return f"<AAMCConcept {self.concept_code}: {self.title}>"


class Topic(Base):
    """Topic model"""

    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    mcat_section = Column(String(10), nullable=False, index=True)
    foundational_concept_id = Column(
        Integer, ForeignKey("aamc_foundational_concepts.id"), nullable=True, index=True
    )
    description = Column(Text, nullable=True)
    difficulty_level = Column(Integer, nullable=True)
    parent_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("difficulty_level >= 1 AND difficulty_level <= 5", name="check_difficulty"),
    )

    def __repr__(self):
        return f"<Topic {self.name}>"


class StudyModule(Base):
    """Study Module model"""

    __tablename__ = "study_modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    mcat_section = Column(String(10), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True, index=True)
    content_type = Column(String(50), nullable=False)  # 'text', 'video', 'flashcard', 'equation_sheet'
    content = Column(JSONB, nullable=False)
    order_index = Column(Integer, nullable=True)
    estimated_time_minutes = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<StudyModule {self.title}>"


class Passage(Base):
    """Passage model for passage-based questions"""

    __tablename__ = "passages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mcat_section = Column(String(10), nullable=False, index=True)
    passage_text = Column(Text, nullable=False)
    passage_images = Column(JSONB, nullable=True)  # Array of image URLs
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    foundational_concept_id = Column(
        Integer, ForeignKey("aamc_foundational_concepts.id"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Passage {self.id}>"


class Question(Base):
    """Question model"""

    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_type = Column(String(20), nullable=False, index=True)  # 'passage_based', 'standalone'
    mcat_section = Column(String(10), nullable=False, index=True)
    passage_id = Column(UUID(as_uuid=True), ForeignKey("passages.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True, index=True)
    foundational_concept_id = Column(
        Integer, ForeignKey("aamc_foundational_concepts.id"), nullable=True, index=True
    )
    difficulty_level = Column(Integer, nullable=True, index=True)

    # Question content
    question_text = Column(Text, nullable=False)
    question_images = Column(JSONB, nullable=True)

    # Answer options (A, B, C, D)
    options = Column(JSONB, nullable=False)  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer = Column(String(1), nullable=False)

    # Explanations
    correct_explanation = Column(Text, nullable=False)
    incorrect_explanations = Column(JSONB, nullable=True)

    # Metadata
    tags = Column(ARRAY(String), nullable=True)
    estimated_time_seconds = Column(Integer, default=90)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Quality metrics
    average_accuracy = Column(Integer, nullable=True)
    times_answered = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint("difficulty_level >= 1 AND difficulty_level <= 5", name="check_question_difficulty"),
        CheckConstraint("correct_answer IN ('A', 'B', 'C', 'D')", name="check_correct_answer"),
    )

    def __repr__(self):
        return f"<Question {self.id}>"
