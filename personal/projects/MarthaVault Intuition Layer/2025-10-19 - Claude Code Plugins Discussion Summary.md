---
Status:: Draft
Priority:: High
Assignee:: Greg
DueDate:: 2025-10-26
Tags:: #idea #system #year/2025 #plugins #hooks #subagents
---

# Claude Code Plugins Discussion Summary

**Date**: 2025-10-19  
**Context**: Exploring Claude Code Plugins feature and implications for MarthaVault automation

---

## What Are Plugins?

**Definition**: Plugins are **bundled collections** of Claude Code customizations that install with a single command.

### Plugin Components

A plugin can contain:
- **Slash commands**: Custom shortcuts (e.g., `/triage`, `/task`)
- **Subagents**: Purpose-built agents for specialized tasks
- **MCP servers**: Tool/data source connections
- **Hooks**: Customize Claude Code behavior at workflow trigger points
- **Skills**: Agent skills (progressive disclosure capabilities)

### Installation & Management

```bash
# Add a marketplace
/plugin marketplace add anthropics/claude-code

# Install a specific plugin
/plugin install feature-dev

# Browse available plugins
/plugin

# Toggle on/off to manage context
/plugin enable marthavault-productivity
/plugin disable marthavault-productivity
```

**Key Feature**: Plugins can be toggled on/off as needed to manage system prompt context and complexity.

---

## Plugins vs Skills: The Relationship

| Concept | What It Is | Scope |
|---------|-----------|-------|
| **Skill** | Single capability (triage, task management) | One specialized procedure |
| **Plugin** | Bundle of multiple extensions | Complete workflow ecosystem |

**Analogy**: Skills are ingredients, Plugins are the complete recipe book.

**Example Structure**:
```
MarthaVault Plugin
├── skills/
│   ├── marthavault-triage/
│   ├── marthavault-tasks/
│   └── memory-query-patterns/
├── commands/
│   ├── quick-note.md
│   └── daily-note.md
├── agents/
│   ├── triage-agent.md
│   └── memory-update-agent.md
├── mcp-servers/
│   └── .mcp.json (Graph + Basic Memory config)
└── hooks/
    ├── post-task-creation.md
    ├── post-file-change.md
    └── pre-commit-validation.md
```

---

## Hooks: Automatic Workflow Enforcement

**What are hooks?** Triggers that customize Claude Code behavior at key workflow points.

### Hook Architecture

**Pattern**: Event → Hook (trigger) → Action (often via subagent)

```
File Change Event
    ↓
Hook (trigger point)
    ↓
Subagent or Script (execution)
    ↓
Result (memory update, validation, etc.)
```

### Priority Hooks for MarthaVault

#### 1. Post-Task-Creation Hook ✅ WANT TO DO

```markdown
# hooks/post-task-creation.md
---
trigger: after_file_create
filter: "**/*.md"
---

After creating any file with `- [ ]` tasks:
1. Extract all checkbox items
2. Mirror to tasks/master_task_list.md
3. Verify parity
4. Report any mirroring failures
```

**Benefit**: Ensures task mirroring happens automatically, no reliance on AI memory.

#### 2. Post-File-Change Hook (Memory Sync) ✅ WANT TO DO

```markdown
# hooks/post-file-change.md
---
trigger: after_file_save
filter: "*.md"
exclude: ["00_Inbox/**", "Archive/**"]
---

When any .md file is saved:
1. Invoke Memory Update Subagent
2. Pass file path and change type (create/update/delete)
3. Subagent updates Graph and Basic Memory incrementally
```

**Benefit**: Real-time memory synchronization. Replaces manual `/sync-vault` command.

**This implements Phase 2 roadmap**:
> "Obsidian Watcher Plugin: Real-time vault indexing and auto-updates to memory systems"

#### 3. Pre-Triage Validation Hook (Optional)

```markdown
# hooks/pre-triage-validation.md
---
trigger: before_file_move
source: "00_Inbox/**"
---

Before moving files from 00_Inbox/:
1. Validate frontmatter exists
2. Check required fields (Status, Priority, Assignee, DueDate, Tags)
3. If validation fails, halt and report errors
```

**Benefit**: Prevents malformed notes from entering the vault.

