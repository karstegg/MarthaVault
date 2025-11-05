---
title: Memory Systems Architecture - Claude Desktop Integration
type: note
permalink: system/memory-systems-architecture-claude-desktop-integration
tags:
- system
- architecture
- claude-desktop
- native-memory
- integration
---

# Memory Systems Architecture - Claude Desktop Integration

**Last Updated**: 2025-11-05
**Status**: Production - Claude Desktop as Primary Interface
**Phase**: 1.5 - Native Memory Integration Layer

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLAUDE DESKTOP (Primary)                    │
│                     Native Memory Engine                        │
│  • Conversational learning (automatic)                          │
│  • Preference learning (from user feedback)                     │
│  • Session continuity (remembers context)                       │
│  • Query orchestration (decides Graph vs Basic vs Vault)        │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Graph Memory │ │ Basic Memory │ │ Vault (Git)  │
│  (MCP Tool)  │ │  (MCP Tool)  │ │ (Source)     │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## Three-Layer Memory Architecture

### Layer 1: Native Memory (Claude Desktop)
**Role**: Conversational Intelligence & Orchestration

**What it does**:
- ✅ **Automatic Learning**: Absorbs information from conversations
- ✅ **Synthesis**: Combines information from multiple sources
- ✅ **Preference Learning**: Adapts to your communication style
- ✅ **Session Context**: Remembers conversation flow
- ✅ **Query Orchestration**: Decides when to use Graph vs Basic

**Example**:
```
You: "What's going on with fire safety?"

Native Memory thinks:
  - Question needs structured facts + recent context
  - Query Graph for strategic alignment
  - Query Basic for recent updates
  - Synthesize complete answer
```

**You experience**: Natural conversation, no manual memory management

---

### Layer 2: Graph Memory (Structured Knowledge)
**Role**: Explicit Facts & Strategic Intelligence

**What it stores**:
- 160+ entities (Personnel, Projects, Tasks, Strategy, Decisions)
- 200+ typed relations (reports_to, assigned_to, aligns_with)
- Strategic weights (Fire Safety 2.0x, BEV 1.5x)

**Storage**: `C:\Users\10064957\.martha\memory.json` (JSONL)
**MCP Server**: `@modelcontextprotocol/server-memory`

**When Native Memory uses it**:
- Org chart queries ("who reports to X?")
- Strategic alignment ("tasks aligned with Y strategy?")
- Relationship traversal ("if X leaves, what's impacted?")
- Entity-centric queries ("all N3 critical tasks")

**Human analogy**: Your conscious explicit memory (facts you can recall on demand)

---

### Layer 3: Basic Memory (Semantic Context)
**Role**: Deep Context & Temporal Search

**What it stores**:
- 613 markdown files (full vault index)
- 574 entities, 975 relations (semantic links)
- FTS5 full-text search index

**Storage**: `C:\Users\10064957\.basic-memory\memory.db` (SQLite)
**MCP Server**: `@kanru/mcp-basic-memory`

**When Native Memory uses it**:
- Semantic search ("find notes about X")
- Temporal queries ("what happened last week?")
- Deep context building (follow links with depth parameter)
- Document-level retrieval ("read note about Y")

**Human analogy**: Your semantic memory (associations, context, when things happened)

---

### Layer 0: Vault (Source of Truth)
**Role**: Git-Backed Markdown Repository

**What it contains**:
- 613 markdown files (notes, tasks, people, projects)
- Git history (versioning, change tracking)
- Obsidian vault structure (folders, tags, links)

**Location**: `C:\Users\10064957\My Drive\GDVault\MarthaVault`
**Sync**: `.vault-sync-checkpoint` tracks last synced commit

**When updated**:
- Manual edits in Obsidian
- Claude Code CLI writes/edits
- `/sync-vault` indexes changes to Graph/Basic Memory

**Human analogy**: Your external memory (notebook, files you wrote down)

---

## Information Flow

### Query Flow (User → Answer)

```
1. User asks question in Claude Desktop
   ↓
2. Native Memory analyzes intent
   ↓
3. Decides which layer(s) to query:
   ├─ Graph MCP (structured facts)
   ├─ Basic MCP (semantic context)
   └─ Vault (direct file read)
   ↓
4. Synthesizes unified answer
   ↓
5. Learns from user feedback
```

