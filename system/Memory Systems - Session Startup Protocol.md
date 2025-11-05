---
title: Memory Systems - Session Startup Protocol
type: note
permalink: system/memory-systems-session-startup-protocol
tags:
- system
- memory-systems
- startup-protocol
- automation
---

# 🔄 UPDATED FOR CLAUDE DESKTOP (2025-11-05)

**This protocol is now OPTIONAL for Claude Desktop users**

Claude Desktop's native memory handles automatic context loading and synthesis. The startup protocol is only needed for:
- Claude Code CLI sessions (automation/background work)
- After long breaks (>1 week)
- When you suspect memory system issues
- On explicit user request

---

## Simplified Startup for Claude Desktop

### Quick Health Check (10 seconds - only when needed)

**Run this ONLY if**:
- First use after setup
- After long break (>1 week)
- Suspecting sync issues
- User explicitly requests verification

```python
# Phase 1: Quick Verification
# 1. Graph Memory health
mcp__memory__search_nodes("Gregory Karsten")
# Expected: Entity with 4-5 direct reports

# 2. Sync status
cat .vault-sync-checkpoint && git rev-parse HEAD
# Expected: Both SHAs match

# 3. Done! Native Memory handles the rest.
```

**Expected output**:
```
✅ Graph Memory: Operational (160+ entities)
✅ Vault Sync: Current (checkpoint = HEAD)

Native Memory will handle context loading automatically.
Ready to assist!
```

---

## Full Startup Protocol (Claude Code CLI Only)

**Use this workflow when running Claude Code CLI for automation:**

# Memory Systems - Session Startup Protocol

**Purpose**: Minimal health check for Claude Desktop with native memory
**When**: Optional - only when troubleshooting or after long break
**Duration**: <10 seconds
**Outcome**: Verify Graph/Basic MCPs operational, native memory handles context

---

## Startup Sequence (Run Automatically)

### Quick Health Check (10 seconds)

**For Claude Desktop with native memory, this is all you need:**

```python
# 1. Verify Graph Memory operational
mcp__memory__search_nodes("Gregory Karsten")
# ✅ Returns org structure → System healthy
# ❌ Empty/error → See troubleshooting

# 2. Verify sync current (optional)
# Only check if Graph query failed or suspected stale data
cat .vault-sync-checkpoint
git rev-parse HEAD
# ✅ Same SHA → In sync
# ❌ Different → Run /sync-vault
```

**Expected Output**:
```
✅ Graph Memory: Operational
✅ Sync: Current
```

