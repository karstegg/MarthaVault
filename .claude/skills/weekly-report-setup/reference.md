# Weekly Report Setup - Technical Reference

## Architecture Overview

The skill uses a single Python script (`weekly_report_setup.py`) that implements the `WeeklyReportSetup` class to orchestrate steps 1-5 of the weekly report workflow.

```
WeeklyReportSetup
├── __init__()                    - Connect to Outlook COM API
├── calculate_current_week()      - Fiscal week calculation
├── get_week_date_range()         - Date range for a week
├── get_target_friday()           - Report send date
├── prompt_week_confirmation()    - User confirmation prompt
├── create_week_folder()          - Create Week XX directory
├── find_emails_by_sender()       - Search Inbox by sender name
├── download_attachments()        - Save email attachments
├── extract_n2_heal()             - Extract HEAL section to text
└── run()                         - Main orchestration method
```

## Implementation Details

### 1. Fiscal Week Calculation

**Constant**: `FISCAL_WEEK_1_START = datetime(2025, 7, 1)`

**Formula**:
```python
week_num = floor((today - July 1, 2025) / 7 days) + 1
```

**Examples**:
- October 27, 2025 = Week 18
- January 15, 2026 = Week 31
- June 30, 2025 = Week 0 (off by one, clamped to Week 1)

**Method**: `calculate_current_week()`
- Called at startup to determine current week
- User can override with `--week=XX` argument

### 2. Week Date Range Calculation

**Method**: `get_week_date_range(week_num)`

Calculates the Monday-Sunday date range for any week:

```python
days_offset = (week_num - 1) * 7
week_start = July 1, 2025 + days_offset days
week_end = week_start + 6 days
```

**Returns**: (Monday date, Sunday date)

**Example for Week 18**:
- Start: October 27, 2025 (Monday)
- End: November 2, 2025 (Sunday)

### 3. Recursive Subfolder Discovery

**Method**: `_add_subfolders_recursive(parent_folder, current_depth=0, max_depth=3)`

**Algorithm**:
1. Check if max_depth reached (default 3 levels)
2. Get parent_folder.Folders collection
3. Iterate through subfolders (COM API uses 1-based indexing)
4. For each subfolder:
   - Add to `self.folders_to_search` list
   - Recursively call on subfolder (current_depth + 1)
5. Return count of subfolders added

**Example Discovered Folders**:
```
Inbox
├── Production
├── Planners
├── NCH2 (N2 emails found here)
├── NCH3 (N3 emails found here)
├── Gloria (Gloria emails found here)
├── Shaft (S&W emails found here)
├── Epiroc (Epiroc emails found here)
├── Projects & Initiatives
│   └── RFID & Paperless
└── ... (45 total subfolders)
```

**Performance**: Folder discovery takes ~1-2 seconds for 45+ folders

### 4. Email Search Logic

**Method**: `find_emails_by_sender(sender_info, start_date, end_date)`

**Search Algorithm**:
1. Build Outlook Restrict() filter string with date range
2. For each folder in `folders_to_search`:
   - Apply Restrict() filter (COM-level filtering, 10-100x faster)
   - Sort by ReceivedTime (newest first)
   - For each restricted item:
     - Check sender name OR email match (dual strategy)
     - Check subject keywords match
     - Return first match
3. Return None if no match found across all folders

**Sender Mappings with Dual Matching**:
```python
SENDERS = {
    'n2': {
        'name': 'Sikelela Nzuza',
        'email': 'Sikelela.Nzuza@assmang.co.za',
        'subject_keywords': ['weekly report', 'eng report', 'nch2', 'n2']
    },
    'n3': {
        'name': 'Sello Sease',
        'email': 'Sello.Sease@assmang.co.za',
        'subject_keywords': ['weekly report', 'eng report', 'nch3', 'n3']
    },
    'gloria': {
        'name': 'Sipho Dubazane',
        'email': 'Sipho.Dubazane@assmang.co.za',
        'subject_keywords': ['weekly report', 'eng report', 'gloria']
    },
    'shafts': {
        'name': 'Xavier Petersen',
        'email': 'Xavier.Petersen@assmang.co.za',
        'subject_keywords': ['weekly report', 'shafts', 'winders', 's&w']
    },
    'epiroc': {
        'name': 'Phillip Moller',
        'email': 'phillip.moller@epiroc.com',
        'subject_keywords': ['brmo weekly report', 'weekly report', 'bev']
    }
}
```

**Outlook COM API Details**:
- `Inbox = namespace.GetDefaultFolder(6)` - Folder ID 6 = Inbox
- `items = folder.Items` - Collection of email items
- `restricted_items = items.Restrict(filter_str)` - Fast COM-level filtering
- `filter_str = "[ReceivedTime] >= 'MM/DD/YYYY HH:MM' AND [ReceivedTime] <= 'MM/DD/YYYY HH:MM'"`
- `items.Sort("[ReceivedTime]", False)` - Sort by date, descending
- `item.SenderName` - Sender's display name
- `item.SenderEmailAddress` - Sender's email
- `item.Subject` - Email subject line
- `item.ReceivedTime` - Datetime of receipt (UTC)

