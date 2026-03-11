

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import config
from schemas import TranscriptionResponse, HealthResponse
from transcriber import load_model, is_model_loaded, transcribe_audio, transcribe_chunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    load_model(model_size=config.WHISPER_MODEL_SIZE, device=config.DEVICE)
    yield

app = FastAPI(
    title="Meeting AI — Speech Recognition Service",
    description="Real-time speech-to-text transcription powered by OpenAI Whisper",
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

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    file: UploadFile = File(..., description="Audio file (WAV, MP3, FLAC)"),
    language: str = Form("auto", description="Language code (en, ko, auto)"),
):
    
    audio_bytes = await file.read()
    logger.info(f"Received audio file: {file.filename} ({len(audio_bytes)} bytes), language={language}")

    result = transcribe_audio(audio_bytes, language=language)

    return TranscriptionResponse(
        text=result["text"],
        language=result["language"],
        segments=result["segments"],
        duration=result["duration"],
    )

@app.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    
    await websocket.accept()
    logger.info("WebSocket client connected for streaming transcription.")

    try:
        while True:

            audio_chunk = await websocket.receive_bytes()

            result = transcribe_chunk(audio_chunk, sample_rate=config.SAMPLE_RATE)

            await websocket.send_json(result)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