#### 4. Pre-Commit Hook (Optional)

```markdown
# hooks/pre-commit.md
---
trigger: before_git_commit
---

Before committing:
1. Check for orphaned tasks (in files but not in master_task_list.md)
2. Validate all frontmatter
3. Report any inconsistencies
4. Option to auto-fix or abort commit
```

**Benefit**: Ensures vault consistency before version control.

---

## Subagents: Specialized Execution

**What are subagents?** Purpose-built agents with focused system prompts for specific domains.

**Advantage**: More reliable than general-purpose Claude because they have narrow, well-defined roles.

### Priority Subagents for MarthaVault

#### 1. Memory Query Subagent ✅ WANT TO DO

```markdown
# agents/memory-query-agent.md
---
name: Memory Query Agent
description: Intelligent context retrieval from Graph and Basic Memory systems
---

Role: Query dual memory systems based on user intent and context patterns.

Capabilities:
- Detect query patterns (people, projects, sites, tasks, recent activity)
- Choose appropriate memory system (Graph vs Basic vs Both)
- Execute parallel queries when comprehensive context needed
- Format and present results with source citations

Decision Logic:

## People & Relationships
Trigger: Person names mentioned
Actions:
1. Graph Memory: `mcp3_search_nodes("[person-name]")` - Get role, reporting structure
2. Basic Memory: `build_context("memory://people/[person-name]", depth=1, project="main")` - Get current projects
Result: Comprehensive person context (role + projects + relationships)

## Projects & Technical Topics
Trigger: Project keywords (BEV, fire safety, capital, equipment)
Actions:
1. Graph Memory: `mcp3_search_nodes("[project-keyword]")` - Get strategic alignment
2. Basic Memory: `search_notes("[topic-keywords]", project="main")` - Get detailed status
Result: Project context (strategic alignment + detailed status)

## Mine Sites & Operations
Trigger: Site names (Nchwaning 2, Nchwaning 3, Gloria, S&W)
Actions:
1. Graph Memory: `mcp3_search_nodes("[site-name]")` - Get assigned personnel
2. Basic Memory: `search_notes("[site-name] [topic]", project="main")` - Get site operations
Result: Site context (personnel + ongoing work)

## Recent Activity
Trigger: "What's new", "recent updates", "current status"
Actions:
1. Basic Memory: `recent_activity(timeframe="1 week", project="main")` - Get recent changes
2. Graph Memory: `mcp3_search_nodes("Q4 2025 Active Phase")` - Get strategic priorities
Result: Recent developments + strategic context

## Task Context Web
Trigger: Questions about specific tasks
Actions:
1. Basic Memory: `search_notes("[task-keywords]", project="main")` - Find in master_task_list.md
2. Extract links: #project, [[Person]], #site/X, #priority/X tags
3. Graph Memory: `open_nodes([linked-entities], depth=2)` - Get full context web
4. Graph Memory: Follow Project→Strategy relations - Get strategic alignment
Result: Understand WHY task matters (Project → Strategy → Priority)

Constraints:
- ALWAYS cite sources with file paths or entity names
- Use parallel queries for comprehensive context
- Prefer Graph Memory for quick lookups, Basic Memory for semantic search
- Use BOTH systems when relationships and content both needed
```

**Benefit**: Specialized agent that knows exactly when and how to query each memory system. More reliable than general Claude trying to remember the decision matrix.

#### 2. Memory Update Subagent ✅ WANT TO DO

