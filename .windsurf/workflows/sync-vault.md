---
description: Synchronize memory systems (Graph + Basic) from vault changes
---

# /sync-vault

Manual vault synchronization command - updates memory systems from Git history.

## Usage

```
/sync-vault              # Sync changes since last checkpoint
/sync-vault --full       # Re-sync entire vault (ignore checkpoint)
/sync-vault --dry-run    # Show what would be synced without doing it
/sync-vault --verbose    # Show detailed processing logs
```

## What This Does

Synchronizes the memory systems (Graph Memory + Basic Memory) with changes in the vault:
- Reads Git history to find changed files
- Updates Graph Memory entities and relations
- Re-indexes documents in Basic Memory
- Tracks sync checkpoint for incremental updates

## Sync Modes

### Standard Sync (Default)

**When to use**: After making changes to vault files

**Process**:
1. Read `.vault-sync-checkpoint` for last synced commit SHA
2. Run `git diff --name-status <checkpoint> HEAD`
3. Filter to relevant folders:
   - `people/`, `projects/`, `tasks/`, `Schedule/`
   - `strategy/`, `system/`, `IDEAS/`, `Operations/`
   - `reference/places/`
4. **Execute sync** for each changed file:
   - **Added/Modified (A/M)**: Read file → Create/update Graph Memory → Index in Basic Memory
   - **Deleted (D)**: Delete from Graph Memory → Delete from Basic Memory
5. Update checkpoint to current HEAD SHA
6. Report summary

### Full Sync (`--full`)

**When to use**: First-time setup, force rebuild, troubleshooting

**Process**:
1. Ignore checkpoint
2. Get ALL files in relevant folders: `git ls-files people/ projects/ tasks/ ...`
3. Mark all as "Added" for full re-index
4. Execute sync for ALL files
5. Update checkpoint to current HEAD SHA
6. Report summary

### Dry Run (`--dry-run`)

**When to use**: Preview changes before syncing

**Process**:
1. Show list of files that would be processed
2. Show change types (A/M/D)
3. Do NOT update memory systems
4. Do NOT update checkpoint

### Verbose Mode (`--verbose`)

**When to use**: Debugging, detailed logging

**Process**:
- Show detailed processing for each file
- Show entity extraction and relation creation
- Show memory API calls and results

## Relevant Folders

Files in these folders are synced to memory systems:

- **`people/`** - Personnel profiles → Graph Memory entities (Person type)
- **`projects/`** - Project documentation → Graph Memory entities (Project type)
- **`tasks/`** - Task lists → Graph Memory entities (Task type)
- **`Schedule/`** - Calendar events → Basic Memory indexing
- **`strategy/`** - Strategic documents → Graph Memory (Strategy type)
- **`system/`** - Policies and skills → Basic Memory indexing
- **`IDEAS/`** - Innovation concepts → Graph Memory (Idea type)
- **`Operations/`** - Operational docs → Basic Memory indexing
- **`reference/places/`** - Mine sites → Graph Memory (Location type)

## Entity Extraction

For each file, extract:

**Graph Memory Entities**:
- **Type**: Person, Project, Location, Task, Idea, Strategy, Decision
- **Name**: From filename or front-matter
- **Observations**: Key facts from content
- **Relations**: Links to other entities (reports_to, assigned_to, located_at, etc.)

**Basic Memory Documents**:
- Full markdown content
- Metadata (tags, dates, assignees)
- Searchable text for semantic queries

## Checkpoint Management

**Checkpoint file**: `.vault-sync-checkpoint`

**Format**:
```
e4f5g6h1234567890abcdef
2025-10-15T14:23:15+02:00
```

**Purpose**: Track last synced commit to enable incremental updates

## Output Format

```
🔄 Syncing memory systems from Git history...

Last sync: 2025-10-05 14:23:15 (commit a1b2c3d)
Current:   2025-10-05 15:30:42 (commit e4f5g6h)

Changed files (15 files):
  ✅ Added (3): people/Smith, John.md, projects/BEV/status.md, ...
  ✅ Modified (10): tasks/master_task_list.md, ...
  ✅ Deleted (2): projects/Old_Project/notes.md, ...

Processing...
  - Created 5 entities in Graph Memory
  - Updated 8 entities in Graph Memory
  - Deleted 1 entity from Graph Memory
  - Created 7 relations in Graph Memory
  - Re-indexed 13 documents in Basic Memory

✅ Sync complete in 2.3 seconds
Memory systems are up-to-date.

Checkpoint updated: e4f5g6h
```

## When to Use

### Manual Sync Needed For:

1. **First-time setup**: Run `/sync-vault --full` to index entire vault
2. **After offline work**: Sync when reconnecting after working without Git
3. **After git pull**: Sync changes from other devices
4. **Troubleshooting**: Verify memory is up-to-date with `--dry-run` first
5. **Force rebuild**: Use `--full` flag to re-index everything
6. **After bulk changes**: Triage, reorganization, mass edits

### Automatic Sync (Future):

⚠️ **Not yet implemented**: Automatic sync via Git post-commit hook

**Planned**: Memory systems update automatically every 5 minutes when Git commits changes

**For now**: Run `/sync-vault` manually after making changes

## Integration with Memory Systems

### Graph Memory (`mcp3_*`)

**Creates/Updates**:
- Entities: People, Projects, Locations, Tasks, Ideas, Strategies
- Relations: reports_to, assigned_to, located_at, aligns_with, etc.
- Observations: Key facts extracted from content

**Deletes**:
- Entities when files are deleted
- Relations when entities are removed

### Basic Memory (`mcp__basic-memory__*`)

**Indexes**:
- Full markdown content for semantic search
- Metadata for filtering
- Tags, dates, assignees for queries

**Removes**:
- Documents when files are deleted
- Updates when files are modified

## Best Practices

1. **Sync after major changes** - Triage, bulk edits, reorganization
2. **Use --dry-run first** - Preview changes before syncing
3. **Full sync periodically** - Monthly full re-index for consistency
4. **Commit before sync** - Ensure Git is up-to-date
5. **Check output** - Verify entities created/updated match expectations

## Error Handling

**If sync fails**:
1. Check Git status: `git status`
2. Verify checkpoint file exists: `.vault-sync-checkpoint`
3. Try dry run: `/sync-vault --dry-run`
4. Force full sync: `/sync-vault --full`
5. Check MCP server connections (Graph Memory, Basic Memory)

**Common issues**:
- Checkpoint file missing → Run `--full` to create
- Git not initialized → Initialize Git first
- MCP servers disconnected → Restart Windsurf
- Malformed markdown → Fix syntax errors in files

## Technical Details

**Git commands used**:
```bash
# Standard sync
git diff --name-status <checkpoint> HEAD

# Full sync
git ls-files people/ projects/ tasks/ Schedule/ strategy/ system/ IDEAS/ Operations/ reference/places/

# Get current commit
git rev-parse HEAD
```

**Memory API calls**:
- `mcp3_create_entities()` - Batch create Graph Memory entities
- `mcp3_create_relations()` - Batch create relations
- `mcp3_delete_entities()` - Remove deleted entities
- Basic Memory auto-indexes via file watcher (if configured)

## Compatibility

**Works with**:
- ✅ Windsurf (this implementation)
- ✅ Claude Code CLI (shared checkpoint file)
- ✅ Obsidian (reads same markdown files)

**Shared state**:
- `.vault-sync-checkpoint` - Used by all tools
- Graph Memory storage - Shared between Windsurf and Claude Code
- Basic Memory storage - Shared between Windsurf and Claude Code

**No conflicts**: Each tool can run `/sync-vault` independently
