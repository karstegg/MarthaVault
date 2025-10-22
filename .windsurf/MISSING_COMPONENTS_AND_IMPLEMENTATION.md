# Missing Components from CLAUDE.md & Implementation Plan

**Created**: 2025-10-15  
**Purpose**: Document what was NOT ported from CLAUDE.md and how to implement missing functionality

---

## Components Successfully Ported ✅

### Rules (Always Active)
- ✅ Identity and operating modes
- ✅ WhatsApp messaging protocol
- ✅ Memory systems usage
- ✅ File organization standards

### Workflows (Manual Execution)
- ✅ `/triage` - Batch inbox processing
- ✅ `/triage-slow` - Interactive inbox processing
- ✅ `/task` - Add tasks to master list
- ✅ `/quick-note` - Create quick notes
- ✅ `/initialize-windsurf-session` - Session onboarding

### MCP Servers (Shared with Claude Code)
- ✅ Graph Memory - 348 entities
- ✅ Basic Memory - Markdown file search
- ✅ WhatsApp - Message sending/receiving

---

## Components NOT Yet Ported ❌

### 1. Automatic Context Retrieval Rules (CRITICAL)

**Location in CLAUDE.md**: Lines 205-255

**What it does**: Proactive memory system queries based on detected patterns

**Patterns**:
- **People & Relationships** → Auto-query Graph + Basic Memory for person context
- **Projects & Technical Topics** → Auto-query for project status + strategic alignment
- **Mine Sites & Operations** → Auto-query for site personnel + ongoing work
- **Recent Activity** → Auto-query for recent changes + strategic priorities
- **Task Context Web** → Auto-query for task relationships + strategic WHY

**Implementation Strategy**:
- ❌ **Cannot be a rule** (rules are static, this requires dynamic behavior)
- ✅ **Must be in assistant's training/prompt** (Windsurf system prompt or memories)
- ✅ **Create a memory** documenting these patterns for auto-retrieval

**Action**: Create memory with context retrieval patterns

---

### 2. Strategic Context Integration

**Location in CLAUDE.md**: Lines 271-301

**What it does**: Priority calculation using strategy multipliers

**Components**:
- Strategy layer documents (CompanyStrategy.md, ActivePhase.md, FocusOfWeek.md)
- Priority calculation formula with ObjectiveWeight multipliers
- Q4 2025 strategic weights (Fire Safety 2.0x, BEV 1.5x, etc.)

**Implementation Strategy**:
- ✅ **Create rule** documenting priority calculation
- ✅ **Reference strategy documents** in Basic Memory
- ✅ **Use Graph Memory** for Project→Strategy relations

**Action**: Create `strategic-priority-calculation.md` rule

---

### 3. Tags Registry Maintenance

**Location in CLAUDE.md**: Lines 415-468

**What it does**: Automatic tag registry updates when creating new tags

**Components**:
- Master registry at `reference/tags.md`
- Auto-update on tag creation
- Tag categories and documentation

**Implementation Strategy**:
- ✅ **Create rule** for tag registry maintenance
- ✅ **Reference registry location** and update protocol

**Action**: Create `tag-registry-maintenance.md` rule

---

### 4. Obsidian Tasks Integration

**Location in CLAUDE.md**: Lines 479-541

**What it does**: Task status types, formatting, queries, dashboards

**Components**:
- Task status symbols: `[ ]` Todo, `[/]` In Progress, `[-]` Cancelled, `[x]` Done
- Task format with emojis (🔴🟡🟢⚪)
- Obsidian Tasks query syntax
- Dashboard views (priority, project, timeline, Kanban)

**Implementation Strategy**:
- ✅ **Create rule** for Obsidian Tasks formatting
- ⚠️ **Query syntax** may not work in Windsurf (Obsidian-specific)
- ✅ **Task format** can be used in markdown files

**Action**: Create `obsidian-tasks-integration.md` rule (with Windsurf limitations noted)

---

### 5. Calendar & Schedule Management

**Location in CLAUDE.md**: Lines 542-564

**What it does**: Calendar event creation in Schedule/ folder

**Components**:
- Event file format: `YYYY-MM-DD - Event Title.md`
- Front-matter with date fields
- Timezone handling (Africa/Johannesburg UTC+2)
- Weekend deadline rules