```markdown
# agents/memory-update-agent.md
---
name: Memory Update Agent
description: Automatically update Graph and Basic Memory from vault changes
---

Role: Maintain memory systems in sync with vault content through incremental updates.

Capabilities:
- Parse frontmatter for structured data
- Extract entity mentions from content
- Detect new entities and relationships
- Create/update Graph Memory entities and relations
- Index content in Basic Memory
- Handle file deletions and moves
- Hash-based change detection (only process if content changed)

Update Logic:

## On File Create/Update
1. Read file content and frontmatter
2. Extract structured data:
   - Status, Priority, Assignee, DueDate from frontmatter
   - Entity mentions: [[Person]], #project, #site/X
   - Task checkboxes: `- [ ]` items
3. Determine entity type from folder location:
   - people/ → Personnel entity
   - projects/ → Project entity
   - tasks/ → Task entity
   - ideas/ → Idea entity
4. Graph Memory updates:
   - Create entity if new (check by name)
   - Update observations if existing
   - Create relations based on mentions and tags
5. Basic Memory updates:
   - Index full content with metadata
   - Update existing note if already indexed
6. Log changes for audit trail

## On File Delete
1. Query Graph Memory for entity by filename
2. Confirm deletion with user (NEVER auto-delete entities)
3. If confirmed, delete entity and orphaned relations
4. Remove from Basic Memory index

## On File Move
1. Detect as delete + create
2. Update entity type if folder changed (e.g., 00_Inbox → projects/)
3. Preserve relations
4. Update Basic Memory path references

## Entity Extraction Rules

### Personnel Entities
- Source: people/*.md files or [[Person Name]] mentions
- Attributes: Role, Site, Reporting structure
- Relations: reports_to, manages, stationed_at, assigned_to

### Project Entities
- Source: projects/*/ folders or #project tags
- Attributes: Status, Priority, Strategic alignment
- Relations: aligns_with (Strategy), assigned_to (Person), located_at (Site)

### Task Entities
- Source: `- [ ]` items in any file
- Attributes: Status, Priority, Assignee, DueDate
- Relations: part_of (Project), assigned_to (Person), located_at (Site)

### Site/Location Entities
- Source: #site/X tags
- Attributes: Type (mine, shaft, surface)
- Relations: stationed_at (Person), located_at (Project/Task)

### Strategy Entities
- Source: strategy/*.md files
- Attributes: Phase, Priority, Success metrics
- Relations: owns_strategy (Person), aligns_with (Project)

## Change Detection
- Calculate MD5 hash of file content
- Compare with stored hash
- Skip processing if hash unchanged (no actual content change)
- Update hash after successful processing

Constraints:
- NEVER delete entities without user confirmation
- Log all changes with timestamp and file path
- Handle conflicts gracefully (e.g., duplicate entity names)
- Preserve manual edits to Graph Memory (don't overwrite user-created entities)
- Batch updates when processing multiple files (e.g., after git pull)
```

**Benefit**: Automates the entire memory synchronization process. Replaces manual `/sync-vault` command with real-time, incremental updates.

**This implements Phase 2 roadmap**:
> "Real-time vault indexing and auto-updates to memory systems"
> "Hash-based change detection"
> "Automatic entity/relation creation from file changes"

#### 3. Triage Subagent (Optional)

```markdown
# agents/triage-agent.md
---
name: Triage Agent
description: Specialized agent for inbox processing with strict standards
---

Role: Process 00_Inbox/ items with strict adherence to frontmatter and naming standards.

Capabilities:
- Validate frontmatter completeness
- Generate canonical filenames (YYYY-MM-DD - Title.md)
- Determine destination folders based on content
- Apply appropriate tags
- Mirror tasks to master list
- Create missing entity links

Constraints:
- NEVER skip frontmatter validation
- ALWAYS use scripts for deterministic operations (filename generation, validation)
- MUST verify task mirroring before completing triage
- Report validation failures clearly
```

**Benefit**: Focused agent that ensures triage consistency. More reliable than general Claude.

---

## Hook + Subagent Integration Pattern

**Combining hooks with subagents creates powerful automation**:

### Example: Automatic Memory Sync

```
User saves file
    ↓
Post-File-Change Hook (trigger)
    ↓
Memory Update Subagent (specialized execution)
    ↓
    ├→ Parse frontmatter and content
    ├→ Extract entities and relations
    ├→ Update Graph Memory via MCP
    └→ Update Basic Memory via MCP
    ↓
Memory systems now in sync (automatic, real-time)
```

**This replaces**:
- Manual `/sync-vault` command
- Relying on AI to remember to update memories
- Batch processing entire vault (slow, inefficient)

**With**:
- Automatic, real-time updates
- Incremental processing (only changed files)
- Hash-based change detection (skip unchanged files)
- Specialized subagent ensures consistency

---

## Plugin Marketplaces

**What are marketplaces?** Curated collections of plugins hosted in git repositories.

### Creating a Marketplace

