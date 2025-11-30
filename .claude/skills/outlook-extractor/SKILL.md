---
name: Outlook Extractor
description: Extract emails, calendar events, contacts, send emails, create/delete meetings via Outlook COM API integration
---

# Outlook Extractor

Programmatic access to Microsoft Outlook for email and calendar management.

## When to Use This Skill

Trigger this skill when the user asks to:
- Extract emails or calendar events
- Send an email
- Create or delete a meeting
- List contacts
- Get Outlook summaries for reporting

**Example triggers:** "extract my emails", "show me my meetings", "send an email", "create a meeting", "delete this meeting"

---

## Quick Start

### Prerequisites
- Windows operating system
- Microsoft Outlook installed and running
- Python 3.7+ with pywin32 installed (`pip install pywin32 --upgrade`)

### Basic Commands

All commands use: `python outlook_extractor.py <command> [options]`

| Command | Purpose |
|---------|---------|
| `emails --days 7 --limit 50` | Extract recent emails from Inbox |
| `emails --days 5 --limit 50 --folder "Sent Items"` | Extract recent sent emails |
| `emails --days 7 --limit 50 --folder-search "Production"` | Search subfolders containing "Production" |
| `emails --days 7 --limit 50 --list-folders` | Show all available folders (Inbox + subfolders) |
| `calendar --days 30 --limit 20` | View upcoming meetings |
| `contacts --limit 100` | List contacts |
| `send-email --to "user@company.com" --subject "Title" --body "Message"` | Send email |
| `send-email --to "user@company.com" --subject "Title" --body "Message" --attachment "C:\path\file.pdf"` | Send email with attachment |
| `delete-email --subject "spam" --limit 5` | Delete emails by criteria |
| `create-meeting --subject "Title" --start "2025-10-25 10:00"` | Create meeting |
| `delete-meeting --subject "Title" --start "2025-10-25 10:00"` | Delete meeting |

### Output Files

Commands generate JSON files for further processing:
- `outlook_emails.json` - Email extraction results
- `outlook_calendar.json` - Calendar events
- `outlook_contacts.json` - Contact list
- `outlook_all.json` - Combined data

---

## Email Folder Options

⚠️ **IMPORTANT**: The `emails` command supports multiple folder types:

### Folder Parameters

| Parameter | Values | Example |
|-----------|--------|---------|
| **`--folder`** | `Inbox` or `Sent Items` | `--folder "Inbox"` (default) |
| **`--folder-search`** | Partial folder name | `--folder-search "Production"` |
| **`--list-folders`** | (no value, flag only) | `--list-folders` |

### Common Folder Examples

**Extract from main Inbox:**
```bash
python outlook_extractor.py emails --days 7 --limit 50
# or explicitly:
python outlook_extractor.py emails --days 7 --limit 50 --folder "Inbox"
```

**Extract from Sent Items:**
```bash
python outlook_extractor.py emails --days 5 --limit 50 --folder "Sent Items"
```

**Search all subfolders matching a pattern:**
```bash
# Find all emails in folders containing "Production"
python outlook_extractor.py emails --days 7 --limit 50 --folder-search "Production"

# Find all emails in folders containing "N2"
python outlook_extractor.py emails --days 7 --limit 50 --folder-search "N2"
```

**List all available folders first (helpful to find subfolder names):**
```bash
python outlook_extractor.py emails --list-folders
```

This shows:
- All top-level folders (Inbox, Sent Items, Drafts, etc.)
- All subfolders under Inbox
- Folder full paths for use with `--folder-search`

---

## Important: Timezone and Working Directory

⚠️ **CRITICAL**: User is on **SAST (South African Standard Time, UTC+2)**

- Calendar times display in SAST in Outlook UI
- Internally stored as UTC
- **Always use local SAST times** when specifying meeting times
- Example: Meeting shows "15:00" in Outlook → use `--start "2025-10-25 15:00"`

The script runs from any folder on the machine - no working directory issues.


## Multiple Email Recipients & Attachments

### Multiple Recipients

⚠️ **CRITICAL**: Use **COMMAS** to separate multiple email addresses (NOT semicolons)

**Correct syntax:**
```bash
python outlook_extractor.py send-email \
  --to "user1@company.com,user2@company.com" \
  --cc "user3@company.com,user4@company.com,user5@company.com"
```

