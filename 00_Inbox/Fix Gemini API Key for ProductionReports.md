# Fix Gemini API Key for ProductionReports Repository

**Status**: Outstanding Task
**Priority**: Medium
**Created**: 2025-10-06

## Problem

The `/pdr-gemini` workflow in **ProductionReports** repository is failing with:
```
Error: Please set an Auth method... GEMINI_API_KEY
```

**Workflow Run**: https://github.com/karstegg/ProductionReports/actions/runs/18270911678

## Root Cause

When we split MarthaVault into two repositories:
- **MarthaVault**: Productivity workspace (WhatsApp bridge, general tools)
- **ProductionReports**: Mining production data reports

The **GEMINI_API_KEY secret** exists in MarthaVault but was never added to ProductionReports.

## Architecture Context

**Data Flow**:
```
WhatsApp Bridge (MarthaVault Codespace)
    ↓ SSH extract data
Gemini Workflow (ProductionReports repo) ← NEEDS GEMINI_API_KEY
    ↓ generate reports
ProductionReports Repository
    ↓ git pull
ProductionData Local Directory
```

**Why This Works**:
- WhatsApp bridge stays in MarthaVault (no duplication)
- Workflow in ProductionReports connects via SSH to extract data
- Reports commit to ProductionReports repo
- Each repo needs its own copy of secrets

## Solution Steps

### 1. Get Gemini API Key
- Go to: https://aistudio.google.com/app/apikey
- Sign in with Google account
- Copy existing API key OR create new one if needed

### 2. Add Secret to ProductionReports
1. Navigate to: https://github.com/karstegg/ProductionReports/settings/secrets/actions
2. Click **"New repository secret"**
3. Name: `GEMINI_API_KEY`
4. Value: [Paste API key from step 1]
5. Click **"Add secret"**

### 3. Verify Secret Is Set
Run this to check (won't show value, just confirms existence):
```bash
gh secret list --repo karstegg/ProductionReports
```

Should show:
```
GEMINI_API_KEY    Updated YYYY-MM-DD
PAT_WITH_CODESPACE    Updated YYYY-MM-DD
```

### 4. Test Workflow
After adding secret, retry the workflow:
```bash
/pdr-gemini 2025-10-02
```

Or manually trigger:
```bash
cd "C:\Users\10064957\My Drive\GDVault\ProductionData"
gh workflow run gemini-pdr-processing.yml --field date="2025-10-02"
```

## Files Updated (Completed 2025-10-06)

✅ Workflow renamed: `gemini-quick-test.yml` → `gemini-pdr-processing.yml`
✅ `/pdr-gemini` command updated with:
- Correct repo URLs (MarthaVault → ProductionReports)
- Correct local paths (MarthaVault → ProductionData)
- Bridge health check documentation
- Early exit logic documentation

**Pending Commit**:
- Workflow rename
- Command documentation updates

## Why Gemini Workflow Matters

**Cost Savings**: FREE Gemini 2.5 Flash vs. PAID Claude API
- Gemini: $0/day, $0/year
- Claude: ~$0.39/day, $142+/year

**Processing Quality**: Claude-quality comprehensive reports using templates

**Features**:
- Bridge health check + auto-restart
- Early exit if no data found
- Equipment validation
- Load target integration
- Source validation for all data

## Notes

After fixing this, the ProductionReports repo will have full autonomous daily production report processing using FREE Gemini AI.

---

#task #outstanding #gemini #api-key #production-reports #year/2025