**Requirements**: Git repo with `.claude-plugin/marketplace.json`

**Example marketplaces**:
- Dan Ávila: DevOps automation, documentation, project management, testing
- Seth Hobson: 80+ specialized sub-agents
- Anthropic official: PR reviews, security, SDK development, meta-plugin

### Using Marketplaces

```bash
# Add marketplace
/plugin marketplace add karstegg/marthavault

# Browse and install
/plugin install marthavault-productivity
```

---

## MarthaVault Plugin Strategy

### Proposed Plugin: `marthavault-productivity`

**Structure**:
```
marthavault-productivity/
├── .claude-plugin/
│   └── plugin.json                 # Plugin metadata
├── skills/
│   ├── marthavault-triage/         # Triage procedures
│   ├── marthavault-tasks/          # Task management
│   ├── memory-query-patterns/      # Memory system usage
│   └── whatsapp-messaging/         # Communication templates
├── commands/
│   ├── quick-note.md               # Simple slash commands
│   └── daily-note.md
├── agents/
│   ├── memory-query-agent.md       # ✅ WANT TO DO
│   └── memory-update-agent.md      # ✅ WANT TO DO
├── mcp-servers/
│   └── .mcp.json                   # Graph + Basic Memory config
└── hooks/
    ├── post-task-creation.md       # ✅ WANT TO DO
    └── post-file-change.md         # ✅ WANT TO DO (memory sync)
```

**Installation**:
```bash
/plugin install marthavault-productivity
```

**Benefits**:
- ✅ Single command install
- ✅ Toggle on/off to manage context
- ✅ Version controlled via Git
- ✅ Shareable (if desired)
- ✅ Bundles all MarthaVault customizations

---

## Comparison: Current vs Plugin Approach

| Aspect | Current (CLAUDE.md + Rules) | Plugin Approach |
|--------|----------------------------|-----------------|
| **Installation** | Manual setup, multiple files | Single `/plugin install` command |
| **Context Management** | Always loaded (large CLAUDE.md) | Toggle on/off as needed |
| **Consistency** | Rely on AI memory | Hooks enforce automatically |
| **Memory Sync** | Manual `/sync-vault` command | Automatic via hooks + subagent |
| **Sharing** | Copy files manually | Git repo + marketplace |
| **Modularity** | Monolithic CLAUDE.md | Separate skills/agents/hooks |
| **Portability** | IDE-specific (Windsurf rules) | Claude Code universal |
| **Real-time Updates** | Batch processing | Incremental, hash-based |

---

## Implementation Roadmap

### Phase 1: Skills (From Previous Discussion)
- ✅ Create individual skills for triage, tasks, memory queries
- ✅ Test progressive disclosure and context efficiency

### Phase 2: Hooks + Memory Update Subagent ✅ PRIORITY

**Implements CLAUDE.md Phase 2 roadmap**:
> "Obsidian Watcher Plugin: Real-time vault indexing and auto-updates to memory systems"

#### Step 2.1: Post-Task-Creation Hook
```
hooks/post-task-creation.md
- Trigger: after_file_create or after_file_save
- Action: Extract `- [ ]` items, mirror to master_task_list.md
- Validation: Verify parity
```

**Benefit**: Automatic task mirroring, no manual intervention needed.

#### Step 2.2: Memory Update Subagent
```
agents/memory-update-agent.md
- Parse frontmatter and content
- Extract entities and relations
- Update Graph Memory (entities, relations)
- Update Basic Memory (content indexing)
- Hash-based change detection
```

**Benefit**: Real-time memory sync, replaces `/sync-vault`.

#### Step 2.3: Post-File-Change Hook
```
hooks/post-file-change.md
- Trigger: after_file_save
- Action: Invoke Memory Update Subagent
- Filter: *.md files, exclude 00_Inbox/ and Archive/
```

**Benefit**: Automatic, incremental memory updates as you work.

**Result**: Achieves Phase 2 goals:
- ✅ Real-time vault indexing
- ✅ Auto-updates to memory systems
- ✅ Hash-based change detection
- ✅ Automatic entity/relation creation

### Phase 3: Memory Query Subagent ✅ PRIORITY

