# /sync-vault [flags]

Manual vault synchronization command - updates memory systems from Git history.

## Usage

```bash
/sync-vault              # Sync changes since last checkpoint
/sync-vault --full       # Re-sync entire vault (ignore checkpoint)
/sync-vault --dry-run    # Show what would be synced without doing it
/sync-vault --verbose    # Show detailed processing logs
```

## Instructions

### Parse Arguments
1. Check for flags: `--full`, `--dry-run`, `--verbose`
2. Set sync mode accordingly

### Standard Sync (no --full flag)
1. Read `.vault-sync-checkpoint` for last synced commit SHA
2. Run `git diff --name-status <checkpoint> HEAD`
3. Filter to relevant folders: people/, projects/, tasks/, Schedule/, strategy/, system/, IDEAS/, Operations/, reference/places/
4. **EXECUTE SYNC** for each changed file:
   - **Added/Modified files**: Read file → Create/update Graph Memory entities → Index in Basic Memory
   - **Deleted files**: Delete from Graph Memory → Delete from Basic Memory
   - Batch API calls where possible (up to 10 entities at a time)
5. Update checkpoint to current HEAD SHA
6. Report summary of entities created/updated/deleted

### Full Sync (--full flag)
1. Ignore checkpoint
2. Get all files in relevant folders: `git ls-files people/ projects/ tasks/ Schedule/ strategy/ system/ IDEAS/ Operations/ reference/places/`
3. Mark all as "Added" (A) for full re-index
4. **EXECUTE SYNC** for ALL files (same as standard sync)
5. Update checkpoint to current HEAD SHA
6. Report summary of all entities indexed

### Dry Run (--dry-run flag)
1. Show list of files that would be processed
2. Show change types (A/M/D)
3. Do NOT update memory systems
4. Do NOT update checkpoint

### Verbose Mode (--verbose flag)
1. Show detailed processing for each file
2. Show entity extraction and relation creation
3. Show memory API calls and results

## Output

Show progress and summary:
```
🔄 Syncing memory systems from Git history...

Last sync: 2025-10-05 14:23:15 (commit a1b2c3d)
Current:   2025-10-05 15:30:42 (commit e4f5g6h)

Changed files (15 files):
  ✅ Added (3): ...
  ✅ Modified (10): ...
  ✅ Deleted (2): ...

Processing...
  - Created 5 entities
  - Updated 8 entities
  - Deleted 1 entity
  - Created 7 relations
  - Re-indexed 13 documents in Basic Memory

✅ Sync complete in 2.3 seconds
Memory systems are up-to-date.

Checkpoint updated: e4f5g6h
```

## When to Use

**Manual sync needed for**:
- First-time setup: Run `/sync-vault --full` to index entire vault
- After offline work: Sync when reconnecting after working without Git plugin
- Troubleshooting: Verify memory is up-to-date
- After git pull: Sync changes from other devices
- Force rebuild: Use `--full` flag to re-index everything

**Automatic sync**: Memory systems update automatically every 5 minutes when Obsidian Git plugin commits changes (via Git post-commit hook).
