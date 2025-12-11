"""
SkillTwin - Dual RAG Models
Section 3.2: Database models for Dual RAG system
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class StudentContext(Base):
    """
    Student-specific context storage (Source A)
    Stores past questions, explanations, and learning interactions
    """
    __tablename__ = "student_contexts"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"), index=True)
    
    # Context type
    context_type: Mapped[str] = mapped_column(String(50))  # "question", "explanation", "chat", "assessment"
    
    # Content
    content: Mapped[str] = mapped_column(Text)
    
    # Related concept (optional)
    concept_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    concept_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Metadata
    subject: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    topic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    
    # Interaction details
    was_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Vector embedding reference (stored in ChromaDB)
    embedding_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AcademicDocument(Base):
    """
    Verified academic material storage (Source B)
    Textbooks, lecture notes, curriculum-aligned content
    """
    __tablename__ = "academic_documents"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    # Document info
    title: Mapped[str] = mapped_column(String(500))
    source_type: Mapped[str] = mapped_column(String(50))  # "textbook", "lecture", "pdf", "curriculum"
    source_name: Mapped[str] = mapped_column(String(255))  # Book name, course name, etc.
    
    # Content (chunked)
    content: Mapped[str] = mapped_column(Text)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    total_chunks: Mapped[int] = mapped_column(Integer, default=1)
    
    # Categorization
    subject: Mapped[str] = mapped_column(String(100), index=True)
    topic: Mapped[str] = mapped_column(String(100), index=True)
    subtopic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    grade_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Metadata
    tags: Mapped[list] = mapped_column(JSON, default=list)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=5)  # 1-10
    
    # Vector embedding reference
    embedding_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Quality & verification
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    quality_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatHistory(Base):
    """
    Chat conversation history for context
    """
    __tablename__ = "chat_histories"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"), index=True)
    session_id: Mapped[str] = mapped_column(String(36), index=True)
    
    # Message details
    role: Mapped[str] = mapped_column(String(20))  # "user", "assistant", "system"
    content: Mapped[str] = mapped_column(Text)
    
    # Context used for this message
    student_context_ids: Mapped[list] = mapped_column(JSON, default=list)
    academic_doc_ids: Mapped[list] = mapped_column(JSON, default=list)
    
    # Related concept
    concept_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    # Feedback
    was_helpful: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GapAnalysis(Base):
    """
    Records discrepancies between student understanding and academic sources
    """
    __tablename__ = "gap_analyses"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_twin_profiles.id"), index=True)
    
    # Gap details
    concept_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    concept_name: Mapped[str] = mapped_column(String(255))
    
    # Analysis
    student_understanding: Mapped[str] = mapped_column(Text)  # What student thinks
    correct_understanding: Mapped[str] = mapped_column(Text)  # What sources say
    gap_description: Mapped[str] = mapped_column(Text)  # The discrepancy
    
    # Severity
    gap_severity: Mapped[str] = mapped_column(String(20))  # "minor", "moderate", "significant", "critical"
    priority_score: Mapped[float] = mapped_column(Float, default=0.5)
    
    # Resolution
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolution_strategy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Source references
    student_context_ids: Mapped[list] = mapped_column(JSON, default=list)
    academic_doc_ids: Mapped[list] = mapped_column(JSON, default=list)
    
    # Timestamps
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
