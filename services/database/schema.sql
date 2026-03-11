

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE meetings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title           VARCHAR(500) NOT NULL,
    started_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ended_at        TIMESTAMP WITH TIME ZONE,
    summary         TEXT,
    topic           VARCHAR(255),
    status          VARCHAR(50) DEFAULT 'in_progress'
                    CHECK (status IN ('in_progress', 'completed', 'archived')),
    language        VARCHAR(10) DEFAULT 'en',
    duration_secs   FLOAT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE speakers (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meeting_id      UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    label           VARCHAR(50) NOT NULL,
    name            VARCHAR(255),
    color           VARCHAR(7) DEFAULT '#6366f1',
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_speakers_meeting ON speakers(meeting_id);

CREATE TABLE transcript_segments (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meeting_id      UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    speaker_id      UUID REFERENCES speakers(id) ON DELETE SET NULL,
    start_time      FLOAT NOT NULL,
    end_time        FLOAT NOT NULL,
    content         TEXT NOT NULL,
    language        VARCHAR(10) DEFAULT 'en',
    confidence      FLOAT DEFAULT 0.0,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_segments_meeting ON transcript_segments(meeting_id);
CREATE INDEX idx_segments_time ON transcript_segments(start_time, end_time);

CREATE TABLE translations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    segment_id      UUID NOT NULL REFERENCES transcript_segments(id) ON DELETE CASCADE,
    target_language  VARCHAR(10) NOT NULL,
    translated_text TEXT NOT NULL,
    confidence      FLOAT DEFAULT 0.0,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_translations_segment ON translations(segment_id);

CREATE TABLE action_items (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meeting_id      UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    description     TEXT NOT NULL,
    assignee        VARCHAR(255),
    priority        VARCHAR(20) DEFAULT 'medium'
                    CHECK (priority IN ('high', 'medium', 'low')),
    status          VARCHAR(50) DEFAULT 'pending'
                    CHECK (status IN ('pending', 'in_progress', 'completed')),
    due_date        TIMESTAMP WITH TIME ZONE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_actions_meeting ON action_items(meeting_id);
CREATE INDEX idx_actions_status ON action_items(status);

CREATE TABLE meeting_topics (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meeting_id      UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    topic_name      VARCHAR(255) NOT NULL,
    keywords        TEXT[],
    relevance       FLOAT DEFAULT 0.0,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_topics_meeting ON meeting_topics(meeting_id);

INSERT INTO meetings (id, title, status, topic, language, summary)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Product Launch Planning',
    'completed',
    'Marketing Strategy',
    'en',
    'The team discussed finalizing the marketing plan and scheduling the campaign launch for Monday.'
);

INSERT INTO speakers (meeting_id, label, name, color) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'SPEAKER_00', 'Sarah Kim', '#6366f1'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'SPEAKER_01', 'James Park', '#f59e0b');
