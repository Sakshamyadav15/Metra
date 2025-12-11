"""
SkillTwin - Learning Twin Profile (LTP) Schemas
Pydantic schemas for API request/response validation
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum


class LearningModalityEnum(str, Enum):
    VISUAL = "visual"
    VERBAL = "verbal"
    ABSTRACT = "abstract"
    ANALOGY = "analogy"
    INTERACTIVE = "interactive"


class MasteryLevelEnum(str, Enum):
    NOT_STARTED = "not_started"
    LEARNING = "learning"
    PARTIAL = "partial"
    MASTERED = "mastered"
    EXPERT = "expert"


# ============ Concept Schemas ============

class ConceptBase(BaseModel):
    name: str
    description: Optional[str] = None
    subject: str
    topic: str
    subtopic: Optional[str] = None
    difficulty_level: int = Field(ge=1, le=10, default=1)
    prerequisite_ids: List[str] = []
    tags: List[str] = []
    estimated_time_minutes: int = 30


class ConceptCreate(ConceptBase):
    pass


class ConceptResponse(ConceptBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Concept Mastery Schemas ============

class ConceptMasteryBase(BaseModel):
    mastery_level: MasteryLevelEnum = MasteryLevelEnum.NOT_STARTED
    mastery_score: float = Field(ge=0.0, le=1.0, default=0.0)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)


class ConceptMasteryUpdate(BaseModel):
    mastery_score: Optional[float] = Field(ge=0.0, le=1.0, default=None)
    confidence_score: Optional[float] = Field(ge=0.0, le=1.0, default=None)
    correct: Optional[bool] = None  # For updating from quiz results


class ConceptMasteryResponse(ConceptMasteryBase):
    id: str
    profile_id: str
    concept_id: str
    attempts_count: int
    correct_count: int
    time_spent_minutes: int
    next_review_at: Optional[datetime]
    review_interval_days: int
    first_seen_at: datetime
    last_practiced_at: Optional[datetime]
    mastered_at: Optional[datetime]
    concept: Optional[ConceptResponse] = None

    class Config:
        from_attributes = True


# ============ Misconception Schemas ============

class MisconceptionBase(BaseModel):
    concept_id: Optional[str] = None
    misconception_type: str
    description: str
    student_response: str
    correct_understanding: str
    severity: str = Field(pattern="^(low|medium|high|critical)$", default="medium")
    detection_source: str


class MisconceptionCreate(MisconceptionBase):
    pass


class MisconceptionUpdate(BaseModel):
    is_resolved: bool = True
    resolution_notes: Optional[str] = None


class MisconceptionResponse(MisconceptionBase):
    id: str
    profile_id: str
    is_resolved: bool
    resolution_notes: Optional[str]
    detected_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============ Learning Session Schemas ============

class LearningSessionBase(BaseModel):
    session_type: str
    concepts_covered: List[str] = []


class LearningSessionCreate(LearningSessionBase):
    pass


class LearningSessionUpdate(BaseModel):
    duration_minutes: Optional[int] = None
    questions_attempted: Optional[int] = None
    questions_correct: Optional[int] = None
    focus_score: Optional[float] = Field(ge=0.0, le=1.0, default=None)
    ended_at: Optional[datetime] = None


class LearningSessionResponse(LearningSessionBase):
    id: str
    profile_id: str
    duration_minutes: int
    questions_attempted: int
    questions_correct: int
    focus_score: Optional[float]
    started_at: datetime
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============ Learning Twin Profile Schemas ============

class ModalityPreferences(BaseModel):
    visual: float = Field(ge=0.0, le=1.0, default=0.5)
    verbal: float = Field(ge=0.0, le=1.0, default=0.5)
    abstract: float = Field(ge=0.0, le=1.0, default=0.5)
    analogy: float = Field(ge=0.0, le=1.0, default=0.5)
    interactive: float = Field(ge=0.0, le=1.0, default=0.5)


class LTPBase(BaseModel):
    modality_preferences: Dict[str, float] = {}


class LTPCreate(LTPBase):
    user_id: str


class LTPUpdate(BaseModel):
    modality_preferences: Optional[Dict[str, float]] = None
    learning_velocity: Optional[float] = None
    retention_rate: Optional[float] = None


class LTPResponse(LTPBase):
    id: str
    user_id: str
    overall_mastery_score: float
    learning_velocity: float
    retention_rate: float
    avg_speech_confidence: float
    avg_articulation_score: float
    total_study_time_minutes: int
    total_concepts_attempted: int
    total_concepts_mastered: int
    current_streak_days: int
    longest_streak_days: int
    created_at: datetime
    updated_at: datetime
    last_activity_at: Optional[datetime]

    class Config:
        from_attributes = True


class LTPDetailedResponse(LTPResponse):
    """Full LTP response with related data"""
    concept_masteries: List[ConceptMasteryResponse] = []
    recent_misconceptions: List[MisconceptionResponse] = []
    recent_sessions: List[LearningSessionResponse] = []

    class Config:
        from_attributes = True


# ============ Analytics Schemas ============

class LTPAnalytics(BaseModel):
    """Analytics summary for dashboard"""
    profile_id: str
    overall_progress: float  # 0-100 percentage
    concepts_by_mastery: Dict[str, int]  # {mastery_level: count}
    subjects_progress: Dict[str, float]  # {subject: progress_percentage}
    learning_velocity_trend: List[float]  # Last 7 days
    top_strengths: List[str]  # Top 5 mastered topics
    areas_for_improvement: List[str]  # Topics needing work
    recommended_next_concepts: List[str]  # Next concepts to learn
    study_time_weekly: List[int]  # Minutes per day, last 7 days
    streak_info: Dict[str, int]  # {current: n, longest: m}


class KnowledgeGraphNode(BaseModel):
    """Node in the knowledge graph visualization"""
    id: str
    name: str
    mastery_level: str
    mastery_score: float
    subject: str
    topic: str


class KnowledgeGraphEdge(BaseModel):
    """Edge in the knowledge graph"""
    source: str
    target: str
    relationship: str = "prerequisite"


class KnowledgeGraphResponse(BaseModel):
    """Full knowledge graph for visualization"""
    nodes: List[KnowledgeGraphNode]
    edges: List[KnowledgeGraphEdge]