**Incorrect syntax (will fail):**
```bash
--to "user1@company.com;user2@company.com"  # ❌ WRONG
--cc "user3@company.com;user4@company.com"  # ❌ WRONG
```

**Real example:**
```bash
python outlook_extractor.py send-email \
  --to "Rudi.Opperman@assmang.co.za" \
  --cc "Jacques.Breet@assmang.co.za,Xavier.Petersen@assmang.co.za,Roelie.Prinsloo@assmang.co.za" \
  --subject "Project Update" \
  --body "Meeting summary..."
```

**Tested and confirmed**: 2025-10-29

### Sending Emails with Attachments

✅ **SUPPORTED**: The `send-email` command fully supports file attachments via the `--attachment` parameter.

**Syntax:**
```bash
python outlook_extractor.py send-email \
  --to "recipient@company.com" \
  --subject "Subject Line" \
  --body "Email body text" \
  --attachment "C:\absolute\path\to\file.pdf"
```

**Important Requirements:**
- **Absolute path required**: Use full path starting with drive letter (C:\...) or UNC path (\\server\...)
- **File must exist**: Script will verify file exists before sending
- **Single attachment only**: For multiple attachments, send separate emails

**Example with multiple recipients and attachment:**
```bash
python outlook_extractor.py send-email \
  --to "engineer1@assmang.co.za,engineer2@assmang.co.za" \
  --cc "manager@assmang.co.za" \
  --subject "Data Collection Template" \
  --body "Please complete the attached template and return by Wednesday." \
  --attachment "C:\Users\10064957\My Drive\GDVault\MarthaVault\00_Inbox\BRMO_Belt_Splicing_Scope_Template.xlsx"
```

**Tested and confirmed**: 2025-11-24

---


## Detailed Documentation

For complete parameter documentation, workflow examples, and error troubleshooting, see:

- **`reference/quick-reference.md`** ⭐ **START HERE** - Fast lookup guide with common commands and folder examples
- **`reference/commands.md`** - All 8 commands with complete parameters and examples
- **`reference/workflows.md`** - Real-world workflow examples (email review, meeting scheduling, batch operations)
- **`reference/email-style-guide.md`** - Email writing style guide for composing emails in Greg's voice
- **`reference/implementation.md`** - Technical architecture and timezone handling
- **`reference/troubleshooting.md`** - Common issues, solutions, and diagnostics

---

## Common Workflows

### Extract Emails by Folder

**Inbox (default):**
```bash
python outlook_extractor.py emails --days 7 --limit 50
```

**Sent Items:**
```bash
python outlook_extractor.py emails --days 5 --limit 50 --folder "Sent Items"
```

**From subfolders (e.g., Production folder and all children):**
```bash
python outlook_extractor.py emails --days 7 --limit 50 --folder-search "Production"
```

**From N2-related subfolders:**
```bash
python outlook_extractor.py emails --days 7 --limit 50 --folder-search "N2"
```

**First, discover all available folder names:**
```bash
python outlook_extractor.py emails --list-folders
```

### Extract Today's Emails
```bash
python outlook_extractor.py emails --days 1 --limit 100
```

### View Next Week's Calendar
```bash
python outlook_extractor.py calendar --days 7 --limit 50
```

### Send Email with Attachment
```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --subject "Q4 Report" \
  --body "Attached is the quarterly report" \
  --attachment "C:\Reports\Q4_2025.pdf"
```

### Create Meeting (SAST Time Format)
```bash
python outlook_extractor.py create-meeting \
  --subject "Q4 Planning" \
  --start "2025-10-28 14:00" \
  --location "Conference Room" \
  --attendees "xavier@company.com,gregory@company.com"
```

### Delete Meeting (SAST Time Format)
```bash
python outlook_extractor.py delete-meeting \
  --subject "Q4 Planning" \
  --start "2025-10-28 14:00"
```

See `reference/workflows.md` for 6+ additional workflow examples.

---

## Email Composition Guidelines

⚠️ **IMPORTANT**: When composing emails on behalf of Greg Karsten, you MUST follow the writing style guide.

### Email Style Guide
A comprehensive email writing style guide is available at `reference/email-style-guide.md`. This guide captures Greg's natural writing patterns, tone, and structure based on analysis of sent emails.

