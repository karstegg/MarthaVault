---
title: Dual Memory System - Quick Reference Guide
type: note
permalink: system/dual-memory-system-quick-reference-guide
tags:
- system
- memory-systems
- quick-reference
- troubleshooting
---

# 🔄 UPDATED FOR CLAUDE DESKTOP (2025-11-05)

**Primary Interface**: Claude Desktop with Native Memory
**MCP Systems**: Specialized tools for precise queries and strategic alignment

---

## Architecture Overview

```
Claude Desktop (Native Memory) ← PRIMARY INTERFACE
├── Conversational learning (automatic synthesis)
├── Preference learning (from your feedback)
├── Session continuity (remembers context)
└── Orchestrates specialized queries:
    ├── Graph MCP → Structured facts (org chart, strategic alignment)
    ├── Basic MCP → Semantic search (deep context, temporal)
    └── Vault → Source of truth (Git-backed markdown)
```

**What This Means**:
- **Native Memory**: Handles conversational learning, synthesis, preferences automatically
- **Graph Memory**: Use for precise entity/relation queries ("who reports to X?", "strategic alignment of Y")
- **Basic Memory**: Use for deep semantic search and temporal queries
- **Claude Code CLI**: Becomes automation engine (runs in background, updates memory systems)

---

## When to Use Each System

### Native Memory (Automatic - Claude Desktop)
**What it does automatically**:
- ✅ Learns from conversations (no manual updates needed)
- ✅ Remembers your preferences and patterns
- ✅ Maintains session context across conversations
- ✅ Synthesizes information from multiple sources
- ✅ Adapts responses based on your feedback

**You don't need to think about this** - it just works in Claude Desktop.

---

### Graph Memory (Explicit Queries - Via MCP)
**When to use**:
- ❓ "Who reports to Gregory Karsten?" → Precise org chart traversal
- ❓ "Which tasks align with Fire Safety strategy?" → Strategic alignment (2.0x weight)
- ❓ "If Philip Moller goes on leave, what's impacted?" → Dependency analysis
- ❓ "Show me all N3 critical tasks" → Entity-centric queries

**How to invoke**: `mcp__memory__search_nodes("query")`

**Advantage**: Structured relations, instant traversal, strategic intelligence encoded in `aligns_with` relations

---

### Basic Memory (Semantic Search - Via MCP)
**When to use**:
- ❓ "What happened last week with BEV?" → Temporal filtering
- ❓ "Find notes about fire safety recent progress" → Semantic search
- ❓ "Context around HD0054 incident" → Deep context building (depth parameter)
- ❓ "Recent decisions about capital projects" → Time + semantic filters

**How to invoke**: `mcp__basic-memory__search_notes("query", project="main")`

**Advantage**: Full-text search, temporal filtering, deep context with link traversal

---

## Hybrid Query Pattern (Best Practice)

**For complex questions, Native Memory orchestrates both MCPs**:

```
User: "What's the status of fire safety and who's working on it?"

Native Memory thinks:
1. Get structured facts (Graph): 
   → search_nodes("fire safety") 
   → Returns: BEV Fire Safety Program, 11 tasks, Johnny leads, 2.0x strategic weight

2. Get semantic context (Basic):
   → search_notes("fire safety recent progress")
   → Returns: Recent meeting notes, status updates, decisions

3. Synthesize answer:
   "BEV Fire Safety Program (2.0x CRITICAL priority) has 11 tasks led by Johnny 
    Hollenbach at N3. Recent progress: [from Basic]. Strategic alignment: Q4 
    Focus Area 1. Tasks: [from Graph relations]."
```

**You just ask naturally** - Native Memory handles the orchestration.

---

## Simplified Startup (Claude Desktop)

**OLD (Claude Code CLI)**: 3-phase startup (10 seconds) - health check + context loading + intelligence

**NEW (Claude Desktop)**: 
- **Native Memory loads conversational context automatically**
- **Only run health check if you suspect issues**
- **MCP queries happen on-demand as needed**

**Quick health check** (only when needed):
```python
# 1. Verify Graph Memory
mcp__memory__search_nodes("Gregory Karsten")

# 2. Verify sync current
cat .vault-sync-checkpoint && git rev-parse HEAD
```

