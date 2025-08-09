# 🤖 Gemini CLI GitHub Actions - Quick Setup Guide

## Overview
This guide provides step-by-step instructions to set up the automated WhatsApp production report processing using Gemini CLI GitHub Actions.

## 🚀 Quick Start (5 minutes)

### Step 1: Configure API Key
1. **Get Gemini API Key**:
   - Visit: https://aistudio.google.com/app/apikey
   - Create new API key
   - Copy the key

2. **Add to GitHub Secrets**:
   - Go to: https://github.com/karstegg/MarthaVault/settings/secrets/actions
   - Click "New repository secret"
   - Name: `GOOGLE_AI_API_KEY`
   - Value: [paste your API key]
   - Click "Add secret"

### Step 2: Validate Setup
Run the validation script:
```powershell
.\scripts\validate-gemini-setup.ps1 -ValidateSecrets -GenerateMockData
```

### Step 3: Test Workflow
1. Go to: https://github.com/karstegg/MarthaVault/actions
2. Select "Process WhatsApp Production Reports"
3. Click "Run workflow"
4. Configure:
   - **Date**: Leave empty (uses today)
   - **Site Filter**: Select "nchwaning3" (has BEV equipment)
   - **Force Reprocess**: Check ✅
5. Click "Run workflow"

### Step 4: Review Results
- Check workflow run status in Actions tab
- Review generated pull request
- Validate file structure in `daily_production/`

## 📁 Files Created

This setup creates these key files:

### GitHub Actions Workflow
```
.github/workflows/process-whatsapp-reports.yml
```
- **Triggers**: Daily 7:30 AM SAST + manual
- **Features**: Parallel site processing, automatic PR creation
- **Output**: Structured JSON + readable Markdown reports

### Setup Documentation
```
GEMINI_CLI_SETUP.md
```
- Complete setup instructions
- Architecture overview
- Troubleshooting guide

### Validation Script
```
scripts/validate-gemini-setup.ps1
```
- Setup validation
- Mock data generation
- Health checks

## 🎯 What This Achieves

### Automated Processing
- **Daily Reports**: Automatic processing at 7:30 AM SAST
- **Parallel Sites**: All 4 sites processed simultaneously
- **Structured Output**: JSON database + human-readable reports
- **Quality Control**: Automatic validation and review workflow

### Data Standards Compliance
- **CLAUDE.md Compliance**: Follows all Section 10.1 requirements
- **Dating Rule**: Report date (when received) vs data date (operations)
- **Equipment Validation**: Cross-referenced against fleet database
- **BEV Analysis**: Battery vs diesel equipment classification

### Integration Ready
- **WhatsApp MCP**: Framework ready for SQLite database connection
- **Claude Review**: Automatic PR creation for validation
- **Scalable**: Handle increasing report volume
- **Auditable**: Complete GitHub Actions logs

## 🔧 Current Status

### ✅ Working Now
- GitHub Actions workflow structure
- Parallel site processing logic  
- Mock data generation for testing
- Pull request automation
- Equipment database integration
- CLAUDE.md format compliance

### 🚧 Next Phase (Production Ready)
- WhatsApp MCP database connection
- Real message extraction from group chat `27834418149-1537194373@g.us`
- Production data processing
- Error handling and recovery
- Claude integration for automated review

## 🧪 Testing with Mock Data

The validation script generates realistic test data:

```powershell
# Generate mock reports for all sites
.\scripts\validate-gemini-setup.ps1 -GenerateMockData

# Files created:
# daily_production/data/2025-08-09_nchwaning2.json
# daily_production/data/2025-08-09_nchwaning3.json
# daily_production/data/2025-08-09_gloria.json
# daily_production/data/2025-08-09_shafts-winders.json
#
# daily_production/2025-08-09 – Nchwaning2 Mock Report.md
# daily_production/2025-08-09 – Nchwaning3 Mock Report.md
# daily_production/2025-08-09 – Gloria Mock Report.md
# daily_production/2025-08-09 – Shafts-winders Mock Report.md
```

## 📊 Expected Workflow Output

Each workflow run generates:

### JSON Database Files
```json
{
  "metadata": {
    "report_date": "2025-08-09",
    "data_date": "2025-08-08", 
    "site": "nchwaning3",
    "engineer": "Sello Sease",
    "source": "WhatsApp Group Chat"
  },
  "safety": { "status": "GREEN", "incidents": [] },
  "production": { "rom_tonnes": 1250, "loads_hauled": 84 },
  "equipment": {
    "availability_percent": 87.5,
    "bev_analysis": {
      "bev_units_available": 6,
      "diesel_units_available": 8
    }
  },
  "source_validation": {
    "rom_tonnes": {
      "value": 1250,
      "source_quote": "ROM: 1250t yesterday",
      "confidence": "HIGH"
    }
  }
}
```

