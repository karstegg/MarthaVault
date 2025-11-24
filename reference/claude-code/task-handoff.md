---
task_id: 20251124-update-claude-md
from: claude-desktop
to: claude-cli
status: pending
created: 2025-11-24 21:35:00
permalink: reference/claude-code/task-handoff
---

## Task: Update CLAUDE.md with Desktop-CLI Handoff Protocol

### Actions Required:

**Add new section to CLAUDE.md after "Identity & Operating Modes" (Section 2):**

Insert the following content as a new subsection:

```markdown
### **Claude Desktop ↔ Claude CLI Task Handoff Protocol**

**Purpose**: Offload slow/bulk file operations from Claude Desktop to Claude CLI for speed and efficiency.

**Communication File**: `reference/claude-code/task-handoff.md`

**Division of Labor**:
- **Claude Desktop (CD)**: Analysis, decisions, triage logic, learning user patterns, memory integration
- **Claude CLI (CCLI)**: Fast file operations, bulk moves, directory creation, system commands, skill execution, slash commands, sub-agent spawning

**When to Use Handoff**:
- Multiple file moves/renames (>3 operations)
- Directory structure creation
- Bulk archive operations
- Any file operation where speed matters
- Operations that require bash/system commands
- **Skill invocations** (e.g., outlook-extractor, process-vfl-schedule)
- **Slash command execution** (e.g., `/vault-sync`, `/triage`, `/process-vfl-schedule`)
- **Sub-agent workflows** that benefit from CCLI's speed and tool access

**Task Format**:
```yaml
---
task_id: YYYYMMDD-HHMM-{sequence}
from: claude-desktop
to: claude-cli
status: pending|in-progress|completed|failed
created: ISO timestamp
executed: ISO timestamp (added by CCLI)
---

## Task: {Brief description}

### Actions Required:
1. Specific action with exact paths
2. Another action with exact paths
3. Execute slash command: /command-name --flags
4. Invoke skill: skill-name with parameters

### Expected Outcome:
- What should exist after completion
- File counts, directory structures
- Command outputs, skill results

### Response Required:
- Confirmation of operations
- List of errors (if any)
- Final state verification
- Command/skill outputs

---
## CCLI Response:
{CCLI fills this section when complete}
```

**Workflow**:
1. CD analyzes and writes handoff task to `reference/claude-code/task-handoff.md`
2. User runs `/task-handoff` in CCLI
3. CCLI executes operations, updates file with status and response
4. CD reads completion and continues workflow

**Command**: `/task-handoff` - Defined in `.claude/commands/task-handoff.md`

**Advanced Use Cases**:
- **Vault Sync**: CD determines sync is needed → handoff `/vault-sync` → CCLI executes in seconds
- **Email Processing**: CD analyzes inbox → handoff skill invocation → CCLI runs outlook-extractor
- **VFL Schedule**: CD identifies PDF → handoff `/process-vfl-schedule` → CCLI extracts and creates events
- **Sub-agent Chains**: CD orchestrates multi-step workflow → CCLI spawns specialized sub-agents for each step

**Benefits**:
- CD focuses on intelligence (what to do)
- CCLI handles execution (doing it fast)
- Async communication via vault
- CD learns patterns, CCLI executes them
- Speed: CCLI operations complete in seconds vs minutes
- Access to full CCLI ecosystem: skills, commands, MCP tools
```

**Location to Insert**: After the "Identity & Operating Modes" section, before "Obsidian Full Calendar" subsection.

### Expected Outcome:
- CLAUDE.md updated with new protocol section
- Protocol documented for future reference
- Integration with existing command structure
- Advanced use cases clearly defined

### Response Required:
- Confirm section added
- Provide line number where inserted
- Any formatting issues

---
## CCLI Response:
{awaiting execution}