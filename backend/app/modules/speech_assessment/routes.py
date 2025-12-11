from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.speech_assessment import services, schemas, models
import uuid
import time

router = APIRouter(
    prefix="/speech-assessment",
    tags=["Speech Assessment"]
)

@router.post("/analyze", response_model=schemas.AssessmentResponse)
async def analyze_speech(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload audio file for speech mastery assessment (Section 3.4).
    Analyzes clarity, confidence, and fluency.
    """
    if not file.filename.endswith(('.wav', '.mp3', '.m4a', '.flac')):
         raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        start_time = time.time()
        content = await file.read()
        
        # 1. Get Duration
        duration = services.AnalysisService.get_audio_duration(content)
        
        # 2. Transcribe
        transcript = await services.TranscriptionService.transcribe_audio(content)
        
        # 3. Analyze
        analysis_result = services.AnalysisService.analyze_speech(transcript, duration)
        
        processing_time = time.time() - start_time
        
        # 4. Save to DB (Mocking ID for now, in real app we'd save the file)
        assessment_id = str(uuid.uuid4())
        
        # In a real implementation, we would save to S3/Local and create a DB entry here.
        # For this prototype, we return the analysis directly.
        
        return schemas.AssessmentResponse(
            id=assessment_id,
            transcript=transcript,
            clarity_score=analysis_result["clarity_score"],
            confidence_score=analysis_result["confidence_score"],
            pace_wpm=analysis_result["pace_wpm"],
            filler_word_count=analysis_result["filler_word_count"],
            feedback=analysis_result["feedback"],
            processing_time=round(processing_time, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/{id}", response_model=schemas.AssessmentResponse)
async def get_assessment(id: str):
    """
    Retrieve past assessment result (Mock)
    """
    return schemas.AssessmentResponse(
        id=id,
        transcript="This is a mock retrieved transcript.",
        clarity_score=0.85,
        confidence_score=0.9,
        pace_wpm=120,
        filler_word_count=2,
        feedback=["Good retrieval."],
        processing_time=0.5
    )