```
agents/memory-query-agent.md
- Detect query patterns (people, projects, sites, tasks)
- Choose appropriate memory system (Graph vs Basic vs Both)
- Execute parallel queries for comprehensive context
- Format results with source citations
```

**Benefit**: Specialized agent that reliably queries memory systems based on context patterns. More consistent than general Claude.

### Phase 4: Bundle as Plugin (Later)

**After testing individual components**:
1. Package skills + hooks + subagents into plugin
2. Create `.claude-plugin/plugin.json` metadata
3. Test installation and toggle functionality
4. Optional: Create marketplace in GitHub repo

### Phase 5: Additional Hooks (Optional)

- Pre-triage validation hook
- Pre-commit consistency check hook
- Post-git-pull batch update hook

---

## Key Decisions Made

1. **Priority Implementation**: Hooks + Memory Update Subagent (Phase 2)
2. **Post-Task-Creation Hook**: ✅ Want to do - automatic task mirroring
3. **Memory Update Subagent**: ✅ Want to do - replaces `/sync-vault`
4. **Memory Query Subagent**: ✅ Want to do - specialized context retrieval
5. **Hook + Subagent Pattern**: Combine triggers with specialized execution
6. **Plugin Bundling**: Later stage, after testing individual components

---

## Alignment with Existing Roadmap

**CLAUDE.md Phase 2 Goals**:
> "Obsidian Watcher Plugin: Real-time vault indexing and auto-updates to memory systems"
> "Hash-based change detection"
> "Automatic entity/relation creation from file changes"

**Plugin Implementation Achieves This**:
- ✅ Post-File-Change Hook = Real-time watcher
- ✅ Memory Update Subagent = Auto-updates to memory systems
- ✅ Hash-based change detection = Built into subagent logic
- ✅ Automatic entity/relation creation = Core subagent capability

**CLAUDE.md Phase 3 Goals**:
> "Skills library with sub-agent spawning"

**Plugin Implementation Achieves This**:
- ✅ Skills library = Individual skills in plugin
- ✅ Sub-agent spawning = Memory Query Subagent, Memory Update Subagent, Triage Subagent

**Conclusion**: The Plugin approach (hooks + subagents + skills) IS the implementation path for Phases 2-3 of the existing roadmap.

---

## Next Steps (Immediate)

### 1. Complete Article Review (Pending)
- ⏳ Context Management (`Managing context on the Claude Developer Platform.md`)
- ⏳ Fast Context / Code Search (`Introducing SWE-grep and SWE-grep-mini RL for Multi-Turn Fast Context Retrieval.md`)

### 2. After Article Review: Implement Phase 2

**Priority Order**:
1. **Memory Update Subagent** (core automation)
2. **Post-File-Change Hook** (triggers subagent)
3. **Post-Task-Creation Hook** (task mirroring)
4. **Memory Query Subagent** (intelligent context retrieval)

### 3. Testing Strategy
- Test hooks trigger correctly
- Verify subagent updates Graph Memory accurately
- Verify subagent updates Basic Memory accurately
- Validate hash-based change detection
- Confirm task mirroring works automatically

### 4. Documentation
- Document hook trigger points
- Document subagent decision logic
- Create troubleshooting guide
- Update CLAUDE.md to reference new automation

---

## Questions for Future Exploration

1. **Hook trigger granularity**: Can hooks filter by folder path? (e.g., exclude 00_Inbox/)
2. **Subagent error handling**: What happens if memory update fails?
3. **Conflict resolution**: How to handle duplicate entity names?
4. **Manual overrides**: How to preserve manual edits to Graph Memory?
5. **Batch processing**: How to handle bulk updates (e.g., after git pull)?
6. **Performance**: Impact of real-time updates on large vaults?
7. **Rollback**: How to undo incorrect memory updates?

---

## References

- **Article**: [Customize Claude Code with plugins](https://www.anthropic.com/news/claude-code-plugins)
- **Marketplaces**:
  - Dan Ávila: DevOps, documentation, project management
  - Seth Hobson: [80+ sub-agents](https://github.com/wshobson/agents)
  - Anthropic official: `anthropics/claude-code`
- **Plugin Location**: `~/.claude/plugins/` (user-installed)
- **Documentation**: [Plugin development docs](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
