---
name: whatsapp-voice-transcribe
description: Download and transcribe WhatsApp voice notes with mining site name corrections
---

# WhatsApp Voice Transcribe

Download WhatsApp voice notes, move them to the vault, transcribe them, and apply common mining site corrections.

## What This Skill Does

1. **Lists** recent WhatsApp messages from a contact
2. **Downloads** audio messages 
3. **Moves** files to vault media folder using Filesystem MCP
4. **Transcribes** using Whisper MCP with gpt-4o-mini-transcribe
5. **Corrects** common mining site mis-transcriptions

## When to Use

- User says "transcribe my voice note"
- User asks to "check my WhatsApp voice messages"
- User mentions transcribing audio from WhatsApp
- User wants to process voice notes from a specific contact

## Step-by-Step Workflow

### Step 1: Find Voice Notes

```
whatsapp:list_messages
- chat_jid: 27833911315@s.whatsapp.net (or other contact)
- limit: 5
- include_context: false
```

Look for messages marked as `[audio - Message ID: ... - Chat JID: ...]`

### Step 2: Download Media

```
whatsapp:download_media
- message_id: [from step 1]
- chat_jid: [from step 1]
```

File downloads to: `C:\whatsapp-mcp\whatsapp-bridge\store\[chat_jid]\audio_[timestamp].ogg`

### Step 3: Move to Vault (CRITICAL)

**Use Filesystem MCP, NOT bash cp:**

```
Filesystem:move_file
- source: C:\whatsapp-mcp\whatsapp-bridge\store\[chat_jid]\audio_[timestamp].ogg
- destination: C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio\[descriptive_name].ogg
```

**Why**: Filesystem MCP operates on Windows directly. Bash runs in Linux container and cannot access C:\ paths.

### Step 4: Transcribe

```
whisper:transcribe_audio
- input_file_name: [filename from step 3]
- model: gpt-4o-mini-transcribe
- response_format: text
```

### Step 5: Apply Corrections

Common mining site mis-transcriptions to correct:

| Mis-Transcribed | Correct | Context |
|-----------------|---------|---------|
| Trinity | Nchwaning 3 / N3 | Most common |
| Hutt | Haut | Plant location |
| Ubuntu | Update | Software context |
| Glory | Gloria | Mine site |
| N2/NCH2 variations | Nchwaning 2 | Letter mix-ups |
| Magalbin | Mugg & Bean | Coffee shop chain |

## Example Usage

**User**: "Transcribe my latest voice note to myself"

**Claude executes**:
1. Lists messages from 27833911315@s.whatsapp.net
2. Finds latest audio: `AC5B1B9A1C849D7E5803F94CAC9FB434`
3. Downloads to WhatsApp store
4. Moves to `media/audio/self_20251127_143637.ogg`
5. Transcribes: "This is a test voice note..."
6. Applies corrections if needed
7. Returns corrected transcription

## Common Contacts

- **Self**: 27833911315@s.whatsapp.net
- **Jacques Breet**: 27834418149@s.whatsapp.net
- **Production Engineering Group**: 27834418149-1537194373@g.us

## Critical Technical Notes

### Why Filesystem:move_file Works

- **Desktop Chat runs in Linux container** - bash commands can't see Windows paths
- **Filesystem MCP runs on Windows** - direct access to C:\ drives
- **move_file handles binary files** - no encoding issues
- **Tested and working** as of 2025-11-28

### Why NOT to Use

❌ `bash cp` - Can't access Windows paths from Linux container
❌ `read_media_file` then `write_file` - Returns "unsupported format"
❌ Python shutil in bash - Same container limitation

✅ `Filesystem:move_file` - Works perfectly

## Validation Checks

Before returning results, verify:
- ✓ Audio file downloaded successfully
- ✓ File moved to `media/audio/` folder
- ✓ Transcription generated
- ✓ Common corrections applied
- ✓ Output formatted clearly

## Output Format

Return structured output:

```
Transcription: "[corrected text]"
File: media/audio/[filename].ogg
Duration: [if available]
Corrections Applied: [list any corrections made]
```

## Troubleshooting

**"File not found" on transcription**
- Verify Step 3 completed (file moved to media/audio/)
- Check filename matches exactly

**"No such file or directory" with bash**
- Don't use bash for file operations
- Use Filesystem:move_file instead

**No audio messages found**
- Verify contact phone number format
- Check WhatsApp MCP is connected
- Try with chat_jid instead of sender_phone_number

## Integration Points

After transcription, consider:
- Extract action items → create tasks
- Add to master_task_list.md
- Link to relevant projects
- Create meeting notes if applicable

## Status

✅ **Production Ready** - Tested 2025-11-28
- Workflow validated in Claude Desktop
- All MCP connections working
- Mining corrections dictionary loaded
