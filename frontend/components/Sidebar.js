'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
    const pathname = usePathname();

    const navItems = [
        { href: '/', icon: '🏠', label: 'Dashboard' },
        { href: '/meetings/live', icon: '🎙️', label: 'Live Meeting' },
        { href: '/meetings/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', icon: '📋', label: 'Recent Meeting' },
        { href: '/search', icon: '🔍', label: 'Search' },
    ];

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">
                <div className="sidebar-logo-icon">🎙️</div>
                <span className="sidebar-logo-text">Meeting AI</span>
            </div>

            <nav className="sidebar-nav">
                {navItems.map((item) => (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={`nav-item ${pathname === item.href ? 'active' : ''}`}
                    >
                        <span className="nav-item-icon">{item.icon}</span>
                        <span>{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className="sidebar-footer">
                <div className="nav-item">
                    <span className="nav-item-icon">⚙️</span>
                    <span>Settings</span>
                </div>
            </div>
        </aside>
    );
}
