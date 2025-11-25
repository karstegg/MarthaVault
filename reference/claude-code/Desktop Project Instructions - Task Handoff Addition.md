---
created: 2025-11-25
purpose: Reference for updating Claude Desktop Project Instructions
status: Ready for integration
permalink: reference/claude-code/desktop-project-instructions-task-handoff-addition
---

# Desktop Project Instructions - Task Handoff Protocol Addition

## Purpose
This document provides the text to add to Claude Desktop's Project Instructions so Desktop remembers the task-handoff protocol for future sessions.

## Location in Project Instructions
Add this section after the **Communication Protocols** section and before the **Conversational Style & Response Brevity** section.

---

## Task Handoff Protocol - Desktop ↔ CLI

### Purpose
Offload slow operations, bulk file processing, and command execution from Claude Desktop to Claude CLI for speed and efficiency.

### When to Use Task Handoff

**ALWAYS use task-handoff for:**
- Slash command execution (`/triage-emails`, `/sync-outlook-calendar`, `/process-vfl-schedule`)
- Skill invocations (outlook-extractor, whisper transcription, etc.)
- Bulk file operations (>3 files to move/rename/create)
- Directory structure creation
- Bash/system command execution
- Any operation where CCLI speed matters

### Division of Labor

**Claude Desktop (CD):**
- Strategic analysis and decision-making
- Triage logic and prioritization
- Learning user patterns via Native Memory
- Context synthesis from multiple sources (Graph + Basic Memory)
- Determining *what* needs to be done and *why*
- Writing task-handoff instructions

**Claude CLI (CCLI):**
- Fast file operations execution
- Skill invocations and slash commands
- System commands and bash execution
- Sub-agent spawning
- MCP tool access and integration
- Executing *how* things get done

### Workflow

**When user requests something CCLI should handle:**

1. **Analyze the request** - Determine what needs to be done and why
2. **Write task-handoff instruction** to `reference/claude-code/task-handoff.md`:

```yaml
---
task_id: YYYYMMDD-HHMM-{sequence}
from: claude-desktop
to: claude-cli
status: pending
created: ISO timestamp
---

## Task: {Brief description}

### Actions Required:
1. Execute slash command: /command-name --flags
2. Or invoke skill: skill-name with parameters
3. Or perform file operations with exact paths

### Expected Outcome:
- Command outputs
- Files created/modified
- Operation confirmations

### Response Required:
- Success/failure status
- Any errors encountered
- Final state verification
```

3. **Update trigger file** - Touch `.claude/.task-handoff-trigger` with current timestamp
4. **Inform user** - Tell them to run `ccli /task-handoff` to execute
5. **Wait for CCLI completion** - CCLI will update task-handoff.md with results
6. **Read results** - Check task-handoff.md for CCLI's response
7. **Continue workflow** - Use results to inform next steps

### Example Use Cases

**Email Triage:**
```
User: "lets ask ccli to do a /triage-emails"
Desktop: [Writes task-handoff instruction for /triage-emails command]
Desktop: "✅ Task handoff written. Run: ccli /task-handoff"
User: [Runs ccli /task-handoff in terminal]
CCLI: [Executes /triage-emails, generates report, updates task-handoff.md]
Desktop: [Reads results, helps user review triage report]
```

**Calendar Sync:**
```
User: "sync my calendar"
Desktop: [Writes task-handoff for /sync-outlook-calendar]
Desktop: "✅ Task handoff written. Run: ccli /task-handoff"
User: [Runs ccli /task-handoff]
CCLI: [Syncs calendar in seconds]
```

**VFL Schedule Processing:**
```
User: "process the VFL schedule PDF"
Desktop: [Analyzes, writes task-handoff for /process-vfl-schedule]
Desktop: "✅ Task handoff written. Run: ccli /task-handoff"
User: [Runs ccli /task-handoff]
CCLI: [Extracts schedule, creates calendar events]
```

### Communication File
- **Path**: `reference/claude-code/task-handoff.md`
- **Format**: Structured YAML frontmatter + markdown content
- **Trigger**: `.claude/.task-handoff-trigger` timestamp file

### Benefits
- Desktop focuses on intelligence (thinking)
- CCLI handles execution (doing fast)
- Clear separation of concerns
- Speed: Operations complete in seconds vs minutes
- Access to full CCLI ecosystem (skills, commands, MCP)
- Async communication via vault files

---

## Integration Notes

After adding this to Project Instructions:
1. Desktop will remember to use task-handoff for appropriate operations
2. Desktop will write proper task-handoff instructions
3. Desktop will inform user to run CCLI commands
4. Desktop will check results and continue workflow

This complements the task-handoff protocol documented in:
- `CLAUDE.md` (Section 2 - for CCLI reference)
- `.claude/commands/task-handoff.md` (CCLI command definition)
- `reference/claude-code/task-handoff.md` (Communication file)