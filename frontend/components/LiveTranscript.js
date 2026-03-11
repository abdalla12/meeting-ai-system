'use client';

import SpeakerBadge from './SpeakerBadge';

const SPEAKER_COLORS = [
    '#6366f1', '#f59e0b', '#10b981', '#f43f5e',
    '#06b6d4', '#8b5cf6', '#ec4899', '#14b8a6',
];

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

export default function LiveTranscript({
    segments = [],
    isLive = false,
    title = 'Transcript',
}) {

    const speakers = [...new Set(segments.map((s) => s.speaker))];

    return (
        <div className="transcript-container" id="live-transcript">
            <div className="transcript-header">
                <h3 style={{ fontWeight: 600, fontSize: '15px' }}>{title}</h3>
                {isLive && (
                    <div className="transcript-live-badge">
                        <span className="transcript-live-dot" />
                        LIVE
                    </div>
                )}
            </div>

            <div className="transcript-body">
                {segments.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
                        <p style={{ fontSize: '32px', marginBottom: '12px' }}>🎙️</p>
                        <p>Waiting for audio stream...</p>
                        <p style={{ fontSize: '13px', marginTop: '8px' }}>Upload an audio file or start a live session</p>
                    </div>
                ) : (
                    segments.map((segment, i) => {
                        const speakerIdx = speakers.indexOf(segment.speaker);
                        const color = SPEAKER_COLORS[speakerIdx % SPEAKER_COLORS.length];

                        return (
                            <div className="transcript-segment" key={i}>
                                <span className="transcript-timestamp">
                                    {formatTime(segment.start)}
                                </span>
                                <div style={{ flex: 1 }}>
                                    <div style={{ marginBottom: '6px' }}>
                                        <SpeakerBadge
                                            label={segment.speaker}
                                            name={segment.speakerName}
                                            index={speakerIdx}
                                            isActive={isLive && i === segments.length - 1}
                                        />
                                    </div>
                                    <div
                                        className="transcript-text"
                                        style={{ borderLeft: `3px solid ${color}`, paddingLeft: '12px' }}
                                    >
                                        {segment.text}
                                        {segment.translation && (
                                            <div style={{
                                                marginTop: '6px',
                                                fontSize: '13px',
                                                color: 'var(--text-secondary)',
                                                fontStyle: 'italic',
                                            }}>
                                                🌐 {segment.translation}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
}
