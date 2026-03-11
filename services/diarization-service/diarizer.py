

import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

_pipeline = None

def load_model(device: str = "cpu", hf_token: str = ""):
    
    global _pipeline
    try:
        from pyannote.audio import Pipeline

        logger.info("Loading pyannote speaker diarization pipeline...")
        _pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token if hf_token else None,
        )
        if device == "cuda":
            import torch
            _pipeline.to(torch.device("cuda"))
        logger.info("Pyannote pipeline loaded successfully.")
    except ImportError:
        logger.warning("pyannote.audio not installed. Using mock diarizer.")
        _pipeline = "mock"
    except Exception as e:
        logger.error(f"Failed to load pyannote pipeline: {e}")
        _pipeline = "mock"

def is_model_loaded() -> bool:
    return _pipeline is not None

def diarize_audio(
    audio_bytes: bytes,
    num_speakers: Optional[int] = None,
) -> Dict[str, Any]:
    
    global _pipeline

    if _pipeline is None:
        load_model()

    if _pipeline == "mock":
        return _mock_diarize(num_speakers)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        params = {}
        if num_speakers is not None:
            params["num_speakers"] = num_speakers

        diarization = _pipeline(tmp_path, **params)

        segments: List[Dict[str, Any]] = []
        speakers_set = set()

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speakers_set.add(speaker)
            segments.append({
                "speaker": speaker,
                "start": round(turn.start, 2),
                "end": round(turn.end, 2),
            })

        segments.sort(key=lambda s: s["start"])

        return {
            "speakers": sorted(list(speakers_set)),
            "segments": segments,
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)

def _mock_diarize(num_speakers: Optional[int] = None) -> Dict[str, Any]:
    
    n = num_speakers or 2
    speakers = [f"SPEAKER_{i:02d}" for i in range(n)]
    segments = [
        {"speaker": "SPEAKER_00", "start": 0.0, "end": 5.2},
        {"speaker": "SPEAKER_01", "start": 5.3, "end": 12.1},
        {"speaker": "SPEAKER_00", "start": 12.5, "end": 18.7},
        {"speaker": "SPEAKER_01", "start": 19.0, "end": 25.3},
    ]
    return {
        "speakers": speakers[:n],
        "segments": segments[:n * 2],
    }
