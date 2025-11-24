# Task Handoff Executor

## Description
Execute file operations specified in the task handoff communication file from Claude Desktop.

## Behavior
1. Read `reference/claude-code/task-handoff.md`
2. Parse the Actions Required section
3. Execute all file operations (create dirs, move files, rename, etc)
4. Update the CCLI Response section with:
   - Status of each operation
   - Any errors encountered
   - Final verification (file counts, confirmations)
5. Set status to `completed` or `failed`

## Usage
```
/task-handoff
```

## Implementation Notes
- Check if task status is `pending` before executing
- Update status to `in-progress` at start
- Provide detailed response for Claude Desktop to read
- Handle errors gracefully and report them
- Verify operations completed successfully before marking complete
