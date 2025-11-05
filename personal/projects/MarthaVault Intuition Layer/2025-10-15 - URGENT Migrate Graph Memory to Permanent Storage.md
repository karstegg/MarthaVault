---
'Status:': null
'Priority:': High
'Assignee:': Greg
'DueDate:': 2025-10-20
'Tags:': null
permalink: personal/projects/martha-vault-intuition-layer/2025-10-15-urgent-migrate-graph-memory-to-permanent-storage
---

# ⚠️ URGENT: Migrate Graph Memory to Permanent Storage

## Problem
Graph Memory is currently stored in the npm package directory which will be **WIPED** if you update or reinstall the package:
```
C:\Users\10064957\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-memory\dist\memory.json
```

## Current Data at Risk
- **348 entities** including personnel, projects, workflows, regulations
- **92KB** of critical knowledge graph data
- Last modified: Oct 15, 2025

## Action Required
Migrate to permanent centralized storage at: `C:\Users\10064957\.martha\memory.json`

### Steps:
1. **Copy the data:**
   ```powershell
   copy "C:\Users\10064957\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-memory\dist\memory.json" "C:\Users\10064957\.martha\memory.json"
   ```

2. **Update Claude Code CLI config** (`C:\Users\10064957\.claude.json`):
   - Find the MarthaVault project section (line ~616)
   - Add env variable to memory server:
   ```json
   "memory": {
     "command": "npx",
     "args": ["-y", "@modelcontextprotocol/server-memory"],
     "env": {
       "MEMORY_FILE_PATH": "C:/Users/10064957/.martha/memory.json"
     }
   }
   ```

3. **Update Windsurf config** (`MarthaVault\.mcp.json`):
   - Change MEMORY_FILE_PATH to: `"C:/Users/10064957/.martha/memory.json"`

4. **Test both IDEs:**
   - Restart Claude Code CLI
   - Restart Windsurf
   - Verify memory persistence in both

## Why This Matters
- Running `npm update` will delete all Graph Memory data
- Centralized storage ensures persistence across package updates
- The `.martha` directory is the intended permanent location per architectural docs

## Reference
- Memory created: Oct 15, 2025
- Configuration documented in Windsurf memory system
- Related: MarthaVault MCP Memory Storage Configuration