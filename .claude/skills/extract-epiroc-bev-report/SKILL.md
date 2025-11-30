---
name: "Extract Epiroc BEV Weekly Report"
description: "Extract key sections from Epiroc BRMO BEV weekly PDF reports into structured markdown format for Week N"
---

# Extract Epiroc BEV Weekly Report

## When to Use This Skill

Use this skill when you need to extract and organize information from Epiroc weekly service reports for Black Rock Mine Operations (BRMO). The skill automatically:
- Extracts General Summary text
- Compiles BEV daily exceptions (only equipment with delays/breakdowns)
- Extracts Planned Work section with maintenance schedule
- Extracts Battery and Charger Status Report with all tables
- Captures Battery Overheat Report
- Includes all Critical Issues summaries

This skill is essential for weekly mining operations reporting when you have a new Epiroc report PDF.

## Usage

### Using Claude Code Slash Command

```bash
/extract-epiroc-bev-report --week=16
/extract-epiroc-bev-report --site=brmo --week=16
```

### Using Command Line

```bash
python extract_epiroc_bev_report.py --week=16
python extract_epiroc_bev_report.py --week 16
python extract_epiroc_bev_report.py 16
```

### Arguments

- `--week=N` or `--week N` or positional `N`: The week number (required)
- `--site=brmo`: Site name (optional, defaults to "brmo")

## Prerequisites

- Epiroc PDF report must be in `Week N/` directory
- Expected filename pattern: `BRMO weekly report LIVE [date].pdf`
- Week directory must exist
- Claude Code's native PDF reading capability (used automatically)

## Data Extraction

The script extracts these sections from the Epiroc PDF:

1. **General Summary** - Purpose and overview text
2. **BEV Daily Exceptions** - Only equipment with reported delays/breakdowns organized by day
3. **Planned Work** - Activities for coming week including maintenance schedule table
4. **Battery and Charger Status Report** - Complete battery inventory with status
5. **Battery Overheat Report** - Overheat incidents summary
6. **Critical Issues** - All critical issues from BEV, CAS L9, and Certiq & Mobilaris sections

## Extraction Logic - What to Include vs Exclude

### General Summary
**INCLUDE:** Extract the exact text from the General Summary section describing Epiroc activities at BRMO

### BEV Weekly Machine Utilization - Daily Exceptions
**CRITICAL FILTERING RULE:** Extract ONLY equipment entries that have actual delays or breakdowns reported. Exclude equipment with no issues.

**INCLUDE:**
- Equipment with failure reasons (electrical, mechanical, tyre bay work, 3rd party faults, etc.)
- Any equipment entry that includes problem description and duration
- Example: `FL 108 - Morning shift: 3rd party supplier fault – Strata. (1H39min)` ✓

**EXCLUDE:**
- Equipment entries with only a dash (no problems reported)
- Example: `FL 98 -` ✗
- Example: `DT 146 -` ✗

**Daily Organization:** List exceptions by day (Saturday, Sunday, Monday, etc.) and only show days that have equipment with issues

**Format:**
```
### [Day Date Year]:
- **EQUIPMENT_ID** - Problem description with duration
```

### Planned Work for Coming Week
**INCLUDE:**
- All bullet points describing planned activities
- The Maintenance Schedule table showing equipment service schedule

**TABLE FORMAT:** Extract as markdown table with columns for each day (Monday-Friday) and equipment IDs

### Battery and Charger Status Report
**INCLUDE:**
- General summary section (ST14-B4 battery packs, MT42-B5 battery packs, 160 kW Chargers info)
- The complete "Table 1: Battery pack availability" with all rows showing: Battery Type, Battery ID, Status, Comment

**TABLE COLUMNS:**
| Battery Type | Battery ID | Status | Comment |
|---|---|---|---|

**Status values:** Working, Breakdown, Surface (preserve exactly as shown)

### Battery Overheat Report
**INCLUDE:**
- Any battery overheat incidents listed
- If no incidents: "- No battery overheating for the week."

**FORMAT:**
```
- [Incident description or "No battery overheating for the week."]
```

