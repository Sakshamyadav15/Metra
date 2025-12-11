"""
SkillTwin - Vector Store Service
ChromaDB integration for semantic search
"""

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings


class VectorStoreService:
    """Service for managing vector embeddings with ChromaDB"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            # Initialize ChromaDB client
            self._client = chromadb.Client(ChromaSettings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.chroma_persist_directory,
                anonymized_telemetry=False
            ))
            
            # Initialize collections
            self._student_collection = self._client.get_or_create_collection(
                name="student_contexts",
                metadata={"description": "Student-specific learning contexts"}
            )
            
            self._academic_collection = self._client.get_or_create_collection(
                name="academic_documents", 
                metadata={"description": "Verified academic materials"}
            )
    
    @property
    def student_collection(self):
        return self._student_collection
    
    @property
    def academic_collection(self):
        return self._academic_collection
    
    async def add_student_context(
        self,
        doc_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Add student context to vector store"""
        self._student_collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata]
        )
        return doc_id
    
    async def add_academic_document(
        self,
        doc_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Add academic document to vector store"""
        self._academic_collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata]
        )
        return doc_id
    
    async def search_student_contexts(
        self,
        query: str,
        profile_id: str,
        n_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search student contexts with optional filters"""
        where_filter = {"profile_id": profile_id}
        if filters:
            where_filter.update(filters)
        
        results = self._student_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        return self._format_results(results)
    
    async def search_academic_documents(
        self,
        query: str,
        n_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search academic documents with optional filters"""
        where_filter = filters if filters else None
        
        results = self._academic_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        return self._format_results(results)
    
    async def dual_search(
        self,
        query: str,
        profile_id: str,
        n_student: int = 5,
        n_academic: int = 5,
        student_filters: Optional[Dict[str, Any]] = None,
        academic_filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Perform dual search across both collections"""
        student_results = await self.search_student_contexts(
            query, profile_id, n_student, student_filters
        )
        academic_results = await self.search_academic_documents(
            query, n_academic, academic_filters
        )
        
        return {
            "student_contexts": student_results,
            "academic_documents": academic_results
        }
    
    def _format_results(self, results: Dict) -> List[Dict[str, Any]]:
        """Format ChromaDB results into a cleaner structure"""
        formatted = []
        
        if not results or not results.get('ids') or not results['ids'][0]:
            return formatted
        
        ids = results['ids'][0]
        documents = results['documents'][0] if results.get('documents') else []
        metadatas = results['metadatas'][0] if results.get('metadatas') else []
        distances = results['distances'][0] if results.get('distances') else []
        
        for i, doc_id in enumerate(ids):
            formatted.append({
                "id": doc_id,
                "content": documents[i] if i < len(documents) else "",
                "metadata": metadatas[i] if i < len(metadatas) else {},
                "score": 1 - distances[i] if i < len(distances) else 0  # Convert distance to similarity
            })
        
        return formatted
    
    async def delete_student_context(self, doc_id: str) -> bool:
        """Delete a student context from vector store"""
        try:
            self._student_collection.delete(ids=[doc_id])
            return True
        except Exception:
            return False
    
    async def delete_academic_document(self, doc_id: str) -> bool:
        """Delete an academic document from vector store"""
        try:
            self._academic_collection.delete(ids=[doc_id])
            return True
        except Exception:
            return False
    
    async def get_collection_stats(self) -> Dict[str, int]:
        """Get stats about the collections"""
        return {
            "student_contexts_count": self._student_collection.count(),
            "academic_documents_count": self._academic_collection.count()
        }


# Singleton instance
vector_store = VectorStoreService()


def get_vector_store() -> VectorStoreService:
    """Dependency for getting vector store instance"""
    return vector_store
