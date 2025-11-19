---
Status: Active
Priority: Critical
Assignee: Claude
DueDate: 2025-11-20
Tags: null
permalink: system/2025-11-19-critical-issue-sync-vault-command-broken-1
---

# CRITICAL: /sync-vault Command Implementation Gap

**Date Discovered:** 2025-11-19
**Severity:** High - Memory systems not updating when manually triggered

---

## Problem Statement

The `/sync-vault` slash command **promises but doesn't deliver** full memory system synchronization.

**Expected behavior (from documentation):**
```
/sync-vault should:
1. Read .vault-sync-checkpoint for last synced commit
2. Run git diff to find changed files
3. For each changed file:
   - Create/update Graph Memory entities
   - Index in Basic Memory
4. Update checkpoint
5. Report summary (X entities created, Y relations, etc.)
```

**Actual behavior:**
```
/sync-vault currently:
1. Updates .vault-sync-checkpoint to current HEAD
2. Does NOTHING else
3. No memory indexing occurs
4. No entity creation
5. No search index updates
```

---

## Root Cause

Two separate commands exist:

1. **`/sync-vault`** (.claude/commands/sync-vault.md)
   - User-facing manual command
   - Documentation describes full sync behavior
   - **Implementation missing** - only updates checkpoint

2. **`/sync-vault-internal`** (.claude/commands/sync-vault-internal.md)
   - Internal command for Git post-commit hook
   - **Fully implemented** - does all memory indexing
   - Not directly callable by user

**Gap:** `/sync-vault` should invoke `/sync-vault-internal` but doesn't.

---

## Evidence (Today's Session)

**Test Case:**
1. Updated bearing temperature monitoring project file
2. Ran `/sync-vault`
3. Checkpoint updated to HEAD (953f2cf)
4. Queried memory systems:
   - ❌ Graph Memory: Empty (no entities)
   - ⚠️ Basic Memory search: Empty (no semantic index)
   - ✅ Basic Memory direct read: Works (file accessible)

**Conclusion:** Files synced, memory systems NOT updated.

---

## Impact

**High Impact:**
- Users expect `/sync-vault` to update memory systems
- Documentation creates false expectation
- Manual entity creation required after every file change
- Search functionality broken after edits
- Memory systems diverge from vault state

**Workaround (current):**
- Manually create entities using `mcp__memory__create_entities`
- Manually index using `mcp__basic-memory__write_note`
- Time-consuming and error-prone

---

## Solution Options

### Option 1: Fix `/sync-vault` to Call Internal Command (RECOMMENDED)

**Modify `.claude/commands/sync-vault.md`:**

```markdown
## Instructions

### Standard Sync (no --full flag)
1. Read `.vault-sync-checkpoint` for last synced commit SHA
2. Run `git diff --name-status <checkpoint> HEAD`
3. Filter to relevant folders: people/, projects/, tasks/, Schedule/, strategy/, system/, IDEAS/, Operations/, reference/places/
4. **Write filtered changes to `.sync-temp-input.txt`**
5. **Execute `/sync-vault-internal` command** to process changes
6. Report summary from internal command output
7. Update checkpoint to current HEAD SHA

### Full Sync (--full flag)
1. Run `git ls-files people/ projects/ tasks/ Schedule/ strategy/ system/ IDEAS/ Operations/ reference/places/`
2. Mark all as "Added" (A) for full re-index
3. **Write to `.sync-temp-input.txt`**
4. **Execute `/sync-vault-internal` command**
5. Report summary
6. Update checkpoint to current HEAD SHA
```

**Benefits:**
- Reuses existing internal implementation
- Minimal code duplication
- Consistent behavior between manual and automated sync

---

### Option 2: Duplicate Internal Logic in Manual Command

Implement full memory indexing directly in `/sync-vault.md` instructions.

**Drawbacks:**
- Code duplication
- Maintenance burden (two places to update)
- Risk of divergence between manual and automated sync

---

### Option 3: Document Current Behavior (NOT RECOMMENDED)

Update `/sync-vault` documentation to say it only updates checkpoint.

**Drawbacks:**
- Users lose expected functionality
- Memory systems remain out of sync
- Reduces value of manual sync command

---

## Recommended Fix (Option 1)

**Implementation Steps:**

1. **Update `/sync-vault` command:**
   - Add step to write `.sync-temp-input.txt`
   - Add step to execute `/sync-vault-internal`
   - Parse and report output summary

2. **Test cases:**
   - Add new file → verify entity created
   - Modify file → verify entity updated
   - Delete file → verify entity removed
   - Run with `--full` flag → verify all files reindexed

3. **Documentation:**
   - Ensure `/sync-vault` docs match actual behavior
   - Add troubleshooting section
   - Document `.sync-temp-input.txt` format

---

## Testing Plan

**Test 1: Add New File**
```bash
# Create test file
echo "# Test Project" > projects/Test/test.md

# Commit
git add . && git commit -m "test"

# Run sync
/sync-vault

# Verify
- Graph Memory: search_nodes("Test Project") should return entity
- Basic Memory: search_notes("Test Project") should return document
```

**Test 2: Modify Existing File**
```bash
# Update test file
echo "Updated content" >> projects/Test/test.md

# Commit
git add . && git commit -m "update"

# Run sync
/sync-vault

# Verify
- Graph Memory: entity observations updated
- Basic Memory: document content updated
```

**Test 3: Delete File**
```bash
# Delete test file
rm projects/Test/test.md

# Commit
git add . && git commit -m "delete"

# Run sync
/sync-vault

# Verify
- Graph Memory: entity removed
- Basic Memory: document removed
```

---

## Priority Justification

**Critical Priority Because:**
1. Breaks core memory system functionality
2. Documentation creates false user expectations
3. Discovered during actual use (not theoretical)
4. Manual workarounds time-consuming
5. Undermines trust in memory systems

**Timeline:**
- Immediate: Document issue (this file) ✅
- Within 24h: Implement Option 1 fix
- Before next session: Test and validate

---

## Related Files

- `.claude/commands/sync-vault.md` - Manual command (needs fix)
- `.claude/commands/sync-vault-internal.md` - Internal implementation (working)
- `.vault-sync-checkpoint` - Checkpoint tracker
- `.sync-temp-input.txt` - Temporary file for change list

---

## Action Items

- [ ] Implement Option 1 fix in `/sync-vault` command
- [ ] Test all three test cases
- [ ] Update session learnings document with fix details
- [ ] Add to CLAUDE.md: "Always run /sync-vault after file changes for memory updates"
- [ ] Consider automatic sync after Edit/Write tool usage

---

**Status:** Issue documented, manual workaround applied for today's session, fix pending implementation.