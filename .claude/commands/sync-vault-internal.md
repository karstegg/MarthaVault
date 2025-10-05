Internal memory sync command - processes Git diff output from temp file.

**IMPORTANT**: This command is called by the Git post-commit hook. It should run quickly (<3 seconds for typical changes) and handle errors gracefully.

## Input

Read from `.sync-temp-input.txt` file in repo root. Format:
```
A  people/New Person.md
M  projects/BEV/update.md
D  00_inbox/old.md
```

Each line: `<change-type> <tab> <file-path>`
- `A` = Added
- `M` = Modified
- `D` = Deleted

## Processing Logic

### 1. Read Input
```
Read .sync-temp-input.txt
Parse each line into (changeType, filePath)
Group by change type: added[], modified[], deleted[]
```

### 2. Process Added Files (A)

For each added file:
- Read file content
- Determine entity type from path:
  - `people/*.md` → Personnel entity
  - `projects/*/*.md` → Project/Decision entity
  - `Schedule/*.md` → Business Process/Event entity
  - `strategy/*.md` → Strategy entity
- Extract key information (front-matter, wikilinks, tags)
- Create Graph Memory entity with observations
- Create relations (reports_to, assigned_to, located_at, aligns_with)
- Write to Basic Memory

### 3. Process Modified Files (M)

For each modified file:
- Use **replace strategy**:
  1. Search Graph Memory for entities with file path in observations
  2. If found: Delete old entities
  3. Read current file content
  4. Create new entities (same as Added logic)
  5. Re-index in Basic Memory (overwrites)

### 4. Process Deleted Files (D)

For each deleted file:
- Search Graph Memory for entities with file path in observations
- Delete entities and their relations
- Delete from Basic Memory

### 5. Batch Operations

- Use `mcp__memory__create_entities` (plural) for multiple entities
- Use `mcp__memory__create_relations` (plural) for multiple relations
- Process independent files in parallel where possible

### 6. Output

Print summary to console:
```
Memory sync complete:
- 3 files processed
- 2 added (4 entities created, 6 relations)
- 1 modified (2 entities updated)
- 0 deleted
```

## Error Handling

- Log errors but continue processing remaining files
- Return exit code 0 if all succeeded
- Return exit code 1 if any errors occurred
- Append details to `.vault-sync.log`

## Performance Targets

- <1 second for 1-3 files
- <3 seconds for 5-10 files
- <10 seconds for 20+ files

## Example Execution

Input file `.sync-temp-input.txt`:
```
A  people/Jane Doe.md
M  projects/BEV/2025-10-05 – Fire Safety Update.md
```

Processing:
1. Read Jane Doe.md → Create Personnel entity "Jane Doe"
2. Create relations (reports_to, stationed_at)
3. Index in Basic Memory
4. Read BEV fire safety file → Delete old "Fire Safety Update" entity
5. Create new entity from current content
6. Re-index in Basic Memory

Output:
```
Memory sync complete:
- 2 files processed
- 1 added (1 entity created, 2 relations)
- 1 modified (1 entity updated)
```
