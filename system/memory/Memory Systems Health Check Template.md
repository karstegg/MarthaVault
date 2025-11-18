---
Status: Active
Priority: High
Assignee:
- - Karsten
  - Gregory
Tags: null
permalink: system/memory/memory-systems-health-check-template
---

# Memory Systems Health Check Template

## Purpose
Systematic verification that all three memory layers (Native, Graph, Basic) are properly synced and operational. Run this after major batch updates or when memory seems stale.

## When to Run This Check
- After Monday triage sessions (bulk file processing)
- After major task status update batches
- When Claude seems to lack recent context
- Monthly maintenance check (1st Monday of month)
- After any memory system configuration changes

## Pre-Check Information Gathering
Record these before starting:
- **Date/Time**: 
- **Trigger**: (What prompted this check?)
- **Last major update**: (When was last big batch of changes?)
- **Expected changes to verify**: (What should be reflected?)

---

## Test Sequence

### Test 1: Native Memory (Conversational Recall)
**Objective**: Verify short-term context retention

**Method**: Ask Claude conversationally about recent work
```
"What did we work on yesterday?"
"What were the priorities from our last triage?"
"What's the status on [recent project/task]?"
```

**Expected Behavior**:
- ✅ Recalls last 24-48 hours of work
- ✅ Knows recent decisions and priority shifts
- ✅ Remembers current week's focus

**Red Flags**:
- ❌ Cannot recall yesterday's work
- ❌ Doesn't know about recent high-priority items
- ❌ Asks for context that was just discussed

**Troubleshooting**:
- If Native Memory gaps: Conversation may be too long, start new session
- Native Memory is session-based, doesn't persist across sessions

---

### Test 2: Basic Memory (File Watcher & Indexing)
**Objective**: Verify real-time vault file indexing

**Method**: Check file watcher status
```bash
# Read watch status
cat "C:\Users\10064957\My Drive\GDVault\MarthaVault\.basic-memory\watch-status.json"

# Check for recent file in vault
ls -lh "C:\Users\10064957\My Drive\GDVault\MarthaVault\tasks\master_task_list.md"
```

**Expected Behavior**:
- ✅ `"running": true`
- ✅ `"error_count": 0`
- ✅ `last_scan` timestamp within last 10 minutes
- ✅ `recent_events` showing recent file modifications
- ✅ Reasonable `synced_files` count (300-400 range)

**Red Flags**:
- ❌ `"running": false`
- ❌ `error_count > 0`
- ❌ `last_scan` > 1 hour old
- ❌ No recent_events for files you know changed
- ❌ `synced_files` drastically different from expected

**Troubleshooting**:
```bash
# Check if watcher process is running
ps aux | grep "watch"

# Restart watcher if needed (check .basic-memory documentation)

# Check for file permission issues
ls -la ".basic-memory/"

# Verify watch-status.json is writable
```

---

### Test 3: Graph Memory (Entity Relationships)
**Objective**: Verify strategic entity relationships (NOT detailed status)

**Method**: Search for recently mentioned entities
```
memory:search_nodes("recent project name")
memory:open_nodes(['Entity Name'])
```

**Expected Behavior**:
- ✅ Entities exist for major projects/people
- ✅ Relations show connections (Person→Project, Project→Strategy)
- ✅ Observations contain timestamped notes
- ⚠️ Status fields may lag (this is OK - observations are source of detail)

**IMPORTANT - These are NOT red flags**:
- ⚠️ Entity Status field not matching vault file status (Expected - use observations)
- ⚠️ Missing detailed task metadata (Expected - use Basic Memory for this)
- ⚠️ Observations more current than Status field (Expected behavior)

**Actual Red Flags**:
- ❌ Major entities completely missing (Person, Project)
- ❌ No observations at all (even old ones)
- ❌ Relations completely broken (everyone reports_to nobody)
- ❌ Empty graph or drastically reduced entity count

**Troubleshooting**:
- Missing entities: May need manual creation via memory tools
- Check if .martha/memory.json exists and is readable
- Verify Graph Memory MCP is configured in .mcp.json

---

### Test 4: Source of Truth Verification
**Objective**: Confirm vault files reflect recent work

**Method**: Read key vault files directly
```
Filesystem:read_text_file("C:\Users\10064957\My Drive\GDVault\MarthaVault\tasks\master_task_list.md")
```

**Expected Behavior**:
- ✅ Recent task completions marked with ✅ and today's date
- ✅ New tasks added from recent work
- ✅ Status updates reflected in file content
- ✅ File modification timestamps recent

**Red Flags**:
- ❌ No updates despite knowing work was done
- ❌ File timestamps old (>24 hours when work was recent)
- ❌ Missing expected tasks or completions

