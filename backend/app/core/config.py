"""
SkillTwin - Core Configuration
Manages all application settings using Pydantic Settings
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "SkillTwin"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./skilltwin.db"
    
    # Google Gemini
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-2.0-flash"
    
    # ChromaDB
    chroma_persist_directory: str = "./chroma_db"
    
    # JWT Authentication
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LTP Settings
    ltp_update_threshold: float = 0.1  # Minimum change to trigger profile update
    concept_mastery_threshold: float = 0.8  # Score needed to mark concept as mastered
    
    # RAG Settings
    rag_top_k_student: int = 5  # Number of student context docs to retrieve
    rag_top_k_academic: int = 5  # Number of academic docs to retrieve
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()


settings = get_settings()
