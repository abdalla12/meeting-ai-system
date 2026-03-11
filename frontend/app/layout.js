import './globals.css';

export const metadata = {
    title: 'Meeting AI — Real-Time Meeting Intelligence',
    description: 'AI-powered meeting transcription, translation, summarization, and action item detection',
    keywords: 'meeting, AI, transcription, translation, summarization, speech recognition',
};

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
