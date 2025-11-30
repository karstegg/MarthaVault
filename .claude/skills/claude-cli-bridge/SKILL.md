---
name: claude-cli-bridge
description: Execute Claude CLI commands and skills from Desktop including outlook-extractor, git operations, and filesystem automation
---

# Claude CLI Bridge

Bridge Desktop to CLI capabilities using the claude-cli-executor MCP server powered by Claude Agent SDK.

## What This Skill Does

Enables Claude Desktop to access **all Claude CLI capabilities**:
- ✅ **Outlook operations** (emails, calendar, contacts, send, meetings)
- ✅ **Git operations** (commit, push, pull, branch management)
- ✅ **Filesystem operations** (direct file manipulation, faster than MCP)
- ✅ **Bash commands** (grep, find, sed, complex scripts)
- ✅ **Slash commands** (/task, /triage, /sync-vault, etc.)
- ✅ **All CLI skills** (outlook-extractor, extract-epiroc-bev-report, etc.)

## When to Use

Trigger this skill when user asks to:
- Extract or send Outlook emails
- Create or delete calendar meetings
- Run git operations
- Execute bash/terminal commands
- Use slash commands (especially /triage, /task)
- Run any CLI skill by name

**Example triggers:**
- "Extract my emails from the past week"
- "Send an email to Sipho about the BEV project"
- "Create a meeting for tomorrow at 2pm"
- "Commit these changes to git"
- "Run /triage on my inbox"
- "Use outlook-extractor to find emails about fire safety"

## How It Works

Uses the `claude-cli-executor` MCP tool: `run_cli_session`

**Flow:**
```
Desktop → MCP Tool → Claude Agent SDK → CLI Session → Windows/Outlook → Result
```

**Authentication:** Uses your Claude subscription via `claude login` (no API credits)

## Common Operations

### Outlook: Extract Emails

**User says:** "Extract emails from the past week"

**Tool call:**
```
run_cli_session({
  "prompt": "Extract emails from the past 7 days using outlook-extractor"
})
```

**What CLI does:**
- Runs: `python outlook_extractor.py emails --days 7 --limit 50`
- Returns: JSON with email list
- Saves: `outlook_emails.json`

### Outlook: Extract from Specific Folder

**User says:** "Show me emails from my Production folder"

**Tool call:**
```
run_cli_session({
  "prompt": "Extract emails from Production folder using outlook-extractor --folder-search 'Production' --days 14"
})
```

### Outlook: Send Email

**User says:** "Send an email to Sipho about the N3 production meeting"

**Tool call:**
```
run_cli_session({
  "prompt": "Use outlook-extractor to send email:\\n--to sipho.dubazane@assmang.co.za\\n--subject 'N3 Production Meeting'\\n--body '[draft message here]'"
})
```

**Important:** Always draft the email first and get user approval before sending!

### Outlook: Create Meeting

**User says:** "Create a meeting tomorrow at 2pm with Xavier about BEV fire safety"

**Tool call:**
```
run_cli_session({
  "prompt": "Use outlook-extractor create-meeting:\\n--subject 'BEV Fire Safety Review'\\n--start '2025-12-01 14:00'\\n--attendees 'xavier.petersen@assmang.co.za'\\n--location 'Conference Room'"
})
```

**Remember:** Times are in SAST (UTC+2)

### Outlook: List Calendar

**User says:** "What meetings do I have this week?"

**Tool call:**
```
run_cli_session({
  "prompt": "Extract calendar events for the next 7 days using outlook-extractor"
})
```

### Git: Commit Changes

**User says:** "Commit my vault changes with message 'Updated BEV notes'"

**Tool call:**
```
run_cli_session({
  "prompt": "Commit all changes in the vault with message 'Updated BEV notes'"
})
```

### Slash Command: Add Task

**User says:** "Add a task to review the fire audit by Friday"

**Tool call:**
```
run_cli_session({
  "prompt": "/task Review fire audit findings by Friday #priority/high #fire-safety"
})
```

### Slash Command: Triage Inbox

**User says:** "Triage my inbox"

**Tool call:**
```
run_cli_session({
  "prompt": "/triage"
})
```

## Outlook-Extractor Commands

All outlook-extractor commands available:

| Command | Purpose | Example |
|---------|---------|---------|
| `emails` | Extract emails | `--days 7 --limit 50 --folder "Inbox"` |
| `emails --folder-search` | Search subfolders | `--folder-search "Production"` |
| `calendar` | Extract meetings | `--days 30 --limit 20` |
| `contacts` | List contacts | `--limit 100` |
| `search-contact` | Find contact | `"Sipho"` |
| `send-email` | Send email | `--to "user@company.com" --subject "Title" --body "Message"` |
| `create-meeting` | Create meeting | `--subject "Title" --start "2025-12-01 14:00"` |
| `delete-meeting` | Delete meeting | `--subject "Title" --start "2025-12-01 14:00"` |

