"""
SkillTwin - Micro Lessons Mock Routes
Mock API endpoints - to be fully implemented
"""

import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.micro_lessons.schemas import (
    MicroLessonCreate,
    MicroLessonResponse,
    GenerateLessonRequest,
    LessonProgressUpdate,
    LessonProgressResponse,
    DailyLessonFeed
)

router = APIRouter(prefix="/lessons", tags=["Micro Lessons (Mock)"])


# ============ Mock Data ============

MOCK_LESSONS = [
    {
        "id": "lesson-001",
        "concept_id": "concept-001",
        "title": "Introduction to Quadratic Equations",
        "description": "Learn the basics of quadratic equations and their standard form",
        "slides": [
            {"slide_number": 1, "title": "What is a Quadratic?", "content": "A quadratic equation has the form ax² + bx + c = 0"},
            {"slide_number": 2, "title": "The Standard Form", "content": "Understanding a, b, and c coefficients"},
            {"slide_number": 3, "title": "Real World Examples", "content": "Projectile motion and area problems"}
        ],
        "narration_script": "Welcome to quadratic equations...",
        "video_url": None,
        "thumbnail_url": "https://placeholder.com/thumbnail.png",
        "difficulty_level": 5,
        "duration_minutes": 5,
        "modality": "visual",
        "quiz_questions": [
            {"question": "What is the standard form?", "options": ["ax+b=0", "ax²+bx+c=0", "x²=a"], "correct_index": 1, "explanation": "The standard form is ax²+bx+c=0"}
        ],
        "is_generated": True,
        "generation_status": "completed",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]


# ============ Mock Endpoints ============

@router.get("", response_model=List[MicroLessonResponse])
async def get_lessons(
    concept_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all micro lessons (mock)"""
    return MOCK_LESSONS


@router.get("/{lesson_id}", response_model=MicroLessonResponse)
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific micro lesson (mock)"""
    for lesson in MOCK_LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    raise HTTPException(status_code=404, detail="Lesson not found")


@router.post("/generate", response_model=MicroLessonResponse)
async def generate_lesson(
    request: GenerateLessonRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a new micro lesson (mock).
    
    In full implementation, this would:
    1. Fetch concept details
    2. Get learner preferences from LTP
    3. Generate slide deck using LLM
    4. Create visual aids
    5. Generate narration script
    6. Optionally create video
    7. Generate quiz questions
    """
    # Mock response
    mock_lesson = {
        "id": str(uuid.uuid4()),
        "concept_id": request.concept_id,
        "title": f"Generated Lesson for {request.concept_id}",
        "description": "This is a mock generated lesson",
        "slides": [
            {"slide_number": 1, "title": "Introduction", "content": "Mock content..."},
            {"slide_number": 2, "title": "Main Concept", "content": "Mock content..."},
            {"slide_number": 3, "title": "Summary", "content": "Mock content..."}
        ],
        "narration_script": "Mock narration script...",
        "video_url": None,
        "thumbnail_url": None,
        "difficulty_level": 5,
        "duration_minutes": 5,
        "modality": request.preferred_modality or "visual",
        "analogy_style": "real-world" if request.include_analogies else None,
        "quiz_questions": [
            {"question": "Mock question?", "options": ["A", "B", "C"], "correct_index": 0, "explanation": "Mock explanation"}
        ] if request.include_quiz else [],
        "is_generated": True,
        "generation_status": "completed",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    return mock_lesson


@router.get("/feed/{profile_id}", response_model=DailyLessonFeed)
async def get_daily_feed(
    profile_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized daily lesson feed (mock).
    
    In full implementation, this would:
    1. Analyze LTP for knowledge gaps
    2. Check spaced repetition schedule
    3. Select appropriate lessons
    4. Rank by priority
    """
    return DailyLessonFeed(
        profile_id=profile_id,
        date=datetime.utcnow(),
        recommended_lessons=MOCK_LESSONS,
        review_lessons=[],
        total_estimated_time=5
    )


@router.post("/progress/{profile_id}/{lesson_id}", response_model=LessonProgressResponse)
async def update_progress(
    profile_id: str,
    lesson_id: str,
    update: LessonProgressUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update lesson progress (mock)"""
    return LessonProgressResponse(
        id=str(uuid.uuid4()),
        profile_id=profile_id,
        lesson_id=lesson_id,
        is_completed=update.is_completed or False,
        progress_percentage=update.progress_percentage or 0,
        time_spent_seconds=update.time_spent_seconds or 0,
        quiz_score=update.quiz_score,
        quiz_attempts=1 if update.quiz_score else 0,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow() if update.is_completed else None
    )


@router.get("/progress/{profile_id}", response_model=List[LessonProgressResponse])
async def get_progress(
    profile_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all lesson progress for a profile (mock)"""
    return []
