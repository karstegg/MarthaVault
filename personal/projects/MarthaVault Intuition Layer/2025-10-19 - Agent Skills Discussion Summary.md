---
'Status:': Draft
'Priority:': High
'Assignee:': Greg
'DueDate:': 2025-10-26
'Tags:': null
permalink: personal/projects/martha-vault-intuition-layer/2025-10-19-agent-skills-discussion-summary
---

# Agent Skills Discussion Summary

**Date**: 2025-10-19  
**Context**: Exploring Claude's new Agent Skills feature and implications for MarthaVault

---

## What Are Agent Skills?

**Core Concept**: Organized folders containing instructions, scripts, and resources that AI agents dynamically discover and load to perform specialized tasks. Like "onboarding guides" that transform general-purpose agents into domain specialists.

### Key Architecture

```
~/.claude/skills/skill-name/
├── SKILL.md                    # Core instructions with YAML frontmatter
├── scripts/                    # Executable code (Python, Bash, etc.)
│   └── example.py
└── reference/                  # Additional documentation
    └── details.md
```

**SKILL.md Structure**:
```yaml
---
name: Skill Name
description: Brief description for Claude to decide relevance
---

# Instructions
When to trigger this skill...

# Procedures
Step-by-step instructions...

# References
See reference/details.md for more...
```

### Progressive Disclosure (3 Levels)

1. **Metadata** (always loaded): `name` + `description` from YAML frontmatter
2. **Core SKILL.md** (loaded when relevant): Full instructions
3. **Additional files** (loaded as needed): Referenced files like `reference/forms.md`

**Result**: Context window only contains what's needed, when needed. With 10 skills, only ~20 lines of metadata loaded vs 5,000 lines of full workflows.

---

## Skills vs Slash Commands: Key Differences

| Feature | Slash Commands | Agent Skills |
|---------|---------------|--------------|
| **Context Loading** | Entire workflow always loaded | Progressive disclosure (metadata → full → details) |
| **Portability** | IDE-specific (`.windsurf/workflows/`, `.claude/commands/`) | Universal (works in Claude.ai, API, Claude Code) |
| **Code Execution** | Via terminal (`run_command`), needs approval | Sandbox execution, no approval, outside context window |
| **Discovery** | User must remember and type command | Claude auto-discovers based on task |
| **Composability** | One command = one workflow | Multiple skills coordinate automatically |
| **Token Usage** | High (full workflow in context) | Low (only relevant parts loaded) |

### When to Use Each

**Keep Slash Commands**:
- Simple, always-needed operations
- IDE-specific workflows
- Explicit control desired

**Use Skills**:
- Complex procedures with conditional logic
- Cross-platform requirements
- Context efficiency needed
- Deterministic code execution required
- AI should discover and combine capabilities

---

## How Code Serves as Both Tool AND Documentation

**Example**: Production report tonnage extraction

```python
# scripts/extract_tonnage.py
"""
Extracts tonnage from WhatsApp production reports.

CRITICAL VALIDATION (from PR #7):
- All numbers MUST trace to source line numbers
- NEVER invent or interpolate missing data
- Return source quotes with line references

Input Format:
    Line 42: "Total hoisted: 5,545t"
    
Output Format:
    {
        "tonnage": 5545,
        "source_line": 42,
        "source_quote": "Total hoisted: 5,545t"
    }
"""

def extract_tonnage(text):
    # Implementation...
```

**As TOOL**: Claude executes → gets deterministic result  
**As DOCUMENTATION**: Claude reads docstring → learns validation rules

**Single source of truth**: Validation rules live in code, not duplicated in markdown.

---

## Skills Auto-Discovery

**No registration needed in CLAUDE.md**. At startup, Claude Code:
1. Scans `~/.claude/skills/` directory
2. Reads YAML frontmatter from every `SKILL.md`
3. Loads only `name` + `description` into system prompt
4. Claude now "knows" all available skills

**Convention-based** (like Obsidian plugins in `.obsidian/plugins/`).

---

## MarthaVault Skills Migration Strategy

