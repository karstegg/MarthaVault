# Transcribe Voice Notes - Technical Reference

## Implementation Details

The skill uses the `mcp__whisper` MCP server (compiled WhatsApp MCP) to:
1. Download audio files from WhatsApp messages
2. Transcribe using `gpt-4o-mini-transcribe` model
3. Apply mining-site-specific corrections
4. Return structured output for task creation

## Corrections Dictionary

Mining terminology commonly mis-transcribed by speech-to-text engines:

```python
CORRECTIONS_DICT = {
    'trinity': 'Nchwaning 3',    # "Trinity" sounds like "Nchwaning 3"
    'n3': 'Nchwaning 3',         # N3 abbreviation variations
    'nch3': 'Nchwaning 3',       # Alternative abbreviation
    'hutt': 'Haut',              # Equipment location
    'ubuntu': 'Update',          # When discussing systems
    'n2': 'Nchwaning 2',         # Nchwaning 2 variations
    'nch2': 'Nchwaning 2',
    'gloria': 'Gloria',          # Usually correct, included for completeness
    'glory': 'Gloria',           # Common variant
}
```

## Adding New Corrections

When you discover a new mis-transcription:

1. **Identify the pattern**: What does the speech engine transcribe? (e.g., "Trinity")
2. **Identify the correct term**: What should it be? (e.g., "Nchwaning 3")
3. **Add to dictionary**: Update `CORRECTIONS_DICT` in `transcribe_voice_notes.py`
4. **Test**: Run `/transcribe-voice-notes --show-corrections` to verify

**Example workflow:**
```python
# In transcribe_voice_notes.py, add:
CORRECTIONS_DICT = {
    # ... existing corrections ...
    'new_mis_transcription': 'Correct Term',
}
```

## MCP Server Integration

The skill uses the compiled WhatsApp MCP server which provides:
- `mcp__whatsapp__list_messages` - Get messages from contact
- `mcp__whatsapp__download_media` - Download audio attachments
- `mcp__whisper__transcribe_audio` - Transcribe using GPT-4o mini

**Configuration location**: `.mcp.json` (global MCP config)

## File Processing Flow

```
WhatsApp Contact
     ↓
[List Messages] → Filter audio messages
     ↓
[Download Media] → Save to temp location
     ↓
[Copy to media/audio/] → Persistent storage
     ↓
[Transcribe Audio] → gpt-4o-mini-transcribe model
     ↓
[Apply Corrections] → Mining site name corrections
     ↓
[Format Output] → JSON with original + corrected text
     ↓
Task Creation Ready
```

## Known Limitations

1. **Homophones**: Speech engines struggle with mining terminology that sounds like common words
2. **Accents**: Some pronunciations may transcribe differently depending on speaker accent
3. **Background noise**: Loud environments (mine sites) may reduce accuracy
4. **Short phrases**: Very brief notes may have lower accuracy

## Performance Characteristics

- Download: ~1-2 seconds per audio file
- Transcription: ~5-10 seconds per file (depends on audio length)
- Correction: <100ms per file
- **Total for 3 voice notes**: ~20-30 seconds

## Accuracy Notes

The `gpt-4o-mini-transcribe` model is optimized for:
- Clear English speech
- Technical terminology
- Meeting transcripts

For mining-site-specific terms, the corrections dictionary compensates for common mis-transcriptions.

## Future Enhancements

1. **Context-aware corrections**: Use previous messages to infer context
2. **Audio quality detection**: Flag low-quality audio before transcription
3. **Speaker diarization**: Identify who is speaking (requires `gpt-4o-transcribe-diarize`)
4. **Custom terminology**: Allow user-defined industry-specific terms
5. **Batch processing**: Handle 10+ voice notes efficiently
6. **Confidence scoring**: Show transcription confidence levels

## Testing the Corrections

**View all corrections:**
```bash
python transcribe_voice_notes.py --show-corrections
```

**Output:**
```
Available Corrections Dictionary:
============================================================
  gloria                → Gloria
  glory                 → Gloria
  hutt                  → Haut
  n2                    → Nchwaning 2
  n3                    → Nchwaning 3
  nch2                  → Nchwaning 2
  nch3                  → Nchwaning 3
  trinity               → Nchwaning 3
  ubuntu                → Update
============================================================
```

## Troubleshooting

**Problem**: Correction not applied
- Check spelling in CORRECTIONS_DICT (case-insensitive matching used)
- Verify transcription contains the mis-transcribed word
- Consider if the word appears as part of another word (regex escaping handles this)

**Problem**: Over-correction
- Add more specific patterns if needed
- Example: If "trinity" appears legitimately, can refine pattern matching

**Problem**: New mining site terms not recognized
- Add to CORRECTIONS_DICT following the format
- Test with `--show-corrections` flag

## Maintenance Schedule

- **Weekly**: Review transcription quality for new patterns
- **Monthly**: Update corrections dictionary with discovered mis-transcriptions
- **Quarterly**: Review MCP server updates for model improvements
