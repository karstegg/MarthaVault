# Extract PPTX HEAL - Technical Reference

## Implementation Details

The script uses `python-pptx` library to parse PowerPoint files and extract text content from tables. It handles two primary table layouts used across mining sites.

### Core Logic

1. **File Discovery**: Locates PPTX in `Week {N}/` directory using site-specific glob patterns
2. **Layout Detection**: Identifies table structure and calls appropriate extraction function
3. **Content Parsing**: Extracts text from table cells, handling multi-line content
4. **Deduplication**: Removes duplicate items within each section
5. **Formatting**: Converts extracted data into standardized text format with bullets
6. **Output**: Saves formatted text with proper encoding

## File Detection

### Search Patterns

**Gloria**:
- Primary: `HEAL page*.pptx`
- Fallback: `*gloria*.pptx`
- Typical file: `HEAL page (003).pptx - AutoRecovered.pptx`

**Shafts & Winders**:
- Primary: `*SHAFTS*WINDERS*.pptx`
- Fallback: `*S&W*.pptx`
- Typical file: `SHAFTS AND WINDERS_HEAL_16_WEEK_10-16Oct2025.pptx`

**N3**:
- Primary: `*N3*HEAL*.pptx`
- Fallback: `*Nchwaning 3*HEAL*.pptx`
- Status: Pending

### Implementation
```python
patterns = {
    "gloria": ["HEAL page*.pptx", "*gloria*.pptx"],
    "shafts-winders": ["*SHAFTS*WINDERS*.pptx", "*S&W*.pptx"],
    "n3": ["*N3*HEAL*.pptx", "*Nchwaning 3*HEAL*.pptx"],
}
```

## Data Extraction Process

### Gloria Layout (4x2 Table)

**Table Structure**:
```
Row 0: [Header]        [Header]
       Highlight      Lowlight
Row 1: [Content]      [Content]
       Highlights    Lowlights
Row 2: [Header]      [Header]
       Emerging      Priorities
       Issues
Row 3: [Content]     [Content]
       Items         Items
```

**Extraction Logic**:
1. Check table is 4 rows × 2 columns minimum
2. Row 1, Col 0 → Highlights section
3. Row 1, Col 1 → Lowlights section
4. Row 3, Col 0 → Emerging Issues section
5. Row 3, Col 1 → Priorities section

**Code**:
```python
def extract_gloria_heal(pptx_path):
    # Row 1: Highlights (left) and Lowlights (right)
    left_col = table.rows[1].cells[0].text.strip()
    right_col = table.rows[1].cells[1].text.strip()
    # Process and deduplicate...
    # Row 3: Emerging Issues and Priorities
    left_col = table.rows[3].cells[0].text.strip()
    right_col = table.rows[3].cells[1].text.strip()
```

### Shafts & Winders Layout (Multiple Single-Cell Tables)

**Table Structure** (First slide only):
- Each table has 1 row × 1 column
- Cell content starts with section header (e.g., "Highlights:")
- Remaining lines are section items

**Tables in Order**:
1. "You Can Help By:" → Actions
2. "Highlights:" → Highlights
3. "Emerging Issues:" → Emerging Issues
4. "Lowlights:" → Lowlights
5. "Priorities:" → Priorities

**Extraction Logic**:
1. Process only first slide (other slides are annual schedules)
2. For each table, identify section from first line
3. Extract remaining lines as section items
4. Skip section headers and empty lines

**Code**:
```python
def extract_shafts_winders_heal(pptx_path):
    slide = prs.slides[0]  # Only first slide
    for shape in slide.shapes:
        if shape.has_table:
            cell_text = table.rows[0].cells[0].text.strip()
            # Detect section from header
            if cell_text.startswith("Highlights"):
                current_section = "Highlights"
            # Extract items under section...
```

### N3 Layout (TBD)

Currently uses generic multi-table extraction similar to S&W. Will be refined when actual N3 PPTX structure is available.

## Data Parsing Techniques

