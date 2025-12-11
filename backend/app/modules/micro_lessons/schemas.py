"""
SkillTwin - Micro Lessons Mock Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SlideContent(BaseModel):
    """Single slide in a micro lesson"""
    slide_number: int
    title: str
    content: str
    visual_description: Optional[str] = None
    narration: Optional[str] = None


class QuizQuestion(BaseModel):
    """Quiz question for micro lesson"""
    question: str
    options: List[str]
    correct_index: int
    explanation: str


class MicroLessonBase(BaseModel):
    concept_id: str
    title: str
    description: Optional[str] = None
    difficulty_level: int = Field(ge=1, le=10, default=5)
    duration_minutes: int = 5
    modality: str = "visual"
    analogy_style: Optional[str] = None


class MicroLessonCreate(MicroLessonBase):
    pass


class MicroLessonResponse(MicroLessonBase):
    id: str
    slides: List[Dict[str, Any]] = []
    narration_script: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    quiz_questions: List[Dict[str, Any]] = []
    is_generated: bool
    generation_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GenerateLessonRequest(BaseModel):
    """Request to generate a micro lesson"""
    profile_id: str
    concept_id: str
    preferred_modality: Optional[str] = None
    include_analogies: bool = True
    include_quiz: bool = True


class LessonProgressBase(BaseModel):
    lesson_id: str


class LessonProgressUpdate(BaseModel):
    progress_percentage: Optional[int] = Field(ge=0, le=100, default=None)
    time_spent_seconds: Optional[int] = None
    quiz_score: Optional[int] = None
    is_completed: Optional[bool] = None


class LessonProgressResponse(BaseModel):
    id: str
    profile_id: str
    lesson_id: str
    is_completed: bool
    progress_percentage: int
    time_spent_seconds: int
    quiz_score: Optional[int]
    quiz_attempts: int
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DailyLessonFeed(BaseModel):
    """Daily personalized lesson feed"""
    profile_id: str
    date: datetime
    recommended_lessons: List[MicroLessonResponse]
    review_lessons: List[MicroLessonResponse]  # Spaced repetition
    total_estimated_time: int  # minutes
