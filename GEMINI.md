# GEMINI.md - Daily Production Report Processing Configuration
*Version 4.0 - ✅ **BREAKTHROUGH ACHIEVED** (2025-08-24)*

## 🚀 **GEMINI 2.5 FLASH PRODUCTION BREAKTHROUGH**

### **✅ COMPLETE SUCCESS STATUS**
**Production-ready autonomous daily production report generation using FREE Gemini 2.5 Flash**

- **Cost Impact**: $0/day (complete replacement for expensive Claude API)
- **Processing Capability**: End-to-end WhatsApp → JSON/Markdown → Repository automation  
- **Quality**: Enterprise-grade data integrity with perfect validation
- **Status**: Fully operational with 8 files generated for July 17, 2025 test

### **🔑 Critical Technical Solution** 
After extensive investigation, the breakthrough was achieved with this exact configuration:

```yaml
# GitHub Actions Workflow: .github/workflows/gemini-quick-test.yml
uses: 'google-github-actions/run-gemini-cli@v0.1.11'  # CRITICAL: v0.1.11 not @v0
with:
  gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
  settings: |-  # CRITICAL: Model must be in settings, NOT gemini_model parameter
    {
      "model": "gemini-2.5-flash",           # FREE model with generous quotas
      "maxSessionTurns": 15,                 # CRITICAL: 15 not 5 for multi-site processing
      "autoAccept": ["list_directory", "read_file", "write_file", "glob"],
      "telemetry": {"enabled": false}
    }
```

### **💡 Key Technical Discoveries**
1. **Model Selection**: Use `settings.model` NOT `gemini_model` parameter (unsupported)
2. **GitHub Action Version**: `@v0.1.11` required for proper tool support (NOT `@v0`)
3. **Session Capacity**: 15 turns needed for complete multi-site processing (NOT 5)
4. **File Persistence**: Auto-commit workflow step required for repository visibility
5. **Data Integrity**: System properly uses `null` for missing data instead of fabrication

### **🎯 Current Production Usage**
```bash
# Trigger autonomous processing for any date
gh workflow run gemini-quick-test.yml --field date=2025-07-17

# Result: Complete JSON + Markdown files automatically created and committed
# Processing time: ~2.5 minutes end-to-end
# Output: 8 files total (4 JSON + 4 Markdown) for all mine sites
```

### **📊 Proven Results (July 17, 2025 Test)**
- ✅ **All 4 mine sites processed**: Gloria, Nchwaning 2, Nchwaning 3, Shafts & Winders
- ✅ **Perfect data integrity**: Nchwaning 3 properly showed "no report" with null values
- ✅ **457 lines of content** generated and committed automatically
- ✅ **Zero rate limiting issues** with Gemini 2.5 Flash free quotas
- ✅ **Files visible locally** after automatic git pull

**📖 Complete Technical Documentation**: See `GEMINI_2.5_FLASH_BREAKTHROUGH_COMPLETE_SOLUTION.md` for the full journey and solution details.

---

## Repository Context

**Project**: MarthaVault - Mining Operations Production Report Automation
**Organization**: Assmang - Black Rock Operations  
**Location**: Northern Cape, South Africa

## Processing Objective

Transform raw WhatsApp production messages into:
1. **JSON files**: Structured data for analysis and querying
2. **Markdown files**: Human-readable reports with analysis and insights

## Mine Sites & Engineers

- **Gloria Mine**: Engineer [[Sipho Dubazane]]
- **Nchwaning 2**: Engineer [[Sikelela Nzuza]] (returned from leave)
- **Nchwaning 3**: Engineer [[Sello Sease]]  
- **Shafts & Winders**: Engineer [[Xavier Peterson]] (infrastructure focus)

## Report Processing Instructions

### Data Extraction Rules
1. **NEVER INVENT DATA** - Extract only actual values from source WhatsApp messages
2. **Source validation required** - Every data point must be traceable to source
3. **Missing data protocol** - Use `null` for unavailable data, do not fabricate
4. **Confidence levels** - Assign HIGH/MEDIUM/LOW confidence to extracted values

### File Structure Requirements

**Target Directory**: `daily_production/data/YYYY-MM/DD/`

**Expected Output Files**:
```
daily_production/data/2025-07-12/
├── 2025-07-12_gloria.json
├── 2025-07-12 – Gloria Daily Report.md
├── 2025-07-12_nchwaning2.json
├── 2025-07-12 – Nchwaning 2 Daily Report.md
├── 2025-07-12_nchwaning3.json
├── 2025-07-12 – Nchwaning 3 Daily Report.md
├── 2025-07-12_shafts_winders.json
└── 2025-07-12 – Shafts & Winders Daily Report.md
```

## JSON Schema Template

