# Monitor Autonomous System Test

## How to Watch the Test in Action

### 1. Create the Test Issue
Copy content from `test-autonomous-trigger.md` and create a new GitHub Issue with:
- **Title**: `🤖 Autonomous Process WhatsApp Reports: 2025-08-09`
- **Labels**: `autonomous-processing`, `daily-production`, `priority-high`

### 2. Monitor GitHub Actions
**URL**: `https://github.com/karstegg/MarthaVault/actions`

**Look for**:
- ✅ Workflow: "🤖 Claude Orchestrated WhatsApp Report Processing"
- ✅ Status: Running → Success
- ✅ Logs show: "Found active Codespace", "Executing WhatsApp report processing"

### 3. Check Codespace Activity
If you have Codespace access:
```bash
# Monitor processing logs
tail -f /tmp/whatsapp-processing.log

# Check if processing script is running
ps aux | grep codespace-direct-processing

# Monitor git activity
git log --oneline -5
```

### 4. Watch for File Creation
**Expected location**: `daily_production/data/2025-08/09/`

**Files that should appear**:
- `2025-08-09_gloria.json` + `2025-08-09 - Gloria Daily Report.md`
- `2025-08-09_nchwaning3.json` + `2025-08-09 - Nchwaning 3 Daily Report.md`
- `2025-08-09_shafts-winders.json` + `2025-08-09 - Shafts & Winders Daily Report.md`

### 5. Monitor Git Commits
**URL**: `https://github.com/karstegg/MarthaVault/commits/master`

**Look for**: New commit with message containing:
- "🤖 Process daily production reports via Codespace MCP"
- "Report Date: 2025-08-09"
- "Autonomous processing from Codespace complete"

### 6. Watch for Review Issue Creation
**URL**: `https://github.com/karstegg/MarthaVault/issues`

**Look for**: New issue titled:
- "🤖 Claude Review Required: 2025-08-09 Reports"
- Labels: `claude-review`, `daily-production`, `autonomous`

### 7. Monitor Claude Review Process
The review issue should get:
- ✅ Claude's automated review comment
- ✅ Either "APPROVED" or "CHANGES REQUESTED" 
- ✅ Auto-close if approved
- ✅ Labels updated based on review result

## Success Timeline (Expected ~5-8 minutes)

```
T+0:00 → Issue created
T+0:30 → GitHub Actions starts
T+1:00 → Codespace SSH connection established  
T+1:30 → WhatsApp MCP data extraction begins
T+2:30 → Gemini processing starts
T+4:00 → Files created and committed
T+4:30 → Review issue created
T+5:00 → Claude review begins
T+6:00 → Review completed and approved
T+6:30 → Original issue auto-closes
T+7:00 → Process complete ✅
```

## Troubleshooting

### If GitHub Actions Fails:
- Check if Codespace is running and accessible
- Verify GITHUB_TOKEN secret is configured in Codespace
- Look for "No active Codespace found" error

### If Codespace Execution Fails:
- Check WhatsApp MCP server is running: `pgrep -f whatsapp-mcp`
- Verify processing script exists: `ls -la .devcontainer/codespace-direct-processing.py`
- Check Python dependencies are installed

### If No Files Created:
- Look at processing logs in Codespace
- Check if Gemini CLI is working: `gemini --version`
- Verify GEMINI_API_KEY is configured

### If Claude Review Doesn't Trigger:
- Check if review issue was created
- Look for "claude-review" label on the issue
- Verify workflow `.github/workflows/claude-review-orchestrated-results.yml` exists

## Manual Fallback Commands

If autonomous system fails, run manually in Codespace:
```bash
# Direct processing
python3 .devcontainer/codespace-direct-processing.py 2025-08-09

# Check system status  
python3 .devcontainer/autonomous-system-status.py

# Create trigger manually
python3 .devcontainer/claude-orchestration-trigger.py 2025-08-09 high
```

**Ready to test the full autonomous workflow!** 🎯