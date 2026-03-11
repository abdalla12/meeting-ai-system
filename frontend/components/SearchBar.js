'use client';

import { useState } from 'react';

export default function SearchBar({ onSearch }) {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (onSearch && query.trim()) {
            onSearch(query.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="search-input-wrapper">
                <span className="search-icon">🔍</span>
                <input
                    id="search-input"
                    type="text"
                    className="search-input"
                    placeholder="Search across all meetings... (e.g., 'marketing plan' or '마케팅 계획')"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    autoComplete="off"
                />
            </div>
        </form>
    );
}
