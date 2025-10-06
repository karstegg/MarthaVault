# Test: Graph Memory Persistence

**Date:** 2025-10-06
**Purpose:** Verify that Graph Memory persists across MCP server restarts

---

## Configuration Applied

Updated `~/.mcp.json` with persistent storage:

```json
"memory": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-memory"],
  "env": {
    "MEMORY_FILE_PATH": "C:/Users/10064957/.martha/memory.json"
  }
}
```

**Storage Location:** `C:/Users/10064957/.martha/memory.json`

---

## Test Plan

### Phase 1: Pre-Restart Test
1. Create test entity in Graph Memory
2. Create test relation
3. Verify entity can be retrieved

### Phase 2: Restart Test
1. Restart Claude Code (reloads MCP servers)
2. Query for test entity
3. Verify persistence

### Phase 3: File Verification
1. Check `C:/Users/10064957/.martha/memory.json` exists
2. Verify JSON structure contains entities
3. Confirm incremental updates work

---

## Test Execution

**Next Steps:**
1. **RESTART CLAUDE CODE** to reload MCP configuration with new env variable
2. After restart, create test entity and verify persistence
3. Update architecture decision document based on results

---

## Expected Outcome

✅ Graph Memory should persist entities and relations to JSON file
✅ Memory should survive MCP server restarts
✅ Phase 2-6 roadmap can proceed without custom memory server

---

## Rollback Plan

If persistence doesn't work:
- Revert to original `~/.mcp.json` configuration
- Reconsider Custom Martha Memory Server (Option 1 from architecture decision doc)
