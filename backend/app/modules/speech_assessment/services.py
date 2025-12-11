import speech_recognition as sr
from pydub import AudioSegment
import io
import re
import os
import uuid
from typing import Tuple, Dict, Any

class TranscriptionService:
    @staticmethod
    async def transcribe_audio(file_content: bytes) -> str:
        """
        Transcribes audio content using SpeechRecognition.
        Supports WAV, FLAC, AIFF. 
        Note: For production, we might need ffmpeg for MP3 conversion via pydub.
        """
        r = sr.Recognizer()
        
        # Determine if we need conversion (heuristic: check header or try-except)
        # For this prototype, we'll try to load it into AudioSegment first to standardize to WAV
        try:
            # Load audio from bytes
            audio = AudioSegment.from_file(io.BytesIO(file_content))
            
            # Export to wav for SpeechRecognition
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)
            
            with sr.AudioFile(wav_io) as source:
                audio_data = r.record(source)
                try:
                    # Using Google Web Speech API for prototype (free, no key needed usually)
                    text = r.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    return ""
                except sr.RequestError:
                    return "Error: Speech service unavailable"
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

class AnalysisService:
    @staticmethod
    def analyze_speech(transcript: str, duration_seconds: float) -> Dict[str, Any]:
        """
        Analyzes speech transcript for mastery indicators.
        """
        if not transcript:
            return {
                "clarity_score": 0.0,
                "confidence_score": 0.0,
                "pace_wpm": 0.0,
                "filler_word_count": 0,
                "feedback": ["Audio was not clear or empty."]
            }

        words = transcript.split()
        word_count = len(words)
        
        # 1. Filler Word Analysis
        filler_words = ['um', 'uh', 'like', 'you know', 'sort of', 'actually', 'basically']
        filler_count = 0
        for filler in filler_words:
            filler_count += len(re.findall(r'\b' + re.escape(filler) + r'\b', transcript.lower()))
            
        # 2. Pace (Words Per Minute)
        wpm = (word_count / duration_seconds) * 60 if duration_seconds > 0 else 0
        
        # 3. Clarity & Confidence (Heuristic)
        # Less fillers = higher confidence
        # Good pacing (100-150 wpm) = higher clarity
        
        confidence_base = 1.0
        confidence_penalty = min(0.5, (filler_count / max(1, word_count)) * 5) # Penalty for fillers
        confidence_score = max(0.0, confidence_base - confidence_penalty)
        
        clarity_score = 0.8 # Base
        if 100 <= wpm <= 160:
            clarity_score = min(1.0, clarity_score + 0.2)
        elif wpm < 80 or wpm > 200:
            clarity_score = max(0.0, clarity_score - 0.3)
            
        feedback = []
        if filler_count > 2:
            feedback.append(f"Detected {filler_count} filler words. Try to pause instead of using fillers.")
        if wpm > 180:
            feedback.append("You are speaking quite fast. Try to slow down for better clarity.")
        if wpm < 90:
            feedback.append("You are speaking a bit slowly. Try to maintain a steady flow.")
        if word_count < 5:
             feedback.append("Explanation was too short to analyze accurately.")
             confidence_score *= 0.5 # Penalize very short answers

        return {
            "clarity_score": round(clarity_score, 2),
            "confidence_score": round(confidence_score, 2),
            "pace_wpm": round(wpm, 1),
            "filler_word_count": filler_count,
            "feedback": feedback
        }

    @staticmethod
    def get_audio_duration(file_content: bytes) -> float:
        try:
            audio = AudioSegment.from_file(io.BytesIO(file_content))
            return len(audio) / 1000.0 # Duration in seconds
        except:
            return 0.0