**That's it!** Native Memory handles the rest.

---

## Claude Desktop Best Practices

### 1. **Let Native Memory Learn Naturally**
- Just have conversations - it learns automatically
- Correct when wrong - it adapts
- No manual memory updates needed

### 2. **Use MCPs for Precision Queries**
- Org chart questions → Graph Memory
- Strategic alignment → Graph Memory
- Semantic search → Basic Memory
- Temporal queries → Basic Memory

### 3. **Trust the Orchestration**
- Native Memory knows when to use Graph vs Basic
- You don't need to specify which system
- Just ask your question naturally

### 4. **Claude Code Runs in Background**
- CLI becomes automation engine
- Updates memory systems automatically
- You interact via Claude Desktop

---

## Transition Guide

### From Claude Code CLI to Claude Desktop

**Before (CLI workflow)**:
1. Open Claude Code terminal
2. Run startup protocol (health + context)
3. Ask questions
4. Manually trigger memory updates

**After (Desktop workflow)**:
1. Open Claude Desktop
2. Ask questions naturally
3. Native Memory + MCPs handle everything
4. CLI runs in background (automation)

**What stays the same**:
- ✅ Graph Memory structure (entities, relations)
- ✅ Basic Memory indexing (semantic search)
- ✅ Vault as source of truth (Git-backed)
- ✅ `/sync-vault` for updates

**What's new**:
- ✅ Native Memory as primary interface
- ✅ Automatic conversational learning
- ✅ Seamless MCP orchestration
- ✅ No manual startup sequence

---

# Dual Memory System - Quick Reference Guide

**Purpose**: Enable Claude Code to understand, verify, and troubleshoot the memory systems like a human uses short-term and long-term memory
**Analogy**: Graph Memory = conscious/explicit memory (facts, relationships), Basic Memory = subconscious/semantic memory (context, associations)
**Status**: Phase 1 Complete and Operational

---

## Quick System Check

### 1. Verify System Health (30 seconds)

```bash
# Check Graph Memory status
mcp__memory__search_nodes("Gregory Karsten")
# Expected: Should return entity with observations and relations
# If empty or error: See [[#Troubleshooting Graph Memory]]

# Check Basic Memory status
mcp__basic-memory__sync_status(project="main")
# Expected: "Sync Status: complete (100%)", 613 files
# If stuck <100%: See [[#Troubleshooting Basic Memory]]

# Check sync checkpoint
cat .vault-sync-checkpoint
# Expected: 40-character SHA matching current git HEAD
# If different: Run /sync-vault to catch up
```

**Healthy system output**:
- ✅ Graph Memory returns entities with relations
- ✅ Basic Memory shows 100% sync (613 files)
- ✅ Checkpoint SHA matches `git rev-parse HEAD`

---

## Native Memory Integration (Claude Desktop)

**Available**: Nov 4, 2025 (rolled out)
**Interface**: Claude Desktop with native memory enabled
**Purpose**: Automatic conversational synthesis layer on top of Graph + Basic MCPs

### Architecture with Native Memory

```
Claude Desktop (Native Memory)
├── Automatic 24hr synthesis from conversations
├── Learns preferences and working style
├── Orchestrates queries to MCP systems
└── Queries Graph + Basic in parallel
    ├── Graph Memory MCP (structured facts/relations)
    ├── Basic Memory MCP (semantic search/indexing)
    └── Obsidian Vault (source of truth)
```

### What Native Memory Handles

**Automatic (no tool calls required)**:
- Recent conversation context (last 24hrs)
- Your communication preferences
- Working patterns and routines
- Decision-making frameworks
- People you mention frequently

**Native Memory learns naturally** through conversation. Don't force-feed context.

### When to Use Each System

**Native Memory** (try first):
- Recent discussions (last few days)
- General questions about work
- People and projects mentioned in conversations
- Your preferences and working style

**Graph Memory** (explicit queries):
- Organizational structure (who reports to whom)
- Strategic alignments (2.0x Fire Safety multiplier)
- Equipment inventory (175 TMM units)
- Task assignments across team
- Relationship traversal (multi-hop queries)

**Basic Memory** (deep search):
- Temporal queries ("what happened last month")
- Semantic search across vault
- Full document context retrieval
- When you need the actual file content

