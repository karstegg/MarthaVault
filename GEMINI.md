# GEMINI.md - Daily Production Report Processing Configuration
*Version 3.0 - GitHub Actions Integration (2025-08-16)*

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
