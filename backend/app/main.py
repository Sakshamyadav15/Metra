"""
SkillTwin - Main FastAPI Application
Adaptive AI Personal Mentor Backend
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db

# Import all models to register them with SQLAlchemy
from app.models.user import User  # noqa: F401
from app.modules.ltp.models import (  # noqa: F401
    LearningTwinProfile,
    Concept,
    ConceptMastery,
    Misconception,
    LearningSession
)
from app.modules.dual_rag.models import (  # noqa: F401
    StudentContext,
    AcademicDocument,
    ChatHistory,
    GapAnalysis
)
from app.modules.micro_lessons.models import MicroLesson  # noqa: F401

# Import routers
from app.modules.ltp.routes import router as ltp_router
from app.modules.dual_rag.routes import router as dual_rag_router
from app.modules.micro_lessons.routes import router as micro_lessons_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup
    print("🚀 Starting SkillTwin Backend...")
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down SkillTwin Backend...")


# Create FastAPI app
app = FastAPI(
    title="SkillTwin API",
    description="""
    ## SkillTwin - Adaptive AI Personal Mentor
    
    A next-generation AI learning system engineered for:
    - Deep personalization through Learning Twin Profiles (LTP)
    - High-fidelity reasoning with Dual RAG
    - Multi-modal mastery assessment
    - Automated instructional content generation
    
    ### Modules
    
    - **LTP (3.1)**: Learning Twin Profile - Cognitive state modeling
    - **Dual RAG (3.2)**: Personalized Reasoning Engine
    - **Micro Lessons (3.3)**: Automated lesson generation (Mock)
    - **Speech Assessment (3.4)**: Speech-based mastery evaluation (Placeholder)
    - **Integrity (3.5)**: Authentication & verification layer (Placeholder)
    """,
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080", "*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ltp_router, prefix=settings.api_v1_prefix)
app.include_router(dual_rag_router, prefix=settings.api_v1_prefix)
app.include_router(micro_lessons_router, prefix=settings.api_v1_prefix)


# Root endpoint
@app.get("/")
async def root():
    return {
        "app": "SkillTwin",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "modules": {
            "ltp": "Learning Twin Profile (3.1) - Active",
            "dual_rag": "Dual RAG Engine (3.2) - Active",
            "micro_lessons": "Micro Lessons (3.3) - Mock",
            "speech_assessment": "Speech Assessment (3.4) - Placeholder",
            "integrity": "Integrity Layer (3.5) - Placeholder"
        }
    }


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# API info
@app.get(f"{settings.api_v1_prefix}/info")
async def api_info():
    return {
        "api_version": "v1",
        "endpoints": {
            "ltp": f"{settings.api_v1_prefix}/ltp",
            "rag": f"{settings.api_v1_prefix}/rag",
            "lessons": f"{settings.api_v1_prefix}/lessons"
        }
    }
