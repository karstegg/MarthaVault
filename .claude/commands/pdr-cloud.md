# /pdr-cloud $ARGUMENTS

Trigger fully autonomous cloud-based daily production report processing.

## Usage
`/pdr-cloud YYYY-MM-DD` - Process WhatsApp messages for specified date in the cloud
`/pdr-cloud today` - Process today's messages  
`/pdr-cloud yesterday` - Process yesterday's messages

## Process Flow
1. **Validate Date**: Parse and validate date format
2. **Trigger GitHub Actions**: Send repository dispatch with date payload
3. **WhatsApp Extraction**: GitHub Actions extracts messages from Codespace
4. **Issue Creation**: Create processing issue with @claude mention
5. **Claude Processing**: Claude processes reports and creates PR
6. **Auto-Validation**: Validate file structure and content
7. **Auto-Merge**: Merge PR after successful validation
8. **Auto-Close**: Close issue with processing summary
9. **Complete Autonomy**: No manual intervention required

## Implementation

### Date Processing
```bash
# Parse date argument
TARGET_DATE="$1"

# Handle relative dates
case "$TARGET_DATE" in
    "today")
        TARGET_DATE=$(date +%Y-%m-%d)
        ;;
    "yesterday")
        TARGET_DATE=$(date -d "yesterday" +%Y-%m-%d)
        ;;
    "")
        echo "❌ Error: Date required"
        echo "Usage: /pdr-cloud YYYY-MM-DD|today|yesterday"
        exit 1
        ;;
esac

# Validate date format
if ! [[ "$TARGET_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "❌ Error: Invalid date format. Use YYYY-MM-DD"
    exit 1
fi
```

### GitHub Repository Dispatch
```bash
echo "🚀 Triggering autonomous cloud processing for $TARGET_DATE..."

# Send repository dispatch to trigger GitHub Actions
gh api repos/karstegg/MarthaVault/dispatches \
  --method POST \
  --field event_type="pdr-cloud" \
  --field client_payload="{\"date\":\"$TARGET_DATE\"}"

if [ $? -eq 0 ]; then
    echo "📡 Repository dispatch sent successfully"
    echo "⏳ GitHub Actions workflow starting..."
    echo "🔗 Monitor progress: https://github.com/karstegg/MarthaVault/actions"
    echo ""
    echo "Expected workflow:"
    echo "  1. Extract WhatsApp messages from Codespace"
    echo "  2. Create processing issue with @claude mention"  
    echo "  3. Claude processes reports and creates PR"
    echo "  4. Auto-validate and auto-merge PR"
    echo "  5. Auto-close issue with summary"
    echo ""
    echo "✅ Autonomous processing initiated for $TARGET_DATE"
    echo "📋 Files will be available after 'git pull' once complete"
else
    echo "❌ Error: Failed to trigger GitHub Actions"
    echo "Check authentication: gh auth status"
    exit 1
fi
```

### Progress Monitoring (Optional)
```bash
# Optional: Monitor workflow progress
echo "🔄 Monitoring workflow progress..."

# Wait a moment for workflow to start
sleep 5

# Get latest workflow run
LATEST_RUN=$(gh run list --workflow="cloud-pdr-processing.yml" --limit=1 --json databaseId --jq '.[0].databaseId')

if [ -n "$LATEST_RUN" ]; then
    echo "📊 Workflow run ID: $LATEST_RUN"
    echo "👀 Use 'gh run watch $LATEST_RUN' to monitor in real-time"
else
    echo "ℹ️  Workflow starting - check GitHub Actions page for progress"
fi
```

## Auto-Processing Features

### WhatsApp Data Extraction
- Connects to Codespace: `cuddly-guacamole-496vp6p46wg39r`
- Queries SQLite database for production messages
- Filters by date range and content keywords
- Extracts full message content for processing

### Claude Processing
- Creates issue with extracted WhatsApp data
- @claude mention triggers processing
- Follows exact /pdr-single workflow logic
- Uses Report Templates for standardized formatting
- Creates both JSON and Markdown files

### Auto-Validation
- Validates file structure: `daily_production/data/YYYY-MM/DD/`
- Checks minimum file count (JSON + Markdown)
- Verifies file sizes are reasonable
- Confirms proper naming conventions

### Auto-Merge
- Merges PR after successful validation
- Uses squash merge with descriptive commit message
- Deletes feature branch automatically
- Updates master branch with processed reports

### Auto-Push to Local
- Automatically triggers local repository sync
- Sends repository dispatch to auto-sync workflow
- Files automatically appear in local repository
- Only affects new/changed files, preserves local work

### Auto-Close
- Closes processing issue with success summary
- Includes processing statistics and file count
- Provides completion confirmation
- Maintains full audit trail

## Error Handling
- **Invalid Date**: Shows usage and exits
- **Network Issues**: Reports authentication problems
- **Processing Failures**: Workflow handles gracefully
- **Validation Failures**: Prevents auto-merge, keeps issue open

## Expected Output
```
🚀 Triggering autonomous cloud processing for 2025-08-13...
📡 Repository dispatch sent successfully
⏳ GitHub Actions workflow starting...
🔗 Monitor progress: https://github.com/karstegg/MarthaVault/actions

Expected workflow:
  1. Extract WhatsApp messages from Codespace
  2. Create processing issue with @claude mention
  3. Claude processes reports and creates PR
  4. Auto-validate and auto-merge PR
  5. Auto-close issue with summary
  6. Auto-push files to local repository

✅ Autonomous processing initiated for 2025-08-13
📋 Files will automatically appear in your local repository

🔄 Monitoring workflow progress...
📊 Workflow run ID: 16925678901
👀 Use 'gh run watch 16925678901' to monitor in real-time
```

## Integration
- Works with existing WhatsApp MCP Codespace setup
- Uses proven GitHub Actions + Codespace integration
- Follows established Report Templates and folder structure
- Maintains compatibility with local /pdr-single workflow

#daily-production #cloud-processing #automation #autonomous #github-actions #whatsapp #year/2025