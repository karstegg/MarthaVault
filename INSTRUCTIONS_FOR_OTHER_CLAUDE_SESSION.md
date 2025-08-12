# Instructions for Other Claude Session
**URGENT UPDATE**: WhatsApp MCP Architecture Changed

## 🚨 **CRITICAL CHANGES MADE**

### Previous Approach (BROKEN):
- ❌ Complex MCP server with JSON-RPC protocols
- ❌ Background service with STDIO communication issues  
- ❌ REST API endpoints that returned 404 errors
- ❌ UV/Python dependency management problems

### NEW Approach (WORKING):
- ✅ **Direct SQLite database access**
- ✅ **Simple SQL queries instead of MCP tools**
- ✅ **Real-time data capture proven working**
- ✅ **No complex protocols or services needed**

## 🏗️ **Current Working Architecture**

```
WhatsApp Web API ←→ Go Bridge ←→ SQLite Database ←→ Direct SQL Queries
                        ↓
                /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db
```

## ⚡ **Immediate Action Items for You:**

### 1. Update Your GitHub Actions Workflows:

**OLD (Don't Use)**:
```yaml
# Don't use MCP tools like this:
- uses: mcp-whatsapp-tools
- run: mcp_extract_messages()
```

**NEW (Use This)**:
```yaml
# Use direct SQLite queries:
- name: Extract WhatsApp Production Data
  run: |
    ssh codespace "cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge && sqlite3 store/messages.db \"SELECT timestamp, content FROM messages WHERE chat_jid = '27834418149-1537194373@g.us' AND timestamp LIKE '2025-08-12%' ORDER BY timestamp DESC LIMIT 10;\""
```

### 2. Update Your Scripts:

**Replace any MCP tool calls with direct SQL**:
```bash
# Instead of: mcp.call("list_messages", {...})
# Use: sqlite3 store/messages.db "SELECT * FROM messages WHERE ..."
```

### 3. Key Database Information:

**Database Location**: `/workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db`

**Table Structure**:
```sql
CREATE TABLE messages (
    id TEXT,
    chat_jid TEXT,
    sender TEXT,
    content TEXT,
    timestamp TIMESTAMP,
    is_from_me BOOLEAN,
    media_type TEXT,
    filename TEXT,
    url TEXT,
    PRIMARY KEY (id, chat_jid)
);
```

**Production Groups**:
- Main: `27834418149-1537194373@g.us` (Engineering discussions)
- N3 Active: `120363204285087803@g.us` (Live production reports)

## 🔧 **Essential Commands for You:**

### Check if Bridge is Running:
```bash
ssh codespace "ps aux | grep bridge"
```

### Start Bridge if Needed:
```bash
ssh codespace "cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge && nohup go run main.go > bridge.log 2>&1 &"
```

### Get Recent Production Messages:
```bash
ssh codespace "cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge && sqlite3 store/messages.db \"SELECT timestamp, substr(content, 1, 100) FROM messages WHERE content LIKE '%ROM%' OR content LIKE '%Product%' OR content LIKE '%Safety%' ORDER BY timestamp DESC LIMIT 5;\""
```

### Get Messages from Specific Date:
```bash
ssh codespace "cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge && sqlite3 store/messages.db \"SELECT timestamp, content FROM messages WHERE timestamp LIKE '2025-08-12%' ORDER BY timestamp DESC;\""
```

## 📊 **Data Format Examples:**

**Live Messages Coming In**:
```
2025-08-12 02:48:41+00:00|A test
2025-08-12 02:30:04+00:00|*South West Development* 11/08/2025 *Safety* Clear *Focus with exact 73w-41s...
2025-08-11 20:16:06+00:00|*Shift*: afternoon shift Date: 11/08/2025 *Safety*: Clear. *Total Faces Loaded=* 07...
```

**Production Report Content**:
- ROM tonnages: "ROM: 846 vs 0", "ROM: 1361 vs 0"  
- Equipment status: "DT: 6/6", "FL: 5/5", "HD: 4/4"
- Safety status: "Safety: Clear", "Safety: All clear"
- Time pattern: 4:00-6:00 AM SAST daily

## 🎯 **Your GitHub Actions Should Now:**

1. **SSH into Codespace** (existing method works)
2. **Query SQLite directly** (no MCP tools needed)
3. **Parse SQL results** (standard text processing)
4. **Process production data** (same as before)

## 📖 **Full Reference Documentation:**

- **Complete Setup Guide**: `WHATSAPP_MCP_COMPLETE_SETUP.md`
- **Claude Memory**: `CLAUDE.md` Section 13
- **Working Examples**: All committed to main branch

## ⚠️ **What NOT to Try:**

- Don't attempt to run MCP server as background service
- Don't use `uv run main.py` in workflows  
- Don't rely on REST API endpoints
- Don't try to fix JSON-RPC communication issues

## ✅ **Verification:**

The system is **LIVE and WORKING RIGHT NOW**:
- Bridge is authenticated and running
- Real-time messages flowing into SQLite
- Test message confirmed at 02:48:41 today
- Production reports coming in at 4:30 AM daily

**Just query the database directly - it's that simple!**

## 🔧 **GitHub Actions Bridge Management**

### **Bridge Startup Pattern for Workflows:**
```yaml
- name: Ensure Bridge is Running
  run: |
    gh codespace ssh -- "
      # Kill any zombie processes
      pkill bridge 2>/dev/null || true
      sleep 3
      
      # Check if bridge is already running
      if ps aux | grep -v grep | grep 'go run main.go' > /dev/null; then
        echo '✅ Bridge already running'
        exit 0
      fi
      
      # Start bridge in background
      cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge
      nohup go run main.go > bridge.log 2>&1 &
      
      # Wait for startup (critical - takes 15-30 seconds)
      sleep 15
      
      # Verify it started
      if ps aux | grep -v grep | grep 'go run main.go' > /dev/null; then
        echo '✅ Bridge started successfully'
        tail -5 bridge.log
      else
        echo '❌ Bridge failed to start'
        cat bridge.log
        exit 1
      fi
    "
```

### **Authentication Verification:**
```yaml
- name: Verify WhatsApp Authentication
  run: |
    gh codespace ssh -- "
      cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge
      
      # Check logs for authentication success
      if tail -20 bridge.log | grep -q 'Connected to WhatsApp'; then
        echo '✅ WhatsApp authenticated'
      else
        echo '❌ Authentication issue - check QR code needed'
        tail -20 bridge.log
        exit 1
      fi
    "
```

### **Database Health Check:**
```yaml
- name: Verify Database Access
  run: |
    gh codespace ssh -- "
      cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge
      
      # Check database and recent data
      if [ -f store/messages.db ]; then
        MESSAGE_COUNT=\$(sqlite3 store/messages.db 'SELECT COUNT(*) FROM messages;')
        LATEST_MSG=\$(sqlite3 store/messages.db 'SELECT timestamp FROM messages ORDER BY timestamp DESC LIMIT 1;')
        
        echo \"📊 Database: \$MESSAGE_COUNT messages\"
        echo \"🕐 Latest: \$LATEST_MSG\"
        
        # Verify recent data (within 24 hours)
        YESTERDAY=\$(date -d '1 day ago' '+%Y-%m-%d')
        RECENT_COUNT=\$(sqlite3 store/messages.db \"SELECT COUNT(*) FROM messages WHERE timestamp >= '\$YESTERDAY';\")
        
        if [ \$RECENT_COUNT -gt 0 ]; then
          echo \"✅ Recent messages: \$RECENT_COUNT\"
        else
          echo \"⚠️  No recent messages - bridge may need restart\"
        fi
      else
        echo '❌ Database not found'
        exit 1
      fi
    "
```

### **Complete Workflow Pattern:**
```yaml
jobs:
  process-reports:
    runs-on: ubuntu-latest
    steps:
    - name: Manage Codespace and Bridge
      env:
        GITHUB_TOKEN: ${{ secrets.GH_PAT }}
      run: |
        # 1. Ensure Codespace is active (SSH auto-starts it)
        gh codespace ssh --repo ${{ github.repository }} -- "echo 'Codespace active'" || {
          echo "Waiting for Codespace to start..."
          sleep 30
        }
        
        # 2. Ensure bridge is running (with retry logic)
        for i in {1..3}; do
          if gh codespace ssh --repo ${{ github.repository }} -- "
            cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge
            if ! ps aux | grep -v grep | grep 'go run main.go'; then
              pkill bridge 2>/dev/null || true
              sleep 3
              nohup go run main.go > bridge.log 2>&1 &
              sleep 15
            fi
            ps aux | grep -v grep | grep 'go run main.go'
          "; then
            echo "✅ Bridge confirmed running"
            break
          else
            echo "⚠️  Bridge attempt $i failed, retrying..."
            sleep 10
          fi
        done
        
        # 3. Extract data using direct SQLite
        gh codespace ssh --repo ${{ github.repository }} -- "
          cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge
          sqlite3 store/messages.db \"SELECT timestamp, content FROM messages WHERE timestamp LIKE '$(date +%Y-%m-%d)%' AND (content LIKE '%ROM%' OR content LIKE '%Product%' OR content LIKE '%Safety%') ORDER BY timestamp DESC;\"
        " > whatsapp_data.txt
```

### **Debug Commands for Troubleshooting:**
```bash
# Check bridge process
gh codespace ssh -- "ps aux | grep bridge"

# Check bridge logs  
gh codespace ssh -- "tail -20 /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/bridge.log"

# Test database access
gh codespace ssh -- "sqlite3 /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db 'SELECT COUNT(*) FROM messages;'"

# Manual bridge restart
gh codespace ssh -- "cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge && pkill bridge; sleep 3; nohup go run main.go > bridge.log 2>&1 &"
```

### **⚠️ Critical Timing Notes:**
- **Bridge startup takes 15-30 seconds** - always wait
- **Codespace auto-starts** when you SSH into it (if stopped)
- **Authentication persists ~20 days** - no QR code needed usually
- **Database is always live** - no sync delays

## 🚀 **Summary for You:**

**Old**: Complex MCP tools → Broken  
**New**: SSH + Direct SQLite queries → Working perfectly

**Key Pattern**: SSH into Codespace → Ensure bridge running → Query SQLite directly

Update your workflows to use this bridge management + SQLite pattern, and everything will work flawlessly.