### Hybrid Query Pattern

```python
# Let native memory try first
User: "What's Sipho working on?"

# If native memory doesn't know → Query Graph
if not_in_native_memory:
    mcp__memory__search_nodes("Sipho Dubazane")
    # Returns: 8 tasks, 2 critical, assigned projects

# For deeper context → Add Basic Memory
if need_details:
    mcp__basic-memory__search_notes("Sipho recent work", project="main")
    # Returns: Meeting notes, emails, progress updates
```

### Startup Protocol (Simplified for Desktop)

**Claude Desktop with native memory needs less explicit context loading.**

Minimal health check (10 seconds):
```bash
# 1. Verify Graph Memory
mcp__memory__search_nodes("Gregory Karsten")
# ✅ Should return org structure

# 2. Verify sync current
cat .vault-sync-checkpoint
# ✅ Should match git HEAD

# 3. Done - native memory handles the rest
```

**Skip full context load** - Native memory already has conversational context.

**Only load explicitly when**:
- First session after long break (>1 week)
- Major project status change
- User explicitly requests full context

### Memory Synthesis Cycle

**How the three layers work together**:

1. **Conversation** → Native Memory learns patterns
2. **Explicit facts** → Graph Memory stores structure  
3. **Documents** → Basic Memory indexes content
4. **Next session** → Native Memory queries Graph/Basic as needed

**Example flow**:
```
User: "Update on fire safety?"
  ↓
Native Memory: "Recent chats about BEV fire program"
  ↓
If need structure → Graph Memory: "11 tasks, Johnny leads, 2.0x priority"
  ↓  
If need details → Basic Memory: "Latest meeting notes, progress reports"
  ↓
Synthesized answer with full context
```

### Best Practices for Desktop

**DO**:
- Let native memory build naturally through conversation
- Use Graph Memory for precise structured queries
- Use Basic Memory when you need actual file content
- Trust native memory for recent context (last week)

**DON'T**:
- Force-load context at every session start
- Query Graph/Basic when native memory already knows
- Duplicate information across systems
- Over-explain memory system operations to user

### Transition from Claude CLI

**Claude CLI** can remain as background automation:
- Calendar sync hooks
- Batch file processing  
- Scheduled vault maintenance
- VFL processing automation

**Claude Desktop** becomes primary interface:
- Natural conversation with memory
- Strategic queries (Graph + Basic)
- Daily task management
- Decision support

---

## How the Dual System Works

### Human Memory Analogy

| Memory Type | Human Equivalent | Purpose | Example Query |
|-------------|------------------|---------|---------------|
| **Graph Memory** | Explicit/Conscious | Facts, relationships, org chart | "Who reports to Greg?" |
| **Basic Memory** | Semantic/Subconscious | Context, associations, recall | "What happened last week with BEV?" |

**Together**: Like how you remember "John is Sarah's manager" (explicit) AND the context of when you learned it (implicit).

---

### The Two Systems

#### Graph Memory (Conscious Facts)

**What it stores**: Structured entities and typed relations
**Think**: LinkedIn profile + org chart + knowledge graph

**Storage**:
- **File**: `C:\Users\10064957\.martha\memory.json` (JSONL format)
- **MCP Server**: `@modelcontextprotocol/server-memory`
- **Structure**: In-memory database, periodic file flush
- **Size**: 160+ entities, 200+ relations

**Entity types**:
- Personnel (40+): Greg, Sipho, Sikelela, Sello, Xavier, etc.
- Projects (15+): BEV Fire Safety, Capital TMM, SA Cranes
- Tasks (83+): All checkbox tasks from master_task_list.md
- Strategy (4): Q4 2025 Active Phase, Company Strategy
- Locations (5): N2, N3, Gloria, Black Rock
- Decisions, Business Processes, Incidents

**Relation types**:
- `reports_to`, `manages`: Organizational hierarchy
- `assigned_to`, `located_at`: Task assignments
- `aligns_with`: Strategic connections (enables priority calc)
- `participates_in`, `made_decision`, `impacts`

**When to use**:
- ✅ "Who reports to X?" (relationship traversal)
- ✅ "What tasks are assigned to Y?" (entity queries)
- ✅ "Which projects align with Z strategy?" (strategic reasoning)
- ❌ "What happened last week?" (no temporal filtering)

