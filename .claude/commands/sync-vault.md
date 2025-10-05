Manual vault synchronization command.

Updates memory systems (Graph Memory + Basic Memory) from Git history.

## Usage

```bash
/sync-vault              # Sync changes since last checkpoint
/sync-vault --full       # Re-sync entire vault (ignore checkpoint)
/sync-vault --dry-run    # Show what would be synced without doing it
/sync-vault --verbose    # Show detailed processing logs
```

## What It Does

1. **Read checkpoint**: Get last synced commit from `.vault-sync-checkpoint`
2. **Get changes**: Run `git diff --name-status <checkpoint> HEAD`
3. **Filter**: Only process relevant folders (people/, projects/, tasks/, etc.)
4. **Sync memory**: Call `/sync-vault-internal` to update memory systems
5. **Update checkpoint**: Store current commit SHA

## When to Use

**Automatic sync (Git hook)**: Memory systems update automatically every 5 minutes when Obsidian Git plugin commits changes.

**Manual sync needed for**:
- **First-time setup**: Run `/sync-vault --full` to index entire vault
- **After offline work**: Sync when reconnecting after working without Git plugin
- **Troubleshooting**: Verify memory is up-to-date
- **After git pull**: Sync changes from other devices
- **Force rebuild**: Use `--full` flag to re-index everything

## Example Output

```
🔄 Syncing memory systems from Git history...

Last sync: 2025-10-05 14:23:15 (commit a1b2c3d)
Current:   2025-10-05 15:30:42 (commit e4f5g6h)

Changed files (15 files):
  ✅ Added (3):
     - people/Jane Doe.md
     - projects/Capital/2025-10-06 – Equipment Purchase.md
     - Schedule/2025-10-15 - Team Meeting.md

  ✅ Modified (10):
     - tasks/master_task_list.md
     - strategy/FocusOfWeek.md
     - projects/BEV/fire-safety.md
     ...

  ✅ Deleted (2):
     - 00_inbox/old-note.md
     - Archive/completed-task.md

Processing...
  - Created 5 entities (Jane Doe, Equipment Purchase, Team Meeting, etc.)
  - Updated 8 entities (Master Task List, Focus of Week, etc.)
  - Deleted 1 entity (old note)
  - Created 7 relations
  - Re-indexed 13 documents in Basic Memory

✅ Sync complete in 2.3 seconds
Memory systems are up-to-date.

Checkpoint updated: e4f5g6h
```

## Flags

### `--full`
Ignore checkpoint and re-sync entire vault.

**Use when**:
- First time running sync
- Suspect memory is out of sync
- Want to rebuild from scratch

**Warning**: May take 30-60 seconds for large vaults.

### `--dry-run`
Show what would be synced without actually updating memory.

**Output**:
- List of files that would be processed
- No entities created/updated/deleted
- No checkpoint update

### `--verbose`
Show detailed processing for each file.

**Output includes**:
- File content analysis
- Entity extraction details
- Relation creation logic
- Graph Memory API calls
- Basic Memory indexing steps

## Monitoring

Check sync logs:
```bash
# View recent sync activity
tail .vault-sync.log

# Check last checkpoint
cat .vault-sync-checkpoint

# View Git commits
git log --oneline -10
```

## Troubleshooting

**Sync seems stale**:
```bash
/sync-vault --full  # Force full re-sync
```

**Errors in log**:
```bash
cat .vault-sync.log  # Check error details
```

**Hook not running**:
```bash
# Test hook manually
.git/hooks/post-commit
```

**Memory out of sync with files**:
```bash
/sync-vault --full --verbose  # Rebuild with details
```

## Technical Details

**Checkpoint file**: `.vault-sync-checkpoint`
- Contains Git commit SHA of last successful sync
- Updated after each successful sync
- Used to calculate diff for incremental updates

**Log file**: `.vault-sync.log`
- Timestamp and status of each sync operation
- Error details for troubleshooting
- Appended to, not overwritten

**Temp file**: `.sync-temp-input.txt`
- Created by Git hook for passing file list
- Deleted after processing
- If found, indicates incomplete sync

**Processing scope**:
- ✅ Synced: people/, projects/, tasks/, Schedule/, strategy/, system/, IDEAS/, Operations/, reference/places/
- ❌ Skipped: media/, Templates/, .obsidian/, Archive/, 00_inbox/

**Memory systems updated**:
- Graph Memory (mcp__memory__*): Entities and relations
- Basic Memory (mcp__basic-memory__*): Document full-text index

## Integration with Obsidian Git Plugin

**Automatic workflow**:
```
1. You edit files in Obsidian
2. Git plugin commits every 5 minutes
3. Git post-commit hook triggers
4. /sync-vault-internal runs
5. Memory systems updated
```

**No manual action needed** unless troubleshooting or forcing full sync.
