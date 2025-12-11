"""
SkillTwin - Learning Twin Profile (LTP) API Routes
REST API endpoints for LTP operations
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.ltp.service import LTPService
from app.modules.ltp.schemas import (
    LTPResponse,
    LTPDetailedResponse,
    LTPUpdate,
    ConceptCreate,
    ConceptResponse,
    ConceptMasteryResponse,
    ConceptMasteryUpdate,
    MisconceptionCreate,
    MisconceptionResponse,
    MisconceptionUpdate,
    LearningSessionCreate,
    LearningSessionResponse,
    LearningSessionUpdate,
    LTPAnalytics,
    KnowledgeGraphResponse
)

router = APIRouter(prefix="/ltp", tags=["Learning Twin Profile"])


# ============ Profile Endpoints ============

@router.post("/profiles/{user_id}", response_model=LTPResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    """Create a new Learning Twin Profile for a user"""
    service = LTPService(db)
    
    # Check if profile already exists
    existing = await service.get_profile_by_user_id(user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )
    
    profile = await service.create_profile(user_id)
    return profile


@router.get("/profiles/user/{user_id}", response_model=LTPDetailedResponse)
async def get_profile_by_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get Learning Twin Profile by user ID with all related data"""
    service = LTPService(db)
    profile = await service.get_profile_by_user_id(user_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Get additional data
    masteries = await service.get_profile_masteries(profile.id)
    misconceptions = await service.get_active_misconceptions(profile.id)
    
    return LTPDetailedResponse(
        **profile.__dict__,
        concept_masteries=masteries[:20],  # Limit for response size
        recent_misconceptions=misconceptions[:10],
        recent_sessions=profile.learning_sessions[-10:] if profile.learning_sessions else []
    )


@router.get("/profiles/{profile_id}", response_model=LTPResponse)
async def get_profile(profile_id: str, db: AsyncSession = Depends(get_db)):
    """Get Learning Twin Profile by profile ID"""
    service = LTPService(db)
    profile = await service.get_profile_by_id(profile_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


@router.patch("/profiles/{profile_id}", response_model=LTPResponse)
async def update_profile(
    profile_id: str,
    update_data: LTPUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update Learning Twin Profile"""
    service = LTPService(db)
    profile = await service.update_profile(profile_id, update_data)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


# ============ Concept Endpoints ============

@router.post("/concepts", response_model=ConceptResponse, status_code=status.HTTP_201_CREATED)
async def create_concept(concept_data: ConceptCreate, db: AsyncSession = Depends(get_db)):
    """Create a new learning concept"""
    service = LTPService(db)
    concept = await service.create_concept(concept_data)
    return concept


@router.get("/concepts", response_model=List[ConceptResponse])
async def get_all_concepts(
    subject: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all concepts, optionally filtered by subject"""
    service = LTPService(db)
    
    if subject:
        concepts = await service.get_concepts_by_subject(subject)
    else:
        concepts = await service.get_all_concepts()
    
    return concepts


@router.get("/concepts/{concept_id}", response_model=ConceptResponse)
async def get_concept(concept_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific concept"""
    service = LTPService(db)
    concept = await service.get_concept(concept_id)
    
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concept not found"
        )
    
    return concept


# ============ Concept Mastery Endpoints ============

@router.get("/profiles/{profile_id}/masteries", response_model=List[ConceptMasteryResponse])
async def get_profile_masteries(profile_id: str, db: AsyncSession = Depends(get_db)):
    """Get all concept masteries for a profile"""
    service = LTPService(db)
    masteries = await service.get_profile_masteries(profile_id)
    return masteries


@router.post("/profiles/{profile_id}/masteries/{concept_id}", response_model=ConceptMasteryResponse)
async def update_concept_mastery(
    profile_id: str,
    concept_id: str,
    update_data: ConceptMasteryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update mastery for a specific concept (e.g., after quiz)"""
    service = LTPService(db)
    
    # Verify profile exists
    profile = await service.get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    mastery = await service.update_concept_mastery(profile_id, concept_id, update_data)
    return mastery


@router.get("/profiles/{profile_id}/due-for-review", response_model=List[ConceptMasteryResponse])
async def get_due_for_review(
    profile_id: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get concepts due for spaced repetition review"""
    service = LTPService(db)
    masteries = await service.get_concepts_due_for_review(profile_id, limit)
    return masteries


# ============ Misconception Endpoints ============

@router.post("/profiles/{profile_id}/misconceptions", response_model=MisconceptionResponse, status_code=status.HTTP_201_CREATED)
async def create_misconception(
    profile_id: str,
    misconception_data: MisconceptionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Record a new misconception"""
    service = LTPService(db)
    misconception = await service.create_misconception(profile_id, misconception_data)
    return misconception


@router.get("/profiles/{profile_id}/misconceptions", response_model=List[MisconceptionResponse])
async def get_active_misconceptions(profile_id: str, db: AsyncSession = Depends(get_db)):
    """Get all active (unresolved) misconceptions"""
    service = LTPService(db)
    misconceptions = await service.get_active_misconceptions(profile_id)
    return misconceptions


@router.patch("/misconceptions/{misconception_id}", response_model=MisconceptionResponse)
async def resolve_misconception(
    misconception_id: str,
    update_data: MisconceptionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Mark a misconception as resolved"""
    service = LTPService(db)
    misconception = await service.resolve_misconception(misconception_id, update_data)
    
    if not misconception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Misconception not found"
        )
    
    return misconception


# ============ Learning Session Endpoints ============

@router.post("/profiles/{profile_id}/sessions", response_model=LearningSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    profile_id: str,
    session_data: LearningSessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Start a new learning session"""
    service = LTPService(db)
    session = await service.start_session(profile_id, session_data)
    return session


@router.patch("/sessions/{session_id}", response_model=LearningSessionResponse)
async def end_session(
    session_id: str,
    update_data: LearningSessionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """End a learning session with final stats"""
    service = LTPService(db)
    session = await service.end_session(session_id, update_data)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


# ============ Analytics Endpoints ============

@router.get("/profiles/{profile_id}/analytics", response_model=LTPAnalytics)
async def get_analytics(profile_id: str, db: AsyncSession = Depends(get_db)):
    """Get comprehensive analytics for a profile"""
    service = LTPService(db)
    
    profile = await service.get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    analytics = await service.get_analytics(profile_id)
    return analytics


@router.get("/profiles/{profile_id}/knowledge-graph", response_model=KnowledgeGraphResponse)
async def get_knowledge_graph(profile_id: str, db: AsyncSession = Depends(get_db)):
    """Get knowledge graph for visualization"""
    service = LTPService(db)
    
    profile = await service.get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    graph = await service.get_knowledge_graph(profile_id)
    return graph


# ============ Modality Preference Endpoints ============

@router.post("/profiles/{profile_id}/modality-feedback")
async def update_modality_preference(
    profile_id: str,
    modality: str,
    success: bool,
    db: AsyncSession = Depends(get_db)
):
    """Update modality preference based on learning outcome"""
    service = LTPService(db)
    await service.update_modality_preference(profile_id, modality, success)
    return {"status": "updated"}


@router.get("/profiles/{profile_id}/preferred-modality")
async def get_preferred_modality(profile_id: str, db: AsyncSession = Depends(get_db)):
    """Get the learner's preferred modality"""
    service = LTPService(db)
    modality = await service.get_preferred_modality(profile_id)
    return {"preferred_modality": modality}
