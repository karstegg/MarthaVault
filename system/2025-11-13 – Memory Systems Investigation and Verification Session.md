---
'Status:': Complete
'Priority:': High
'Assignee:': Greg
'DueDate:': null
'Tags:': null
permalink: system/2025-11-13-memory-systems-investigation-and-verification-session
---

# Memory Systems Investigation and Verification Session

**Date**: 2025-11-13
**Session Type**: Troubleshooting and Testing
**Duration**: ~2 hours
**Outcome**: ✅ Systems verified healthy and operating as designed

---

## Executive Summary

Investigation into perceived "stale" memory systems revealed that both Graph Memory and Basic Memory are functioning correctly. What appeared to be 37 hours of sync lag was actually a misunderstanding of:
1. How git auto-backup commits work (675 commits ≠ 675 content changes)
2. When MCP servers run (session-only, not persistent background)
3. Database timestamp interpretation (normal lag after commits)

**Key Discovery**: Basic Memory auto-sync is working with **9-second latency** when Claude Code is running.

---

## Investigation Findings

### 1. Basic Memory Auto-Sync - VERIFIED WORKING ✅

**Test case**:
- Created file: `00_Inbox/2025-11-13.md` at 17:35:00
- Database indexed: 17:35:09 (9 seconds later)
- Content verified readable via MCP tools

**Configuration** (`~/.basic-memory/config.json`):
```json
{
  "sync_changes": true,
  "sync_delay": 1000,
  ...
}
```

**Requirements**:
- MCP server must be actively running (during Claude sessions)
- File watcher monitors entire vault for changes
- No manual `/sync-vault` needed while Claude running

---

### 2. Folder Indexing Strategy - INTENTIONAL DESIGN ✅

| System | Scope | 00_Inbox Included? |
|--------|-------|-------------------|
| **Basic Memory** | Entire vault (file watcher) | ✅ YES |
| **Graph Memory** | Selective folders (`/sync-vault`) | ❌ NO (intentional) |

**Graph Memory folders**:
- people/, projects/, tasks/, Schedule/
- strategy/, system/, IDEAS/, Operations/
- reference/places/

**Rationale for excluding 00_Inbox from Graph Memory**:
- Inbox is temporary staging area
- Files moved by `/triage` to permanent locations
- Prevents duplicate entities (staging + permanent)
- Basic Memory provides search coverage for inbox

**Decision**: Keep current configuration (confirmed 2025-11-13)

---

### 3. Git Auto-Backup Behavior - EXPLAINED ✅

**The "675 Commits" Mystery**:
- Total commits since Oct 6, 2025: **675**
- Actual content changes: **~3 files** (N3 Electrical Foreman docs)
- Auto-backup frequency: Every 5 minutes (Obsidian Git plugin)

**Typical auto-backup commit contents**:
- `.vault-sync-checkpoint` (updated)
- `.obsidian/workspace.json` (workspace state)
- `.sync-pending.txt` (sync tracking)

**Key insight**: High commit count ≠ high content change count with auto-backup enabled.

**Verification**:
- Checkpoint SHA matches HEAD: `40c92ec` ✅
- No unsynced content changes in indexed folders
- Database timestamp appearing "stale" was misleading (no new content to sync)

---

### 4. MCP Server Lifecycle - CLARIFIED ✅

**How MCP servers work**:
- Run only during active Claude Code or Claude Desktop sessions
- Not persistent background services (Phase 2 future enhancement)
- Auto-sync (`sync_changes: true`) requires active server

**Current workflow** (optimal):
- Keep Claude Code + MarthaVault running together
- Real-time sync via file watcher (9-second latency)
- Manual `/sync-vault` only needed after offline vault changes

**Phase 2 enhancements** (future):
- Persistent background MCP service
- Git post-commit hook auto-trigger
- Zero-latency updates even when Claude closed

---

## System Status - FINAL VERIFICATION

| Component | Status | Evidence |
|-----------|--------|----------|
| **Basic Memory auto-sync** | ✅ WORKING | 9-second latency verified |
| **Graph Memory sync** | ✅ WORKING | Checkpoint matches HEAD |
| **Vault sync checkpoint** | ✅ CURRENT | 40c92ec (no lag) |
| **Entity count** | ✅ GROWING | 666 entities in Basic Memory |
| **Folder indexing** | ✅ AS DESIGNED | Intentional selective coverage |
| **MCP servers** | ✅ ACTIVE | Running during session |

---

## Graph Memory Updates

Created 4 new entities to preserve session insights:

1. **Basic Memory Auto-Sync Verification** (System Documentation)
   - 9-second latency verification
   - Configuration details
   - Test case documentation

2. **Memory Systems Folder Indexing Strategy** (System Architecture)
   - Basic vs Graph folder coverage
   - 00_Inbox exclusion rationale
   - Design decision documentation

3. **Git Auto-Backup vs Content Changes** (System Behavior)
   - 675 commits explanation
   - Auto-backup behavior patterns
   - Checkpoint interpretation guide

4. **MCP Server Session Lifecycle** (System Architecture)
   - Session-only execution model
   - Phase 2 enhancement roadmap
   - Optimal workflow guidance

**Relations created**: 5 relations linking entities to existing memory graph

---

## Lessons Learned

### 1. Database Timestamps Can Mislead
- Database `updated_at` shows last write time
- Doesn't mean system is "behind" if no content changed
- Always verify: checkpoint SHA vs HEAD, not timestamps

### 2. Commit Count ≠ Content Volume
- Auto-backup plugins create many commits
- Most commits are workspace state, not content
- Use `git diff --name-status` to find real changes

### 3. Real-Time Sync Requires Active Server
- `sync_changes: true` works perfectly
- But only while MCP server running
- Current workflow (Claude + vault together) is optimal

### 4. Folder Strategy Matters
- Selective indexing prevents entity pollution
- Temporary staging areas (inbox) should stay out of Graph
- Basic Memory provides comprehensive search anyway

---

## Recommendations

### Keep Current Workflow ✅
- Continue running Claude Code + MarthaVault together
- Real-time sync via file watcher works perfectly
- No changes needed to configuration

### Manual Sync Only When Needed
Run `/sync-vault` only in these cases:
- After working on vault while Claude was closed
- After pulling changes from git remote
- When troubleshooting suspected sync issues
- For full rebuild: `/sync-vault --full`

### Phase 2 Optional
Persistent background sync is nice-to-have, not required:
- Current 9-second latency is excellent
- Manual restart sync is quick and reliable
- Implement only if you need 24/7 monitoring

---

## Related Documentation

- [[system/Dual Memory System - Quick Reference Guide]]
- [[system/Memory Systems Architecture - Claude Desktop Integration]]
- [[system/Memory Systems Implementation & Validation Report]]
- [[.claude/commands/sync-vault.md]]

---

## Session Metadata

**Participants**: Greg + Claude Code (Sonnet 4.5)
**Investigation triggered by**: Question about memory update status
**Tools used**:
- sqlite3 queries on memory.db
- git log analysis
- MCP tool testing (read_note, build_context)
- Real-time file creation test

**Outcome**: All systems verified healthy. No action required. Continue current workflow.

---

#system #memory-systems #investigation #verification #troubleshooting #2025-11-13