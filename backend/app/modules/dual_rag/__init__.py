"""Dual RAG Module - Personalized Reasoning Engine (Section 3.2)"""
from app.modules.dual_rag.models import (
    StudentContext,
    AcademicDocument,
    ChatHistory,
    GapAnalysis
)
from app.modules.dual_rag.service import DualRAGService
from app.modules.dual_rag.vector_store import VectorStoreService, get_vector_store
from app.modules.dual_rag.routes import router as dual_rag_router

__all__ = [
    "StudentContext",
    "AcademicDocument",
    "ChatHistory",
    "GapAnalysis",
    "DualRAGService",
    "VectorStoreService",
    "get_vector_store",
    "dual_rag_router"
]