**Implementation Strategy**:
- ✅ **Already in triage workflows** (basic implementation)
- ✅ **Create dedicated rule** for calendar management details

**Action**: Create `calendar-schedule-management.md` rule

---

### 6. Assignment Logic

**Location in CLAUDE.md**: Lines 566-576

**What it does**: Auto-detect assignees from phrases like "for Jane", "John to..."

**Components**:
- Phrase detection patterns
- Auto-create person notes if missing
- Assignee front-matter population

**Implementation Strategy**:
- ✅ **Create rule** documenting assignment detection patterns
- ✅ **Include person note creation template**

**Action**: Create `assignment-detection.md` rule

---

### 7. Additional Slash Commands

**Location in CLAUDE.md**: Lines 609-618

**Missing workflows**:
- `/new-note` - Create structured notes with folder placement
- `/nn` - Alias for /new-note
- `/sync-vault` - Vault synchronization (exists in .claude/commands/)

**Implementation Strategy**:
- ✅ **Port from `.claude/commands/`** to `.windsurf/workflows/`

**Action**: Create missing workflow files

---

### 8. Git Functionality

**Location in CLAUDE.md**: Lines 648-655

**What it does**: Conventional commit messages

**Components**:
- Commit message format: `type: description`
- Types: `docs:`, `tasks:`, `ideas:`, `fix:`, `feat:`

**Implementation Strategy**:
- ✅ **Create rule** for commit message conventions
- ⚠️ **Git operations** - Windsurf has built-in Git support
- ✅ **Use Windsurf's native Git UI** for commits/pushes
- ✅ **Rule provides message format guidance**

**Action**: Create `git-commit-conventions.md` rule

---

## Git Functionality Implementation

### How Git Works in Windsurf

**Built-in Git Support**:
- ✅ Windsurf has native Git integration in the UI
- ✅ Source control panel shows changes
- ✅ Commit, push, pull via UI or command palette
- ✅ Branch management built-in

**What We Need to Add**:
- ✅ **Commit message conventions** (via rule)
- ✅ **Workflow guidance** (when to commit, what to include)
- ❌ **NOT needed**: Custom Git commands (use Windsurf's built-in)

### Git Workflow Rule

**Location**: `.windsurf/rules/git-commit-conventions.md`

**Content**:
- Conventional commit format
- When to commit (after triage, after task completion, etc.)
- Branch naming conventions (if any)
- Push/pull protocols

---

## Implementation Priority

### High Priority (Do Now)
1. ✅ **Context retrieval patterns** - Create memory
2. ✅ **Strategic priority calculation** - Create rule
3. ✅ **Git commit conventions** - Create rule

### Medium Priority (Do Soon)
4. ✅ **Tag registry maintenance** - Create rule
5. ✅ **Obsidian Tasks integration** - Create rule
6. ✅ **Calendar management** - Create rule
7. ✅ **Assignment detection** - Create rule

### Low Priority (Do Later)
8. ⚠️ **Additional workflows** - Port `/new-note`, `/nn`, `/sync-vault`
9. ⚠️ **Dashboard views** - May not work in Windsurf (Obsidian-specific)

---

## Why Some Things Can't Be Rules

**Rules are static** - They provide knowledge but don't trigger actions

**Cannot be rules**:
- ❌ Automatic context retrieval (requires dynamic query execution)
- ❌ Automatic tag registry updates (requires file modification)
- ❌ Automatic person note creation (requires file creation)

**Must be**:
- ✅ **Memories** - For patterns that should influence behavior
- ✅ **Workflows** - For explicit user-triggered actions
- ✅ **Assistant behavior** - Trained responses based on rules + memories

---

## Next Steps

1. **Create remaining rules** (strategic priority, git, tags, calendar, assignment, tasks)
2. **Create context retrieval memory** (automatic query patterns)
3. **Port missing workflows** (/new-note, /nn, /sync-vault)
4. **Test Git integration** using Windsurf's built-in UI
5. **Document limitations** (Obsidian-specific features that won't work)

---

**Status**: In Progress  
**Last Updated**: 2025-10-15
