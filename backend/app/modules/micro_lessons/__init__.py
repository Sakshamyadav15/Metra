"""Micro Lessons Module - Mock (Section 3.3)"""
from app.modules.micro_lessons.models import MicroLesson, LessonProgress
from app.modules.micro_lessons.routes import router as micro_lessons_router

__all__ = [
    "MicroLesson",
    "LessonProgress",
    "micro_lessons_router"
]