---

#### Basic Memory (Semantic Context)

**What it stores**: Full-text indexed documents with semantic search
**Think**: Google for your vault + brain's associative memory

**Storage**:
- **Database**: `C:\Users\10064957\.basic-memory\memory.db` (SQLite)
- **Config**: `C:\Users\10064957\.basic-memory\config.json`
- **MCP Server**: `@kanru/mcp-basic-memory`
- **Index**: FTS5 full-text search + entity relations
- **Size**: 613 files, 574 entities, 975 relations

**Config** (`config.json`):
```json
{
  "projects": {
    "main": "C:/Users/10064957/My Drive/GDVault/MarthaVault"
  },
  "default_project": "main"
}
```

**CRITICAL**: Database `project.path` must match config path. Check with:
```bash
sqlite3 ~/.basic-memory/memory.db "SELECT name, path FROM project;"
# Must show: main | C:/Users/10064957/My Drive/GDVault/MarthaVault
```

**When to use**:
- ✅ "What happened last week?" (temporal: `recent_activity`)
- ✅ "Find notes about BEV fire safety" (semantic search)
- ✅ "Context around this meeting?" (`build_context` with depth)
- ❌ "Who reports to Greg?" (slower than Graph for relations)

---

## Progressive Discovery Pattern

### How Claude Should Think (Like a Human)

**Question**: "What's the status of the BEV fire safety program?"

**Step 1: Quick fact check (Graph Memory - 1 second)**
```python
mcp__memory__search_nodes("BEV Fire Safety")
# Returns: Project entity + strategic alignment (2.0x weight) + 11 assigned tasks + Johnny Hollenbach leads it
```

**Step 2: Semantic context (Basic Memory - 2 seconds)**
```python
mcp__basic-memory__search_notes("BEV fire safety recent status", project="main")
# Returns: Recent meeting notes, decisions, progress updates
```

**Step 3: Deep dive if needed (Breadcrumb follow)**
```python
# Graph shows: "HD0054 Fire Incident triggered this program"
mcp__memory__search_nodes("HD0054 Fire Incident")
# Returns: Incident details + timeline + actions

# Basic shows: Reference to "projects/BEV/2025-10-18 – BRMO Epiroc Weekly Report"
mcp__basic-memory__read_note("projects/bev/2025-10-18-brmo-epiroc-weekly-report", project="main")
# Returns: Full report with equipment status
```

**Pattern**: Start broad (Graph facts) → Add context (Basic semantic) → Follow breadcrumbs (recursive discovery)

---

## Decision Tree: Which Memory to Use?

```
Query about...
├─ Relationships/org chart? → Graph Memory (reports_to, manages)
├─ Strategic alignment/priority? → Graph Memory (aligns_with relations)
├─ "What happened when"? → Basic Memory (temporal filtering)
├─ Semantic search? → Basic Memory (FTS5 full-text)
├─ Complex question? → BOTH in parallel
└─ Specific file? → Direct Read tool
```

**Examples**:

| Question | System | Tool | Why |
|----------|--------|------|-----|
| "Who reports to Greg?" | Graph | `search_nodes("Gregory Karsten")` | Structured relations |
| "Tasks assigned to Sello?" | Graph | `search_nodes("Sello Sease")` | Entity-centric query |
| "What's critical for fire safety?" | Graph | `search_nodes("fire safety")` + check `aligns_with` | Strategic reasoning |
| "What happened last week?" | Basic | `recent_activity(timeframe="1 week")` | Temporal filter |
| "Context for BEV project?" | Basic | `build_context("memory://projects/bev", depth=2)` | Deep context |
| "Find notes about capital" | Basic | `search_notes("capital projects")` | Semantic search |

---

## Data Storage Locations

### Graph Memory
```
📁 C:\Users\10064957\.martha\
├── memory.json          # Entity/relation storage (JSONL)
└── (in-memory cache)    # MCP server holds current state
```

**Persistence model**: In-memory with periodic file flush
- Writes to memory.json on clean shutdown or periodically
- **Don't rely on file timestamp** to verify sync
- **Always verify via queries**: `search_nodes("entity-name")`

