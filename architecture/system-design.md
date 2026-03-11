# System Design — Meeting Intelligence Platform

## Overview

The system is a **microservices architecture** with four AI-powered services connected via Kafka message queues. Data is persisted in PostgreSQL and indexed in Elasticsearch for semantic search.

## Data Flow

```mermaid
sequenceDiagram
    participant Client as Browser / WebRTC
    participant GW as API Gateway
    participant Kafka as Kafka
    participant STT as Speech Service
    participant Diar as Diarization Service
    participant Trans as Translation Service
    participant Sum as Summarization Service
    participant DB as PostgreSQL
    participant ES as Elasticsearch

    Client->>GW: Audio stream (WebSocket)
    GW->>Kafka: Publish audio chunks
    Kafka->>STT: Consume audio
    STT->>STT: Whisper transcription
    STT->>Kafka: Publish transcript segments
    Kafka->>Diar: Consume audio + transcript
    Diar->>Diar: Speaker segmentation
    Diar->>Kafka: Publish diarized segments
    Kafka->>Trans: Consume segments
    Trans->>Trans: MarianMT KO↔EN
    Trans->>Kafka: Publish translations
    Kafka->>Sum: Consume full transcript
    Sum->>Sum: T5 summarization + action extraction
    Sum->>DB: Store results
    Sum->>ES: Index for search
    DB->>Client: REST API → Dashboard
    ES->>Client: Search results
```

## Service Boundaries

| Service | Responsibility | Model | Port |
|---|---|---|---|
| Speech Service | Audio → text transcription | Whisper (base/small) | 8001 |
| Diarization Service | Speaker identification & segmentation | pyannote.audio | 8002 |
| Translation Service | Bidirectional KO ↔ EN | MarianMT | 8003 |
| Summarization Service | Summary, action items, topics | T5 + BERTopic | 8004 |

## Data Models

```mermaid
erDiagram
    MEETING ||--o{ TRANSCRIPT_SEGMENT : contains
    MEETING ||--o{ ACTION_ITEM : produces
    MEETING ||--o{ SPEAKER : has
    TRANSCRIPT_SEGMENT }o--|| SPEAKER : spoken_by
    TRANSCRIPT_SEGMENT ||--o| TRANSLATION : translated_to

    MEETING {
        uuid id PK
        string title
        timestamp started_at
        timestamp ended_at
        text summary
        string topic
        string status
    }

    SPEAKER {
        uuid id PK
        uuid meeting_id FK
        string label
        string name
        string color
    }

    TRANSCRIPT_SEGMENT {
        uuid id PK
        uuid meeting_id FK
        uuid speaker_id FK
        float start_time
        float end_time
        text content
        string language
    }

    TRANSLATION {
        uuid id PK
        uuid segment_id FK
        string target_language
        text translated_text
    }

    ACTION_ITEM {
        uuid id PK
        uuid meeting_id FK
        text description
        string assignee
        string status
        timestamp due_date
    }
```

## Scalability Considerations

- **Kafka partitioning**: Scale consumers horizontally per service
- **Model serving**: GPU-backed pods with autoscaling
- **Elasticsearch**: Sharded index for high-volume search
- **WebSocket fan-out**: Redis Pub/Sub for multi-client broadcast
