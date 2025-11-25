## Task Handoff Protocol - Desktop ↔ CLI

### When to Use
- Slash commands (`/triage-emails`, `/sync-outlook-calendar`)
- Skill invocations (outlook-extractor, etc.)
- Bulk file operations (>3 files)
- Bash/system commands

### Workflow
1. **Analyze** - Determine what/why
2. **Write** task-handoff to `reference/claude-code/task-handoff.md`:
```yaml
---
task_id: YYYYMMDD-HHMM-{sequence}
from: claude-desktop
to: claude-cli
status: pending
created: ISO timestamp
---

## Task: {description}

### Actions Required:
1. Execute: /command-name OR invoke skill OR file operations

### Expected Outcome:
- Command outputs, files created, confirmations

### Response Required:
- Status, errors, verification
```
3. **Update** `.claude/.task-handoff-trigger` timestamp
4. **Inform** user: "Run: ccli /task-handoff"
5. **Wait** for CCLI completion
6. **Read** results from task-handoff.md
7. **Continue** workflow with results

### Division of Labor
- **Desktop**: Analyze, decide, write instructions (thinking)
- **CCLI**: Execute, run commands, operate files (doing fast)

---