**File format** (JSONL - JSON Lines):
```json
{"type":"entity","name":"Gregory Karsten","entityType":"Personnel","observations":["..."]}
{"type":"relation","from":"Sipho Dubazane","to":"Gregory Karsten","relationType":"reports_to"}
```

---

### Basic Memory
```
📁 C:\Users\10064957\.basic-memory\
├── config.json          # Project mappings
├── memory.db            # SQLite database (entities, relations, FTS5 index)
└── (logs)
```

**Database schema** (key tables):
```sql
-- Project configuration
project (id, name, path, is_active, is_default)

-- Entities (notes, people, projects)
entity (id, name, entity_type, permalink, project_id, content)

-- Full-text search index
entity_fts (content indexed with FTS5)

-- Relations between entities
relation (from_entity_id, to_entity_id, relation_type)
```

**Check database health**:
```bash
sqlite3 ~/.basic-memory/memory.db "
SELECT 
  (SELECT COUNT(*) FROM entity) as entities,
  (SELECT COUNT(*) FROM relation) as relations,
  (SELECT path FROM project WHERE name='main') as vault_path;
"
```

Expected: `574|975|C:/Users/10064957/My Drive/GDVault/MarthaVault`

---

### Vault Sync Checkpoint
```
📁 C:\Users\10064957\My Drive\GDVault\MarthaVault\
└── .vault-sync-checkpoint    # Last synced git commit SHA
```

**Purpose**: Track which git commit was last synced to Graph Memory

**Workflow**:
1. User edits files in vault
2. Obsidian Git plugin commits changes
3. `/sync-vault` compares checkpoint SHA to current HEAD
4. Only changed files get processed
5. Checkpoint updated to new HEAD

**Check sync status**:
```bash
# Current checkpoint
cat .vault-sync-checkpoint
# Output: 9d9e18e9dfb2e84ae1919ca6d43bd2ba16d5efc0

# Current HEAD
git rev-parse HEAD
# Output: 9d9e18e9dfb2e84ae1919ca6d43bd2ba16d5efc0

# If different: Changes exist that haven't been synced
# Run: /sync-vault
```

---

## Troubleshooting Guide

### Graph Memory Issues

#### Problem: `search_nodes()` returns empty results

**Diagnosis**:
```bash
# Check file exists
ls -lah .martha/memory.json
# Check entity count
grep -c '"type":"entity"' .martha/memory.json
```

**Fixes**:
1. **If file missing**: Run `/sync-vault --full` to rebuild
2. **If entity count low** (<100): Run `/sync-vault --full`
3. **If MCP server down**: Restart with `/mcp restart memory`

---

#### Problem: Recent changes not in Graph Memory

**Diagnosis**:
```bash
# Check if changes are committed
git status
# Check checkpoint vs HEAD
cat .vault-sync-checkpoint
git rev-parse HEAD
```

**Fix**:
1. **If uncommitted changes**: Wait for Obsidian Git auto-commit OR manually commit
2. **If checkpoint behind HEAD**: Run `/sync-vault`

---

#### Problem: Memory.json file shows old timestamp

**This is NORMAL** - MCP server uses in-memory database.

