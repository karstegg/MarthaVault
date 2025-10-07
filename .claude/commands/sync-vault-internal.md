# /sync-vault-internal

**IMPORTANT**: This is an internal command called by the Git post-commit hook. Execute quickly and handle errors gracefully.

## Instructions

1. **Read input file** `.sync-temp-input.txt` in repo root
   - Format: `<change-type><tab><file-path>` (one per line)
   - Change types: A (added), M (modified), D (deleted)
   - Parse and group by change type

2. **Process ADDED files (A)**:
   - Read file content
   - Determine entity type from path:
     - `people/*.md` → Personnel entity
     - `projects/*/*.md` → Project/Decision entity
     - `Schedule/*.md` → Business Process entity
     - `strategy/*.md` → Strategy entity
     - `tasks/*.md` → Task entity (only master_task_list.md)
     - `IDEAS/*.md` → Idea entity
     - `reference/places/*.md` → Location entity
   - Extract metadata: title, front-matter, wikilinks, tags, role, email, etc.
   - **Graph Memory**: Create entities using `mcp__memory__create_entities` and relations using `mcp__memory__create_relations`
   - **Basic Memory**: Index document using `mcp__basic-memory__write_note` (project="main", folder from path, tags from front-matter)

3. **Process MODIFIED files (M)**:
   - Read updated file content
   - **Graph Memory**:
     - Search for entities with file path using `mcp__memory__search_nodes`
     - If found: Delete old entity with `mcp__memory__delete_entities`, then create new (ensures observations are current)
     - Create updated relations
   - **Basic Memory**: Re-index using `mcp__basic-memory__write_note` (overwrites existing)

4. **Process DELETED files (D)**:
   - Extract entity name from file path
   - **Graph Memory**:
     - Search for entity using `mcp__memory__search_nodes`
     - Delete with `mcp__memory__delete_entities` (relations auto-deleted)
   - **Basic Memory**: Delete using `mcp__basic-memory__delete_note`

5. **Output summary**:
   ```
   Memory sync complete:
   - X files processed
   - Y added (N entities, M relations)
   - Z modified (N entities updated)
   - W deleted
   ```

6. **Error handling**:
   - Log errors to `.vault-sync.log` but continue processing
   - Return success even if some files fail (graceful degradation)

## Performance Target
- <3 seconds for typical changes (1-10 files)
