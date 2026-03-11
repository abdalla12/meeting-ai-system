'use client';

import Sidebar from '../components/Sidebar';
import MeetingCard from '../components/MeetingCard';

const DEMO_MEETINGS = [
    {
        id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        title: 'Product Launch Planning',
        date: 'Mar 10, 2026',
        duration: '45 min',
        status: 'completed',
        topic: 'Marketing Strategy',
        speakerCount: 2,
        speakers: ['Sarah Kim', 'James Park'],
    },
    {
        id: 'live',
        title: 'Weekly Engineering Standup',
        date: 'Today',
        duration: '12 min (ongoing)',
        status: 'in_progress',
        topic: 'Sprint Review',
        speakerCount: 4,
        speakers: ['Alex Chen', 'Yuna Lee', 'Dev Team', 'PM'],
    },
    {
        id: '3',
        title: 'Investor Q1 Report Review',
        date: 'Mar 8, 2026',
        duration: '60 min',
        status: 'completed',
        topic: 'Financial Review',
        speakerCount: 3,
        speakers: ['CEO', 'CFO', 'COO'],
    },
    {
        id: '4',
        title: 'Customer Onboarding Process',
        date: 'Mar 7, 2026',
        duration: '30 min',
        status: 'archived',
        topic: 'Customer Success',
        speakerCount: 2,
        speakers: ['Support Lead', 'Product Manager'],
    },
    {
        id: '5',
        title: '한국어 미팅 — 마케팅 전략',
        date: 'Mar 6, 2026',
        duration: '55 min',
        status: 'completed',
        topic: '마케팅',
        speakerCount: 3,
        speakers: ['김민수', '이지은', '박서준'],
    },
    {
        id: '6',
        title: 'Cross-functional Design Sprint',
        date: 'Mar 5, 2026',
        duration: '90 min',
        status: 'completed',
        topic: 'UX Design',
        speakerCount: 5,
        speakers: ['Designer', 'Engineer', 'PM', 'QA', 'Data'],
    },
];

const STATS = [
    { value: '247', label: 'Total Meetings', icon: '📊' },
    { value: '1,284', label: 'Action Items', icon: '✅' },
    { value: '12', label: 'Languages', icon: '🌐' },
    { value: '98.2%', label: 'Accuracy', icon: '🎯' },
];

export default function DashboardPage() {
    return (
        <div className="app-layout">
            <Sidebar />
            <main className="main-content">
                {}
                <div className="page-header">
                    <h1 className="page-title">Dashboard</h1>
                    <p className="page-subtitle">Real-time meeting intelligence at a glance</p>
                </div>

                {}
                <div className="grid-4" style={{ marginBottom: '32px' }}>
                    {STATS.map((stat, i) => (
                        <div className="stat-card" key={i}>
                            <div style={{ fontSize: '24px', marginBottom: '8px' }}>{stat.icon}</div>
                            <div className="stat-value">{stat.value}</div>
                            <div className="stat-label">{stat.label}</div>
                        </div>
                    ))}
                </div>

                {}
                <div
                    className="card"
                    style={{
                        marginBottom: '32px',
                        background: 'linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.1) 100%)',
                        borderColor: 'rgba(99,102,241,0.3)',
                    }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                                <span className="transcript-live-badge">
                                    <span className="transcript-live-dot" />
                                    LIVE NOW
                                </span>
                                <h3 style={{ fontSize: '18px', fontWeight: '600' }}>Weekly Engineering Standup</h3>
                            </div>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                                4 speakers • 12 min elapsed • Auto-translating Korean ↔ English
                            </p>
                        </div>
                        <a href="/meetings/live" className="btn btn-primary">Join Live</a>
                    </div>
                </div>

                {}
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h2 style={{ fontSize: '20px', fontWeight: '700' }}>Recent Meetings</h2>
                    <button className="btn btn-secondary">View All</button>
                </div>

                <div className="grid-3">
                    {DEMO_MEETINGS.map((meeting) => (
                        <MeetingCard key={meeting.id} meeting={meeting} />
                    ))}
                </div>
            </main>
        </div>
    );
}