**Full documentation:** See `~/.claude/skills/outlook-extractor/SKILL.md`

## Email Style Guide

When composing emails, follow Greg's style from `outlook-extractor/reference/email-style-guide.md`:

- **Greeting:** "Hi [Name]" (colleagues) or "Good morning" (formal)
- **Structure:** Short paragraphs (1-3 sentences), blank lines between
- **Tone:** Direct, professional, action-oriented
- **Closing:** Always "Regards" + "Greg"
- **@ Mentions:** Use for specific actions: "@Xavier please review"

**Always draft emails for user approval before sending!**

## Common Contacts

Quick reference for email addresses:

| Name | Email | Role |
|------|-------|------|
| Rudi Opperman | Rudi.Opperman@assmang.co.za | Operations Manager |
| Jacques Breet | Jacques.Breet@assmang.co.za | Engineering Manager |
| Sipho Dubazane | Sipho.Dubazane@assmang.co.za | Engineer - Gloria |
| Sikelela Nzuza | Sikelela.Nzuza@assmang.co.za | Engineer - N2 |
| Sello Sease | Sello.Sease@assmang.co.za | Engineer - N3 |
| Xavier Petersen | Xavier.Petersen@assmang.co.za | Engineer - S&W |

**To find others:** Use `search-contact` command

## Technical Notes

### MCP Server: claude-cli-executor

**Location:** `C:\Users\10064957\.claude\mcp-servers\claude-cli-executor\server.py`

**Tool:** `run_cli_session(prompt, context_files?)`

**Technology:** Claude Agent SDK (uses your Claude subscription via `claude login`)

**Working Directory:** `C:\Users\10064957\My Drive\GDVault\MarthaVault`

**Logs:** `~/.claude/mcp-servers/claude-cli-executor/server.log`

### Authentication

No API key needed! Uses Claude Code authentication:
```bash
claude login  # One-time setup
```

This uses your Claude subscription (Pro/Max/Team/Enterprise).

### Timeouts

Default: 300 seconds (5 minutes)
Can specify in prompt if needed for long operations.

## Approval Workflow

**Operations requiring approval:**
- ✅ Sending emails (ALWAYS draft first)
- ✅ Creating meetings (confirm details)
- ✅ Deleting content (verify before execution)
- ✅ Git push operations (review changes)

**Auto-approved operations:**
- ✅ Reading emails/calendar
- ✅ Searching contacts
- ✅ Listing files
- ✅ Extracting data

## Error Handling

**If MCP tool fails:**
1. Check if Claude CLI is installed: `claude --version`
2. Check if logged in: `claude login`
3. Check server logs: `~/.claude/mcp-servers/claude-cli-executor/server.log`
4. Verify Outlook is running (for outlook-extractor)

**If Outlook operations fail:**
- Ensure Outlook is open and running
- Verify pywin32 installed: `pip install pywin32 --upgrade`
- Check timezone (use SAST times: UTC+2)

## Examples in Action

### Example 1: Email Workflow

**User:** "Check my emails from Production Engineering group this week and summarize"

**Claude:**
1. Calls `run_cli_session` with prompt: "Extract emails from folder-search 'Production' for past 7 days"
2. CLI runs outlook-extractor
3. Returns email JSON
4. Claude analyzes and summarizes for user
5. User sees: "You have 15 emails, key topics: BEV updates, N3 production issues, fire safety audit..."

### Example 2: Send Email with Context

**User:** "Send an email to Xavier about the BEV fire door modifications based on the project notes"

**Claude:**
1. Calls `run_cli_session` with context_files: ["projects/BEV/Fire Safety/2025-11-15 - Fire Door Mods.md"]
2. Drafts email following style guide
3. Shows draft to user: "Here's the draft email..."
4. **Waits for approval**
5. On approval: Calls `run_cli_session` to send via outlook-extractor
6. Confirms: "Email sent to Xavier"

### Example 3: Meeting Creation

**User:** "Schedule a BEV review meeting for Monday 2pm with the team"

**Claude:**
1. Identifies attendees from context (Rudi, Jacques, site engineers)
2. Calls `run_cli_session` to create meeting
3. Confirms: "Meeting created: BEV Review - Monday 14:00 SAST"

## Status

✅ **Production Ready** - MCP server built and tested
⚠️ **Requires Setup:**
1. Restart Claude Desktop to load MCP
2. Verify `claude login` is authenticated
3. Test with simple command: "List my folders in Outlook"

## Next Steps

1. **Test the bridge:** "Extract my emails from this week"
2. **Create outlook skill:** Dedicated skill for common Outlook operations
3. **Add more CLI skills:** As you build them in CLI, they auto-work here

---

**Remember:** This bridge gives you the full power of Claude CLI from Desktop, with Desktop's Native Memory learning and document creation capabilities combined!
