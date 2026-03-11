from pydantic import BaseModel, Field
from typing import List, Optional

class DiarizationSegment(BaseModel):
    speaker: str = Field(..., description="Speaker label (e.g. SPEAKER_00)")
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")

class DiarizationRequest(BaseModel):
    num_speakers: Optional[int] = Field(None, description="Expected number of speakers")

class DiarizationResponse(BaseModel):
    speakers: List[str] = Field(..., description="List of detected speaker labels")
    segments: List[DiarizationSegment] = Field(..., description="Speaker segments with timestamps")

class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool = False
    version: str = "1.0.0"