### Critical Issues Summary
**INCLUDE ALL THREE SECTIONS:**
1. BEV - Critical Issues Summary
2. CAS L9 Implementation - Critical Issues Summary
3. Certiq & Mobilaris - Critical Issues Summary

Extract all bullet points from each section exactly as written

## Output Files

- **Location**: `Week N/Epiroc_BEV_Weekly_Report_WeekN_Extracted.md`
- **Format**: Markdown with organized sections and tables
- **Content**: Structured extraction ready for inclusion in weekly reports

## CSV Structure & Content

*Not applicable - this skill produces markdown output, not CSV files*

## Example Outputs

### Sample BEV Daily Exceptions - Week 16 (what to extract and what to exclude):

**Saturday 11 October 2025 - Full equipment list in PDF:**
```
1. FL 98 -                          ← EXCLUDE (no issues)
2. FL 99 -                          ← EXCLUDE (no issues)
3. FL 107 -                         ← EXCLUDE (no issues)
4. FL 108 - Morning shift: 3rd party supplier fault – Strata. (1H39min)  ← INCLUDE
5. FL 112 - Morning shift: Electrical breakdown – Grease system not working. (50min) ← INCLUDE
6. FL 113 –                         ← EXCLUDE (no issues)
7. DT 146 -                         ← EXCLUDE (no issues)
...
```

**Extracted output for Saturday:**
```
### Saturday 11 October 2025:
- **FL 108** - Morning shift: 3rd party supplier fault – Strata. (1H39min)
- **FL 112** - Morning shift: Electrical breakdown – Grease system not working. (50min)
```

**Sunday 12 October 2025 - Full list:**
```
1. FL 98 -                          ← EXCLUDE
2. FL 99 -                          ← EXCLUDE
...
7. DT 146 - Morning shift: Electrical breakdown: 24V – Aircon fault, changed evaporator fan. (3H29min) ← INCLUDE
...
```

**Extracted output for Sunday:**
```
### Sunday 12 October 2025:
- **DT 146** - Morning shift: Electrical breakdown: 24V – Aircon fault, changed evaporator fan. (3H29min)
```

### Sample Battery Table:
```
| Battery Type | Battery ID | Status | Comment |
|---|---|---|---|
| B4 - ST14 | VPY-00011 | Working | |
| B4 - ST14 | VPY-00088 | Breakdown | TMS/Subpack/VCB connector. |
```

### Sample Maintenance Schedule:
```
| Monday 20-Oct-25 | Tuesday 21-Oct-25 | Wednesday 22-Oct-25 | Thursday 23-Oct-25 | Friday 24-Oct-25 |
|---|---|---|---|---|
| DT0160 | DT0131 | DT0147 | DT0154 | DT0148 |
```

## Validation Checks

The skill performs these quality checks:
- PDF file exists in Week N directory
- PDF contains expected sections (BEV Report, Battery sections, etc.)
- Extract contains at least one daily exception entry
- Output markdown is properly formatted
- Battery table has correct columns and data types

## Common Issues & Troubleshooting

**PDF file not found:**
- Ensure the Epiroc PDF exists in the `Week N/` directory
- Check filename matches pattern: `BRMO weekly report LIVE [date].pdf`
- Verify week number is correct

**No data extracted:**
- PDF may be corrupted or in unexpected format
- Check that PDF contains standard Epiroc report sections
- Verify PDF is not password-protected

**Missing sections:**
- Some weeks may not have all sections (e.g., no battery overheat incidents)
- Script handles missing sections gracefully with "No X for the week" entries
- Check source PDF for actual data availability

**Table formatting issues:**
- Markdown tables may display incorrectly if cell content contains pipes (|)
- Script escapes pipes automatically
- Open markdown in proper viewer if display issues occur

## Next Steps After Extraction

1. Review the generated markdown file for accuracy
2. Copy relevant sections into your weekly report template
3. Cross-reference equipment IDs with site-specific equipment lists
4. Verify battery pack statuses match physical inventory
5. Integrate critical issues into weekly operations summary
6. Archive the extraction for historical reference