**Key Style Points:**
- **Direct and Concise** - Get to the point quickly
- **Professional but Approachable** - Use "Hi [Name]" for colleagues, "Good morning" for formal
- **Short Paragraphs** - 1-3 sentences with blank lines between
- **Action-Oriented** - Use @ mentions and clear requests
- **Standard Closing** - Always use "Regards" + "Greg"

### Contact Search
When user refers to someone by first name only (e.g., "send to Sipho"), use the `search-contact` command:
```bash
python outlook_extractor.py search-contact "Sipho"
```

This searches both personal contacts and Global Address List (GAL) to find the email address automatically.

### Approval Workflow
**All emails MUST be reviewed by user before sending.** Claude Code will automatically prompt for approval when using the send-email command.

### Quick Reference
```bash
# Search for contact by first name
python outlook_extractor.py search-contact "Xavier"

# Send email (will prompt for approval)
python outlook_extractor.py send-email \
  --to "recipient@company.com" \
  --subject "Subject Line" \
  --body "Email content following style guide"
```

**For complete style guidelines**, see `reference/email-style-guide.md`

---

## Execution Mode: Background Operations

⚠️ **IMPORTANT**: Data extraction operations (emails, calendar, contacts, search-contact) should run in the background to allow you to continue working.

### Background Execution
When Claude invokes this skill for read operations, commands will run asynchronously in the background:

**Commands that run in background:**
- ✅ `emails` - Extract emails while you work on other tasks
- ✅ `calendar` - Extract calendar events in background
- ✅ `contacts` - List contacts asynchronously
- ✅ `search-contact` - Search for contacts in background

**Commands that run synchronously:**
- ⚠️ `send-email` - Runs after your approval (synchronous for safety)
- ⚠️ `create-meeting` - Runs after your approval (synchronous for safety)
- ⚠️ `delete-meeting` - Runs after your approval (synchronous for safety)

### How It Works
1. You request email extraction: "extract my emails from the past week"
2. Claude starts the extraction in background
3. You can continue with other tasks immediately
4. When extraction completes, Claude notifies you and processes the results
5. You never have to wait for long-running data extractions

### Permission Configuration
The following commands are pre-approved and will run automatically without asking for permission:
```bash
pip install pywin32 --upgrade
python outlook_extractor.py emails*
python outlook_extractor.py calendar*
python outlook_extractor.py contacts*
python outlook_extractor.py search-contact*
```

Send operations (`send-email`, `create-meeting`, `delete-meeting`) always require your explicit approval.

---

## How This Skill Works

1. **Auto-Discovery**: Claude discovers this skill at startup by reading the SKILL.md metadata
2. **Model-Invoked**: Claude autonomously decides to use this skill when your request matches the description
3. **Script Execution**: Claude runs `scripts/outlook_extractor.py` with appropriate parameters
4. **Output Processing**: Results are saved to JSON files for further analysis or sharing

---

## Key Features

✅ **Timezone Aware** - Automatically handles SAST ↔ UTC conversion
✅ **Portable** - Works from any folder on the machine
✅ **No Relative Paths** - All paths are absolute for reliability
✅ **Comprehensive Error Handling** - Clear error messages for troubleshooting
✅ **Production Ready** - Fully tested on Windows with Outlook 2021+

⚠️ **Known Limitation**: Email priority (`--priority` parameter) cannot be set due to Outlook COM API security restrictions. All emails send with normal priority.

---

## Troubleshooting

**Python execution fails?**
- Verify Outlook is running
- Check pywin32 is installed: `python -c "import win32com.client"`
- See `reference/troubleshooting.md` for detailed diagnostics

**Meeting not found when deleting?**
- Ensure you're using the correct SAST time (what you see in Outlook UI)
- Include exact subject text
- See `reference/troubleshooting.md` Issue #2

**Script runs but no results?**
- Try expanding the date range: `--days 30` instead of `--days 7`
- Check Outlook sync status
- See `reference/troubleshooting.md` Issue #4

---

## Next Steps

**For detailed guidance**, refer to the reference files:
- Start with `reference/commands.md` for parameter details
- Check `reference/workflows.md` for real-world examples
- Review `reference/email-style-guide.md` before composing emails
- Use `reference/troubleshooting.md` when things don't work

**Need help?** All reference files are bundled in this skill directory.
