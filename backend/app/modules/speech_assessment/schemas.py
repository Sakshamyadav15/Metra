from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class AssessmentResponse(BaseModel):
    """Schema for returning assessment results"""
    id: str
    transcript: Optional[str] = None
    clarity_score: float = Field(..., description="0-1 score for clarity")
    confidence_score: float = Field(..., description="0-1 score for confidence")
    pace_wpm: float = Field(..., description="Words per minute")
    filler_word_count: int
    feedback: List[str] = Field(default_factory=list)
    processing_time: float
    
    model_config = ConfigDict(from_attributes=True)

class AudioUploadResponse(BaseModel):
    """Schema for audio upload response"""
    assessment_id: str
    message: str
    status: str
