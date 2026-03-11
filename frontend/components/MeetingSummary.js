'use client';

export default function MeetingSummary({ summary = '', topic = '', actionItems = [] }) {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {}
            <div className="summary-panel" id="meeting-summary">
                <div className="summary-header">
                    <span>📝</span>
                    Meeting Summary
                </div>
                <div className="summary-body">
                    {topic && (
                        <div style={{ marginBottom: '16px' }}>
                            <span className="meeting-card-topic" style={{ fontSize: '13px' }}>
                                {topic}
                            </span>
                        </div>
                    )}
                    <p className="summary-text">
                        {summary || 'Summary will be generated after the meeting ends...'}
                    </p>
                </div>
            </div>

            {}
            <div className="summary-panel" id="action-items">
                <div className="summary-header">
                    <span>✅</span>
                    Action Items
                    {actionItems.length > 0 && (
                        <span style={{
                            marginLeft: 'auto',
                            background: 'var(--gradient-primary)',
                            color: 'white',
                            padding: '2px 10px',
                            borderRadius: '100px',
                            fontSize: '12px',
                            fontWeight: '600',
                        }}>
                            {actionItems.length}
                        </span>
                    )}
                </div>
                <div className="summary-body">
                    {actionItems.length === 0 ? (
                        <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
                            Action items will be detected from the conversation...
                        </p>
                    ) : (
                        <div className="action-list">
                            {actionItems.map((item, i) => (
                                <div className="action-item" key={i}>
                                    <div className={`action-checkbox`} />
                                    <div style={{ flex: 1 }}>
                                        <div className="action-text">{item.description}</div>
                                        {item.assignee && (
                                            <div style={{
                                                fontSize: '12px',
                                                color: 'var(--text-muted)',
                                                marginTop: '4px',
                                            }}>
                                                👤 {item.assignee}
                                            </div>
                                        )}
                                    </div>
                                    <span className={`action-priority priority-${item.priority || 'medium'}`}>
                                        {item.priority || 'medium'}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
