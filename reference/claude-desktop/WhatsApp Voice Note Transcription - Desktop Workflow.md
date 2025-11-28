# WhatsApp Voice Note Transcription - Desktop Workflow

**Last Updated**: 2025-11-28  
**Status**: ✅ Tested and Working in Claude Desktop

---

## Overview

Complete workflow for downloading WhatsApp voice notes and transcribing them in Claude Desktop using MCP tools.

## Prerequisites

- WhatsApp MCP server connected
- Whisper MCP server connected
- Voice notes available in WhatsApp

---

## 3-Step Desktop Workflow

### Step 1: List Messages to Find Voice Notes

```
List my recent messages to myself (or from [contact]) to find audio messages
```

**Claude will execute:**
```
whatsapp:list_messages
- sender_phone_number: [contact]
- limit: 10
- include_context: false
```

**Look for:** `[audio - Message ID: XXXXX - Chat JID: YYYYY]`

---

### Step 2: Download and Move to Vault

**User request:**
```
Download the latest voice note and move it to my vault media folder
```

**Claude executes:**

1. **Download:**
```
whatsapp:download_media
- message_id: [from step 1]
- chat_jid: [from step 1]
```
→ Downloads to: `C:\whatsapp-mcp\whatsapp-bridge\store\[chat_jid]\audio_[timestamp].ogg`

2. **Move to vault:**
```
Filesystem:move_file
- source: C:\whatsapp-mcp\whatsapp-bridge\store\[chat_jid]\audio_[timestamp].ogg
- destination: C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio\[descriptive_name].ogg
```

**✅ Critical**: Use `Filesystem:move_file` NOT bash `cp` - the Filesystem MCP operates on Windows directly.

---

### Step 3: Transcribe

**User request:**
```
Transcribe the voice note
```

**Claude executes:**
```
whisper:transcribe_audio
- input_file_name: [filename from step 2]
- model: gpt-4o-mini-transcribe
- response_format: text
```

---

## Common Mining Site Corrections

Apply these corrections manually after transcription:

| Mis-Transcribed | Correct Term | Context |
|-----------------|--------------|---------|
| Trinity | Nchwaning 3 / N3 | Most common error |
| Hutt | Haut | Plant location |
| Ubuntu | Update | Software context |
| Glory | Gloria | Mine site name |
| N2/NCH2 | Nchwaning 2 | Letter variations |

---

## Example: Complete Workflow

**User:** "Check my latest voice note to myself and transcribe it"

**Claude executes:**

1. `whatsapp:list_messages` → Found audio message `AC5B1B9A...`
2. `whatsapp:download_media` → Downloaded to WhatsApp store
3. `Filesystem:move_file` → Moved to `media/audio/self_20251127_143637.ogg`
4. `whisper:transcribe_audio` → Returns transcription text
5. Apply corrections → Replace "Trinity" with "Nchwaning 3" if present

**Output:**
```
Transcription: "This is an overview of the Nchwaning 3 underground plant conveyors."
File: media/audio/self_20251127_143637.ogg
```

---

## Why This Works in Desktop (Not Just CLI)

**Desktop has these advantages:**
- ✅ Filesystem MCP for Windows file operations
- ✅ WhatsApp MCP for message access
- ✅ Whisper MCP for transcription
- ✅ Native Memory for workflow learning

**Key insight**: Use `Filesystem:move_file` instead of bash commands - it operates directly on Windows, bypassing the Linux container limitation.

---

## Troubleshooting

### "File not found" on transcription
- **Cause**: File wasn't moved to `media/audio/` 
- **Fix**: Verify Step 2 completed successfully

### "Unsupported format" on read_media_file
- **Cause**: Tool returns base64 but isn't displayed properly
- **Fix**: Use `move_file` instead (it handles binary correctly)

### Bash `cp` fails with "No such file or directory"
- **Cause**: Bash runs in Linux container, can't see `C:\` paths
- **Fix**: Use `Filesystem:move_file` MCP tool

### Missing corrections in output
- **Review**: Check corrections dictionary in this document
- **Apply**: Manual find/replace after transcription

---

## Advanced: Batch Processing

**User request:**
```
Transcribe my last 5 voice notes to myself
```

**Claude will:**
1. List last 5 audio messages
2. Download each → Move to vault (with numbered filenames)
3. Transcribe each
4. Return consolidated list with corrections applied

---

## Integration with Task Management

After transcription:

1. **Extract action items** from transcribed text
2. **Create task files** in `tasks/`
3. **Add to master_task_list.md** with proper tags
4. **Link to projects** if relevant

**Example task creation:**
```
- [ ] Fix Trinity plant conveyor alignment issue #priority/high #site/N3 📅 2025-11-29
```

---

## Technical Notes

**Why Desktop ≠ CLI for this:**
- CLI has direct Windows PowerShell access
- CLI skills are Python scripts with subprocess calls
- Desktop uses MCP tools that bridge to Windows
- Desktop Chat has Native Memory (learns your patterns)

**Desktop advantage:**
- Conversational workflow (no slash commands needed)
- Native Memory learns your corrections preferences
- Can combine with web search for technical context
- Better for ad-hoc requests vs. batch operations

**CLI advantage:**
- Direct system access (no MCP needed)
- Better for automated batch processing
- Can use Python scripts directly
- Skills with subprocess calls

---

## Status: Production Ready ✅

Tested 2025-11-28 with:
- WhatsApp self-chat (27833911315)
- Voice note from 2025-11-27 14:36
- Successfully downloaded, moved, and transcribed
- Workflow documented and repeatable

---

## Next Steps

1. Test with different contacts
2. Build up corrections dictionary based on actual usage
3. Consider creating formatted output templates
4. Integrate with task creation workflow
5. Add to Project Instructions for easy reference
