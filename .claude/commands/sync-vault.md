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

2. Get current HEAD commit SHA:
   ```bash
   git rev-parse HEAD
   ```

3. Get changed files:

   **Standard sync (no --full):**
   ```bash
   # Read checkpoint
   checkpoint=$(cat .vault-sync-checkpoint 2>/dev/null || echo "")

   # Get changes since checkpoint
   if [ -n "$checkpoint" ]; then
       git diff --name-status $checkpoint HEAD
   else
       # No checkpoint - do full sync
       git ls-files
   fi
   ```

   **Full sync (--full flag):**
   ```bash
   # Get all tracked files
   git ls-files
   ```

4. Filter to relevant folders:
   - `people/`
   - `projects/`
   - `tasks/`
   - `Schedule/`
   - `strategy/`
   - `system/`
   - `IDEAS/`
   - `Operations/`
   - `reference/places/`

5. Group files by change type:
   - A (Added) or new files in --full mode
   - M (Modified)
   - D (Deleted)

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

1. **Update checkpoint file:**
   ```bash
   echo "<current-HEAD-sha>" > .vault-sync-checkpoint
   ```

2. **Calculate and display summary:**
   ```
   🔄 Memory systems synchronized

   Last sync: <checkpoint-date> (commit <short-sha>)
   Current:   <current-date> (commit <short-sha>)

   Changed files (<total> files):
     ✅ Added (<count>)
     ✅ Modified (<count>)
     ✅ Deleted (<count>)

   Memory operations:
     - Graph Memory: <N> entities created/updated, <M> relations
     - Basic Memory: <N> documents indexed

   ✅ Sync complete
   Checkpoint updated: <current-HEAD-sha>
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

- **Batch operations**: Process up to 10 entities at once in create_entities calls
- **Parallel reads**: Read multiple files in parallel when possible
- **Skip unchanged**: If file content hash matches previous sync, skip processing
- **Target**: Complete typical sync (1-10 files) in <5 seconds

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
