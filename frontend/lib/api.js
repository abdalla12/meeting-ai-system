const API_BASE = {
    speech: process.env.NEXT_PUBLIC_SPEECH_API || 'http://localhost:8001',
    diarization: process.env.NEXT_PUBLIC_DIARIZATION_API || 'http://localhost:8002',
    translation: process.env.NEXT_PUBLIC_TRANSLATION_API || 'http://localhost:8003',
    summarization: process.env.NEXT_PUBLIC_SUMMARIZATION_API || 'http://localhost:8004',
};

export async function transcribeAudio(file, language = 'auto') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);

    const res = await fetch(`${API_BASE.speech}/transcribe`, {
        method: 'POST',
        body: formData,
    });
    return res.json();
}

export async function diarizeAudio(file, numSpeakers = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (numSpeakers) formData.append('num_speakers', numSpeakers);

    const res = await fetch(`${API_BASE.diarization}/diarize`, {
        method: 'POST',
        body: formData,
    });
    return res.json();
}

export async function translateText(text, sourceLang, targetLang) {
    const res = await fetch(`${API_BASE.translation}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text,
            source_language: sourceLang,
            target_language: targetLang,
        }),
    });
    return res.json();
}

export async function summarizeTranscript(transcript, maxLength = 200) {
    const res = await fetch(`${API_BASE.summarization}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript, max_length: maxLength }),
    });
    return res.json();
}

export async function extractActions(transcript) {
    const res = await fetch(`${API_BASE.summarization}/extract-actions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript }),
    });
    return res.json();
}

export async function extractTopics(transcript, numTopics = 5) {
    const res = await fetch(`${API_BASE.summarization}/extract-topics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript, num_topics: numTopics }),
    });
    return res.json();
}

export async function checkHealth(service) {
    try {
        const res = await fetch(`${API_BASE[service]}/health`);
        return res.json();
    } catch {
        return { status: 'unreachable', model_loaded: false };
    }
}