**Dual Sender Matching**:
```python
# Match on name OR email address
sender_match = (
    sender_info['name'].lower() in item.SenderName.lower() or
    sender_info['email'].lower() in sender_email.lower()
)
```

**Subject Keyword Filtering**:
```python
# Must contain at least one keyword
subject = item.Subject.lower()
subject_match = any(
    keyword.lower() in subject
    for keyword in sender_info['subject_keywords']
)
```

**Timezone Handling** (per CLAUDE.md):
- Outlook COM API returns UTC times
- SAST (South African Standard Time) = UTC+2
- Date comparison uses naive datetime (timezone removed)
- `datetime.replace(tzinfo=None)` removes timezone info

### 5. Attachment Download

**Method**: `download_attachments(email_item, week_folder, sender_key)`

**Process**:
1. Access `email_item.Attachments` collection
2. Iterate through each attachment (1-indexed in COM API)
3. Get filename: `attachment.FileName`
4. Build filepath: `week_folder / filename`
5. Save: `attachment.SaveAsFile(filepath)`
6. Track filename in `self.downloaded_files`

**Outlook COM API Details**:
- `email_item.Attachments` - Collection of attachments
- `attachments.Count` - Number of attachments
- `attachments.Item(i)` - Get attachment by 1-based index
- `attachment.FileName` - Original filename
- `attachment.SaveAsFile(path)` - Save to disk (overwrites if exists)

