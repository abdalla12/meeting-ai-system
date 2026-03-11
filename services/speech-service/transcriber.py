

import io
import logging
import tempfile
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

_model = None
_model_size = None

def load_model(model_size: str = "base", device: str = "cpu"):
    
    global _model, _model_size
    try:
        import whisper
        logger.info(f"Loading Whisper model '{model_size}' on {device}...")
        _model = whisper.load_model(model_size, device=device)
        _model_size = model_size
        logger.info(f"Whisper model '{model_size}' loaded successfully.")
    except ImportError:
        logger.warning("openai-whisper not installed. Using mock transcriber.")
        _model = "mock"
        _model_size = model_size
    except Exception as e:
        logger.error(f"Failed to load Whisper model: {e}")
        _model = "mock"
        _model_size = model_size

def is_model_loaded() -> bool:
    return _model is not None

def transcribe_audio(
    audio_bytes: bytes,
    language: str = "auto",
    sample_rate: int = 16000
) -> Dict[str, Any]:
    
    global _model

    if _model is None:
        load_model()

    if _model == "mock":
        return _mock_transcribe(language)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        options = {}
        if language and language != "auto":
            options["language"] = language

        result = _model.transcribe(tmp_path, **options)

        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"].strip()
            })

        detected_lang = result.get("language", language)
        duration = segments[-1]["end"] if segments else 0.0

        return {
            "text": result["text"].strip(),
            "language": detected_lang,
            "segments": segments,
            "duration": round(duration, 2)
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)

def transcribe_chunk(audio_chunk: bytes, sample_rate: int = 16000) -> Dict[str, Any]:
    
    global _model

    if _model is None or _model == "mock":
        return {"type": "partial", "text": "[streaming transcription...]"}

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_chunk)
        tmp_path = tmp.name

    try:
        result = _model.transcribe(tmp_path)
        return {
            "type": "final",
            "text": result["text"].strip(),
            "start": 0.0,
            "end": 0.0
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)

def _mock_transcribe(language: str) -> Dict[str, Any]:
    
    return {
        "text": "We need to finalize the marketing plan. The campaign should start next Monday.",
        "language": "en" if language == "auto" else language,
        "segments": [
            {"start": 0.0, "end": 3.5, "text": "We need to finalize the marketing plan."},
            {"start": 3.6, "end": 6.2, "text": "The campaign should start next Monday."}
        ],
        "duration": 6.2
    }
