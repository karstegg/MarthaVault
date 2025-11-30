---
name: Transcribe Voice Notes
description: Download WhatsApp voice notes, transcribe them, and correct common mining site mis-transcriptions (max 300 chars)
---

# Transcribe Voice Notes

Transcribe WhatsApp voice notes with automatic correction of commonly mis-transcribed mining terminology.

## When to Use This Skill

- You have WhatsApp voice notes to process
- You want automatic transcription with mining-site name corrections
- You need structured task creation from voice note content

## Usage

**Via slash command:**
```
/transcribe-voice-notes
```

**Via Python (if running independently):**
```bash
python transcribe_voice_notes.py --contact "27833911315" --limit 5
```

## Prerequisites

- WhatsApp MCP server running and authenticated
- `gpt-4o-mini-transcribe` model access
- `media/audio/` folder exists in vault

## Data Extraction

The skill performs these steps:

1. **Download**: Gets all audio messages from specified WhatsApp contact
2. **Copy**: Moves audio files to `media/audio/` for processing
3. **Transcribe**: Uses `gpt-4o-mini-transcribe` to convert audio to text
4. **Correct**: Applies mining site name corrections from built-in dictionary
5. **Output**: Returns corrected transcriptions ready for task creation

## Common Mis-Transcriptions (Corrections Applied)

| Mis-Transcribed | Actual Term | Notes |
|-----------------|------------|-------|
| Trinity | Nchwaning 3 / N3 | Most common - sounds like "Trinity" |
| Hutt | Haut | Plant/equipment location |
| Ubuntu | Update | When discussing software/systems |
| N2/NCH2 | Nchwaning 2 | Sometimes transcribed as different letters |
| Glory/Gloria | Gloria | Mine site name (usually correct) |

## Example Outputs

**Input**: Voice note: "This is an overview of the Trinity underground plant conveyors."

**Processed**: "This is an overview of the Nchwaning 3 underground plant conveyors."

**Input**: Voice note: "Why only ten faces blasted?"

**Processed**: "Why only ten faces blasted?" (No corrections needed)

## Output Format

Returns array of corrected transcriptions:
```json
{
  "transcriptions": [
    {
      "timestamp": "2025-11-26 06:49",
      "original": "This is an overview of the Trinity underground plant conveyors.",
      "corrected": "This is an overview of the Nchwaning 3 underground plant conveyors.",
      "corrections_applied": ["Trinity → Nchwaning 3"],
      "file_name": "voice_20251126_065442.ogg"
    }
  ]
}
```

## Validation Checks

- ✓ All audio files successfully downloaded
- ✓ All files copied to `media/audio/`
- ✓ All transcriptions generated
- ✓ Common corrections applied
- ✓ Output formatted for task creation

## Common Issues & Troubleshooting

**Issue**: "File not found" on transcription
- **Solution**: Ensure file was copied to `media/audio/` before transcribing

**Issue**: Correction not applied
- **Solution**: Check if term is in corrections dictionary; add new terms as needed

**Issue**: Wrong contact selected
- **Solution**: Verify phone number format (use 27XXXXXXXXX format without +)

## Next Steps After Transcription

1. Review corrected transcriptions
2. Create tasks from voice note content
3. Add to task list with appropriate tags (#site, #priority)
4. Link to relevant projects if applicable

## Advanced: Adding New Corrections

Edit the `corrections_dict` in `transcribe_voice_notes.py`:

```python
corrections_dict = {
    'trinity': 'Nchwaning 3',
    'hutt': 'Haut',
    'ubuntu': 'Update',
    # Add new corrections here
}
```

Then restart the skill for changes to take effect.