**Example: "What's the BEV fire safety status?"**

```
Native Memory → Graph: search_nodes("BEV Fire Safety")
  Returns: Program entity, 11 tasks, Johnny leads, 2.0x weight
  
Native Memory → Basic: search_notes("BEV fire safety recent")
  Returns: Recent meeting notes, progress updates
  
Native Memory synthesizes:
  "BEV Fire Safety Program (2.0x CRITICAL) has 11 tasks led by 
   Johnny Hollenbach. Recent progress: [meetings]. Strategic 
   alignment: Q4 Focus Area 1. Next: [from task due dates]."
```

---

### Update Flow (Changes → Memory Systems)

```
1. You edit file in Obsidian
   ↓
2. Obsidian Git plugin commits (auto, every 5-10 min)
   ↓
3. Git post-commit hook triggers (future automation)
   ↓
4. Claude Code CLI runs /sync-vault
   ↓
5. Changed files processed:
   ├─ Entities extracted → Graph Memory
   ├─ Full-text indexed → Basic Memory
   └─ Checkpoint updated
   ↓
6. Next Claude Desktop session sees updates
```

**Current**: Step 4 is manual (`/sync-vault`)
**Phase 2**: Automated via Obsidian watcher plugin

---

## Role Separation

### Claude Desktop (Primary Interface)
**You interact with this**

**Strengths**:
- Natural conversation
- Automatic learning
- Context synthesis
- Preference adaptation

**Use for**:
- Daily work and questions
- Strategic discussions
- Task management
- Project planning

---

### Claude Code CLI (Background Automation)
**Runs in background for automation**

**Strengths**:
- File operations (write, edit)
- Batch processing
- Git operations
- Scheduled tasks

**Use for**:
- Daily production reports (automated)
- Email processing (Outlook sync)
- WhatsApp integration (automated triage)
- Calendar sync (Outlook ↔ Obsidian)
- Memory system updates (`/sync-vault`)

---

## Decision Matrix: Which Layer When?

| Query Type | Native Memory | Graph MCP | Basic MCP | Direct Vault |
|------------|---------------|-----------|-----------|--------------|
| "Who reports to X?" | Orchestrates → | ✅ Use | ❌ Slower | ❌ Manual |
| "Strategic alignment?" | Orchestrates → | ✅ Use (aligns_with) | ❌ No relations | ❌ Manual |
| "What happened last week?" | Orchestrates → | ❌ No temporal | ✅ Use (recent_activity) | ❌ Manual |
| "Find notes about X" | Orchestrates → | ❌ No FTS | ✅ Use (semantic) | ❌ Manual |
| "Casual chat/learning" | ✅ Handles internally | ❌ Not needed | ❌ Not needed | ❌ Not needed |
| "Complex synthesis" | ✅ Uses all layers | ✅ Facts | ✅ Context | ✅ Source |

**Key insight**: You almost never need to think about which layer. Native Memory orchestrates automatically.

---

## Integration Points

### Claude Desktop ↔ MCP Tools