**Verification** (don't check file, check queries):
```bash
# Correct way to verify
mcp__memory__search_nodes("recent-entity-name")
# If found: Memory is working (file will flush later)
# If not found: Entity wasn't created, check sync
```

---

### Basic Memory Issues

#### Problem: Sync stuck at <100%

**Diagnosis**:
```bash
mcp__basic-memory__sync_status(project="main")
# Check: sync progress, file count, any errors
```

**Fixes**:
1. **Restart MCP server**: `/mcp restart basic-memory`
2. **Check vault path**: See [[#Problem: Wrong vault path indexed]]
3. **Check file permissions**: Ensure vault folder is accessible

---

#### Problem: Wrong vault path indexed

**Diagnosis**:
```bash
sqlite3 ~/.basic-memory/memory.db "SELECT name, path FROM project;"
# Should show: main | C:/Users/10064957/My Drive/GDVault/MarthaVault
# If different: Path mismatch!
```

**Fix**:
```bash
# Update database path
sqlite3 ~/.basic-memory/memory.db "
UPDATE project 
SET path = 'C:/Users/10064957/My Drive/GDVault/MarthaVault',
    updated_at = datetime('now') 
WHERE name = 'main';
"

# Restart Basic Memory MCP server
/mcp restart basic-memory

# Verify sync starts
mcp__basic-memory__sync_status(project="main")
```

---

#### Problem: Search returns no results

**Diagnosis**:
```bash
# Check if database exists
ls -lah ~/.basic-memory/memory.db

# Check entity count
mcp__basic-memory__sync_status(project="main")
# Should show: "574 entities"
```

**Fixes**:
1. **If entity count = 0**: Database needs rebuild, restart MCP server
2. **If sync incomplete**: Wait for 100% sync
3. **If search syntax wrong**: Check query examples in [[#Basic Memory]]

---

### Sync Issues

#### Problem: `/sync-vault` doesn't find new files

**Diagnosis**:
```bash
# Check git status
git status
# Any "M" or "??" files? They're uncommitted

# Check diff since checkpoint
git diff --name-status $(cat .vault-sync-checkpoint) HEAD
# Shows files changed since last sync
```

**Fix**:
1. **Commit changes first**:
   ```bash
   git add .
   git commit -m "update: sync changes"
   ```
2. **Then sync**:
   ```bash
   /sync-vault
   ```

---

#### Problem: Sync creates duplicate entities

**Diagnosis**:
```bash
mcp__memory__search_nodes("person-name")
# Returns multiple entities with same name?
```

**Fix**: Manual cleanup required
1. Identify duplicate entity IDs
2. Delete duplicates (future: automated deduplication)
3. For now: Rebuild with `/sync-vault --full`

---

## Common Patterns & Best Practices

### Pattern 1: Progressive Discovery (Like Human Memory Recall)

**Question**: "What's going on with the N3 GES recruitment?"

**Step 1: Quick recall (Graph - "I remember...")**
```python
result = mcp__memory__search_nodes("N3 GES Recruitment")
# Returns: Task entity with due date, priority, owner (Greg), stakeholder (Sello Sease)
# Observation: "Interview phase completed"
```

**Step 2: Recent context (Basic - "Let me think about when...")**
```python
context = mcp__basic-memory__search_notes("N3 GES recruitment status", project="main")
# Returns: Recent meeting notes, email threads, interview feedback
```

**Step 3: Deep dive (Follow breadcrumbs)**
```python
# Graph showed: Stakeholder is Sello Sease
sello_context = mcp__memory__search_nodes("Sello Sease")
# Returns: Sello is N3 engineer, has 11 tasks, GES vacancy is for his site

# Basic showed: Reference to "Louisa Breet" as HR lead
louisa = mcp__memory__search_nodes("Louisa Breet")
# Returns: HR Recruitment Superintendent, lead contact
```

**Result**: Built complete picture by following associations (like human memory)

---

### Pattern 2: Strategic Context Breadcrumbs

**Question**: "Why is the DT171 bearing replacement critical?"

**Breadcrumb trail**:
```python
# 1. Find task
task = mcp__memory__search_nodes("DT171 bearing")
# Shows: Priority=critical, assigned to Philip Moller, due Oct 28

# 2. Follow assignee
person = mcp__memory__search_nodes("Philip Moller")
# Shows: Epiroc site manager, has 5 BEV equipment tasks

# 3. Check strategic alignment
strategy = mcp__memory__search_nodes("BEV Programme")
# Shows: aligns_with → Q4 2025 Active Phase

# 4. Get priority weight
q4 = mcp__memory__search_nodes("Q4 2025 Active Phase")
# Shows: "BEV Program Optimization & Scale (HIGH, weight 1.5)"
```

**Answer**: Critical because BEV = 1.5x strategic priority + equipment down 5+ days = production impact

---

### Pattern 3: Impact Analysis (Reverse Traversal)

**Question**: "If Philip Moller goes on leave, what's impacted?"

```python
# 1. Find person
philip = mcp__memory__search_nodes("Philip Moller")
# Returns: Entity + 5 assigned tasks visible in relations

# 2. Check task priorities
# From relations: 2 critical (DT171, Certiq renewal), 3 high (Strata, CAS upgrades)

# 3. Check blocking dependencies
certiq = mcp__memory__search_nodes("Certiq Mobilaris")
# Returns: "CRITICAL - blocks S2 optimization"

# 4. Strategic impact
# Certiq task aligns_with BEV Programme → 1.5x weight
# If delayed: S2 optimization blocked = production impact
```

**Answer**: 5 tasks blocked, S2 optimization stalled, BEV strategic priority at risk

---

## Verification Checklist

Use this before starting any session to ensure memory systems are healthy:

```bash
# ✅ 1. Graph Memory responsive
mcp__memory__search_nodes("Gregory Karsten")
# Expected: Entity with 4 direct reports

# ✅ 2. Basic Memory synced
mcp__basic-memory__sync_status(project="main")
# Expected: "complete (100%)", 613 files

# ✅ 3. Checkpoint current
cat .vault-sync-checkpoint && git rev-parse HEAD
# Expected: Same SHA on both lines

# ✅ 4. Entity counts reasonable
grep -c '"type":"entity"' .martha/memory.json
# Expected: >100 entities

# ✅ 5. Database healthy
sqlite3 ~/.basic-memory/memory.db "SELECT COUNT(*) FROM entity;"
# Expected: ~574 entities
```

**If all ✅**: System healthy, proceed normally
**If any ❌**: Follow troubleshooting for that component

---

## Related Documentation

**Core guides**:
- [[system/Memory Systems Implementation & Validation Report.md]] - Complete history and testing
- [[system/Memory System Performance Testing Framework.md]] - Test suite
- [[README.md]] - 6-phase roadmap (Phase 1 complete)

**Usage examples**:
- [[CLAUDE.md#Memory Systems Architecture]] - Integration in main workflow
- [[system/policy.md#Priority Calculation]] - Strategic alignment formula

**Troubleshooting**:
- [[reference/claude-code/2025-10-21 – Calendar Automation System.md]] - MCP patterns
- [[.claude/commands/sync-vault.md]] - Sync command reference

---

## Quick Reference Commands

### Graph Memory
```python
# Search entities
mcp__memory__search_nodes("query")

# Get specific entities (returns full details + relations)
mcp__memory__open_nodes(["Entity Name 1", "Entity Name 2"])

# Read entire graph (warning: large response)
mcp__memory__read_graph()

# Create entities (batch up to 10)
mcp__memory__create_entities(entities=[...])

# Create relations
mcp__memory__create_relations(relations=[...])
```

### Basic Memory
```python
# Search notes (semantic)
mcp__basic-memory__search_notes("query", project="main")

# Build context with depth
mcp__basic-memory__build_context("memory://path/to/note", depth=2, project="main")

# Recent activity (temporal)
mcp__basic-memory__recent_activity(timeframe="1 week", project="main")

# Read specific note
mcp__basic-memory__read_note("note-title-or-permalink", project="main")

# Sync status
mcp__basic-memory__sync_status(project="main")
```

### Vault Sync
```bash
# Incremental sync (changed files only)
/sync-vault

# Full rebuild (all files)
/sync-vault --full

# Dry run (show what would sync)
/sync-vault --dry-run

# Check checkpoint
cat .vault-sync-checkpoint
git rev-parse HEAD
```

---

## Memory Analogy Summary

**Think of it like human memory**:

**Graph Memory** = **Explicit/Declarative Memory**
- Facts you can consciously recall
- "Greg manages 4 engineers"
- "BEV Fire Safety has 2.0x priority"
- Instant, precise, structured

**Basic Memory** = **Semantic/Episodic Memory**
- Context and associations
- "That BEV meeting last week where we discussed..."
- "I remember reading about fire safety in..."
- Rich, contextual, associative

**Together** = **How humans actually remember**
- Start with facts (Graph): "Who is Johnny Hollenbach?"
- Add context (Basic): "What's he working on lately?"
- Follow associations: "What's the BEV Fire Safety Program about?"
- Build complete understanding through progressive discovery

**The system mimics natural memory retrieval**: Start with conscious recall (Graph facts) → Trigger associative memory (Basic context) → Follow breadcrumbs recursively → Build complete picture.

---

**Last Updated**: 2025-11-04
**Status**: ✅ Operational and Validated
**Next**: Phase 2 - Real-time watcher (auto-sync on file changes)

#system #memory-systems #quick-reference #troubleshooting #architecture