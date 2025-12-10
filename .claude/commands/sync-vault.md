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

### Step 1: Parse Arguments and Get Changed Files

1. Parse command flags:
   - `--full`: Full vault re-index (ignore checkpoint)
   - `--dry-run`: Show what would sync without executing
   - `--verbose`: Show detailed processing

2. Get checkpoint timestamp:
   ```bash
   checkpoint=$(cat .vault-sync-checkpoint 2>/dev/null || echo "")
   ```

3. Get changed files using **TWO methods in parallel**:

   **Method A: Git committed changes (git diff)**
   ```bash
   current_head=$(git rev-parse HEAD)

   if [ -n "$checkpoint" ] && git rev-parse --verify "$checkpoint" >/dev/null 2>&1; then
       # Checkpoint is a valid commit SHA
       git diff --name-status $checkpoint HEAD
   else
       # Invalid/missing checkpoint - use timestamp method only
       echo ""
   fi
   ```

   **Method B: File modification time (for uncommitted changes)**
   ```bash
   # Get last sync timestamp from checkpoint file modification time
   if [ -f ".vault-sync-checkpoint" ]; then
       checkpoint_date=$(stat -c %y .vault-sync-checkpoint 2>/dev/null || stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" .vault-sync-checkpoint)
   else
       checkpoint_date="1970-01-01"
   fi

   # Find all modified files since checkpoint using filesystem timestamps
   find people projects tasks Schedule strategy system IDEAS Operations reference/places \
     -type f -name "*.md" -newermt "$checkpoint_date" 2>/dev/null
   ```

   **Full sync (--full flag):**
   ```bash
   # Get all markdown files in relevant folders
   find people projects tasks Schedule strategy system IDEAS Operations reference/places \
     -type f -name "*.md" 2>/dev/null
   ```

4. **Merge both file lists** (deduplicate):
   - Combine git diff output + find output
   - Remove duplicates
   - Mark each file as Added (A), Modified (M), or new (N)

5. Filter to relevant folders:
   - `people/`
   - `projects/`
   - `tasks/`
   - `Schedule/`
   - `strategy/`
   - `system/`
   - `IDEAS/`
   - `Operations/`
   - `reference/places/`

6. Group files by change type:
   - A (Added) - new files from git
   - M (Modified) - changed files from git or filesystem
   - D (Deleted) - deleted from git diff
   - N (New uncommitted) - found by find but not in git

