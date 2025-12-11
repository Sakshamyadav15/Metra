"""
SkillTwin - Micro Lessons Mock Module (Section 3.3)
Mock implementation for Automated Micro Lesson Generation Pipeline
To be fully implemented by team
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class MicroLesson(Base):
    """
    Mock model for generated micro lessons
    Full implementation pending
    """
    __tablename__ = "micro_lessons"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id"))
    
    # Lesson content
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Slides/content
    slides: Mapped[list] = mapped_column(JSON, default=list)  # List of slide objects
    narration_script: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Media
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Metadata
    difficulty_level: Mapped[int] = mapped_column(Integer, default=5)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=5)
    
    # Personalization tags
    modality: Mapped[str] = mapped_column(String(50), default="visual")
    analogy_style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Assessment
    quiz_questions: Mapped[list] = mapped_column(JSON, default=list)
    
    # Status
    is_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    generation_status: Mapped[str] = mapped_column(String(50), default="pending")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LessonProgress(Base):
    """Track student progress through micro lessons"""
    __tablename__ = "lesson_progress"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"))
    lesson_id: Mapped[str] = mapped_column(String(36), ForeignKey("micro_lessons.id"))
    
    # Progress
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    progress_percentage: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Quiz results
    quiz_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    quiz_attempts: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