---

## Interpretation Guide

### Healthy System Indicators
1. **Native Memory**: Conversational recall of last 24-48 hours ✅
2. **Basic Memory**: Active file watching, last_scan <10 min, 0 errors ✅
3. **Graph Memory**: Entities exist with relations and observations ✅
4. **Vault Files**: Reflect recent work with current timestamps ✅

### Expected Behaviors (NOT Problems)
| Observation | Status | Explanation |
|-------------|--------|-------------|
| Graph Memory Status field lags vault file | ⚠️ Expected | Status details live in observations, entity Status is high-level summary |
| Native Memory lacks deep history | ⚠️ Expected | Native Memory is for recent context, use Graph/Basic for history |
| Graph Memory missing task details | ⚠️ Expected | Tasks tracked in vault files (Basic Memory), Graph tracks strategic entities |
| Basic Memory scan lag 5-10 min | ⚠️ Expected | File watcher polls periodically, not instant |

### Actual Problems (Require Action)
| Symptom | Severity | Action |
|---------|----------|--------|
| Basic Memory errors > 0 | 🔴 Critical | Check logs, file permissions, restart watcher |
| Last scan > 1 hour old | 🔴 Critical | Watcher crashed, check process and restart |
| Native Memory can't recall today | 🟡 Medium | Session too long, start fresh session |
| Graph Memory missing major entities | 🟡 Medium | Manual entity creation needed |
| Vault files unchanged despite work | 🔴 Critical | File system issue, check sync/permissions |

---

## Test Results Template

```markdown
## Health Check Results - [DATE]

**Trigger**: [Why running this check]
**Last Major Update**: [When]

### 1. Native Memory
- Status: ✅/⚠️/❌
- Can recall: [List what it remembers]
- Gaps: [Any missing context]

### 2. Basic Memory  
- Running: ✅/❌
- Last Scan: [timestamp]
- Error Count: [number]
- Synced Files: [count]
- Status: ✅/⚠️/❌

### 3. Graph Memory
- Entity Count: [number]
- Recent Entity: [name - to verify recency]
- Relations Working: ✅/❌
- Observations Present: ✅/❌
- Status: ✅/⚠️/❌

### 4. Vault Files
- master_task_list.md updated: ✅/❌
- Recent timestamp: [date/time]
- Expected changes present: ✅/❌
- Status: ✅/⚠️/❌

### Overall Assessment
- **System Health**: ✅ Healthy / ⚠️ Degraded / ❌ Critical
- **Issues Found**: [List or "None"]
- **Actions Needed**: [List or "None"]

### Notes
[Any additional observations or context]
```

---

## Remediation Procedures

### If Basic Memory File Watcher Failed
```bash
# Check watcher process
ps aux | grep watch

# Check error logs
cat .basic-memory/logs/watcher.log

# Restart watcher (example - check actual command in .basic-memory/README)
python .basic-memory/src/watcher.py restart

# Verify restart
cat .basic-memory/watch-status.json
```

### If Graph Memory Entities Missing
```
# Create missing entities
memory:create_entities({
  entities: [{
    name: "Entity Name",
    entityType: "Project|Person|Location|Strategy",
    observations: ["Key fact 1", "Key fact 2"]
  }]
})

# Verify creation
memory:search_nodes("Entity Name")
```

### If Native Memory Gaps Present
**Action**: Start fresh Claude Desktop session
- Native Memory doesn't persist across sessions
- Long conversations degrade context quality
- Fresh session = fresh Native Memory

### If Vault Files Stale
```bash
# Check file permissions
ls -la "path/to/file.md"

# Check Google Drive sync status
# (Look for sync icon in File Explorer)

# Verify file is writable
echo "test" >> "path/to/file.md"
```

---

## Maintenance Schedule

### Weekly (Every Monday)
- Quick health check during morning triage
- Verify Basic Memory watcher active
- Spot-check Native Memory recall

### Monthly (1st Monday)
- Full health check (all 4 tests)
- Document results using template above
- Archive results to `system/memory/health-checks/YYYY-MM.md`

### After Major Changes
- Memory system configuration changes
- MCP server updates
- Large batch processing (>50 files)
- System crashes or unexpected restarts

---

## Related Documentation
- [[system/memory/Memory Systems Architecture.md]] - Overall design
- [[system/memory/2025-11-18 – Memory Systems Health Check.md]] - Example completed check
- [[reference/claude-code/MCP Servers Configuration.md]] - MCP setup
- [[tasks/master_task_list.md]] - Primary source of truth for task status

---

**Template Version**: 1.0  
**Created**: 2025-11-18  
**Last Updated**: 2025-11-18  
**Owner**: [[Karsten, Gregory]]