

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

import config
from schemas import DiarizationResponse, HealthResponse
from diarizer import load_model, is_model_loaded, diarize_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model(device=config.DEVICE, hf_token=config.HF_AUTH_TOKEN)
    yield

app = FastAPI(
    title="Meeting AI — Speaker Diarization Service",
    description="Speaker identification using pyannote.audio",
    version=config.SERVICE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        model_loaded=is_model_loaded(),
        version=config.SERVICE_VERSION,
    )

@app.post("/diarize", response_model=DiarizationResponse)
async def diarize(
    file: UploadFile = File(..., description="Audio file (WAV, MP3, FLAC)"),
    num_speakers: Optional[int] = Form(None, description="Expected number of speakers"),
):
    
    audio_bytes = await file.read()
    logger.info(f"Received audio: {file.filename} ({len(audio_bytes)} bytes), num_speakers={num_speakers}")

    result = diarize_audio(audio_bytes, num_speakers=num_speakers)

    return DiarizationResponse(
        speakers=result["speakers"],
        segments=result["segments"],
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
