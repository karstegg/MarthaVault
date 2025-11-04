---
Status:: Reference
Priority:: High
Assignee:: Claude
DueDate::
Tags:: #year/2025 #reference #whatsapp #transcription #workflow
---

# WhatsApp Voice Note Transcription Workflow

## Standard Procedure

When transcribing WhatsApp voice notes, **ALWAYS** follow this workflow:

### Step 1: Download Media
```
mcp__whatsapp__download_media(message_id, chat_jid)
```
This downloads the audio file to the WhatsApp bridge store.

### Step 2: Copy to Media Folder
**CRITICAL**: Immediately after downloading, copy the file to the MarthaVault media/audio folder:

```bash
cp "SOURCE_PATH" "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio\DESCRIPTIVE_NAME.ogg"
```

**Naming Convention**:
- Use format: `{sender}_{YYYYMMDD}_{HHMMSS}.ogg`
- Example: `bosduif_20251031_114559.ogg`
- Keep sender names lowercase and simple

### Step 3: Transcribe Audio
```
mcp__whisper__transcribe_audio(
    input_file_name="DESCRIPTIVE_NAME.ogg",
    model="gpt-4o-mini-transcribe",
    response_format="text"
)
```

**Note**: The Whisper MCP server is configured to look in:
`C:/Users/10064957/My Drive/GDVault/MarthaVault/media/audio`

This is set in `.mcp.json` via the `AUDIO_FILES_PATH` environment variable.

## Why This Matters

1. **File Accessibility**: Whisper MCP can only access files in its configured audio folder
2. **Archival**: Keeps all voice notes in one organized location
3. **Naming**: Descriptive filenames make it easy to find transcriptions later
4. **Consistency**: Ensures repeatable workflow every time

## Example Full Workflow

```
User: "What did bosduif's last voice note say?"

1. Download:
   mcp__whatsapp__download_media("3A53B456518CA0255707", "27836383038@s.whatsapp.net")
   → Returns: C:\whatsapp-mcp\whatsapp-bridge\store\27836383038@s.whatsapp.net\audio_20251031_114559.ogg

2. Copy to media folder:
   cp "C:\whatsapp-mcp\whatsapp-bridge\store\27836383038@s.whatsapp.net\audio_20251031_114559.ogg" \
      "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio\bosduif_20251031_114559.ogg"

3. Transcribe:
   mcp__whisper__transcribe_audio("bosduif_20251031_114559.ogg", "gpt-4o-mini-transcribe", "text")
   → Returns transcription text
```

## Common Mistakes to Avoid

❌ **DON'T**: Try to transcribe directly from WhatsApp bridge store path
❌ **DON'T**: Use generic filenames like "audio_123.ogg"
❌ **DON'T**: Skip the copy step

✅ **DO**: Always copy to media/audio first
✅ **DO**: Use descriptive, consistent naming
✅ **DO**: Keep original WhatsApp filenames as reference in the copied name

## Configuration Reference

**MCP Configuration** (`.mcp.json`):
```json
{
  "mcpServers": {
    "whisper": {
      "env": {
        "AUDIO_FILES_PATH": "C:/Users/10064957/My Drive/GDVault/MarthaVault/media/audio"
      }
    }
  }
}
```

## Related References
- [[reference/claude-code/2025-10-21 – Calendar Automation System.md]] - Similar automation pattern
- [[media/audio/]] - Audio archive location

#workflow #whatsapp #transcription #automation #year/2025