```json
{
  "report_metadata": {
    "date": "YYYY-MM-DD",
    "data_date": "YYYY-MM-DD",
    "site": "Site Name",
    "engineer": "Engineer Name", 
    "timestamp": "HH:MM",
    "report_type": "Daily Report"
  },
  "safety": {
    "status": "clear|incidents",
    "incidents": 0,
    "details": []
  },
  "production": {
    "rom": {"actual": 0, "target": 0, "variance": 0, "variance_percentage": 0},
    "decline": {"actual": 0, "target": 0, "variance": 0, "variance_percentage": 0},
    "product": {"actual": 0, "target": 0, "variance": 0, "variance_percentage": 0},
    "loads": [{"shift": "day|afternoon|night", "load_number": 1, "truckloads_tipped": 0, "target": null}],
    "blast": {"faces": null, "breakdown": null, "note": "Description or 'Nothing Reported'"}
  },
  "equipment_availability": {
    "tmm": {"DT": 0, "FL": 0, "HD": 0, "RT": 0, "SR": 0},
    "specialized": [{"code": "UV|GD|DZ|LD", "availability": 0}]
  },
  "shift_readiness": {
    "production_tmm": {
      "DT": {"available": 0, "total": 0}, "FL": {"available": 0, "total": 0},
      "HD": {"available": 0, "total": 0}, "RT": {"available": 0, "total": 0}, "SR": {"available": 0, "total": 0}
    }
  },
  "breakdowns": {"current_breakdowns": [{"unit": "Equipment Code", "issue": "Description"}]},
  "operational": {"main_fans": "operational|issues", "plant_blockages": 0, "fire_alarms": 0},
  "source_validation": {
    "field_name": {
      "value": "extracted_value", "source_line": "line_number_from_whatsapp_data",
      "source_quote": "exact_text_from_source", "confidence": "HIGH|MEDIUM|LOW"
    }
  }
}
```

## Markdown Report Template

```markdown
---
JSONData:: [[YYYY-MM-DD_site.json]]
---

# Site Daily Report
**Date**: Report Date (Data from Previous Day)  
**Engineer**: [[Engineer Name]]  
**Site**: Site Name  

## Safety Status
✅ **Status** - Description

## Production Performance
| Metric | Actual | Target | Variance | Performance |
|--------|--------|--------|----------|-------------|
| **ROM** | 0t | 0t | 0t | **0% (0% variance)** 🟢/⚠️/🔴 |
| **Decline** | 0t | 0t | 0t | **0% (0% variance)** 🟢/⚠️/🔴 |
| **Product** | 0t | 0t | 0t | **0% (0% variance)** 🟢/⚠️/🔴 |

### Equipment Status
| Equipment | Availability | Status |
|-----------|-------------|---------|
| **DT** | **0%** | 🟢/⚠️/🔴 Assessment |
| **FL** | **0%** | 🟢/⚠️/🔴 Assessment |

### Critical Issues
1. **🔴 URGENT**: Description
2. **⚠️ MEDIUM**: Description

---
*Report processed: Processing Date | Data period: Data Date | Source: WhatsApp HH:MM*

#daily-production #site-tag #engineer-tag #year/2025
```

## Equipment Code Reference

### TMM (Trackless Mobile Machinery)
- **DT**: Dump Truck
- **FL**: Front-end Loader  
- **HD**: Hydraulic Drill
- **RT**: Roof Bolter
- **SR**: Scraper

### Specialized Equipment
- **UV**: Utility Vehicle
- **GD**: Grader (often written as GR - correction needed)
- **DZ**: Dozer
- **LD**: Light Delivery Vehicle

## Performance Indicators

### Status Icons
- 🟢 Good performance (>90%)
- ⚠️ Needs attention (70-90%)  
- 🔴 Critical issues (<70%)

### Priority Levels
- **🔴 URGENT**: Production shortfalls >20%, safety incidents, critical equipment failures
- **⚠️ MEDIUM**: Equipment breakdowns, moderate performance issues
- **📊 FOLLOW-UP**: Trends, optimization opportunities

## Data Quality Requirements

1. **Source Traceability**: Every data point must reference source line and quote
2. **Confidence Assessment**: HIGH for clear numbers, MEDIUM for interpreted, LOW for unclear
3. **Null Handling**: Use `null` for missing data, never fabricate
4. **Mathematical Accuracy**: Verify calculations and variance percentages
5. **Consistency**: Maintain uniform formatting and structure

## Success Criteria

- **Complete file pairs**: Each site must have both JSON and Markdown files
- **Accurate data extraction**: All numbers traceable to source
- **Professional formatting**: Consistent, readable reports
- **Proper file organization**: Correct directory structure
- **Source validation**: All data points properly validated