### What Should Become Skills (Procedural Knowledge)

| CLAUDE.md Section | Skill Name | Why |
|-------------------|-----------|-----|
| §6 Intake & Triage | `marthavault-triage` | Complex procedure with validation |
| §7 Task Management | `marthavault-tasks` | Task creation + mirroring logic |
| §8 WhatsApp Messaging | `whatsapp-messaging` | Templates + style rules |
| §2.5 Memory Systems | `memory-query-patterns` | When/how to query Graph vs Basic |
| §4 File-Naming & Front-Matter | `note-creation` | Filename generation + frontmatter validation |
| §5 Tagging Rules | `tag-taxonomy` | Tag validation + registry |

### What Should Stay in CLAUDE.md (Context/Identity)

- Repository identity & purpose
- Operating modes (Autonomous vs Command)
- Conversational style
- Folder structure
- Core principles

**Result**: CLAUDE.md becomes lean "who am I" document (~200 lines), skills handle "how to do X"

---

## Clarifications from Discussion

### Q: Why org/people as a skill?

**A: This was wrong.** People/org should NOT be skills because:
- Skills = **"How to do X"** (procedures)
- Memory = **"Facts about Y"** (data)

**Correct approach**: Skills **reference** memory systems:

```markdown
# SKILL.md for marthavault-tasks
## When creating tasks involving personnel
1. Query Graph Memory: `mcp3_search_nodes("[person-name]")`
2. Check their current assignments
3. Tag task with appropriate #site/X
```

### Q: Where are scripts stored and run?

**Storage**: Inside skill folder at `~/.claude/skills/skill-name/scripts/`

**Execution**: Claude Code secure sandbox
- Claude runs: `python scripts/extract_tonnage.py`
- Script executes **outside context window** (no token usage)
- Returns deterministic result

### Q: Should skills be referenced in CLAUDE.md?

**A: No.** Auto-discovery handles it. Skills are self-documenting.

**Optional**: Add human-readable "what skills are installed" section for documentation, but not required for Claude.

---

## Recommended Implementation Path

### Phase 1: MarthaVault Triage Skill (Proof of Concept)

**Create**: `~/.claude/skills/marthavault-triage/`

```
marthavault-triage/
├── SKILL.md
├── scripts/
│   ├── validate_frontmatter.py     # Check Status/Priority/Assignee/DueDate/Tags
│   ├── generate_filename.py        # YYYY-MM-DD - Title.md format
│   └── mirror_task.py              # Add to master_task_list.md
├── reference/
│   ├── frontmatter_schema.yaml     # Required fields
│   └── tag_taxonomy.md             # Valid tags registry
└── templates/
    ├── project_note.md
    ├── person_note.md
    └── meeting_note.md
```

**SKILL.md Structure**:
```markdown
---
name: MarthaVault Triage
description: Process inbox notes with frontmatter validation and task mirroring
---

# When to trigger
User mentions "triage", "process inbox", or working with 00_Inbox/ items.

# Triage Workflow
1. Scan 00_Inbox/ for .md files
2. For each file:
   - RUN `scripts/validate_frontmatter.py` to check required fields
   - Determine destination folder based on content type
   - RUN `scripts/generate_filename.py` for canonical naming
   - If contains `- [ ]` tasks, RUN `scripts/mirror_task.py`
   - Move file to destination

# Validation Rules
See `reference/frontmatter_schema.yaml` for required fields:
- Status:: Draft|Active|Complete
- Priority:: Low|Med|High
- Assignee:: <Owner>
- DueDate:: YYYY-MM-DD
- Tags:: #task #year/2025 <context>

# Task Mirroring
All checkbox items must appear in `tasks/master_task_list.md`.
Use `scripts/mirror_task.py` to ensure parity.

# Tag Taxonomy
See `reference/tag_taxonomy.md` for valid tags and their meanings.
```

**Benefits**:
- Deterministic validation (no AI hallucination on required fields)
- Progressive disclosure (only loads when triaging)
- Portable across platforms
- No temp file creation needed
- Bundled reference materials

