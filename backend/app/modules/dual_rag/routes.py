"""
SkillTwin - Dual RAG API Routes
REST API endpoints for Dual RAG operations
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.dual_rag.service import DualRAGService
from app.modules.dual_rag.vector_store import get_vector_store, VectorStoreService
from app.modules.dual_rag.schemas import (
    StudentContextCreate,
    StudentContextResponse,
    AcademicDocumentCreate,
    AcademicDocumentBulkCreate,
    AcademicDocumentResponse,
    DualRAGQuery,
    DualRAGResponse,
    GapAnalysisResponse,
    GapResolution,
    ExplanationRequest,
    ExplanationResponse,
    SemanticSearchQuery,
    SemanticSearchResponse,
    ChatMessageResponse,
    ChatFeedback
)

router = APIRouter(prefix="/rag", tags=["Dual RAG"])


# ============ Student Context Endpoints ============

@router.post("/contexts/{profile_id}", response_model=StudentContextResponse, status_code=status.HTTP_201_CREATED)
async def add_student_context(
    profile_id: str,
    context_data: StudentContextCreate,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """Add a student context (question, explanation, etc.) to the knowledge base"""
    service = DualRAGService(db, vector_store)
    context = await service.add_student_context(profile_id, context_data)
    return context


@router.get("/contexts/{profile_id}", response_model=List[StudentContextResponse])
async def get_student_contexts(
    profile_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get student contexts for a profile"""
    service = DualRAGService(db)
    contexts = await service.get_student_contexts(profile_id, limit)
    return contexts


# ============ Academic Document Endpoints ============

@router.post("/documents", response_model=AcademicDocumentResponse, status_code=status.HTTP_201_CREATED)
async def add_academic_document(
    doc_data: AcademicDocumentCreate,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """Add an academic document to the knowledge base"""
    service = DualRAGService(db, vector_store)
    document = await service.add_academic_document(doc_data)
    return document


@router.post("/documents/bulk", response_model=List[AcademicDocumentResponse], status_code=status.HTTP_201_CREATED)
async def add_academic_documents_bulk(
    bulk_data: AcademicDocumentBulkCreate,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """Bulk add academic documents"""
    service = DualRAGService(db, vector_store)
    documents = await service.add_academic_documents_bulk(bulk_data.documents)
    return documents


@router.get("/documents", response_model=List[AcademicDocumentResponse])
async def get_academic_documents(
    subject: Optional[str] = None,
    topic: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get academic documents with optional filters"""
    service = DualRAGService(db)
    documents = await service.get_academic_documents(subject, topic, limit)
    return documents


# ============ Dual RAG Query Endpoints ============

@router.post("/query", response_model=DualRAGResponse)
async def process_query(
    query: DualRAGQuery,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """
    Process a query through the Dual RAG system.
    Retrieves student context and academic sources, detects gaps, and generates response.
    """
    service = DualRAGService(db, vector_store)
    response = await service.process_query(query)
    return response


@router.post("/explain", response_model=ExplanationResponse)
async def generate_explanation(
    request: ExplanationRequest,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """Generate a personalized explanation for a concept"""
    service = DualRAGService(db, vector_store)
    response = await service.generate_explanation(request)
    return response


# ============ Gap Analysis Endpoints ============

@router.get("/gaps/{profile_id}", response_model=List[GapAnalysisResponse])
async def get_unresolved_gaps(
    profile_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get unresolved knowledge gaps for a profile"""
    service = DualRAGService(db)
    gaps = await service.get_unresolved_gaps(profile_id)
    return gaps


@router.post("/gaps/{gap_id}/resolve", response_model=GapAnalysisResponse)
async def resolve_gap(
    gap_id: str,
    resolution: GapResolution,
    db: AsyncSession = Depends(get_db)
):
    """Mark a knowledge gap as resolved"""
    service = DualRAGService(db)
    gap = await service.resolve_gap(gap_id, resolution)
    
    if not gap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gap not found"
        )
    
    return gap


# ============ Search Endpoints ============

@router.post("/search", response_model=SemanticSearchResponse)
async def semantic_search(
    query: SemanticSearchQuery,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """Perform semantic search across the knowledge base"""
    service = DualRAGService(db, vector_store)
    response = await service.semantic_search(query)
    return response


# ============ Chat History Endpoints ============

@router.get("/chat/{profile_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(
    profile_id: str,
    session_id: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get chat history for a profile"""
    service = DualRAGService(db)
    history = await service.get_chat_history(profile_id, session_id, limit)
    return history


@router.post("/chat/feedback")
async def submit_chat_feedback(
    feedback: ChatFeedback,
    db: AsyncSession = Depends(get_db)
):
    """Submit feedback for a chat message"""
    service = DualRAGService(db)
    success = await service.submit_feedback(feedback.message_id, feedback.was_helpful)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    return {"status": "feedback recorded"}


# ============ Stats Endpoint ============

@router.get("/stats")
async def get_vector_store_stats(
    vector_store: VectorStoreService = Depends(get_vector_store)
):
    """Get vector store statistics"""
    stats = await vector_store.get_collection_stats()
    return stats
