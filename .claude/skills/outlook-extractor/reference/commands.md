# Outlook Extractor - Complete Command Reference

All commands use the format: `python outlook_extractor.py <command> [options]`

---

## 1. Extract Emails

Extract emails from your inbox with flexible date and limit options.

### Command
```bash
python outlook_extractor.py emails --days 7 --limit 50
```

### Parameters
- `--days` (integer, default: 30) - Number of days back to search
- `--limit` (integer, default: 20) - Maximum emails to return

### Output
Saves to `outlook_emails.json` with structure:
```json
{
  "From": "sender@company.com",
  "Subject": "Email Subject",
  "ReceivedTime": "2025-10-20T09:30:00",
  "Unread": false,
  "Attachments": 2
}
```

### Examples

**Today's emails (high limit):**
```bash
python outlook_extractor.py emails --days 1 --limit 100
```

**Last week's emails:**
```bash
python outlook_extractor.py emails --days 7 --limit 50
```

**Last 90 days (all):**
```bash
python outlook_extractor.py emails --days 90 --limit 1000
```

---

## 2. Extract Calendar Events

View upcoming meetings and appointments.

### Command
```bash
python outlook_extractor.py calendar --days 7 --limit 20
```

### Parameters
- `--days` (integer, default: 7) - Number of days ahead to check
- `--limit` (integer, default: 20) - Maximum events to return

### Output
Saves to `outlook_calendar.json` with structure:
```json
{
  "Subject": "Team Meeting",
  "Start": "2025-10-22T14:00:00+00:00",
  "End": "2025-10-22T15:00:00+00:00",
  "Location": "Conference Room A",
  "Organizer": "Gregory Karsten"
}
```

### Examples

**Next 7 days:**
```bash
python outlook_extractor.py calendar --days 7 --limit 50
```

**Next 30 days (all):**
```bash
python outlook_extractor.py calendar --days 30 --limit 100
```

**Next 3 months:**
```bash
python outlook_extractor.py calendar --days 90 --limit 200
```

---

## 3. Extract Contacts

List contacts from your address book.

### Command
```bash
python outlook_extractor.py contacts --limit 100
```

### Parameters
- `--limit` (integer, default: 100) - Maximum contacts to return

### Output
Saves to `outlook_contacts.json` with structure:
```json
{
  "Name": "Xavier Petersen",
  "Email": "xavier.petersen@company.com",
  "Phone": "+27 11 123 4567",
  "Company": "Assmang"
}
```

### Examples

**All contacts:**
```bash
python outlook_extractor.py contacts --limit 1000
```

**First 50 contacts:**
```bash
python outlook_extractor.py contacts --limit 50
```

---

## 4. Send Email

Send an email with optional CC, BCC, attachments, and priority.

### Command
```bash
python outlook_extractor.py send-email \
  --to "recipient@company.com" \
  --subject "Email Subject" \
  --body "Email message text" \
  --cc "cc@company.com" \
  --bcc "bcc@company.com" \
  --attachment "C:\path\to\file.pdf" \
  --priority "high"
```

### Parameters
- `--to` (required, string) - Email recipient(s), comma-separated for multiple
- `--subject` (required, string) - Email subject line
- `--body` (required, string) - Email message body
- `--cc` (optional, string) - CC recipient(s), comma-separated
- `--bcc` (optional, string) - BCC recipient(s), comma-separated
- `--attachment` (optional, string) - Absolute file path to attach
- `--priority` (optional, choices: low/normal/high) - Email priority (default: normal)

### Important Notes
- Use absolute file paths for attachments: `C:\Reports\file.pdf` not `Reports\file.pdf`
- Recipient emails must be in valid format: `user@company.com`
- Multiple recipients: `--to "user1@company.com,user2@company.com"`
- Email sends immediately (no draft option)

### Examples

**Simple email:**
```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --subject "Project Update" \
  --body "Here is the latest project update"
```

**Email with CC and BCC:**
```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --cc "gregory.karsten@company.com" \
  --bcc "archive@company.com" \
  --subject "Q4 Operations Report" \
  --body "Attached is the Q4 operations report"
```

**Email with attachment:**
```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --subject "Q4 Report" \
  --body "Please find the attached Q4 report" \
  --attachment "C:\Reports\Q4_2025.pdf"
```

**High priority email:**
```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --subject "URGENT: System Issue" \
  --body "Critical system issue requires immediate attention" \
  --priority "high"
```

**Multiple recipients:**
```bash
python outlook_extractor.py send-email \
  --to "xavier@company.com,gregory@company.com,melissa@company.com" \
  --subject "Team Meeting Tomorrow" \
  --body "Reminder: Team meeting tomorrow at 2 PM"
```

**Multiple recipients with attachment:**
```bash
python outlook_extractor.py send-email \
  --to "engineer1@assmang.co.za,engineer2@assmang.co.za,engineer3@assmang.co.za" \
  --cc "manager@assmang.co.za" \
  --subject "Data Collection Template - Please Complete" \
  --body "Please complete the attached template and return by Wednesday, 26 November 2025" \
  --attachment "C:\Users\10064957\My Drive\GDVault\MarthaVault\00_Inbox\BRMO_Belt_Splicing_Scope_Template.xlsx"
```

---

## 5. Create Calendar Meeting

Create a new calendar event with attendees and location.