### Multi-Line Cell Content

PowerPoint tables can contain multiple lines within a single cell. Extract by:

```python
for line in cell_text.split('\n'):
    line = line.strip()
    if line:
        heal_data[section].append(line)
```

### Deduplication

Remove duplicate items within each section:

```python
if line not in heal_data[section]:
    heal_data[section].append(line)
```

### Numbering Artifact Cleanup

Remove leading numbers, bullets, and dashes:

```python
item = item.lstrip('0123456789. •–-')
item = item.strip()
```

## Output Formatting

### Section Order
1. Highlights
2. Lowlights
3. Emerging Issues
4. Priorities
5. Actions

### Format Rules
- Section header on its own line
- Each item prefixed with bullet (•)
- Blank line between sections
- UTF-8 encoding
- No trailing blank lines

### Example Output
```
Highlights
• Item 1
• Item 2

Lowlights
• Item 1

Emerging Issues

Priorities
• Item 1
```

## Error Handling

### File Not Found
- Search fails if Week directory or matching PPTX missing
- Print error to stderr with descriptive message
- Return False, exit code 1

### Table Parsing Errors
- Catch exceptions during table cell access
- Print error with context
- Return False, exit code 1

### Encoding Issues
- Use UTF-8 encoding for all file operations
- Handles special characters (bullets, dashes, underscores)

## Performance Characteristics

- **Speed**: ~100ms for typical PPTX (< 70KB)
- **Memory**: Minimal (single slide processing)
- **Scalability**: Handles files with multiple tables efficiently

## Testing Coverage

Tested with:
- ✓ Gloria Week 16 (4x2 table layout)
- ✓ Shafts & Winders Week 16 (multi-table layout)
- ⏳ N3 (pending PPTX availability)

Test cases:
- File not found (Week directory missing)
- Invalid PPTX (corrupted file)
- Empty sections (no content under header)
- Multi-line cells (content split across lines)
- Duplicate items (same text in multiple cells)

## Known Issues & Workarounds

### Issue: Numbering Artifacts
**Description**: Row 3 left column of Gloria tables contains "1." numbering
**Cause**: PowerPoint formatting or manual entry
**Workaround**: Check for "1." and skip if found
```python
if left_col and left_col != "1.":
    # Process content...
```

### Issue: Auto-Recovered Files
**Description**: Gloria file may be named `HEAL page (003).pptx - AutoRecovered.pptx`
**Cause**: PowerPoint crash recovery
**Workaround**: Use glob pattern `HEAL page*.pptx` to catch variations

### Issue: Empty Sections
**Description**: Some sections may have no content (e.g., Gloria "Emerging Issues")
**Cause**: No issues to report for that week
**Expected**: Empty section displays as header only with blank line

## Future Enhancements

1. **N3 Layout Detection**: Add specific handling once actual file structure known
2. **Validation Rules**: Require minimum items per section (e.g., warn if no Highlights)
3. **Formatting Variants**: Handle additional PPTX layouts if introduced
4. **Output Formats**: Add CSV export option for data integration
5. **Batch Processing**: Extract multiple sites in single command

## Dependencies

- `python-pptx>=0.6.23`: Parse and extract PPTX content
- Python 3.10+: Type hints, pathlib usage
- Standard library: argparse, sys, pathlib, os

## Code Structure

```
extract_pptx_heal.py
├── find_pptx_file()          # File discovery
├── extract_gloria_heal()      # Gloria-specific extraction
├── extract_shafts_winders_heal()  # S&W-specific extraction
├── extract_n3_heal()          # N3 extraction (generic for now)
├── format_heal_output()       # Output formatting
├── extract_heal()             # Main orchestration
└── main()                     # CLI entry point
```

## Configuration

All configuration is embedded in code patterns:

**Site Patterns**: Update `patterns` dict in `find_pptx_file()`
**Section Order**: Update `sections` list in `format_heal_output()`
**Output Format**: Modify `format_heal_output()` function
