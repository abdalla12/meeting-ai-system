'use client';

import { useState } from 'react';
import Sidebar from '../../../components/Sidebar';
import LiveTranscript from '../../../components/LiveTranscript';
import MeetingSummary from '../../../components/MeetingSummary';
import SpeakerBadge from '../../../components/SpeakerBadge';

const DEMO_SEGMENTS = [
    {
        speaker: 'SPEAKER_00',
        speakerName: 'Sarah Kim',
        start: 0.0,
        end: 8.5,
        text: 'Good morning everyone. Let\'s discuss the product launch timeline. We need to finalize the marketing plan by end of this week.',
        translation: '좋은 아침이에요. 제품 출시 일정에 대해 논의합시다. 이번 주 말까지 마케팅 계획을 마무리해야 합니다.',
    },
    {
        speaker: 'SPEAKER_01',
        speakerName: 'James Park',
        start: 9.0,
        end: 18.2,
        text: 'Agreed. I\'ve prepared the campaign brief. The social media campaign should start next Monday, and we need to coordinate with the design team.',
        translation: '동의합니다. 캠페인 브리프를 준비했습니다. 소셜 미디어 캠페인은 다음 주 월요일에 시작해야 하며, 디자인 팀과 조율이 필요합니다.',
    },
    {
        speaker: 'SPEAKER_00',
        speakerName: 'Sarah Kim',
        start: 19.0,
        end: 28.3,
        text: 'Great, what about the press release? We should send it out at least 3 days before the launch. Can you handle the media outreach?',
        translation: '좋아요, 보도 자료는 어떻게 되나요? 출시 최소 3일 전에 발송해야 합니다. 미디어 홍보를 담당해 주실 수 있나요?',
    },
    {
        speaker: 'SPEAKER_01',
        speakerName: 'James Park',
        start: 29.0,
        end: 38.5,
        text: 'Sure, I\'ll draft the press release today and share it for review tomorrow. We also need to update the landing page with the new pricing.',
    },
    {
        speaker: 'SPEAKER_00',
        speakerName: 'Sarah Kim',
        start: 39.0,
        end: 48.0,
        text: 'Perfect. Let me summarize our action items: finalize the marketing plan, start the social media campaign on Monday, draft the press release, and update the landing page.',
    },
    {
        speaker: 'SPEAKER_01',
        speakerName: 'James Park',
        start: 48.5,
        end: 55.0,
        text: 'Sounds good. I\'ll set up a follow-up meeting for Thursday to review progress. Let\'s make this launch a success!',
    },
];

const DEMO_SUMMARY = 'The team discussed the product launch timeline, focusing on finalizing the marketing plan, coordinating the social media campaign launch for Monday, preparing the press release, and updating the landing page with new pricing. Both team members committed to specific deliverables with a follow-up review scheduled for Thursday.';

const DEMO_ACTIONS = [
    { description: 'Finalize marketing plan by end of week', assignee: 'Sarah Kim', priority: 'high' },
    { description: 'Start social media campaign on Monday', assignee: 'James Park', priority: 'high' },
    { description: 'Draft press release and share for review', assignee: 'James Park', priority: 'medium' },
    { description: 'Update landing page with new pricing', assignee: 'James Park', priority: 'medium' },
    { description: 'Set up follow-up meeting for Thursday', assignee: 'James Park', priority: 'low' },
];

export default function MeetingDetailPage({ params }) {
    const [showTranslation, setShowTranslation] = useState(true);
    const [activeLang, setActiveLang] = useState('en');

    return (
        <div className="app-layout">
            <Sidebar />
            <main className="main-content">
                {}
                <div className="page-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '8px' }}>
                        <h1 className="page-title">Product Launch Planning</h1>
                        <span className="status-badge status-completed">✓ Completed</span>
                    </div>
                    <p className="page-subtitle">Mar 10, 2026 • 55 seconds • 2 speakers</p>
                </div>

                {}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <SpeakerBadge label="SPEAKER_00" name="Sarah Kim" index={0} />
                        <SpeakerBadge label="SPEAKER_01" name="James Park" index={1} />
                    </div>

                    <div className="lang-toggle">
                        <button
                            className={`lang-btn ${activeLang === 'en' ? 'active' : ''}`}
                            onClick={() => setActiveLang('en')}
                        >
                            English
                        </button>
                        <button
                            className={`lang-btn ${activeLang === 'ko' ? 'active' : ''}`}
                            onClick={() => setActiveLang('ko')}
                        >
                            한국어
                        </button>
                        <button
                            className={`lang-btn ${activeLang === 'both' ? 'active' : ''}`}
                            onClick={() => setActiveLang('both')}
                        >
                            Both
                        </button>
                    </div>
                </div>

                {}
                <div className="grid-2">
                    {}
                    <LiveTranscript
                        segments={DEMO_SEGMENTS.map(seg => ({
                            ...seg,
                            translation: activeLang === 'both' || activeLang === 'ko' ? seg.translation : undefined,
                        }))}
                        isLive={false}
                        title="Meeting Transcript"
                    />

                    {}
                    <MeetingSummary
                        summary={DEMO_SUMMARY}
                        topic="Product Launch Strategy"
                        actionItems={DEMO_ACTIONS}
                    />
                </div>
            </main>
        </div>
    );
}
