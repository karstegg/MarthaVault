# Gemini CLI GitHub Actions Setup

## Overview
This document provides setup instructions for the WhatsApp production report automation using Gemini CLI GitHub Actions with 1M context window processing.

## Architecture
```
WhatsApp Group → MCP Bridge → SQLite → Gemini CLI → Structured Output → Claude Review
```

## Required Secrets

### GitHub Repository Secrets
Add these secrets in your repository settings (`Settings > Secrets and variables > Actions`):

1. **`GOOGLE_AI_API_KEY`** (Required)
   - Your Google AI API key for Gemini CLI
   - Get from: https://aistudio.google.com/app/apikey
   - Used for: Gemini CLI processing and analysis

2. **`WHATSAPP_MCP_CONFIG`** (Optional - for production)
   - WhatsApp MCP configuration if needed
   - Used for: Authentication with WhatsApp bridge

## Installation Steps

### 1. Enable GitHub Actions
Ensure GitHub Actions are enabled in your repository:
- Go to `Settings > Actions > General`
- Set "Actions permissions" to "Allow all actions and reusable workflows"

### 2. Configure Gemini CLI API Key
1. Visit https://aistudio.google.com/app/apikey
2. Create new API key
3. Copy the key
4. In your GitHub repo: `Settings > Secrets and variables > Actions`
5. Click "New repository secret"
6. Name: `GOOGLE_AI_API_KEY`
7. Value: [your API key]
8. Click "Add secret"

### 3. Test the Workflow
You can trigger the workflow manually to test:

1. Go to `Actions` tab in your GitHub repository
2. Select "Process WhatsApp Production Reports"
3. Click "Run workflow"
4. Configure options:
   - **Date**: Leave empty for today, or specify YYYY-MM-DD
   - **Site Filter**: Choose specific site or "all"
   - **Force Reprocess**: Check if you want to reprocess existing reports

## Workflow Features

### Automatic Scheduling
- **Runs daily at 7:30 AM SAST** (5:30 UTC)
- Processes previous day's reports automatically
- Creates pull request for Claude review

### Manual Triggering  
- **On-demand processing** via workflow dispatch
- **Site-specific filtering** (nchwaning2, nchwaning3, gloria, shafts-winders)
- **Date range selection** for historical processing
- **Force reprocessing** option for corrections

### Parallel Processing
The workflow automatically detects multiple sites and processes them in parallel:

- **Nchwaning 2**: Johan Kotze reports (diesel fleet focus)
- **Nchwaning 3**: Sello Sease reports (BEV testing site)
- **Gloria**: Sipho Dubazane reports (silo management)
- **Shafts & Winders**: Xavier Peterson reports (infrastructure)

### Output Structure
Each run generates:

**JSON Database Files**:
```
daily_production/data/YYYY-MM-DD_[site].json
```

**Readable Reports**:
```
daily_production/YYYY-MM-DD – [Site] Daily Report.md
```

**Pull Request**: Automatic PR creation for Claude review with:
- Complete file manifest
- Processing summary
- Validation requirements
- Review instructions

## Data Processing Standards

### Critical Dating Rule 🚨
**Files named with REPORT DATE (when received), NOT data date (operational period)**

Example:
- WhatsApp received July 10th → filename: `2025-07-10_site.json`
- Contains July 9th operations → documented in JSON as `data_date: 2025-07-09`

### Validation Requirements
Every processed report includes:
- **Source Validation**: Data points with source quotes and confidence levels
- **Equipment Cross-Reference**: Validation against fleet database
- **BEV Analysis**: Battery vs diesel equipment classification
- **Missing Data Protocol**: `null` values when data not in source (never fabricated)

### Equipment Integration
- **Standard Codes**: Cross-referenced against `equipment_codes.md`
- **Fleet Database**: BEV classification from `brmo_fleet_database.json`
- **Error Detection**: Common mistakes like GR→GD corrections

## Current Implementation Status

### ✅ Completed
- GitHub Actions workflow structure
- Parallel site processing logic
- Gemini CLI integration framework
- Output format compliance with CLAUDE.md
- Pull request automation
- Mock data generation for testing

### 🚧 Pending Implementation
- **WhatsApp MCP Database Connection**: Actual SQLite integration
- **Message Extraction**: Real WhatsApp group chat processing
- **Production Data**: Replace mock outputs with actual data
- **Error Handling**: Production-grade error recovery
- **Claude Integration**: Automated review triggering

## Testing the Setup

### 1. Run Test Workflow
```bash
# Trigger via GitHub Actions UI or:
gh workflow run "Process WhatsApp Production Reports" \
  --field date="2025-08-09" \
  --field site_filter="nchwaning3" \
  --field force_reprocess="true"
```

### 2. Verify Outputs
Check that the workflow:
- ✅ Creates proper directory structure
- ✅ Generates JSON and Markdown files
- ✅ Follows dating convention (report date not data date)
- ✅ Creates pull request for review
- ✅ Includes proper metadata and front-matter