**If --dry-run flag:** Print file list and exit (don't continue to Step 2)

---

### Step 2: Process Changed Files and Update Memory Systems

For each changed file, execute the appropriate memory operations:

#### Process ADDED Files (A)

For each added file:

1. **Read file content** using Read tool
2. **Extract metadata:**
   - Title from frontmatter or first H1
   - Tags from frontmatter
   - Wikilinks `[[Person Name]]`
   - Entity type based on folder:
     - `people/*.md` → Personnel
     - `projects/*/*.md` → Project
     - `Schedule/*.md` → Business Process
     - `strategy/*.md` → Strategy
     - `tasks/master_task_list.md` → Task
     - `IDEAS/*.md` → Idea
     - `reference/places/*.md` → Location
     - `system/*.md` → System Enhancement

3. **Create Graph Memory entity:**
   ```
   Use mcp__memory__create_entities with:
   - name: extracted title
   - entityType: determined from path
   - observations: array of key facts from content (5-10 observations)
   ```

4. **Create relations** if wikilinks found:
   ```
   Use mcp__memory__create_relations for each [[Person]] or [[Project]] link
   ```

5. **Index in Basic Memory:**
   ```
   Use mcp__basic-memory__write_note with:
   - title: extracted title
   - content: full markdown content
   - folder: derived from file path (e.g., "projects/Capital/Project Name")
   - tags: extracted from frontmatter (comma-separated string)
   - project: "main"
   ```

#### Process MODIFIED Files (M)

For each modified file:

1. **Read updated file content** using Read tool
2. **Extract metadata** (same as Added files)
3. **Update Graph Memory:**
   ```
   a. Search for existing entity by name using mcp__memory__search_nodes
   b. If found:
      - Delete old entity with mcp__memory__delete_entities
      - Create new entity with mcp__memory__create_entities (updated observations)
      - Create updated relations with mcp__memory__create_relations
   c. If not found: Create new entity (file was added outside Git)
   ```

4. **Re-index in Basic Memory:**
   ```
   Use mcp__basic-memory__write_note (overwrites existing document)
   - Same parameters as Added files
   ```

#### Process DELETED Files (D)

For each deleted file:

1. **Extract entity name** from file path
2. **Delete from Graph Memory:**
   ```
   a. Search for entity using mcp__memory__search_nodes
   b. If found: Delete with mcp__memory__delete_entities
   ```

3. **Delete from Basic Memory:**
   ```
   Use mcp__basic-memory__delete_note with identifier from permalink
   ```

---

### Step 3: Update Checkpoint and Report Summary

1. **Update checkpoint file with current timestamp:**
   ```bash
   # Write current ISO-8601 timestamp
   date -Iseconds > .vault-sync-checkpoint
   ```

2. **Calculate and display summary:**
   ```
   🔄 Vault sync complete

   Last sync: <checkpoint-timestamp>
   Current:   <current-timestamp>
   Gap: <N> days

   Changed files (<total> files):
     ✅ Added: <count>
     ✅ Modified: <count>
     ✅ Deleted: <count>

   Memory operations:
     - Graph Memory: <N> entities created/updated, <M> relations
     - Basic Memory: <P> documents indexed

   ✅ Sync complete
   Checkpoint updated: <current-timestamp>
   ```

3. **If gap > 7 days:** Display warning
   ```
   ⚠️  WARNING: 16-day gap detected since last sync
   Memory systems may be significantly out of date.
   Consider running /sync-vault more frequently.
   ```

---

## Metadata Extraction Guide

### People Files (people/*.md)

Extract:
- **Name**: From filename or frontmatter title
- **Role**: From "Role::" or "## Role" section
- **Email**: From "Email:" or contact section
- **Wikilinks**: All [[Project]] and [[Person]] references
- **Observations**: Role, responsibilities, current projects, reporting structure

### Project Files (projects/*/*.md)

Extract:
- **Name**: From title or filename
- **Type**: Project, Decision, or Business Process
- **Status**: From frontmatter Status field
- **Priority**: From frontmatter Priority field
- **Wikilinks**: [[Person]] assignees, [[Location]] sites
- **Observations**: Scope, budget, timeline, status, next steps, key decisions

### Schedule Files (Schedule/*.md)

Extract:
- **Event name**: From title
- **Date/Time**: From frontmatter date, startTime, endTime
- **Type**: Meeting, event, or recurring process
- **Attendees**: [[Person]] links in content
- **Observations**: Meeting purpose, decisions, action items

### Strategy Files (strategy/*.md)

Extract:
- **Name**: Strategy or initiative name
- **Type**: Strategy entity
- **Objectives**: Key goals and targets
- **Observations**: Strategic priorities, objectives, weights, timelines

---

## Error Handling

- **File read errors**: Log warning, skip file, continue processing
- **Memory API errors**: Log error, continue with remaining files
- **Missing checkpoint**: Treat as first sync (process all files as Added)
- **Git command errors**: Report error and exit gracefully

**Error log location:** `.vault-sync.log`

---

## Performance Considerations

### Batch Processing Strategy

**For large syncs (20+ files):**

1. **Read files in batches of 5-10** using parallel Read tool calls
2. **Extract all metadata** from each batch before moving to next
3. **Create entities in batches of 10** using single `create_entities` call
4. **Create relations in batches of 20** using single `create_relations` call
5. **Index Basic Memory sequentially** (one write_note at a time to avoid conflicts)

**Example batch workflow for 66 files:**
```
Batch 1 (files 1-10):
  - Read 10 files in parallel
  - Extract entities/observations
  - create_entities (10 entities)
  - create_relations (up to 20 relations)
  - write_note × 10

Batch 2 (files 11-20):
  - Repeat...
```

### Optimization Rules

- **Parallel reads**: Use parallel Read calls when files are independent
- **Batch API calls**: Always batch create_entities/create_relations (max 10 per call)
- **Sequential writes**: Basic Memory write_note calls must be sequential
- **Skip unchanged**: If file modification time matches checkpoint exactly, skip
- **Target performance**:
  - Small sync (1-10 files): <10 seconds
  - Medium sync (11-50 files): <60 seconds
  - Large sync (50+ files): <3 minutes

---

## When to Use

**Manual sync needed for:**
- First-time setup: Run `/sync-vault --full` to index entire vault
- After manual file edits outside Obsidian
- After git pull from other devices
- Troubleshooting: Verify memory is up-to-date
- Force rebuild: Use `--full` flag to re-index everything

**Automatic sync**: Memory systems update automatically via Git post-commit hook.

---

## Examples

```bash
# Standard sync (changes since last checkpoint)
/sync-vault

# Full vault re-index
/sync-vault --full

# Preview changes without executing
/sync-vault --dry-run

# Detailed processing logs
/sync-vault --verbose

# Combine flags
/sync-vault --full --verbose
```
