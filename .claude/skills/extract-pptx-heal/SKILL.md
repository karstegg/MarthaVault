---
name: Extract HEAL Text from PowerPoint
description: Extract HEAL matrix content from PowerPoint slides and save as formatted text files matching N2 HEAL format
---

# Extract HEAL Text from PowerPoint

## When to Use This Skill

Use this skill to extract HEAL content (Highlights, Emerging Issues, Lowlights, Priorities, Actions) from PowerPoint presentations and save them as properly formatted text files. Works with both:
- **Table-based layouts** (Gloria, Shafts & Winders)
- **Section-based layouts** (future variations)

## Usage

### Via Slash Command (Recommended)

```bash
/extract-pptx-heal gloria 16
/extract-pptx-heal shafts-winders 16
/extract-pptx-heal n3 16
```

### Via CLI

```bash
python extract_pptx_heal.py gloria 16
python extract_pptx_heal.py shafts-winders 16
python extract_pptx_heal.py --site=gloria --week=16
```

## Arguments

- **site**: `gloria`, `shafts-winders`, or `n3` (required)
- **week**: Week number (e.g., 16) (required)

## Prerequisites

- Python 3.10+
- `python-pptx` library (already installed globally)
- PPTX file located in `Week {N}/` directory matching naming convention

## What This Skill Does

### Data Extraction

The script:
1. **Locates** the PPTX file in `Week {N}/` directory
2. **Parses** table and text structures to identify HEAL sections
3. **Extracts** content under each section header
4. **Organizes** items into standard HEAL categories:
   - Highlights
   - Lowlights
   - Emerging Issues
   - Priorities
   - Actions (if present)
5. **Formats** output with bullet points and section headings
6. **Validates** that content was successfully extracted

### Output Files

The script creates a single text file:

**Format**: `{Site} HEAL Page Week{N}.txt`

**Examples**:
- `Gloria HEAL Page Week16.txt`
- `Shafts and Winders HEAL Page Week16.txt`
- `N3 HEAL Page Week16.txt`

**Location**: `Week {N}/` directory (same as source PPTX)

## CSV Structure & Content

**File Format**: Plain text with line-numbered entries

**Structure**:
```
Highlights
• Item 1
• Item 2

Lowlights
• Item 1

Emerging Issues
• Item 1

Priorities
• Item 1
• Item 2

Actions
• Item 1
```

**Line Numbers**: Read tool displays automatically (e.g., "1→", "2→")

**Section Detection**:
- **Gloria**: 4x2 table layout (Highlights/Lowlights in left/right columns)
- **Shafts & Winders**: Separate tables per section with headers
- **N3**: Detected from file structure

## Site-Specific Data Locations

### Gloria
- **File**: `HEAL page (003).pptx - AutoRecovered.pptx` (or latest HEAL page PPTX)
- **Table Layout**: 4 rows x 2 columns
  - Row 0: Headers (Highlight | Lowlight)
  - Row 1: Content (Highlights left | Lowlights right)
  - Row 2: Headers (Emerging Issues | Priorities)
  - Row 3: Content (Emerging left | Priorities right)

### Shafts & Winders
- **File**: `SHAFTS AND WINDERS_HEAL_{N}_WEEK_*.pptx`
- **Table Layout**: Multiple single-cell tables, one per section
- **Sections**: Headers in first line (e.g., "Highlights:", "Emerging Issues:")

### N3
- **File**: `N3 HEAL Page*.pptx` (pending)
- **Note**: Currently outstanding; script will process when available

## Example Outputs

### Gloria Week 16
```
Highlights
• TMM availability increase from 82% to 86%
• DT0152 transported safely to Broncho
• DT0106 transmission was replaced safely

Lowlights
• DT availability 71%
• DT0152 Line boring
• DT0105 Nerospec

Emerging Issues

Priorities
• Steel cord belt splice scanning...
• Stabilis to submit proposal...
```

### Shafts & Winders Week 16
```
Highlights
• WTFitter Team repaired hot water issue at Nch3 B-Level
• BM Team replaced bolts on guides at Bunton

Emerging Issues
• Low compliment of Fitters and Riggers
• Massive impact of providing Changehouses maintenance

Lowlights
• Positions taking considerable time to fill

Priorities
• Shaft Repair Work with Solrock Team
• Employee Engagement/Resignations
```

## Validation Checks

The script performs these quality checks:

- ✓ PPTX file exists and is readable
- ✓ Content extracted contains expected HEAL sections
- ✓ No empty sections (validates data presence)
- ✓ Output file created successfully
- ✓ All items include bullet points

## Common Issues & Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found" error | Check PPTX file is in `Week {N}/` directory with correct naming |
| Empty sections extracted | Verify PPTX table structure matches expected layout; check for formatting differences |
| Encoding errors | Script uses UTF-8; ensure Windows locale supports special characters |
| Partial content extracted | Some PPTX files have mixed layouts; verify table structure in SKILL documentation |

## Next Steps After Extraction

1. **Review** the generated text file for accuracy
2. **Compare** with source PPTX slides visually if needed
3. **Use** in report generation workflow
4. **Archive** in Week folder for audit trail

## Notes

- N2 HEAL content is typically already in text format (manual entry)
- N3 PPTX extraction will be added when file becomes available
- Future weeks can use this skill without modification
- Supports both table-based and section-based PowerPoint layouts