**Configuration** (`.claude/settings.json` or equivalent):
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "basic-memory": {
      "command": "node",
      "args": ["C:/Users/10064957/.basic-memory/index.js"]
    }
  }
}
```

**How it works**:
1. Claude Desktop loads MCP servers on startup
2. Native Memory can call MCP tools as needed
3. Tools return structured data
4. Native Memory synthesizes into natural language

---

### Claude Code CLI ↔ Vault

**Configuration** (`.claude/commands/sync-vault.md`):
- Incremental sync: Compare checkpoint to HEAD
- Full sync: Process all files in relevant folders
- Update Graph Memory entities
- Re-index Basic Memory documents

**Trigger**: Manual `/sync-vault` or post-commit hook (Phase 2)

---

## Best Practices

### For You (User)
1. ✅ **Use Claude Desktop for everything interactive**
2. ✅ **Let Native Memory learn naturally** (no manual updates)
3. ✅ **Correct when wrong** (Native Memory adapts)
4. ✅ **Use Claude Code CLI for automation** (background tasks)
5. ✅ **Run `/sync-vault` after major vault changes** (or wait for auto-sync)

### For Claude Desktop
1. ✅ **Trust Native Memory to orchestrate** (it knows when to use MCPs)
2. ✅ **Use Graph for structured queries** (org chart, strategic alignment)
3. ✅ **Use Basic for semantic/temporal** (recent activity, find notes)
4. ✅ **Synthesize complete answers** (don't just dump MCP results)
5. ✅ **Learn from user feedback** (adapt responses based on corrections)

### For Claude Code CLI
1. ✅ **Run as automation engine** (not primary interface)
2. ✅ **Keep memory systems synced** (`/sync-vault` after changes)
3. ✅ **Handle file operations** (write reports, edit notes)
4. ✅ **Process background tasks** (email, WhatsApp, calendar)
5. ✅ **Update checkpoint** (track what's been indexed)

---

## Migration Path

### Phase 1: Dual Memory Foundation ✅ **COMPLETE**
- Graph Memory operational (160+ entities)
- Basic Memory operational (613 files indexed)
- Vault sync working (`/sync-vault`)
- Testing complete (4x faster, validated)

### Phase 1.5: Native Memory Integration ✅ **CURRENT**
- Claude Desktop as primary interface
- Native Memory orchestrates MCP queries
- Simplified startup (10s health check only)
- Documentation updated for Desktop workflow

### Phase 2: Real-Time Automation (NEXT)
- Obsidian watcher plugin (auto-sync on file changes)
- Post-commit hook (automatic `/sync-vault`)
- Background Claude Code CLI (scheduled tasks)
- Zero-latency memory updates

### Phase 3: Behavioral Intelligence
- SQLite reflex cache (learn from user edits)
- Confidence scoring (strengthen patterns)
- Skills library (sub-agent spawning)
- Native Memory + Graph + Behavioral = full intelligence

---

## Success Metrics

**System Health**:
- ✅ Native Memory responds naturally
- ✅ Graph Memory <1s response time
- ✅ Basic Memory 100% synced
- ✅ Vault checkpoint current

**User Experience**:
- ✅ No manual memory management needed
- ✅ Answers include strategic context automatically
- ✅ Progressive discovery feels natural
- ✅ System adapts to your style

**Integration Quality**:
- ✅ Native Memory calls MCPs appropriately
- ✅ Synthesis feels seamless (not just data dump)
- ✅ Background CLI runs without interruption
- ✅ Sync lag <5 minutes (future: real-time)

---

## Troubleshooting

### "Native Memory doesn't seem to remember X"
**Possible causes**:
1. Information not yet in MCP systems → Run `/sync-vault`
2. Query needs explicit MCP call → Ask to search Graph/Basic directly
3. Native Memory learning curve → Give feedback, it will adapt

### "MCP tools not working"
**Check**:
1. MCP servers loaded? (Check Claude Desktop settings)
2. Graph Memory accessible? (`mcp__memory__search_nodes("test")`)
3. Basic Memory synced? (Was working in CLI test)

### "Vault out of sync"
**Fix**:
```bash
# Check sync status
cat .vault-sync-checkpoint && git rev-parse HEAD

# If different, sync
/sync-vault
```

---

## Related Documentation

**Core Architecture**:
- [[system/Dual Memory System - Quick Reference Guide]] - Updated for Desktop
- [[system/Memory Systems - Session Startup Protocol]] - Simplified for Desktop
- [[system/Memory Systems Implementation & Validation Report]] - Full history

**Automation**:
- [[.claude/commands/sync-vault.md]] - Sync command reference
- [[README.md]] - 6-phase roadmap (Phase 1.5 current)

**Skills & Integration**:
- [[.claude/skills/outlook-extractor/]] - Email automation
- [[reference/claude-code/WhatsApp Voice Note Transcription.md]] - WhatsApp integration

---

**Architecture Status**: ✅ Production Ready
**Primary Interface**: Claude Desktop with Native Memory
**Background Automation**: Claude Code CLI
**Next Phase**: Real-time vault watcher (Phase 2)

#system #architecture #claude-desktop #native-memory #integration #phase-1.5
