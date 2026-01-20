---
'Status:': Reference
'Tags:': null
'Source:': https://argmaxinc.com
permalink: reference/claude-code/argmax-on-device-transcription
---

# Argmax - On-Device Transcription & Speaker Diarization

## Overview

Argmax develops SDKs for running foundation models locally on-device. Key products:

- **WhisperKit Pro** - Speech-to-text (real-time + file)
- **SpeakerKit Pro** - Speaker diarization (who said what)
- **DiffusionKit** - Image generation (coming soon)

## Key Features

### WhisperKit Pro
- Real-time streaming transcription
- Word-level timestamps
- Subtitle export
- Claims faster/more accurate than cloud APIs

### SpeakerKit Pro
- Voice activity detection
- Speaker diarization
- Based on Pyannote, optimized for speed

## Technical Details

- **Platform:** Apple Silicon (Mac, iPhone, iPad)
- **Frameworks:** CoreML, MLX
- **Power:** <3W with all features active
- **Latency:** Real-time capable

## Pricing

- Open-source tier available
- Pro tier: API key required, fixed per-device pricing
- No per-minute cloud costs

## Comparison to Whisper MCP

| Feature | Whisper MCP | Argmax |
|---------|-------------|--------|
| Transcription | Yes | Yes |
| Speaker ID | No | Yes |
| Real-time | No | Yes |
| Windows | Yes | No (Mac only) |

## Limitation

Currently Apple Silicon only - not usable on Windows work machine.

## When to Revisit

- If Windows/Linux support added
- If switching to Mac for personal use
- For mobile transcription apps

## Links

- Website: https://argmaxinc.com
- X Announcement: https://x.com/i/status/2001296557556040028

---

Archived via ClaudeBox triage 2025-12-20.