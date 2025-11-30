# Outlook Extractor – Quick Reference Guide

**Updated**: November 23, 2025
**For Claude Code Users**: Fast lookup guide for common email extraction tasks

---

## Most Common Commands

### Get Emails from Inbox
```bash
python outlook_extractor.py emails --days 7 --limit 50
```
Extracts last 7 days, max 50 emails, saves to `outlook_emails.json`

### Get Sent Items
```bash
python outlook_extractor.py emails --days 5 --limit 50 --folder "Sent Items"
```
Extracts your sent emails from last 5 days

### Search Subfolders
```bash
python outlook_extractor.py emails --folder-search "NCH2" --days 7 --limit 50
```
Finds all emails in folders containing "NCH2" (case-insensitive)

### List All Folders
```bash
python outlook_extractor.py emails --list-folders
```
Shows complete folder structure with 76+ folders and subfolders

---

## Quick Folder Reference

### Production Folders
```bash
# N2 emails
python outlook_extractor.py emails --folder-search "NCH2" --days 7 --limit 50

# N3 emails
python outlook_extractor.py emails --folder-search "NCH3" --days 7 --limit 50

# Gloria emails
python outlook_extractor.py emails --folder-search "Gloria" --days 7 --limit 50

# Shafts & Winders
python outlook_extractor.py emails --folder-search "Shaft" --days 7 --limit 50
```

### OEM/Vendor Folders
```bash
# All Epiroc emails
python outlook_extractor.py emails --folder-search "Epiroc" --days 7 --limit 50

# Komatsu
python outlook_extractor.py emails --folder-search "Komatsu" --days 7 --limit 50

# Cummins
python outlook_extractor.py emails --folder-search "Cummins" --days 7 --limit 50
```

### Procurement/Finance
```bash
# Procurement folder
python outlook_extractor.py emails --folder-search "Procurement" --days 7 --limit 50

# Finance emails
python outlook_extractor.py emails --folder-search "Finance" --days 7 --limit 50
```

### HR & Training
```bash
python outlook_extractor.py emails --folder-search "HR & Training" --days 7 --limit 50
```

---

## Send Emails (with Attachments)

### Simple Email
```bash
python outlook_extractor.py send-email \
  --to "recipient@company.com" \
  --subject "Email Subject" \
  --body "Email message"
```

### Email with Multiple Recipients
```bash
python outlook_extractor.py send-email \
  --to "email1@company.com,email2@company.com" \
  --cc "manager@company.com" \
  --subject "Subject" \
  --body "Message"
```

### Email with File Attachment ✅
```bash
python outlook_extractor.py send-email \
  --to "recipient@company.com" \
  --subject "Data Collection" \
  --body "Please complete and return" \
  --attachment "C:\path\to\file.xlsx"
```

### Important: Attachment Requirements
- **Must use absolute path** (full path from C:\)
- **File must exist** before sending
- **Single attachment only** (send separate emails for multiple)

---

## Parameter Reference

| Parameter | Values | Example | Notes |
|-----------|--------|---------|-------|
| `--days` | Number | `--days 7` | How far back to search (default: 30) |
| `--limit` | Number | `--limit 50` | Max emails to return (default: 20) |
| `--folder` | `Inbox`, `Sent Items` | `--folder "Sent Items"` | Only for main folders |
| `--folder-search` | Text | `--folder-search "Production"` | Search subfolders by name |
| `--list-folders` | (flag) | `--list-folders` | Show all available folders |

---

## Common Mistakes & Fixes

| ❌ Wrong | ✅ Right | Why |
|---------|---------|-----|
| `emails-sent` | `emails --folder "Sent Items"` | Wrong command name |
| `--format json` | (output is JSON by default) | Parameter doesn't exist |
| `--folder Production` | `--folder-search "Production"` | `--folder` is for main folders only |
| `--days=7` | `--days 7` | Use space, not equals |
| `-days 7` | `--days 7` | Use double dash |
| `--list-folders --days 7` | `--list-folders` | Flags don't combine |

---

## When to Use Each Command

### Use `--folder "Sent Items"` When:
- Extracting emails **you sent**
- Checking sent communication history
- Reviewing drafts/sent items

### Use `--folder-search "keyword"` When:
- Searching across **all subfolders** with a name pattern
- Looking for emails from a specific site (N2, N3, Gloria)
- Searching for OEM/vendor emails (Epiroc, Komatsu, etc.)
- Don't know exact folder structure

### Use `--list-folders` When:
- Discovering available folder names first
- Confirming folder structure
- Planning which folders to search

---

## Daily Workflow Example

**Monday Morning - Review N2 Production**
```bash
# 1. Check N2 folder for new emails (last 24 hours)
python outlook_extractor.py emails --folder-search "NCH2" --days 1 --limit 20

# 2. Review sent emails to N2 contacts (last 7 days)
python outlook_extractor.py emails --folder "Sent Items" --days 7 --limit 50

# 3. Check Epiroc communications
python outlook_extractor.py emails --folder-search "Epiroc" --days 3 --limit 30
```

**Weekly Procurement Review**
```bash
# Get all procurement emails from past week
python outlook_extractor.py emails --folder-search "Procurement" --days 7 --limit 100

# Get OEM/vendor updates
python outlook_extractor.py emails --folder-search "OEMs" --days 7 --limit 100
```

**HR/Admin Tasks**
```bash
# HR communications
python outlook_extractor.py emails --folder-search "HR & Training" --days 7 --limit 50

# Time & Attendance
python outlook_extractor.py emails --folder-search "Time & Attendance" --days 7 --limit 20
```

---

## Output

All commands save results to:
- **File**: `outlook_emails.json`
- **Location**: Current working directory (`C:\Users\10064957\.claude\skills\outlook-extractor\scripts\`)
- **Format**: JSON array with fields:
  - `From` - Sender name
  - `Subject` - Email subject
  - `ReceivedTime` or `SentOn` - Timestamp
  - `Unread` - Read status (Inbox only)
  - `Attachments` - Count of attachments

---

## Troubleshooting

**Command hangs or takes >30 seconds?**
- Normal - Outlook COM API is slow
- Use smaller `--limit` values for faster results
- Run in background: `python outlook_extractor.py emails --days 1 --limit 20 &`

**"No emails found"?**
- Check folder name is correct
- Increase `--days` value (default: 30 days)
- Use `--list-folders` to verify folder exists

**"Subfolder not found"?**
- Run `--list-folders` to see exact folder names
- Folder names are case-sensitive in exact paths
- Use `--folder-search` instead for fuzzy matching

**Getting Unicode errors?**
- Cosmetic error only - files are saved successfully
- Check `outlook_emails.json` was created
- Verify with: `dir outlook_emails.json`

---

## Full Documentation

For complete documentation:
- **SKILL.md** – User guide with all workflows
- **commands.md** – All 8 commands with full parameters
- **workflows.md** – Real-world usage examples
- **troubleshooting.md** – Detailed error solutions

---

## Pro Tips

1. **Always start with `--list-folders`** to understand your folder structure
2. **Use small `--limit` values for testing** (e.g., `--limit 10`)
3. **Narrow `--days` for faster results** (e.g., `--days 1` for today's emails)
4. **Combine with background execution** for large searches:
   ```bash
   python outlook_extractor.py emails --folder-search "Production" --days 30 --limit 500 &
   ```
5. **Save results with timestamps** for tracking:
   ```bash
   # Manual: copy outlook_emails.json to dated filename
   copy outlook_emails.json outlook_emails_2025-11-23.json
   ```
