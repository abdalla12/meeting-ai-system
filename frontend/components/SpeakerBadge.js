'use client';

const SPEAKER_COLORS = [
    '#6366f1', '#f59e0b', '#10b981', '#f43f5e',
    '#06b6d4', '#8b5cf6', '#ec4899', '#14b8a6',
];

export default function SpeakerBadge({ label, name, index = 0, isActive = false }) {
    const color = SPEAKER_COLORS[index % SPEAKER_COLORS.length];

    return (
        <div
            className="speaker-badge"
            style={{
                backgroundColor: `${color}15`,
                borderColor: `${color}40`,
                color: color,
            }}
        >
            <span
                className="speaker-dot"
                style={{
                    backgroundColor: color,
                    animation: isActive ? 'pulse-dot 1s infinite' : 'none',
                }}
            />
            <span>{name || label}</span>
        </div>
    );
}
