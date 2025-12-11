from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class IdentityVerificationRequest(BaseModel):
    user_id: str
    image_data_base64: str = Field(..., description="Base64 encoded image of the user")

class VerificationResponse(BaseModel):
    verified: bool
    confidence: float
    message: str
    details: Optional[Dict[str, Any]] = None

class SpoofCheckRequest(BaseModel):
    media_data_base64: str
    media_type: str = Field(..., pattern="^(audio|video)$")

class SpoofCheckResponse(BaseModel):
    is_spoof: bool
    spoof_probability: float
    spoofType: Optional[str] = None
    integrity_score: float
