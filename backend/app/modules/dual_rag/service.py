"""
SkillTwin - Dual RAG Service
Business logic for Dual RAG Personalized Reasoning Engine
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dual_rag.models import (
    StudentContext,
    AcademicDocument,
    ChatHistory,
    GapAnalysis
)
from app.modules.dual_rag.schemas import (
    StudentContextCreate,
    AcademicDocumentCreate,
    ChatMessageCreate,
    DualRAGQuery,
    DualRAGResponse,
    RetrievedContext,
    GapAnalysisCreate,
    GapResolution,
    ExplanationRequest,
    ExplanationResponse,
    SemanticSearchQuery,
    SemanticSearchResult,
    SemanticSearchResponse
)
from app.modules.dual_rag.vector_store import VectorStoreService, get_vector_store
from app.modules.ltp.service import LTPService
from app.core.config import settings

# Optional: Import OpenAI for LLM calls
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class DualRAGService:
    """
    Dual RAG Service - Implements the core reasoning engine
    Retrieves and fuses student context with academic materials
    """
    
    def __init__(self, db: AsyncSession, vector_store: VectorStoreService = None):
        self.db = db
        self.vector_store = vector_store or get_vector_store()
        self.ltp_service = LTPService(db)
        
        # Initialize OpenAI client if available
        self.openai_client = None
        if OPENAI_AVAILABLE and settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    # ============ Student Context Operations ============
    
    async def add_student_context(
        self,
        profile_id: str,
        context_data: StudentContextCreate
    ) -> StudentContext:
        """Add a new student context and index it for retrieval"""
        context_id = str(uuid.uuid4())
        
        # Create database record
        context = StudentContext(
            id=context_id,
            profile_id=profile_id,
            **context_data.model_dump()
        )
        self.db.add(context)
        
        # Add to vector store
        metadata = {
            "profile_id": profile_id,
            "context_type": context_data.context_type.value,
            "concept_id": context_data.concept_id,
            "concept_name": context_data.concept_name,
            "subject": context_data.subject,
            "topic": context_data.topic,
            "was_correct": context_data.was_correct,
            "created_at": datetime.utcnow().isoformat()
        }
        # Filter out None values
        metadata = {k: v for k, v in metadata.items() if v is not None}
        
        embedding_id = await self.vector_store.add_student_context(
            doc_id=context_id,
            content=context_data.content,
            metadata=metadata
        )
        context.embedding_id = embedding_id
        
        await self.db.commit()
        await self.db.refresh(context)
        return context
    
    async def get_student_contexts(
        self,
        profile_id: str,
        limit: int = 50
    ) -> List[StudentContext]:
        """Get recent student contexts"""
        result = await self.db.execute(
            select(StudentContext)
            .where(StudentContext.profile_id == profile_id)
            .order_by(StudentContext.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    # ============ Academic Document Operations ============
    
    async def add_academic_document(
        self,
        doc_data: AcademicDocumentCreate
    ) -> AcademicDocument:
        """Add an academic document and index it"""
        doc_id = str(uuid.uuid4())
        
        # Create database record
        document = AcademicDocument(
            id=doc_id,
            **doc_data.model_dump()
        )
        self.db.add(document)
        
        # Add to vector store
        metadata = {
            "source_type": doc_data.source_type.value,
            "source_name": doc_data.source_name,
            "subject": doc_data.subject,
            "topic": doc_data.topic,
            "subtopic": doc_data.subtopic,
            "grade_level": doc_data.grade_level,
            "difficulty_level": doc_data.difficulty_level,
            "title": doc_data.title
        }
        metadata = {k: v for k, v in metadata.items() if v is not None}
        
        embedding_id = await self.vector_store.add_academic_document(
            doc_id=doc_id,
            content=doc_data.content,
            metadata=metadata
        )
        document.embedding_id = embedding_id
        
        await self.db.commit()
        await self.db.refresh(document)
        return document
    
    async def add_academic_documents_bulk(
        self,
        documents: List[AcademicDocumentCreate]
    ) -> List[AcademicDocument]:
        """Bulk add academic documents"""
        results = []
        for doc_data in documents:
            doc = await self.add_academic_document(doc_data)
            results.append(doc)
        return results
    
    async def get_academic_documents(
        self,
        subject: Optional[str] = None,
        topic: Optional[str] = None,
        limit: int = 50
    ) -> List[AcademicDocument]:
        """Get academic documents with optional filters"""
        query = select(AcademicDocument)
        
        if subject:
            query = query.where(AcademicDocument.subject == subject)
        if topic:
            query = query.where(AcademicDocument.topic == topic)
        
        query = query.order_by(AcademicDocument.created_at.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    # ============ Dual RAG Query Processing ============
    
    async def process_query(self, query: DualRAGQuery) -> DualRAGResponse:
        """
        Main Dual RAG processing pipeline
        1. Retrieve relevant student context
        2. Retrieve relevant academic materials
        3. Detect gaps/contradictions
        4. Generate personalized response
        """
        student_contexts = []
        academic_contexts = []
        
        # Get learner's profile for personalization
        profile = await self.ltp_service.get_profile_by_id(query.profile_id)
        preferred_modality = "visual"  # Default
        if profile:
            preferred_modality = await self.ltp_service.get_preferred_modality(query.profile_id)
        
        # Build filters
        student_filters = {}
        academic_filters = {}
        
        if query.subject:
            student_filters["subject"] = query.subject
            academic_filters["subject"] = query.subject
        if query.topic:
            student_filters["topic"] = query.topic
            academic_filters["topic"] = query.topic
        
        # Retrieve student context (Source A)
        if query.include_student_context:
            raw_student = await self.vector_store.search_student_contexts(
                query=query.query,
                profile_id=query.profile_id,
                n_results=query.max_student_results,
                filters=student_filters if student_filters else None
            )
            
            student_contexts = [
                RetrievedContext(
                    id=r["id"],
                    source="student",
                    content=r["content"],
                    relevance_score=r["score"],
                    metadata=r["metadata"]
                )
                for r in raw_student
            ]
        
        # Retrieve academic materials (Source B)
        if query.include_academic_sources:
            raw_academic = await self.vector_store.search_academic_documents(
                query=query.query,
                n_results=query.max_academic_results,
                filters=academic_filters if academic_filters else None
            )
            
            academic_contexts = [
                RetrievedContext(
                    id=r["id"],
                    source="academic",
                    content=r["content"],
                    relevance_score=r["score"],
                    metadata=r["metadata"]
                )
                for r in raw_academic
            ]
        
        # Detect gaps
        gaps = await self._detect_gaps(
            query.profile_id,
            query.query,
            student_contexts,
            academic_contexts
        )
        
        # Generate response
        answer, confidence = await self._generate_response(
            query.query,
            student_contexts,
            academic_contexts,
            preferred_modality,
            gaps
        )
        
        # Save to chat history if session provided
        if query.session_id:
            await self._save_chat_message(
                profile_id=query.profile_id,
                session_id=query.session_id,
                role="user",
                content=query.query,
                concept_id=query.concept_id
            )
            await self._save_chat_message(
                profile_id=query.profile_id,
                session_id=query.session_id,
                role="assistant",
                content=answer,
                concept_id=query.concept_id,
                student_context_ids=[c.id for c in student_contexts],
                academic_doc_ids=[c.id for c in academic_contexts]
            )
        
        # Store this interaction as new student context
        await self.add_student_context(
            profile_id=query.profile_id,
            context_data=StudentContextCreate(
                context_type="chat",
                content=f"Q: {query.query}\nA: {answer[:500]}",  # Truncate long answers
                concept_id=query.concept_id,
                subject=query.subject,
                topic=query.topic
            )
        )
        
        return DualRAGResponse(
            answer=answer,
            student_contexts=student_contexts,
            academic_contexts=academic_contexts,
            gaps_detected=gaps,
            confidence_score=confidence,
            modality_used=preferred_modality,
            sources_cited=[c.metadata.get("source_name", "Unknown") for c in academic_contexts[:3]]
        )
    
    async def _detect_gaps(
        self,
        profile_id: str,
        query: str,
        student_contexts: List[RetrievedContext],
        academic_contexts: List[RetrievedContext]
    ) -> List[Dict]:
        """Detect contradictions/gaps between student understanding and academic sources"""
        gaps = []
        
        # If we have both student context and academic sources, analyze for gaps
        if not student_contexts or not academic_contexts:
            return gaps
        
        # Simple keyword-based gap detection (can be enhanced with LLM)
        # For now, we'll return empty list - this would be enhanced with actual LLM analysis
        
        if self.openai_client:
            # Build prompts for gap analysis
            student_text = "\n".join([c.content for c in student_contexts[:3]])
            academic_text = "\n".join([c.content for c in academic_contexts[:3]])
            
            try:
                response = await self.openai_client.chat.completions.create(
                    model=settings.openai_model,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are an educational analyst. Compare the student's understanding 
                            with the academic sources and identify any misconceptions or gaps.
                            Return a JSON array of gaps, each with:
                            - concept_name: the concept with the gap
                            - student_understanding: what the student seems to believe
                            - correct_understanding: what the academic source states
                            - gap_description: brief description of the discrepancy
                            - severity: "minor", "moderate", "significant", or "critical"
                            If no gaps found, return empty array []."""
                        },
                        {
                            "role": "user",
                            "content": f"""Query: {query}
                            
Student's context/history:
{student_text}

Academic sources:
{academic_text}

Identify gaps between student understanding and academic truth."""
                        }
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                
                import json
                result = json.loads(response.choices[0].message.content)
                gaps = result.get("gaps", [])
                
                # Save detected gaps to database
                for gap in gaps:
                    await self.create_gap_analysis(
                        profile_id=profile_id,
                        gap_data=GapAnalysisCreate(
                            concept_name=gap.get("concept_name", "Unknown"),
                            student_understanding=gap.get("student_understanding", ""),
                            correct_understanding=gap.get("correct_understanding", ""),
                            gap_description=gap.get("gap_description", ""),
                            gap_severity=gap.get("severity", "moderate"),
                            student_context_ids=[c.id for c in student_contexts],
                            academic_doc_ids=[c.id for c in academic_contexts]
                        )
                    )
            except Exception as e:
                # Log error but don't fail the main query
                print(f"Gap analysis error: {e}")
        
        return gaps
    
    async def _generate_response(
        self,
        query: str,
        student_contexts: List[RetrievedContext],
        academic_contexts: List[RetrievedContext],
        modality: str,
        gaps: List[Dict]
    ) -> Tuple[str, float]:
        """Generate personalized response using retrieved context"""
        
        # Build context strings
        student_text = "\n".join([
            f"- {c.content}" for c in student_contexts
        ]) if student_contexts else "No previous context available."
        
        academic_text = "\n".join([
            f"- [{c.metadata.get('source_name', 'Source')}]: {c.content}" 
            for c in academic_contexts
        ]) if academic_contexts else "No academic sources found."
        
        # Modality-specific instructions
        modality_instructions = {
            "visual": "Use diagrams descriptions, bullet points, and visual metaphors. Structure information visually.",
            "verbal": "Explain thoroughly with detailed verbal descriptions. Use conversational tone.",
            "abstract": "Focus on underlying principles and theoretical frameworks. Use formal language.",
            "analogy": "Use many real-world analogies and comparisons to familiar concepts.",
            "interactive": "Include questions, prompts for reflection, and step-by-step walkthroughs."
        }
        
        modality_guide = modality_instructions.get(modality, modality_instructions["visual"])
        
        if self.openai_client:
            try:
                response = await self.openai_client.chat.completions.create(
                    model=settings.openai_model,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""You are SkillTwin, an adaptive AI personal mentor. 
                            
Your task is to answer the student's question using both their personal learning history 
and verified academic sources. Personalize your explanation based on their learning style.

Learning Style Preference: {modality}
Style Guide: {modality_guide}

Guidelines:
1. Reference the student's past interactions to build on their existing knowledge
2. Use academic sources for accuracy and cite them
3. Address any misconceptions gently
4. Keep explanations clear and at the appropriate level
5. End with a thought-provoking question or next step"""
                        },
                        {
                            "role": "user",
                            "content": f"""Student's Question: {query}

Student's Learning History:
{student_text}

Academic Sources:
{academic_text}

Known Gaps/Misconceptions to Address:
{gaps if gaps else "None detected"}

Please provide a personalized explanation."""
                        }
                    ],
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                confidence = 0.85  # Could be calculated based on source quality
                
                return answer, confidence
                
            except Exception as e:
                print(f"LLM generation error: {e}")
        
        # Fallback response without LLM
        fallback = f"""Based on your question about "{query}", here's what I found:

**From Academic Sources:**
{academic_text[:500] if academic_text else "No sources available."}

**Building on Your Previous Learning:**
{student_text[:300] if student_text != "No previous context available." else "This appears to be a new topic for you."}

For a more detailed, personalized explanation, please ensure the AI service is configured."""
        
        return fallback, 0.5
    
    async def _save_chat_message(
        self,
        profile_id: str,
        session_id: str,
        role: str,
        content: str,
        concept_id: Optional[str] = None,
        student_context_ids: List[str] = None,
        academic_doc_ids: List[str] = None
    ) -> ChatHistory:
        """Save a chat message to history"""
        message = ChatHistory(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            session_id=session_id,
            role=role,
            content=content,
            concept_id=concept_id,
            student_context_ids=student_context_ids or [],
            academic_doc_ids=academic_doc_ids or []
        )
        self.db.add(message)
        await self.db.commit()
        return message
    
    # ============ Gap Analysis Operations ============
    
    async def create_gap_analysis(
        self,
        profile_id: str,
        gap_data: GapAnalysisCreate
    ) -> GapAnalysis:
        """Create a gap analysis record"""
        gap = GapAnalysis(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            **gap_data.model_dump()
        )
        self.db.add(gap)
        await self.db.commit()
        await self.db.refresh(gap)
        
        # Also create a misconception in LTP if significant
        if gap_data.gap_severity in ["significant", "critical"]:
            from app.modules.ltp.schemas import MisconceptionCreate
            await self.ltp_service.create_misconception(
                profile_id=profile_id,
                misconception_data=MisconceptionCreate(
                    concept_id=gap_data.concept_id,
                    misconception_type="knowledge_gap",
                    description=gap_data.gap_description,
                    student_response=gap_data.student_understanding,
                    correct_understanding=gap_data.correct_understanding,
                    severity=gap_data.gap_severity.value,
                    detection_source="dual_rag"
                )
            )
        
        return gap
    
    async def get_unresolved_gaps(self, profile_id: str) -> List[GapAnalysis]:
        """Get unresolved gaps for a profile"""
        result = await self.db.execute(
            select(GapAnalysis)
            .where(
                and_(
                    GapAnalysis.profile_id == profile_id,
                    GapAnalysis.is_resolved == False
                )
            )
            .order_by(GapAnalysis.priority_score.desc())
        )
        return list(result.scalars().all())
    
    async def resolve_gap(
        self,
        gap_id: str,
        resolution: GapResolution
    ) -> Optional[GapAnalysis]:
        """Mark a gap as resolved"""
        result = await self.db.execute(
            select(GapAnalysis).where(GapAnalysis.id == gap_id)
        )
        gap = result.scalar_one_or_none()
        
        if gap:
            gap.is_resolved = True
            gap.resolution_strategy = resolution.resolution_strategy
            gap.resolved_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(gap)
        
        return gap
    
    # ============ Explanation Generation ============
    
    async def generate_explanation(
        self,
        request: ExplanationRequest
    ) -> ExplanationResponse:
        """Generate a personalized explanation for a concept"""
        
        # Get concept info
        concept = await self.ltp_service.get_concept(request.concept_id)
        if not concept:
            return ExplanationResponse(
                explanation="Concept not found.",
                modality_used="visual"
            )
        
        # Get preferred modality
        modality = request.preferred_modality
        if not modality:
            modality = await self.ltp_service.get_preferred_modality(request.profile_id)
        
        # Query the dual RAG system
        query_text = request.question or f"Explain {concept.name} in detail"
        
        rag_response = await self.process_query(DualRAGQuery(
            profile_id=request.profile_id,
            query=query_text,
            concept_id=request.concept_id,
            subject=concept.subject,
            topic=concept.topic
        ))
        
        return ExplanationResponse(
            explanation=rag_response.answer,
            modality_used=modality,
            analogies=[],  # Would extract from LLM response
            examples=[],
            related_concepts=[],
            sources=rag_response.sources_cited,
            follow_up_questions=[
                f"Can you explain how {concept.name} relates to real-world applications?",
                f"What are common mistakes when learning {concept.name}?",
                f"Can you give me a practice problem about {concept.name}?"
            ]
        )
    
    # ============ Semantic Search ============
    
    async def semantic_search(
        self,
        query: SemanticSearchQuery
    ) -> SemanticSearchResponse:
        """Perform semantic search across documents"""
        results = []
        
        filters = {}
        if query.subject:
            filters["subject"] = query.subject
        if query.topic:
            filters["topic"] = query.topic
        
        if query.source in ["student", "all"]:
            # Note: For student search we'd need profile_id - this is a general search
            pass
        
        if query.source in ["academic", "all"]:
            academic_results = await self.vector_store.search_academic_documents(
                query=query.query,
                n_results=query.limit,
                filters=filters if filters else None
            )
            
            for r in academic_results:
                results.append(SemanticSearchResult(
                    id=r["id"],
                    source="academic",
                    content=r["content"],
                    score=r["score"],
                    metadata=r["metadata"]
                ))
        
        return SemanticSearchResponse(
            results=results,
            total_found=len(results)
        )
    
    # ============ Chat History ============
    
    async def get_chat_history(
        self,
        profile_id: str,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[ChatHistory]:
        """Get chat history for a profile"""
        query = select(ChatHistory).where(ChatHistory.profile_id == profile_id)
        
        if session_id:
            query = query.where(ChatHistory.session_id == session_id)
        
        query = query.order_by(ChatHistory.created_at.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def submit_feedback(
        self,
        message_id: str,
        was_helpful: bool
    ) -> bool:
        """Submit feedback for a chat message"""
        result = await self.db.execute(
            select(ChatHistory).where(ChatHistory.id == message_id)
        )
        message = result.scalar_one_or_none()
        
        if message:
            message.was_helpful = was_helpful
            await self.db.commit()
            return True
        return False
