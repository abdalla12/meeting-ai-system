# API Contracts

## Speech Service (Port 8001)

### `POST /transcribe`
Upload an audio file for transcription.

**Request**: `multipart/form-data`
| Field | Type | Description |
|---|---|---|
| `file` | binary | Audio file (WAV, MP3, FLAC) |
| `language` | string | Language code (e.g. `en`, `ko`, `auto`) |

**Response** `200 OK`:
```json
{
  "text": "We need to finalize the marketing plan.",
  "language": "en",
  "segments": [
    { "start": 0.0, "end": 3.5, "text": "We need to finalize" },
    { "start": 3.5, "end": 6.2, "text": "the marketing plan." }
  ],
  "duration": 6.2
}
```

### `WebSocket /ws/transcribe`
Real-time streaming transcription.

**Client → Server**: Raw audio bytes (16kHz, 16-bit PCM)
**Server → Client**:
```json
{ "type": "partial", "text": "We need to..." }
{ "type": "final", "text": "We need to finalize the marketing plan.", "start": 0.0, "end": 6.2 }
```

---

## Diarization Service (Port 8002)

### `POST /diarize`
Identify speakers in audio.

**Request**: `multipart/form-data`
| Field | Type | Description |
|---|---|---|
| `file` | binary | Audio file |
| `num_speakers` | int | Expected number of speakers (optional) |

**Response** `200 OK`:
```json
{
  "speakers": ["SPEAKER_00", "SPEAKER_01"],
  "segments": [
    { "speaker": "SPEAKER_00", "start": 0.0, "end": 5.2 },
    { "speaker": "SPEAKER_01", "start": 5.3, "end": 12.1 }
  ]
}
```

---

## Translation Service (Port 8003)

### `POST /translate`
Translate text between Korean and English.

**Request**:
```json
{
  "text": "마케팅 계획을 마무리해야 합니다.",
  "source_language": "ko",
  "target_language": "en"
}
```

**Response** `200 OK`:
```json
{
  "translated_text": "We need to finalize the marketing plan.",
  "source_language": "ko",
  "target_language": "en",
  "confidence": 0.94
}
```

---

## Summarization Service (Port 8004)

### `POST /summarize`
Generate a meeting summary.

**Request**:
```json
{
  "transcript": "Speaker 1: We need to finalize marketing...",
  "max_length": 150,
  "min_length": 50
}
```

**Response** `200 OK`:
```json
{
  "summary": "The team discussed finalizing the marketing plan and scheduling the campaign launch for Monday.",
  "topic": "Product Launch Planning"
}
```

### `POST /extract-actions`
Extract action items from transcript.

**Request**:
```json
{
  "transcript": "Speaker 1: We need to finalize... Speaker 2: Campaign starts Monday."
}
```

**Response** `200 OK`:
```json
{
  "action_items": [
    { "description": "Finalize marketing plan", "assignee": "Speaker 1", "priority": "high" },
    { "description": "Launch campaign Monday", "assignee": "Speaker 2", "priority": "medium" }
  ]
}
```

### `POST /extract-topics`
Extract topics from meeting transcript.

**Request**:
```json
{
  "transcript": "...",
  "num_topics": 5
}
```

**Response** `200 OK`:
```json
{
  "topics": [
    { "name": "Marketing Strategy", "keywords": ["marketing", "campaign", "launch"], "relevance": 0.92 },
    { "name": "Timeline", "keywords": ["monday", "schedule", "deadline"], "relevance": 0.78 }
  ]
}
```

---

## Health Check (All Services)

### `GET /health`
**Response** `200 OK`:
```json
{ "status": "healthy", "model_loaded": true, "version": "1.0.0" }
```