### Phase 2: Task Management Skill

**Create**: `~/.claude/skills/marthavault-tasks/`

```
marthavault-tasks/
├── SKILL.md
├── scripts/
│   └── task_mirror.py              # Ensure parity with master list
└── templates/
    └── task_template.md
```

### Phase 3: Memory Query Patterns Skill

**Create**: `~/.claude/skills/memory-query-patterns/`

```
memory-query-patterns/
├── SKILL.md                        # When to use Graph vs Basic Memory
└── reference/
    ├── entity_types.md             # Graph Memory entities
    ├── query_patterns.md           # Common query patterns
    └── decision_matrix.md          # Which memory system for what
```

**SKILL.md excerpt**:
```markdown
---
name: Memory Query Patterns
description: Intelligent context retrieval from Graph and Basic Memory systems
---

# When to trigger
User mentions people, projects, sites, tasks, or asks "what's the context for..."

# Decision Matrix

## Use Graph Memory when:
- Quick entity lookups (person, project, site)
- Relationship traversal (who reports to whom)
- Strategic alignment (Project→Strategy relations)

## Use Basic Memory when:
- Natural language search needed
- Temporal filtering (recent updates, after date)
- Full document content search
- Task details from master_task_list.md

## Use BOTH in parallel for:
- Comprehensive person context (role + current projects)
- Project context (strategic alignment + detailed status)
- Site operations (personnel + ongoing work)

# Query Patterns

## People & Relationships
1. Graph Memory: `mcp3_search_nodes("[person-name]")`
2. Basic Memory: `build_context("memory://people/[person-name]", depth=1, project="main")`

## Projects & Technical Topics
1. Graph Memory: `mcp3_search_nodes("[project-keyword]")`
2. Basic Memory: `search_notes("[topic-keywords]", project="main")`

## Recent Activity
1. Basic Memory: `recent_activity(timeframe="1 week", project="main")`
2. Graph Memory: `mcp3_search_nodes("Q4 2025 Active Phase")`
```

### Phase 4: Slim Down CLAUDE.md

**Remove from CLAUDE.md** (move to skills):
- Detailed triage procedures
- Task management workflows
- Memory query patterns
- WhatsApp messaging templates
- Detailed tagging rules

**Keep in CLAUDE.md** (~200 lines):
- Repository identity & purpose
- Operating modes
- Conversational style
- Folder structure overview
- Brief reference to skills directory

---

## Key Decisions Made

1. **ProductionReports repo**: Keep separate, don't touch. It has its own CLAUDE.md and workflow.
2. **People/org data**: NOT a skill. Skills reference memory systems, don't duplicate data.
3. **CLAUDE.md**: Don't reference skills. Auto-discovery handles it.
4. **Migration focus**: MarthaVault productivity workflows only.

---

## Next Steps (Pending)

1. **Complete article review**:
   - ✅ Agent Skills (engineering blog + news announcement)
   - ⏳ Plugins (`Customize Claude Code with plugins.md`)
   - ⏳ Context Management (`Managing context on the Claude Developer Platform.md`)
   - ⏳ Fast Context / Code Search (`Introducing SWE-grep and SWE-grep-mini RL for Multi-Turn Fast Context Retrieval.md`)

2. **After article review**: Decide on implementation priority
   - Start with triage skill as proof-of-concept?
   - Or implement multiple skills in parallel?

3. **Testing strategy**: How to validate skills work correctly?

---

## References

- **Engineering Blog**: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Product Announcement**: [Claude Skills: Customize AI for your workflows](https://www.anthropic.com/news/skills)
- **Skills Repository**: [anthropics/skills](https://github.com/anthropics/skills) (marketplace)
- **Skills Location**: `~/.claude/skills/` (user-installed)

---

## Questions for Future Exploration

1. How do skills interact with MCP servers? Can SKILL.md reference MCP tool calls?
2. Can skills be version-controlled and shared via Git?
3. What's the testing/validation workflow for skills?
4. How to handle skill updates without breaking existing workflows?
5. Can skills call other skills? (Composability limits)