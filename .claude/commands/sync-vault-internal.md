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
   - Extract metadata: title, front-matter, wikilinks, tags
   - Create Graph Memory entities using `mcp__memory__create_entities`
   - Create relations using `mcp__memory__create_relations`
   - Write to Basic Memory using `mcp__basic-memory__write_note`

3. **Process MODIFIED files (M)**:
   - Search Graph Memory for entities with file path in observations
   - If found: Delete old entities with `mcp__memory__delete_entities`
   - Read current file content
   - Create new entities (same as Added logic)
   - Update Basic Memory (write_note overwrites existing)

4. **Process DELETED files (D)**:
   - Search Graph Memory for entities with file path
   - Delete entities and relations with `mcp__memory__delete_entities`
   - Delete from Basic Memory using `mcp__basic-memory__delete_note`

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
