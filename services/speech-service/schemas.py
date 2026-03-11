from pydantic import BaseModel, Field
from typing import List, Optional

class TranscriptSegment(BaseModel):
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    text: str = Field(..., description="Transcribed text for this segment")

class TranscriptionRequest(BaseModel):
    language: Optional[str] = Field("auto", description="Language code (en, ko, auto)")

class TranscriptionResponse(BaseModel):
    text: str = Field(..., description="Full transcribed text")
    language: str = Field(..., description="Detected or specified language")
    segments: List[TranscriptSegment] = Field(default_factory=list, description="Time-aligned segments")
    duration: float = Field(..., description="Total audio duration in seconds")

class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool = False
    version: str = "1.0.0"

class WSTranscriptMessage(BaseModel):
    type: str = Field(..., description="'partial' or 'final'")
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