**Error Handling**:
- Catches exceptions per attachment (one failure doesn't stop others)
- Tracks successful downloads in list
- Returns count of successfully downloaded files

### 6. N2 HEAL Extraction

**Method**: `extract_n2_heal(email_item, week_folder, week_num)`

**Two-Step Process**:

**Step 1 - Python Script (Automated)**:
- Extract raw email body from N2 email
- Save to `N2 Email Body - WeekXX.txt`
- Notify user to ask Claude for parsing

**Step 2 - Claude Parsing (Manual Request)**:
- User asks Claude to parse the email body
- Claude reads `N2 Email Body - WeekXX.txt`
- Claude creates formatted `N2 HEAL Page WeekXX.txt` with 4 sections:
  - Highlight
  - Emerging Issues
  - Actions
  - Lowlights
- **Claude automatically deletes `N2 Email Body - WeekXX.txt`** after successful parsing

**Algorithm (Python Script)**:
1. Extract raw email body: `email_item.Body`
2. Save complete body to: `N2 Email Body - WeekXX.txt`
3. Print notification for user to request Claude parsing

**Claude Parsing Process**:
1. Read raw email body file
2. Identify HEAL sections (Highlight, Emerging Issues, Actions, Lowlights)
3. Extract bullet points with proper formatting
4. Write to `N2 HEAL Page WeekXX.txt` with section headers and bullets
5. **Delete intermediate file**: `N2 Email Body - WeekXX.txt`

**Benefits of Claude-Powered Parsing**:
- No brittle pattern matching in Python
- Handles format variations intelligently
- More robust and maintainable
- Clear separation: Python extracts, Claude interprets

### 7. User Confirmation Flow

**Method**: `prompt_week_confirmation(auto_week)`

**Process**:
1. Calculate current week automatically
2. Determine date range for that week
3. Display: `"Detected Week 18 (Oct 27 - Nov 02, 2025)\nProceed? (Y/n): "`
4. Read user input
5. If 'n': Exit with "Setup cancelled"
6. Otherwise: Continue with confirmed week

**Override**: `--week=XX` argument skips this prompt entirely

### 8. Folder Creation

**Method**: `create_week_folder(week_num)`

**Process**:
1. Build path: `BASE_REPORTS_DIR / f"Week {week_num}"`
2. Create with `Path.mkdir(parents=True, exist_ok=True)`
3. Verify folder exists
4. Return Path object or None on error

**Base Directory**:
```python
BASE_REPORTS_DIR = r"C:\Users\10064957\OneDrive - African Rainbow Minerals\Senior Production Engineer (Acting - January 2025)\Weekly Reports"
```

### 9. Main Orchestration

**Method**: `run(manual_week=None)`

**Flow**:
1. Display header banner
2. Calculate/confirm week number
3. Create Week XX folder
4. Search for N2, N3, Gloria, S&W emails
5. Search for Epiroc email
6. Download all attachments
7. Extract N2 HEAL
8. Generate summary report
9. Display next steps

**State Tracking**:
- `self.found_emails` - Dict of {sender_key: email_item}
- `self.downloaded_files` - List of downloaded filenames
- `self.missing_emails` - List of emails not found

## Dependencies

### Python Libraries
- `sys`, `os` - Standard library
- `argparse` - Argument parsing
- `datetime`, `timedelta` - Date calculations
- `pathlib.Path` - File path handling
- `re` - Regex (imported but not currently used)
- `win32com.client` - Outlook COM API (external: pywin32)

### System Requirements
- Windows operating system
- Microsoft Outlook installed and running
- Python 3.7+
- pywin32 package: `pip install pywin32 --upgrade`

## Error Handling

### Connection Errors
```python
try:
    self.outlook = win32com.client.GetActiveObject("Outlook.Application")
except:
    self.outlook = win32com.client.Dispatch("Outlook.Application")
```
- Tries to get active instance first
- Falls back to creating new instance
- Exits with error if both fail

### Email Search Errors
```python
try:
    # ... search logic
except Exception as e:
    print(f"✗ Error searching emails: {e}", file=sys.stderr)
    return []
```
- Exceptions printed to stderr
- Returns empty list (non-fatal)
- Process continues

### Individual Item Processing
```python
for item in items:
    try:
        # ... process item
    except Exception as e:
        continue  # Skip this item
```
- Each item wrapped in try-except
- Failures don't stop processing other items
- All successes tracked

### Attachment Download
```python
for i in range(1, count + 1):
    try:
        # ... download
    except Exception as e:
        print(f"  ✗ Failed to download attachment: {e}", file=sys.stderr)
        continue
```
- Per-attachment error handling
- One failure doesn't prevent others

### File Operations
```python
try:
    week_folder.mkdir(parents=True, exist_ok=True)
    if week_folder.exists():
        # success
except Exception as e:
    # error
```
- Explicit existence checks
- Exceptions caught and reported

## Output Format

### Console Output

**Section Headers** (step tracking):
```
[1/5] Creating Week 18 folder
[2/5] Searching for weekly report emails
```

**Success Indicators**:
```
✓ Connected to Outlook
✓ Week 18 folder ready: ...
✓ Found: N2 Weekly Report October 23-25
✓ Downloaded: filename.xlsx
✓ Extracted HEAL: N2 HEAL Page Week18.txt
```

**Warning Indicators**:
```
⚠ Could not extract HEAL content from email body
ℹ No attachments found
```

**Error Indicators**:
```
✗ Error connecting to Outlook: ...
✗ Not found
```

### Summary Report
```
[5/5] Setup Summary
  ============================================================
  Week folder: ...
  Files downloaded: 8

  Downloaded files:
    • Nch2 Weekly Report 23 Oct 2025.xlsx
    • ...

  Missing emails:
    • Gloria Report

  ============================================================
  ✓ Setup complete! Ready for data extraction (steps 6-12)
```

## Performance Characteristics

- **Outlook Connection**: ~1-2 seconds (first time), cached thereafter
- **Email Search**: ~2-5 seconds per sender (depends on inbox size)
- **Attachment Download**: ~1-10 seconds (depends on file sizes)
- **HEAL Extraction**: <1 second
- **Total Runtime**: 15-30 seconds typical

## Testing Coverage

**Scenarios Tested**:
- ✓ Auto-detect week with confirmation
- ✓ Manual week specification (--week=XX)
- ✓ Outlook connection (active instance vs. new instance)
- ✓ Email search (found, not found)
- ✓ Multiple attachments download
- ✓ Single attachment download
- ✓ No attachments
- ✓ Timezone handling (UTC normalization)
- ✓ HEAL extraction (with standard format)
- ✓ Week folder creation (new folder, existing folder)
- ✓ Missing emails (continues, reports)
- ✓ Summary report generation

## Future Enhancements

1. **Email Body Parsing**: Implement more robust HEAL extraction with regex patterns
2. **Configuration File**: Store sender names in config.ini instead of hardcoding
3. **Auto-Extract Integration**: Option to auto-run steps 6-12 after setup
4. **Email Subject Search**: Add subject line matching for more specific email finding
5. **Backup Contacts**: Support alternate contact names as fallback
6. **Email Retry Logic**: Auto-retry failed downloads with exponential backoff
7. **Duplicate Detection**: Check if files already exist in Week XX folder
8. **Archive Integration**: Auto-move old emails to archive folder

## Known Limitations

1. **Single Outlook Instance**: Requires one Outlook instance (no multi-instance support)
2. **Recursive Depth**: Searches up to 3 levels of subfolders (configurable in code)
3. **Archived Emails**: Does not search Archived folders outside of Inbox
4. **HEAL Extraction**: Pattern matching may fail with non-standard email formatting
5. **File Overwrite**: Will overwrite existing files in Week XX folder without warning
6. **No Filtering**: Downloads all attachments (can't pick and choose)
7. **Subject Keywords Required**: Email must contain at least one keyword from list to be found