**If ❌**: Run troubleshooting from [[system/Dual Memory System - Quick Reference Guide#Troubleshooting Guide]]

**Note**: With native memory, skip explicit context loading. Native memory already has:
- Recent conversations (last 24hrs)
- Strategic priorities mentioned
- People and projects discussed
- Your working patterns

**Only load context explicitly when**:
- First session after >1 week break
- User requests full strategic overview  
- Major project status change

---

## Startup Output (Simplified for Desktop)

**Healthy (default - silent)**:
```
✅ Memory systems operational
```

**If issues detected**:
```
⚠️ Graph Memory: Empty response
→ Run /sync-vault

✅ Ready to assist
```

---

## Automated Repair Workflow

**If user confirms repair**, run this sequence:

```bash
# 1. Restart MCP servers
/mcp restart memory
/mcp restart basic-memory

# Wait 5 seconds for startup
sleep 5

# 2. Verify Basic Memory path
sqlite3 ~/.basic-memory/memory.db "
SELECT name, path FROM project WHERE name='main';
"
# If wrong path: Run path fix from Quick Reference Guide

# 3. Run vault sync
/sync-vault

# 4. Verify Graph Memory
mcp__memory__search_nodes("Gregory Karsten")

# 5. Verify Basic Memory
mcp__basic-memory__sync_status(project="main")

# 6. Report results
echo "✅ Repair complete - all systems operational"
# OR
echo "❌ Repair failed - manual intervention required"
```

---

## Progressive Discovery During Session

**Throughout conversation**, use this thinking pattern:

### Question Classification

**User asks about...**

1. **Person** ("Who is X?" / "What does Y do?")
   - Start: `search_nodes("person-name")` (Graph - org chart, role, team)
   - Enrich: `search_notes("person-name recent work")` (Basic - current projects)
   - Follow: Check `assigned_to` relations for their tasks

2. **Project** ("Status of X project?")
   - Start: `search_nodes("project-name")` (Graph - owner, strategic alignment)
   - Enrich: `search_notes("project-name status")` (Basic - recent updates)
   - Follow: `aligns_with` relations to show strategic priority

3. **Task** ("What needs to be done for X?")
   - Start: `search_nodes("task-keyword")` (Graph - assignee, due date, priority)
   - Enrich: `build_context("memory://tasks/master-task-list", depth=2)` (Basic - full context)
   - Follow: Check `located_at` and `assigned_to` for dependencies

4. **Strategy** ("What are the priorities?")
   - Start: `search_nodes("Q4 2025 Active Phase")` (Graph - focus areas with weights)
   - Enrich: `search_notes("strategic priorities current")` (Basic - recent strategic discussions)
   - Follow: `aligns_with` relations backwards to find aligned projects/tasks

5. **Temporal** ("What happened last week?")
   - Start: `recent_activity(timeframe="1 week")` (Basic - file changes)
   - Enrich: `search_nodes("recent-entity-names")` (Graph - entity details)
   - Follow: Build narrative from timeline + entity context

---

## Breadcrumb Following Example

**User**: "What's going on with fire safety?"

**Thinking process**:

```
1. Initial query (Graph - broad):
   search_nodes("fire safety")
   → Found: BEV Fire Safety Program entity
   → Observations: 11 tasks, led by Johnny Hollenbach
   → Relations: aligns_with → Safety & Compliance Excellence (2.0x weight)
   
2. Follow breadcrumb: Who is Johnny?
   search_nodes("Johnny Hollenbach")
   → Personnel entity
   → Observations: BEV Fire Safety lead, N3 site
   → Relations: Has 10+ assigned tasks
   
3. Follow breadcrumb: What triggered this program?
   Observation mentions: "HD0054 fire incident triggered..."
   search_nodes("HD0054 Fire Incident")
   → Incident entity
   → Observations: October 2025, independent investigation, DMRE reporting
   → Relations: triggered_fire_safety_programme_for → BEV Programme
   
4. Recent context (Basic - narrow):
   search_notes("fire safety recent progress", project="main")
   → Recent meeting notes, status updates
   
5. Synthesize answer:
   "BEV Fire Safety Program (2.0x strategic priority) has 11 tasks led by Johnny Hollenbach
    at N3. Triggered by HD0054 fire incident in October. Recent progress: [from Basic Memory].
    Critical tasks: [from Graph relations]. Strategic importance: Aligns with Safety & Compliance
    Excellence (Q4 2025 Focus Area 1)."
```

**Pattern**: Graph gives structure (what, who, why) → Basic gives narrative (how, when, context) → Recursive breadcrumbs build complete picture

---

## Session End Protocol

**Before session closes**, optionally:

1. **Save session insights** (if significant discoveries made):
   ```python
   mcp__basic-memory__write_note(
     title=f"Session Insights {DATE}",
     content="Key discoveries and decisions from this session",
     folder="Daily",
     project="main"
   )
   ```

2. **Update task statuses** (if tasks were completed):
   ```python
   # Mark completed tasks in Graph Memory
   # (Future: automated task status sync)
   ```

3. **Verify sync** (if major changes were made):
   ```bash
   git status  # Check for uncommitted changes
   /sync-vault  # Sync if needed
   ```

---

## Integration with Existing Workflows

### SessionStart Hook (Future)

**When implemented**, this protocol runs automatically:

```yaml
# .claude/hooks/session-start.md
name: Memory System Startup Check
trigger: session_start
commands:
  - run: python .claude/scripts/memory_health_check.py
  - if_fail: notify_user("Memory systems need attention")
  - run: python .claude/scripts/load_session_context.py
  - output: Display strategic priorities and near-term tasks
```

### Manual Invocation (Current)

**User can trigger with**:
```
/memory-check
```

Or Claude proactively runs at session start.

---

## Success Metrics

**Healthy session startup**:
- ✅ All health checks pass in <5 seconds
- ✅ Context loaded and displayed to user
- ✅ No manual troubleshooting required
- ✅ User can immediately start working with full context

**Degraded but functional**:
- ⚠️ Some systems need attention but workarounds available
- ⚠️ Context partially loaded
- ⚠️ User notified of issues
- ✅ Session can proceed with reduced capability

**Critical failure**:
- ❌ Cannot load context or answer queries
- ❌ Repair workflow offered
- ❌ Session should pause until fixed

---

**Last Updated**: 2025-11-05
**Status**: Simplified for Claude Desktop with native memory
**Interface**: Claude Desktop (primary), Claude CLI (automation)
**Next**: Native memory learns naturally, minimal startup needed

#system #memory-systems #startup-protocol #automation #health-check