/**
 * SpeechBloom AI - Microphone Recording & Web Audio
 * Encodes directly to standard 16kHz Mono PCM WAV for universal backend acoustic processing.
 * Also integrates real-time SpeechRecognition with live transcript callbacks.
 */

// Universal 16-bit Mono PCM WAV Encoder
function encodeWAV(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  function writeString(offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }

  // RIFF Chunk Descriptor
  writeString(0, 'RIFF');
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(8, 'WAVE');

  // "fmt " Sub-chunk
  writeString(12, 'fmt ');
  view.setUint32(16, 16, true);          // Subchunk1Size (16 for PCM)
  view.setUint16(20, 1, true);           // AudioFormat (1 = PCM)
  view.setUint16(22, 1, true);           // NumChannels (1 = Mono)
  view.setUint32(24, sampleRate, true);  // SampleRate
  view.setUint32(28, sampleRate * 2, true); // ByteRate (SampleRate * NumChannels * BitsPerSample/8)
  view.setUint16(32, 2, true);           // BlockAlign (NumChannels * BitsPerSample/8)
  view.setUint16(34, 16, true);          // BitsPerSample (16 bits)

  // "data" Sub-chunk
  writeString(36, 'data');
  view.setUint32(40, samples.length * 2, true);

  // Write 16-bit PCM amplitude values
  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }

  return new Blob([buffer], { type: 'audio/wav' });
}


class AudioRecorder {
  constructor() {
    this.stream = null;
    this.audioContext = null;
    this.processor = null;
    this.input = null;
    this.recordedSamples = [];
    this.isRecording = false;
    this.recognition = null;
    this.transcript = '';
    this.onTranscriptUpdate = null;
  }

  async start(language = 'english', transcriptCallback = null) {
    this.recordedSamples = [];
    this.transcript = '';
    this.onTranscriptUpdate = transcriptCallback;

    // 1. Initialize Microphone Audio Stream
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        sampleRate: 16000,
        echoCancellation: true,
        noiseSuppression: true
      }
    });

    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.audioContext = new AudioContextClass({ sampleRate: 16000 });
    this.input = this.audioContext.createMediaStreamSource(this.stream);

    // Buffer audio samples
    const bufferSize = 4096;
    this.processor = this.audioContext.createScriptProcessor(bufferSize, 1, 1);
    this.processor.onaudioprocess = (e) => {
      if (!this.isRecording) return;
      const channelData = e.inputBuffer.getChannelData(0);
      for (let i = 0; i < channelData.length; i++) {
        this.recordedSamples.push(channelData[i]);
      }
    };

    this.input.connect(this.processor);
    this.processor.connect(this.audioContext.destination);
    this.isRecording = true;

    // 2. Start Real-Time Web Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        this.recognition = new SpeechRecognition();
        this.recognition.lang = language.toLowerCase() === 'hindi' ? 'hi-IN' : 'en-US';
        this.recognition.interimResults = true;
        this.recognition.continuous = true;

        this.recognition.onresult = (event) => {
          let currentHeard = '';
          for (let i = event.resultIndex; i < event.results.length; ++i) {
            currentHeard += event.results[i][0].transcript;
          }
          if (currentHeard.trim()) {
            this.transcript = currentHeard.trim();
            console.log('[Live Recognition] Heard:', this.transcript);
            if (this.onTranscriptUpdate) {
              this.onTranscriptUpdate(this.transcript);
            }
          }
        };

        this.recognition.onerror = (e) => {
          console.warn('[SpeechRecognition] Notice:', e.error);
        };

        this.recognition.start();
      } catch (err) {
        console.warn('Speech recognition notice:', err);
      }
    }
  }

  stop() {
    return new Promise((resolve) => {
      this.isRecording = false;

      if (this.recognition) {
        try { this.recognition.stop(); } catch (e) {}
      }

      setTimeout(() => {
        if (this.processor && this.input) {
          try {
            this.input.disconnect();
            this.processor.disconnect();
          } catch (e) {}
        }

        if (this.stream) {
          this.stream.getTracks().forEach(track => track.stop());
        }

        if (this.audioContext && this.audioContext.state !== 'closed') {
          this.audioContext.close();
        }

        // Encode recorded PCM samples to standard 16kHz WAV Blob
        const wavBlob = encodeWAV(this.recordedSamples, 16000);
        resolve({ blob: wavBlob, transcript: this.transcript });
      }, 200);
    });
  }
}

async function uploadAndAnalyzeAudio(audioBlob, metadata, transcript = '') {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'speech_recording.wav');
  formData.append('child_id', metadata.child_id || getSelectedChildId());
  formData.append('language', metadata.language || 'english');
  formData.append('target_word', metadata.target_word || '');
  formData.append('target_phoneme', metadata.target_phoneme || '');
  formData.append('observed_transcript', transcript || metadata.observed_transcript || '');

  // 1. Save recording to backend
  const saveRes = await fetch('/api/recording', {
    method: 'POST',
    body: formData
  });
  const saveData = await saveRes.json();
  if (!saveRes.ok || !saveData.success) {
    throw new Error(saveData.message || 'Failed to save audio recording');
  }

  // 2. Trigger acoustic & phonetic analysis
  const finalTranscript = transcript || saveData.observed_transcript || metadata.observed_transcript || '';
  const analyzeRes = await apiCall('/api/analyze', 'POST', {
    recording_id: saveData.recording_id,
    observed_transcript: finalTranscript
  });
  return analyzeRes;
}
