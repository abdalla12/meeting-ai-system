

export class TranscriptionSocket {
    constructor(url = 'ws://localhost:8001/ws/transcribe') {
        this.url = url;
        this.ws = null;
        this.onTranscript = null;
        this.onError = null;
        this.onClose = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                this.reconnectAttempts = 0;
                resolve();
            };

            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (this.onTranscript) {
                    this.onTranscript(data);
                }
            };

            this.ws.onerror = (error) => {
                if (this.onError) this.onError(error);
                reject(error);
            };

            this.ws.onclose = () => {
                if (this.onClose) this.onClose();
                this._tryReconnect();
            };
        });
    }

    sendAudioChunk(chunk) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(chunk);
        }
    }

    disconnect() {
        this.maxReconnectAttempts = 0;
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    _tryReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
            setTimeout(() => this.connect().catch(() => { }), delay);
        }
    }
}
