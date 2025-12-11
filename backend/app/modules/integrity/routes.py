from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.integrity import schemas, services

router = APIRouter(
    prefix="/integrity",
    tags=["Integrity & Authentication"]
)

@router.post("/verify-identity", response_model=schemas.VerificationResponse)
async def verify_identity(request: schemas.IdentityVerificationRequest):
    """
    Verifies user identity against registered biometric data.
    Section 3.5: Pre-assessment identity verification.
    """
    try:
        result = services.IdentityService.verify_identity(request.user_id, request.image_data_base64)
        return schemas.VerificationResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}"
        )

@router.post("/check-spoof", response_model=schemas.SpoofCheckResponse)
async def check_spoof(request: schemas.SpoofCheckRequest):
    """
    Checks media for signs of deepfake or manipulation.
    Section 3.5: Audio/Video spoof detection.
    """
    try:
        result = services.SpoofDetectionService.detect_spoof(request.media_data_base64, request.media_type)
        return schemas.SpoofCheckResponse(**result)
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Spoof check failed: {str(e)}"
        )