### 3. Validate Structure
Generated files should match:
- **JSON Schema**: Structured data for analysis
- **Markdown Format**: Human-readable reports with proper front-matter
- **File Naming**: CLAUDE.md conventions
- **Equipment Validation**: Cross-referenced against fleet database

## WhatsApp MCP Integration

### Database Schema
The workflow expects access to WhatsApp MCP SQLite database with:

```sql
-- Messages table structure
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    chat_jid TEXT,           -- '27834418149-1537194373@g.us'
    sender TEXT,             -- Engineer name/phone
    content TEXT,            -- Message content
    timestamp DATETIME,      -- Message timestamp
    is_from_me BOOLEAN,      -- Direction flag
    media_type TEXT          -- Media attachments
);
```

### Query Patterns
The Gemini CLI uses these query patterns:

```sql
-- Recent production messages
SELECT timestamp, sender, content 
FROM messages 
WHERE chat_jid = '27834418149-1537194373@g.us' 
AND timestamp > datetime('now', '-24 hours')
ORDER BY timestamp DESC;

-- Specific date range
SELECT timestamp, sender, content 
FROM messages 
WHERE chat_jid = '27834418149-1537194373@g.us' 
AND date(timestamp) = '2025-08-09'
ORDER BY timestamp ASC;
```

### Engineer Detection
Maps WhatsApp senders to engineers:
- **Johan Kotze** → Nchwaning 2 reports
- **Sello Sease** → Nchwaning 3 reports  
- **Sipho Dubazane** → Gloria reports
- **Xavier Peterson** → Shafts & Winders reports

## Production Deployment

### 1. WhatsApp MCP Setup
```bash
# In GitHub Codespace or runner
cd /workspaces/MarthaVault/whatsapp-mcp-server
npm install
node whatsapp-bridge.js  # Maintain authenticated session
```

### 2. Database Access
```bash
# Verify database connectivity
sqlite3 /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db
.tables
.schema messages
SELECT COUNT(*) FROM messages WHERE chat_jid = '27834418149-1537194373@g.us';
```

### 3. Gemini CLI Configuration
```bash
# Install in GitHub Actions runner
curl -fsSL https://github.com/google-gemini/gemini-cli/releases/latest/download/gemini-cli-linux-x64 -o gemini
chmod +x gemini
sudo mv gemini /usr/local/bin/

# Configure with API key
export GOOGLE_AI_API_KEY=${{ secrets.GOOGLE_AI_API_KEY }}
gemini --version
```

## Monitoring and Maintenance

### GitHub Actions Monitoring
- **Workflow History**: Check Actions tab for run status
- **Artifact Storage**: 30-day retention for processed reports
- **PR Creation**: Automatic review assignment to @karstegg
- **Error Notifications**: Failed runs trigger alerts

### Data Quality Checks
- **Source Validation**: Every data point includes confidence score
- **Equipment Cross-Reference**: Automatic validation against fleet database
- **BEV Analysis**: Correct classification for Nchwaning 3
- **Dating Compliance**: Report date vs data date validation

### Troubleshooting
Common issues and solutions:

**Workflow fails to start**:
- Check GOOGLE_AI_API_KEY secret is set
- Verify Actions permissions are enabled
- Confirm workflow syntax is valid

**No reports detected**:
- Verify WhatsApp MCP database connectivity
- Check group chat ID: '27834418149-1537194373@g.us'
- Confirm message timestamp filtering

**Data validation errors**:
- Review equipment_codes.md for correct TMM codes
- Update fleet database if new equipment added
- Check engineer name mapping for site assignment

## Integration Benefits

### Automation Advantages
- **Free Processing**: Google AI API quotas for Gemini CLI
- **1M Context Window**: Comprehensive cross-site analysis
- **Parallel Processing**: Multiple sites simultaneously
- **Cloud Native**: No local dependencies or maintenance

### Data Quality Benefits
- **Consistent Processing**: Same logic applied to all sites
- **Source Traceability**: Every data point linked to WhatsApp message
- **Equipment Validation**: Automatic cross-referencing
- **BEV Analysis**: Specialized handling for battery equipment

### Operational Benefits
- **Daily Automation**: Reports processed without manual intervention
- **Pull Request Workflow**: Structured review process
- **Audit Trail**: Complete GitHub Actions execution logs
- **Scalable**: Handle increasing volume of reports

## Next Steps

1. **Configure API Key**: Add GOOGLE_AI_API_KEY to repository secrets
2. **Test Workflow**: Run manual trigger to verify setup
3. **Review Mock Output**: Validate file structure and naming conventions
4. **Plan WhatsApp Integration**: Prepare for production database connection
5. **Monitor Daily Runs**: Verify automated processing at 7:30 AM SAST

The Gemini CLI GitHub Actions workflow is ready for testing and gradual production deployment as WhatsApp MCP integration becomes available.
