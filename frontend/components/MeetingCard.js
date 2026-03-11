'use client';

import Link from 'next/link';

const SPEAKER_COLORS = [
    '#6366f1', '#f59e0b', '#10b981', '#f43f5e',
    '#06b6d4', '#8b5cf6', '#ec4899', '#14b8a6',
];

export default function MeetingCard({ meeting }) {
    const statusClass =
        meeting.status === 'in_progress' ? 'status-live' :
            meeting.status === 'completed' ? 'status-completed' :
                'status-archived';

    const statusLabel =
        meeting.status === 'in_progress' ? '● LIVE' :
            meeting.status === 'completed' ? '✓ Completed' :
                'Archived';

    return (
        <Link href={`/meetings/${meeting.id}`}>
            <div className="meeting-card" id={`meeting-card-${meeting.id}`}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                    <h3 className="meeting-card-title">{meeting.title}</h3>
                    <span className={`status-badge ${statusClass}`}>{statusLabel}</span>
                </div>

                <div className="meeting-card-meta">
                    <span>📅 {meeting.date || 'Today'}</span>
                    <span>⏱️ {meeting.duration || '45 min'}</span>
                    <span>👥 {meeting.speakerCount || 2} speakers</span>
                </div>

                {meeting.topic && (
                    <span className="meeting-card-topic">{meeting.topic}</span>
                )}

                <div className="meeting-card-speakers">
                    {(meeting.speakers || ['Speaker 1', 'Speaker 2']).map((speaker, i) => (
                        <div
                            key={i}
                            className="speaker-badge"
                            style={{
                                backgroundColor: `${SPEAKER_COLORS[i % SPEAKER_COLORS.length]}15`,
                                borderColor: `${SPEAKER_COLORS[i % SPEAKER_COLORS.length]}40`,
                                color: SPEAKER_COLORS[i % SPEAKER_COLORS.length],
                            }}
                        >
                            <span
                                className="speaker-dot"
                                style={{ backgroundColor: SPEAKER_COLORS[i % SPEAKER_COLORS.length] }}
                            />
                            {speaker}
                        </div>
                    ))}
                </div>
            </div>
        </Link>
    );
}