### Command
```bash
python outlook_extractor.py create-meeting \
  --subject "Meeting Title" \
  --start "2025-10-25 10:00" \
  --end "2025-10-25 11:00" \
  --location "Conference Room" \
  --attendees "xavier@company.com,gregory@company.com" \
  --body "Meeting description"
```

### Parameters
- `--subject` (required, string) - Meeting title
- `--start` (required, string) - Start time in format `YYYY-MM-DD HH:MM` (SAST local time)
- `--end` (optional, string) - End time in format `YYYY-MM-DD HH:MM` (defaults to 1 hour after start)
- `--location` (optional, string) - Meeting location
- `--attendees` (optional, string) - Comma-separated email addresses
- `--body` (optional, string) - Meeting description/notes

### Important: Timezone
⚠️ **Use local SAST time** (what you see in Outlook UI)
- Outlook shows: 15:00 → use `--start "2025-10-25 15:00"`
- Do NOT use UTC times
- The script handles UTC conversion internally

### Examples

**Simple 1-hour meeting:**
```bash
python outlook_extractor.py create-meeting \
  --subject "Team Standup" \
  --start "2025-10-28 09:00"
```

**Meeting with specific end time:**
```bash
python outlook_extractor.py create-meeting \
  --subject "Q4 Planning Session" \
  --start "2025-10-28 09:00" \
  --end "2025-10-28 11:30"
```

**Meeting with location:**
```bash
python outlook_extractor.py create-meeting \
  --subject "Board Meeting" \
  --start "2025-10-30 14:00" \
  --end "2025-10-30 15:30" \
  --location "SHERQ Conference Room"
```

**Meeting with attendees:**
```bash
python outlook_extractor.py create-meeting \
  --subject "Project Kickoff" \
  --start "2025-11-01 10:00" \
  --end "2025-11-01 11:00" \
  --attendees "xavier@company.com,gregory@company.com,melissa@company.com"
```

**Meeting with all options:**
```bash
python outlook_extractor.py create-meeting \
  --subject "Q4 Operations Review" \
  --start "2025-10-28 14:00" \
  --end "2025-10-28 15:30" \
  --location "Admin Conference Room" \
  --attendees "xavier@company.com,gregory@company.com,marina@company.com" \
  --body "Quarterly operations review and planning for next quarter"
```

---

## 6. Delete Calendar Meeting

Delete a meeting from your calendar.

### Command
```bash
python outlook_extractor.py delete-meeting \
  --subject "Meeting Title" \
  --start "2025-10-25 10:00"
```

### Parameters
- `--subject` (required, string) - Exact meeting title to delete
- `--start` (required, string) - Start time in format `YYYY-MM-DD HH:MM` (SAST local time)

### Important Notes
- **Match must be exact**: Subject text must match exactly (case-sensitive)
- **Use local SAST time**: Same time format you see in Outlook UI
- **Both parameters required**: Subject and time together uniquely identify the meeting
- **Deletion is immediate**: No undo available

### Examples

**Delete specific meeting:**
```bash
python outlook_extractor.py delete-meeting \
  --subject "Q4 Planning Session" \
  --start "2025-10-28 09:00"
```

**Delete another meeting:**
```bash
python outlook_extractor.py delete-meeting \
  --subject "Team Standup" \
  --start "2025-10-29 09:00"
```

---

## Help Command

Get command-specific help:

```bash
python outlook_extractor.py --help
python outlook_extractor.py emails --help
python outlook_extractor.py send-email --help
python outlook_extractor.py create-meeting --help
python outlook_extractor.py delete-meeting --help
```

---

## Common Parameter Patterns

### Date/Time Formats
- Days: Integer (1, 7, 30, 90, 365)
- Times: `YYYY-MM-DD HH:MM` format (24-hour, SAST)
  - Example: `2025-10-28 14:30` = 2:30 PM SAST

### Email Addresses
- Single: `user@company.com`
- Multiple: `user1@company.com,user2@company.com,user3@company.com`
- Must be valid email format

### File Paths
- Always use absolute paths: `C:\Users\username\Documents\file.pdf`
- Not relative: `Documents\file.pdf` won't work
- Path must exist before sending

### Priority Levels
- `low` - Low priority
- `normal` - Default priority
- `high` - High/urgent priority

---

## Output Files Generated

Each command generates a JSON file (overwritten on each run):

| Command | Output File | Content |
|---------|-------------|---------|
| emails | outlook_emails.json | Array of email objects |
| calendar | outlook_calendar.json | Array of meeting objects |
| contacts | outlook_contacts.json | Array of contact objects |
| send-email | (none) | Feedback in console |
| create-meeting | (none) | Feedback in console |
| delete-meeting | (none) | Feedback in console |
| all | outlook_all.json | Combined emails, calendar, contacts |

---

## Troubleshooting Commands

### Check Prerequisites
```bash
# Check Python version
python --version

# Check pywin32 installed
python -c "import win32com.client; print('pywin32 OK')"

# Check Outlook connection
python -c "import win32com.client; o = win32com.client.GetActiveObject('Outlook.Application'); print('Outlook connected')"
```

### Verify Outlook Status
- Keep Outlook open during execution
- Check Outlook is in "Online" mode (not offline)
- Verify calendar/inbox is synced

See `reference/troubleshooting.md` for detailed diagnostics.
