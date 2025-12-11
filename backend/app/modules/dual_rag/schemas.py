"""
SkillTwin - Dual RAG Schemas
Pydantic schemas for Dual RAG API
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# ============ Enums ============

class ContextType(str, Enum):
    QUESTION = "question"
    EXPLANATION = "explanation"
    CHAT = "chat"
    ASSESSMENT = "assessment"


class SourceType(str, Enum):
    TEXTBOOK = "textbook"
    LECTURE = "lecture"
    PDF = "pdf"
    CURRICULUM = "curriculum"


class GapSeverity(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"
    CRITICAL = "critical"


# ============ Student Context Schemas ============

class StudentContextBase(BaseModel):
    context_type: ContextType
    content: str
    concept_id: Optional[str] = None
    concept_name: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    tags: List[str] = []
    was_correct: Optional[bool] = None
    confidence_score: Optional[float] = Field(ge=0.0, le=1.0, default=None)


class StudentContextCreate(StudentContextBase):
    pass


class StudentContextResponse(StudentContextBase):
    id: str
    profile_id: str
    embedding_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Academic Document Schemas ============

class AcademicDocumentBase(BaseModel):
    title: str
    source_type: SourceType
    source_name: str
    content: str
    subject: str
    topic: str
    subtopic: Optional[str] = None
    grade_level: Optional[str] = None
    tags: List[str] = []
    difficulty_level: int = Field(ge=1, le=10, default=5)


class AcademicDocumentCreate(AcademicDocumentBase):
    pass


class AcademicDocumentBulkCreate(BaseModel):
    """For uploading multiple document chunks"""
    documents: List[AcademicDocumentCreate]


class AcademicDocumentResponse(AcademicDocumentBase):
    id: str
    chunk_index: int
    total_chunks: int
    embedding_id: Optional[str]
    is_verified: bool
    quality_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ Chat Schemas ============

class ChatMessageBase(BaseModel):
    content: str
    concept_id: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    session_id: str


class ChatMessageResponse(BaseModel):
    id: str
    profile_id: str
    session_id: str
    role: str
    content: str
    student_context_ids: List[str]
    academic_doc_ids: List[str]
    concept_id: Optional[str]
    was_helpful: Optional[bool]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatFeedback(BaseModel):
    message_id: str
    was_helpful: bool


# ============ Dual RAG Query/Response Schemas ============

class DualRAGQuery(BaseModel):
    """Query for the Dual RAG system"""
    profile_id: str
    query: str
    session_id: Optional[str] = None
    concept_id: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    include_student_context: bool = True
    include_academic_sources: bool = True
    max_student_results: int = 5
    max_academic_results: int = 5


class RetrievedContext(BaseModel):
    """A single piece of retrieved context"""
    id: str
    source: str  # "student" or "academic"
    content: str
    relevance_score: float
    metadata: Dict[str, Any] = {}


class DualRAGResponse(BaseModel):
    """Response from Dual RAG system"""
    answer: str
    student_contexts: List[RetrievedContext]
    academic_contexts: List[RetrievedContext]
    gaps_detected: List["GapAnalysisResponse"] = []
    confidence_score: float
    modality_used: str
    sources_cited: List[str]


# ============ Gap Analysis Schemas ============

class GapAnalysisBase(BaseModel):
    concept_id: Optional[str] = None
    concept_name: str
    student_understanding: str
    correct_understanding: str
    gap_description: str
    gap_severity: GapSeverity
    priority_score: float = Field(ge=0.0, le=1.0, default=0.5)


class GapAnalysisCreate(GapAnalysisBase):
    student_context_ids: List[str] = []
    academic_doc_ids: List[str] = []


class GapAnalysisResponse(GapAnalysisBase):
    id: str
    profile_id: str
    is_resolved: bool
    resolution_strategy: Optional[str]
    student_context_ids: List[str]
    academic_doc_ids: List[str]
    detected_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class GapResolution(BaseModel):
    resolution_strategy: str


# ============ Explanation Generation Schemas ============

class ExplanationRequest(BaseModel):
    """Request for personalized explanation"""
    profile_id: str
    concept_id: str
    question: Optional[str] = None
    preferred_modality: Optional[str] = None  # Override profile preference
    difficulty_level: Optional[int] = Field(ge=1, le=10, default=None)


class ExplanationResponse(BaseModel):
    """Personalized explanation response"""
    explanation: str
    modality_used: str
    analogies: List[str] = []
    examples: List[str] = []
    related_concepts: List[str] = []
    sources: List[str] = []
    follow_up_questions: List[str] = []


# ============ Search Schemas ============

class SemanticSearchQuery(BaseModel):
    """Semantic search across documents"""
    query: str
    source: str = "all"  # "student", "academic", "all"
    subject: Optional[str] = None
    topic: Optional[str] = None
    limit: int = 10


class SemanticSearchResult(BaseModel):
    """Search result item"""
    id: str
    source: str
    content: str
    score: float
    metadata: Dict[str, Any]


class SemanticSearchResponse(BaseModel):
    """Search response"""
    results: List[SemanticSearchResult]
    total_found: int


# Update forward reference
DualRAGResponse.model_rebuild()
