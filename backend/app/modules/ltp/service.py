"""
SkillTwin - Learning Twin Profile (LTP) Service
Business logic for managing learner cognitive profiles
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.ltp.models import (
    LearningTwinProfile,
    Concept,
    ConceptMastery,
    Misconception,
    LearningSession,
    MasteryLevel
)
from app.modules.ltp.schemas import (
    LTPCreate,
    LTPUpdate,
    ConceptCreate,
    ConceptMasteryUpdate,
    MisconceptionCreate,
    MisconceptionUpdate,
    LearningSessionCreate,
    LearningSessionUpdate,
    LTPAnalytics,
    KnowledgeGraphNode,
    KnowledgeGraphEdge,
    KnowledgeGraphResponse
)
from app.core.config import settings


class LTPService:
    """Service class for Learning Twin Profile operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ============ LTP CRUD Operations ============
    
    async def create_profile(self, user_id: str) -> LearningTwinProfile:
        """Create a new Learning Twin Profile for a user"""
        profile = LearningTwinProfile(
            id=str(uuid.uuid4()),
            user_id=user_id,
            modality_preferences={
                "visual": 0.5,
                "verbal": 0.5,
                "abstract": 0.5,
                "analogy": 0.5,
                "interactive": 0.5
            }
        )
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile
    
    async def get_profile_by_user_id(self, user_id: str) -> Optional[LearningTwinProfile]:
        """Get LTP by user ID"""
        result = await self.db.execute(
            select(LearningTwinProfile)
            .where(LearningTwinProfile.user_id == user_id)
            .options(
                selectinload(LearningTwinProfile.concept_masteries),
                selectinload(LearningTwinProfile.misconceptions),
                selectinload(LearningTwinProfile.learning_sessions)
            )
        )
        return result.scalar_one_or_none()
    
    async def get_profile_by_id(self, profile_id: str) -> Optional[LearningTwinProfile]:
        """Get LTP by profile ID"""
        result = await self.db.execute(
            select(LearningTwinProfile)
            .where(LearningTwinProfile.id == profile_id)
            .options(
                selectinload(LearningTwinProfile.concept_masteries),
                selectinload(LearningTwinProfile.misconceptions),
                selectinload(LearningTwinProfile.learning_sessions)
            )
        )
        return result.scalar_one_or_none()
    
    async def update_profile(self, profile_id: str, update_data: LTPUpdate) -> Optional[LearningTwinProfile]:
        """Update LTP with new data"""
        profile = await self.get_profile_by_id(profile_id)
        if not profile:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(profile, key, value)
        
        profile.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(profile)
        return profile
    
    async def update_activity(self, profile_id: str) -> None:
        """Update last activity timestamp and streak"""
        profile = await self.get_profile_by_id(profile_id)
        if not profile:
            return
        
        now = datetime.utcnow()
        
        # Update streak
        if profile.last_activity_at:
            days_since_last = (now.date() - profile.last_activity_at.date()).days
            if days_since_last == 1:
                profile.current_streak_days += 1
            elif days_since_last > 1:
                profile.current_streak_days = 1
        else:
            profile.current_streak_days = 1
        
        # Update longest streak
        if profile.current_streak_days > profile.longest_streak_days:
            profile.longest_streak_days = profile.current_streak_days
        
        profile.last_activity_at = now
        profile.updated_at = now
        await self.db.commit()
    
    # ============ Concept Operations ============
    
    async def create_concept(self, concept_data: ConceptCreate) -> Concept:
        """Create a new concept"""
        concept = Concept(
            id=str(uuid.uuid4()),
            **concept_data.model_dump()
        )
        self.db.add(concept)
        await self.db.commit()
        await self.db.refresh(concept)
        return concept
    
    async def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get concept by ID"""
        result = await self.db.execute(
            select(Concept).where(Concept.id == concept_id)
        )
        return result.scalar_one_or_none()
    
    async def get_concepts_by_subject(self, subject: str) -> List[Concept]:
        """Get all concepts for a subject"""
        result = await self.db.execute(
            select(Concept).where(Concept.subject == subject)
        )
        return list(result.scalars().all())
    
    async def get_all_concepts(self) -> List[Concept]:
        """Get all concepts"""
        result = await self.db.execute(select(Concept))
        return list(result.scalars().all())
    
    # ============ Concept Mastery Operations ============
    
    async def get_or_create_concept_mastery(
        self, 
        profile_id: str, 
        concept_id: str
    ) -> ConceptMastery:
        """Get existing mastery record or create new one"""
        result = await self.db.execute(
            select(ConceptMastery)
            .where(
                and_(
                    ConceptMastery.profile_id == profile_id,
                    ConceptMastery.concept_id == concept_id
                )
            )
        )
        mastery = result.scalar_one_or_none()
        
        if not mastery:
            mastery = ConceptMastery(
                id=str(uuid.uuid4()),
                profile_id=profile_id,
                concept_id=concept_id,
                next_review_at=datetime.utcnow() + timedelta(days=1)
            )
            self.db.add(mastery)
            await self.db.commit()
            await self.db.refresh(mastery)
            
            # Update profile stats
            profile = await self.get_profile_by_id(profile_id)
            if profile:
                profile.total_concepts_attempted += 1
                await self.db.commit()
        
        return mastery
    
    async def update_concept_mastery(
        self,
        profile_id: str,
        concept_id: str,
        update_data: ConceptMasteryUpdate
    ) -> Optional[ConceptMastery]:
        """Update mastery record with new learning data"""
        mastery = await self.get_or_create_concept_mastery(profile_id, concept_id)
        
        # Handle quiz/practice result
        if update_data.correct is not None:
            mastery.attempts_count += 1
            if update_data.correct:
                mastery.correct_count += 1
            
            # Recalculate mastery score based on accuracy
            mastery.mastery_score = mastery.correct_count / mastery.attempts_count
            
            # Update spaced repetition using SM-2 algorithm
            mastery = self._update_spaced_repetition(mastery, update_data.correct)
        
        # Direct score updates
        if update_data.mastery_score is not None:
            mastery.mastery_score = update_data.mastery_score
        
        if update_data.confidence_score is not None:
            mastery.confidence_score = update_data.confidence_score
        
        # Update mastery level based on score
        mastery.mastery_level = self._calculate_mastery_level(mastery.mastery_score)
        
        # Check if newly mastered
        if (mastery.mastery_level in [MasteryLevel.MASTERED.value, MasteryLevel.EXPERT.value] 
            and mastery.mastered_at is None):
            mastery.mastered_at = datetime.utcnow()
            
            # Update profile stats
            profile = await self.get_profile_by_id(profile_id)
            if profile:
                profile.total_concepts_mastered += 1
                await self.db.commit()
        
        mastery.last_practiced_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(mastery)
        return mastery
    
    def _calculate_mastery_level(self, score: float) -> str:
        """Calculate mastery level from score"""
        if score >= 0.95:
            return MasteryLevel.EXPERT.value
        elif score >= 0.8:
            return MasteryLevel.MASTERED.value
        elif score >= 0.5:
            return MasteryLevel.PARTIAL.value
        elif score > 0:
            return MasteryLevel.LEARNING.value
        return MasteryLevel.NOT_STARTED.value
    
    def _update_spaced_repetition(self, mastery: ConceptMastery, correct: bool) -> ConceptMastery:
        """Update spaced repetition parameters using SM-2 algorithm"""
        if correct:
            if mastery.review_interval_days == 1:
                mastery.review_interval_days = 6
            else:
                mastery.review_interval_days = int(mastery.review_interval_days * mastery.ease_factor)
            mastery.ease_factor = min(2.5, mastery.ease_factor + 0.1)
        else:
            mastery.review_interval_days = 1
            mastery.ease_factor = max(1.3, mastery.ease_factor - 0.2)
        
        mastery.next_review_at = datetime.utcnow() + timedelta(days=mastery.review_interval_days)
        return mastery
    
    async def get_concepts_due_for_review(self, profile_id: str, limit: int = 10) -> List[ConceptMastery]:
        """Get concepts that need review based on spaced repetition"""
        result = await self.db.execute(
            select(ConceptMastery)
            .where(
                and_(
                    ConceptMastery.profile_id == profile_id,
                    ConceptMastery.next_review_at <= datetime.utcnow()
                )
            )
            .order_by(ConceptMastery.next_review_at)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_profile_masteries(self, profile_id: str) -> List[ConceptMastery]:
        """Get all mastery records for a profile"""
        result = await self.db.execute(
            select(ConceptMastery)
            .where(ConceptMastery.profile_id == profile_id)
            .options(selectinload(ConceptMastery.concept))
        )
        return list(result.scalars().all())
    
    # ============ Misconception Operations ============
    
    async def create_misconception(
        self,
        profile_id: str,
        misconception_data: MisconceptionCreate
    ) -> Misconception:
        """Record a new misconception"""
        misconception = Misconception(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            **misconception_data.model_dump()
        )
        self.db.add(misconception)
        await self.db.commit()
        await self.db.refresh(misconception)
        return misconception
    
    async def get_active_misconceptions(self, profile_id: str) -> List[Misconception]:
        """Get unresolved misconceptions"""
        result = await self.db.execute(
            select(Misconception)
            .where(
                and_(
                    Misconception.profile_id == profile_id,
                    Misconception.is_resolved == False
                )
            )
            .order_by(Misconception.detected_at.desc())
        )
        return list(result.scalars().all())
    
    async def resolve_misconception(
        self,
        misconception_id: str,
        update_data: MisconceptionUpdate
    ) -> Optional[Misconception]:
        """Mark a misconception as resolved"""
        result = await self.db.execute(
            select(Misconception).where(Misconception.id == misconception_id)
        )
        misconception = result.scalar_one_or_none()
        
        if misconception:
            misconception.is_resolved = update_data.is_resolved
            misconception.resolution_notes = update_data.resolution_notes
            misconception.resolved_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(misconception)
        
        return misconception
    
    # ============ Learning Session Operations ============
    
    async def start_session(
        self,
        profile_id: str,
        session_data: LearningSessionCreate
    ) -> LearningSession:
        """Start a new learning session"""
        session = LearningSession(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            **session_data.model_dump()
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        
        # Update activity
        await self.update_activity(profile_id)
        
        return session
    
    async def end_session(
        self,
        session_id: str,
        update_data: LearningSessionUpdate
    ) -> Optional[LearningSession]:
        """End a learning session with final stats"""
        result = await self.db.execute(
            select(LearningSession).where(LearningSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if session:
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(session, key, value)
            
            if not session.ended_at:
                session.ended_at = datetime.utcnow()
            
            # Calculate duration if not provided
            if session.duration_minutes == 0:
                duration = session.ended_at - session.started_at
                session.duration_minutes = int(duration.total_seconds() / 60)
            
            # Update profile study time
            profile = await self.get_profile_by_id(session.profile_id)
            if profile:
                profile.total_study_time_minutes += session.duration_minutes
                await self.db.commit()
            
            await self.db.commit()
            await self.db.refresh(session)
        
        return session
    
    # ============ Analytics Operations ============
    
    async def get_analytics(self, profile_id: str) -> LTPAnalytics:
        """Generate comprehensive analytics for a profile"""
        profile = await self.get_profile_by_id(profile_id)
        masteries = await self.get_profile_masteries(profile_id)
        misconceptions = await self.get_active_misconceptions(profile_id)
        
        # Concepts by mastery level
        concepts_by_mastery = {}
        subjects_progress = {}
        subject_totals = {}
        
        for m in masteries:
            level = m.mastery_level
            concepts_by_mastery[level] = concepts_by_mastery.get(level, 0) + 1
            
            if m.concept:
                subject = m.concept.subject
                if subject not in subjects_progress:
                    subjects_progress[subject] = 0
                    subject_totals[subject] = 0
                subjects_progress[subject] += m.mastery_score
                subject_totals[subject] += 1
        
        # Calculate subject progress percentages
        for subject in subjects_progress:
            if subject_totals[subject] > 0:
                subjects_progress[subject] = (subjects_progress[subject] / subject_totals[subject]) * 100
        
        # Get top strengths (mastered concepts)
        top_strengths = [
            m.concept.name for m in masteries 
            if m.mastery_level in [MasteryLevel.MASTERED.value, MasteryLevel.EXPERT.value]
            and m.concept
        ][:5]
        
        # Areas for improvement (low mastery + misconceptions)
        areas_for_improvement = [
            m.concept.name for m in masteries
            if m.mastery_level in [MasteryLevel.LEARNING.value, MasteryLevel.PARTIAL.value]
            and m.concept
        ][:5]
        
        # Calculate overall progress
        total_concepts = len(masteries) if masteries else 1
        mastered_count = len([m for m in masteries if m.mastery_level in [MasteryLevel.MASTERED.value, MasteryLevel.EXPERT.value]])
        overall_progress = (mastered_count / total_concepts) * 100 if total_concepts > 0 else 0
        
        return LTPAnalytics(
            profile_id=profile_id,
            overall_progress=overall_progress,
            concepts_by_mastery=concepts_by_mastery,
            subjects_progress=subjects_progress,
            learning_velocity_trend=[profile.learning_velocity] * 7 if profile else [0] * 7,
            top_strengths=top_strengths,
            areas_for_improvement=areas_for_improvement,
            recommended_next_concepts=[],  # Would need more logic
            study_time_weekly=[0] * 7,  # Would need session aggregation
            streak_info={
                "current": profile.current_streak_days if profile else 0,
                "longest": profile.longest_streak_days if profile else 0
            }
        )
    
    async def get_knowledge_graph(self, profile_id: str) -> KnowledgeGraphResponse:
        """Generate knowledge graph for visualization"""
        masteries = await self.get_profile_masteries(profile_id)
        concepts = await self.get_all_concepts()
        
        # Create mastery lookup
        mastery_lookup = {m.concept_id: m for m in masteries}
        
        nodes = []
        edges = []
        
        for concept in concepts:
            mastery = mastery_lookup.get(concept.id)
            nodes.append(KnowledgeGraphNode(
                id=concept.id,
                name=concept.name,
                mastery_level=mastery.mastery_level if mastery else MasteryLevel.NOT_STARTED.value,
                mastery_score=mastery.mastery_score if mastery else 0.0,
                subject=concept.subject,
                topic=concept.topic
            ))
            
            # Add prerequisite edges
            for prereq_id in concept.prerequisite_ids:
                edges.append(KnowledgeGraphEdge(
                    source=prereq_id,
                    target=concept.id,
                    relationship="prerequisite"
                ))
        
        return KnowledgeGraphResponse(nodes=nodes, edges=edges)
    
    # ============ Modality Preference Learning ============
    
    async def update_modality_preference(
        self,
        profile_id: str,
        modality: str,
        success: bool,
        learning_rate: float = 0.1
    ) -> None:
        """Update modality preference based on learning success"""
        profile = await self.get_profile_by_id(profile_id)
        if not profile or modality not in profile.modality_preferences:
            return
        
        current_pref = profile.modality_preferences[modality]
        
        # Increase preference if successful, decrease if not
        if success:
            new_pref = min(1.0, current_pref + learning_rate)
        else:
            new_pref = max(0.0, current_pref - learning_rate * 0.5)
        
        profile.modality_preferences[modality] = new_pref
        profile.updated_at = datetime.utcnow()
        await self.db.commit()
    
    async def get_preferred_modality(self, profile_id: str) -> str:
        """Get the most preferred learning modality"""
        profile = await self.get_profile_by_id(profile_id)
        if not profile or not profile.modality_preferences:
            return "visual"  # Default
        
        return max(profile.modality_preferences, key=profile.modality_preferences.get)
