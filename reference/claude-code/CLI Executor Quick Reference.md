---
'Status:': Active
'Priority:': Critical
'Tags:': null
'Updated:': 2025-11-30
permalink: reference/claude-code/cli-executor-quick-reference
---

# Project Instructions Update: CLI Executor MCP

## CRITICAL CHANGE - Task Handoff DEPRECATED ❌

The manual task-handoff protocol is **obsolete**. Use cli-executor MCP instead.

## New Architecture ✅

**claude-cli-executor MCP** provides direct CLI access from Desktop:
- All Outlook operations (email, calendar, send)
- All CLI skills (automatically loaded)
- Git operations
- Bash commands
- File operations

## Usage from Desktop

### Natural Language (via cli-executor skill)
```
"Extract my emails from last week"
"Send email to Jacques about BEV project"
"Check my calendar for tomorrow"
```

### Direct Tool Call
```
Use claude-cli-executor MCP to [task description]
```

## Configuration

**Location:** `~/.claude/mcp-servers/claude-cli-executor/`

**Key settings:**
```python
allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill"]
setting_sources=["user", "project"]  # Loads all skills
```

**Result:** Auto-execution without approval prompts

## Skills Integration

Skills loaded from:
- `~/.claude/skills/` (system-wide)
- `MarthaVault\.claude\skills\` (project)

Available: outlook-extractor, whatsapp-transcribe, weekly-report-setup, etc.

## What Changed

### Old Way ❌
1. Desktop writes task-handoff.md
2. User runs: `ccli /task-handoff`
3. CLI executes and writes results
4. Desktop reads results

### New Way ✅
1. Desktop calls cli-executor MCP
2. Done ✨

## Benefits

- **No manual steps** - Fully automated
- **Stay in Desktop** - No terminal switching
- **Fast execution** - Direct SDK integration
- **Skills work** - All loaded and available
- **Outlook works** - Email/calendar seamless

## Desktop Skill

Install `cli-executor` skill in Desktop for easy access:
- Provides natural language triggers
- Documents common operations
- Lists contact emails
- Shows command examples

## Status

✅ **Production Ready** (Nov 30, 2025)
- Outlook: Working
- Skills: Loading correctly
- Email send: Tested successfully
- Auto-execution: No approval prompts

## Full Documentation

See: `reference/claude-code/CLI Executor MCP Architecture.md`