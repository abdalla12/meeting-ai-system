'use client';

import { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import SearchBar from '../../components/SearchBar';

const DEMO_RESULTS = [
    {
        id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        meetingTitle: 'Product Launch Planning',
        date: 'Mar 10, 2026',
        speaker: 'Sarah Kim',
        snippet: 'We need to <mark>finalize the marketing plan</mark> by end of this week.',
        relevance: 0.95,
    },
    {
        id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        meetingTitle: 'Product Launch Planning',
        date: 'Mar 10, 2026',
        speaker: 'James Park',
        snippet: 'The social media <mark>campaign</mark> should start next <mark>Monday</mark>.',
        relevance: 0.88,
    },
    {
        id: '3',
        meetingTitle: 'Investor Q1 Report Review',
        date: 'Mar 8, 2026',
        speaker: 'CEO',
        snippet: 'Our <mark>marketing</mark> spend increased by 15% but the ROI doubled compared to last quarter.',
        relevance: 0.72,
    },
    {
        id: '5',
        meetingTitle: '한국어 미팅 — 마케팅 전략',
        date: 'Mar 6, 2026',
        speaker: '김민수',
        snippet: '<mark>마케팅 계획</mark>을 다시 검토하고 캠페인 일정을 조정해야 합니다.',
        relevance: 0.68,
    },
];

export default function SearchPage() {
    const [results, setResults] = useState([]);
    const [hasSearched, setHasSearched] = useState(false);
    const [query, setQuery] = useState('');

    const handleSearch = (searchQuery) => {
        setQuery(searchQuery);
        setHasSearched(true);

        setResults(DEMO_RESULTS);
    };

    return (
        <div className="app-layout">
            <Sidebar />
            <main className="main-content">
                <div className="page-header" style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto 40px' }}>
                    <h1 className="page-title">Search Meetings</h1>
                    <p className="page-subtitle">Semantic search across all meeting transcripts, notes, and action items</p>
                </div>

                <div className="search-container">
                    <SearchBar onSearch={handleSearch} />

                    {hasSearched && (
                        <>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                marginBottom: '20px',
                            }}>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                                    Found <strong style={{ color: 'var(--text-primary)' }}>{results.length}</strong> results
                                    for &ldquo;<strong style={{ color: 'var(--accent-primary)' }}>{query}</strong>&rdquo;
                                </p>
                            </div>

                            {results.map((result, i) => (
                                <a
                                    key={i}
                                    href={`/meetings/${result.id}`}
                                    className="search-result"
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                                        <span className="search-result-title">{result.meetingTitle}</span>
                                        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                                            {Math.round(result.relevance * 100)}% relevant
                                        </span>
                                    </div>
                                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '8px' }}>
                                        📅 {result.date} • 👤 {result.speaker}
                                    </div>
                                    <p
                                        className="search-result-snippet"
                                        dangerouslySetInnerHTML={{ __html: result.snippet }}
                                    />
                                </a>
                            ))}
                        </>
                    )}

                    {!hasSearched && (
                        <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
                            <p style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</p>
                            <p style={{ fontSize: '16px' }}>Search in English or Korean across all meetings</p>
                            <p style={{ fontSize: '14px', marginTop: '8px' }}>
                                Try: &ldquo;marketing plan&rdquo;, &ldquo;action items&rdquo;, or &ldquo;마케팅 계획&rdquo;
                            </p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