### Markdown Reports
```markdown
---
Status:: #status/new
Priority:: #priority/medium
Assignee:: [[Sello Sease]]
JSONData:: [[daily_production/data/2025-08-09_nchwaning3.json]]
---

# Nchwaning3 Daily Production Report
**Date**: 2025-08-09 | **Engineer**: [[Sello Sease]] | **Site**: Nchwaning3

## Executive Summary
Production on track with 87.5% equipment availability. BEV fleet showing strong performance.

## Safety Status
- **Status**: GREEN
- **Incidents**: None reported
- **Safety Meetings**: Conducted as scheduled

## Production Performance
- **ROM Tonnes**: 1,250t (+5% vs target)
- **Product Tonnes**: 1,180t
- **Loads Hauled**: 84 loads
- **Equipment Availability**: 87.5%

## BEV vs Diesel Analysis
- **BEV Units Available**: 6/7 dump trucks, 5/6 front loaders
- **Diesel Units Available**: 8/9 dump trucks, 4/5 front loaders
- **BEV Performance**: 91% availability vs 84% diesel

## Source Validation
All data points verified against WhatsApp messages with HIGH confidence.

#daily-report #nchwaning3 #year/2025 #sello-sease
```

### Pull Request Creation
Each workflow automatically creates a pull request with:
- **Title**: "🤖 Daily Production Reports - YYYY-MM-DD"
- **Body**: Complete processing summary, file manifest, validation requirements
- **Reviewers**: @karstegg assigned for Claude review
- **Labels**: `daily-reports`, `automation`, `gemini-cli`

## 🔍 Monitoring and Maintenance

### Daily Monitoring
1. **Check GitHub Actions**: Verify 7:30 AM SAST runs complete successfully
2. **Review Pull Requests**: Validate generated reports for data accuracy
3. **Monitor API Usage**: Track Gemini API quota consumption

### Weekly Health Checks
```powershell
# Run full validation
.\scripts\validate-gemini-setup.ps1 -ValidateSecrets -TestMode

# Check for missing reports
Get-ChildItem "daily_production\data" -Filter "*.json" | 
    Group-Object { $_.Name.Split('_')[0] } | 
    Where-Object { $_.Count -lt 4 }
```

### Monthly Maintenance
- Review equipment database for new additions
- Update engineer assignments if personnel changes
- Validate WhatsApp group chat access
- Check GitHub Actions quota usage

## 🚨 Troubleshooting

### Common Issues

**Workflow fails to start**:
```bash
# Check secrets configuration
gh secret list

# Verify workflow syntax
gh workflow list
```

**No reports detected**:
- Verify WhatsApp group chat ID: `27834418149-1537194373@g.us`
- Check message timestamp filtering
- Confirm engineer name mapping

**Data validation errors**:
- Review equipment codes against fleet database
- Check BEV classification for Nchwaning 3
- Validate source quotes and confidence scores

**Pull request creation fails**:
- Check repository permissions
- Verify GitHub token scope
- Review branch protection rules

### Error Recovery
```powershell
# Reprocess specific date/site
gh workflow run "Process WhatsApp Production Reports" \
  --field date="2025-08-09" \
  --field site_filter="nchwaning3" \
  --field force_reprocess="true"

# Generate manual test data
.\scripts\validate-gemini-setup.ps1 -GenerateMockData
```

## 🔮 Future Enhancements

### Phase 2: Production Integration
- **WhatsApp MCP Connection**: Direct SQLite database access
- **Real-time Processing**: Message webhooks for immediate processing
- **Advanced Analytics**: Trend analysis and predictive insights
- **Alert System**: Automatic notifications for critical issues

### Phase 3: Advanced Features
- **Multi-language Support**: Afrikaans and local language processing
- **Voice Message Processing**: Audio transcription and analysis
- **Image Analysis**: Equipment photos and diagram interpretation
- **Integration Expansion**: Connect to SCADA, ERP, and maintenance systems

## 📞 Support and Contact

### Documentation
- **CLAUDE.md**: Complete vault constitution and standards
- **GEMINI_CLI_SETUP.md**: Detailed technical setup guide
- **WORKFLOWS.md**: GitHub Actions integration patterns

### Validation Tools
- **validate-gemini-setup.ps1**: Complete setup validation
- **GitHub Actions Logs**: Full execution traces
- **Equipment Database**: Fleet validation and BEV classification

### Key Personnel
- **Greg Karsten**: Senior Production Engineer (Repository Owner)
- **GitHub Actions**: Automated processing coordination
- **Claude Review Agent**: Data validation and quality control

---

## ✅ Ready to Deploy!

Your Gemini CLI GitHub Actions setup is ready for testing and gradual production deployment. The automation framework provides:

- **Immediate Value**: Structured daily reports with consistent formatting
- **Scalable Architecture**: Handle increasing report volume automatically  
- **Quality Assurance**: Built-in validation and review processes
- **Future Ready**: Framework for WhatsApp MCP integration

Start with the validation script, test the workflow manually, then enable daily automation once you're satisfied with the results.

**Next Step**: Run `.\scripts\validate-gemini-setup.ps1 -ValidateSecrets -GenerateMockData` to begin testing! 🚀
