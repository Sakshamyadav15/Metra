"""
SkillTwin - Learning Twin Profile (LTP) Models
Section 3.1: Persistent representation of learner's evolving cognitive state
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, JSON, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import enum


class LearningModality(str, enum.Enum):
    """Preferred explanation modality"""
    VISUAL = "visual"
    VERBAL = "verbal"
    ABSTRACT = "abstract"
    ANALOGY = "analogy"
    INTERACTIVE = "interactive"


class MasteryLevel(str, enum.Enum):
    """Concept mastery levels"""
    NOT_STARTED = "not_started"
    LEARNING = "learning"
    PARTIAL = "partial"
    MASTERED = "mastered"
    EXPERT = "expert"


class LearningTwinProfile(Base):
    """
    Learning Twin Profile (LTP) - Core cognitive state model
    Tracks the learner's evolving understanding, preferences, and patterns
    """
    __tablename__ = "learning_twin_profiles"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True)
    
    # Overall metrics
    overall_mastery_score: Mapped[float] = mapped_column(Float, default=0.0)
    learning_velocity: Mapped[float] = mapped_column(Float, default=1.0)  # Concepts per day
    retention_rate: Mapped[float] = mapped_column(Float, default=0.8)  # Memory retention coefficient
    
    # Preferred modality (stored as JSON for flexibility)
    modality_preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    # Example: {"visual": 0.8, "verbal": 0.6, "abstract": 0.4, "analogy": 0.9}
    
    # Speech-based confidence metrics
    avg_speech_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    avg_articulation_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Learning statistics
    total_study_time_minutes: Mapped[int] = mapped_column(Integer, default=0)
    total_concepts_attempted: Mapped[int] = mapped_column(Integer, default=0)
    total_concepts_mastered: Mapped[int] = mapped_column(Integer, default=0)
    current_streak_days: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak_days: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="learning_profile")
    concept_masteries: Mapped[List["ConceptMastery"]] = relationship(
        "ConceptMastery", 
        back_populates="profile",
        cascade="all, delete-orphan"
    )
    misconceptions: Mapped[List["Misconception"]] = relationship(
        "Misconception",
        back_populates="profile",
        cascade="all, delete-orphan"
    )
    learning_sessions: Mapped[List["LearningSession"]] = relationship(
        "LearningSession",
        back_populates="profile",
        cascade="all, delete-orphan"
    )


class Concept(Base):
    """
    Knowledge concepts/topics that can be learned
    Forms the knowledge graph structure
    """
    __tablename__ = "concepts"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    subject: Mapped[str] = mapped_column(String(100), index=True)
    topic: Mapped[str] = mapped_column(String(100), index=True)
    subtopic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)  # 1-10 scale
    
    # Prerequisites (stored as JSON list of concept IDs)
    prerequisite_ids: Mapped[list] = mapped_column(JSON, default=list)
    
    # Metadata
    tags: Mapped[list] = mapped_column(JSON, default=list)
    estimated_time_minutes: Mapped[int] = mapped_column(Integer, default=30)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    masteries: Mapped[List["ConceptMastery"]] = relationship(
        "ConceptMastery",
        back_populates="concept"
    )


class ConceptMastery(Base):
    """
    Tracks individual concept mastery for each learner
    Links LTP to specific concepts with mastery metrics
    """
    __tablename__ = "concept_masteries"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"))
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id"))
    
    # Mastery metrics
    mastery_level: Mapped[str] = mapped_column(String(20), default=MasteryLevel.NOT_STARTED.value)
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0.0 to 1.0
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)  # Self-reported + assessed
    
    # Learning history
    attempts_count: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_minutes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Spaced repetition
    next_review_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    review_interval_days: Mapped[int] = mapped_column(Integer, default=1)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)  # SM-2 algorithm
    
    # Timestamps
    first_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_practiced_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    mastered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    profile: Mapped["LearningTwinProfile"] = relationship("LearningTwinProfile", back_populates="concept_masteries")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="masteries")


class Misconception(Base):
    """
    Tracks identified misconceptions for targeted correction
    Critical for personalized remediation
    """
    __tablename__ = "misconceptions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"))
    concept_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("concepts.id"), nullable=True)
    
    # Misconception details
    misconception_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    student_response: Mapped[str] = mapped_column(Text)  # What the student said/answered
    correct_understanding: Mapped[str] = mapped_column(Text)  # What they should understand
    
    # Severity and status
    severity: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, critical
    is_resolved: Mapped[bool] = mapped_column(default=False)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Detection metadata
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    detection_source: Mapped[str] = mapped_column(String(50))  # "quiz", "speech", "chat", etc.
    
    # Relationships
    profile: Mapped["LearningTwinProfile"] = relationship("LearningTwinProfile", back_populates="misconceptions")


class LearningSession(Base):
    """
    Tracks individual learning sessions for analytics
    """
    __tablename__ = "learning_sessions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"))
    
    # Session details
    session_type: Mapped[str] = mapped_column(String(50))  # "lesson", "practice", "assessment", "chat"
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Activity metrics
    concepts_covered: Mapped[list] = mapped_column(JSON, default=list)
    questions_attempted: Mapped[int] = mapped_column(Integer, default=0)
    questions_correct: Mapped[int] = mapped_column(Integer, default=0)
    
    # Engagement metrics
    focus_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Derived from behavior
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    profile: Mapped["LearningTwinProfile"] = relationship("LearningTwinProfile", back_populates="learning_sessions")


# Import User model to resolve forward references
from app.models.user import User
