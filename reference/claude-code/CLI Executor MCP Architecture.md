---
'Status:': Active
'Priority:': High
'Tags:': null
'Created:': 2025-11-30
permalink: reference/claude-code/cli-executor-mcp-architecture
---

# CLI Executor MCP Architecture

## Overview

The **claude-cli-executor MCP** bridges Claude Desktop to all CLI capabilities, eliminating the need for manual task-handoff workflows.

## Architecture

```
Claude Desktop
    ↓
cli-executor MCP Server (Windows)
    ↓
Claude Agent SDK
    ↓
Claude CLI (ccli)
    ↓
All CLI Capabilities:
- Outlook operations (email, calendar)
- Git operations
- Bash commands
- File operations
- All CLI skills
```

## Configuration

**Location:** `C:\Users\10064957\.claude\mcp-servers\claude-cli-executor\`

**Key files:**
- `server.py` - MCP server implementation
- `pyproject.toml` - Dependencies (mcp, claude-agent-sdk)

**Desktop config:** `C:\Users\10064957\AppData\Roaming\Claude\claude_desktop_config.json`
```json
"claude-cli-executor": {
  "command": "uv",
  "args": [
    "--directory",
    "C:/Users/10064957/.claude/mcp-servers/claude-cli-executor",
    "run",
    "server.py"
  ],
  "env": {
    "WORKING_DIR": "C:/Users/10064957/My Drive/GDVault/MarthaVault"
  }
}
```

## Key Features

### Auto-Execution (No Approval Prompts)

**ClaudeAgentOptions configuration:**
```python
allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill"]
setting_sources=["user", "project"]  # Load skills from filesystem
```

This allows CLI operations to execute without approval prompts, making Desktop → CLI seamless.

### Skills Integration

Skills are loaded from:
- **User skills:** `~/.claude/skills/` (system-wide)
- **Project skills:** `MarthaVault\.claude\skills\` (vault-specific)

Available skills:
- outlook-extractor
- whatsapp-transcribe
- extract-epiroc-bev-report
- extract-pptx-heal
- weekly-report-setup
- transcribe-voice-notes
- cli-executor (Desktop skill wrapper)

### Authentication

Uses Claude Code authentication (`claude login`) - no API key needed.

## Usage from Desktop

### Direct MCP Tool Call

```
Use the cli-executor MCP to extract emails from the past week
```

Desktop → MCP → CLI → Result

### Via cli-executor Skill

User can also install the `cli-executor` skill in Desktop, which provides natural language triggers:

```
Extract my emails from last week
Check my calendar for tomorrow
Send an email to Jacques about BEV project
```

## Desktop Skill

**Location:** `MarthaVault\.claude\skills\cli-executor\SKILL.md`

Provides easy access to common operations:
- Outlook: emails, calendar, contacts, send-email, create-meeting
- Git: commit, push, pull, branch
- Filesystem: read, write, search
- Bash: any command execution

## Comparison: Task-Handoff vs CLI Executor

### Old Way (Task-Handoff) ❌ DEPRECATED

1. Desktop analyzes request
2. Desktop writes `reference/claude-code/task-handoff.md`
3. Desktop updates `.claude/.task-handoff-trigger`
4. **User manually runs:** `ccli /task-handoff`
5. CLI reads task-handoff.md
6. CLI executes commands
7. CLI writes results to task-handoff.md
8. Desktop reads results
9. Desktop continues workflow

**Problems:**
- Manual step required (breaks flow)
- Context switching (Desktop → Terminal → Desktop)
- Slower iteration
- User must remember to run ccli

### New Way (CLI Executor) ✅ ACTIVE

1. Desktop calls cli-executor MCP
2. Done ✨

**Benefits:**
- Fully automated (no manual steps)
- Stay in Desktop (no context switching)
- Fast execution (parallel operations possible)
- Skills automatically available
- Outlook integration working seamlessly

## Implementation Details

### Bypass Approval Prompts

The `--dangerously-skip-permissions` CLI flag is **not available** in Agent SDK. Instead, we use:

```python
allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill"]
```

This explicitly permits tools without approval prompts.

### Skills Execution

Skills guide CLI behavior. Example flow:

1. Desktop: "Use outlook-extractor skill to get emails"
2. CLI: Reads `outlook-extractor/SKILL.md`
3. CLI: Understands it needs `outlook_extractor.py emails --days X`
4. CLI: Executes Python script via Bash tool
5. CLI: Returns results to Desktop

Skills contain:
- Instructions for the CLI
- Python script paths
- MCP tool documentation
- Usage examples
- Progressive discovery patterns

## Common Operations

### Email Extraction
```
Extract my emails from the past 3 days
```
→ Runs outlook-extractor → Returns formatted summary

### Calendar Sync
```
Sync my Outlook calendar
```
→ Runs `/sync-outlook-calendar` slash command → Creates events in Schedule/

### Send Email
```
Send email to Jacques about BEV project status update
```
→ Drafts email → Uses outlook-extractor send-email → Confirms delivery

### Git Operations
```
Commit all changes with message "Updated project docs"
```
→ `git add . && git commit -m "message"` → Returns commit hash

## Technical Notes

### Working Directory
All CLI sessions run in: `C:\Users\10064957\My Drive\GDVault\MarthaVault`

### Session Management
- Each MCP call creates new CLI session
- Sessions are isolated
- Full conversation history returned
- No persistent state between calls

### Error Handling
- MCP returns structured JSON with status
- Errors include full traceback
- Timeouts configurable (default 300s)

### Logging
Server logs: `C:\Users\10064957\.claude\mcp-servers\claude-cli-executor\server.log`

## Migration Notes

### Deprecated: Task-Handoff Protocol

The task-handoff protocol (`reference/claude-code/task-handoff.md`) is now **deprecated** and should not be used for new workflows.

**When to still use CLI directly:**
- Complex multi-step workflows requiring human oversight
- Operations where you want to see incremental progress
- Learning/debugging CLI capabilities
- Long-running tasks (>5 minutes)

**When to use cli-executor MCP:**
- Quick operations (email, calendar, git)
- Automated workflows
- Operations that don't require monitoring
- When you want to stay in Desktop

### Removed Commands

These Desktop commands are no longer needed:
- ❌ "Run: ccli /task-handoff"
- ❌ Writing to `task-handoff.md`
- ❌ Updating `.task-handoff-trigger`

### New Pattern

Simply call the MCP tool or use natural language with the cli-executor skill:
- ✅ "Extract my emails"
- ✅ "Check my calendar"
- ✅ "Send email to..."

## Future Enhancements

Potential improvements:
- Streaming responses for long operations
- Parallel CLI session management
- Session persistence for conversational workflows
- Enhanced error recovery
- Progress indicators for long-running tasks

## Status

✅ **Production Ready** (November 30, 2025)
- Outlook integration: Working
- Skills loading: Working
- Auto-execution: Working
- Email send/receive: Tested
- No approval prompts: Confirmed

## References

- MCP Server: `~/.claude/mcp-servers/claude-cli-executor/`
- Desktop Skill: `MarthaVault\.claude\skills\cli-executor/`
- Agent SDK Docs: https://docs.claude.com/en/api/agent-sdk/overview
- Outlook Extractor: `.claude/skills/outlook-extractor/`