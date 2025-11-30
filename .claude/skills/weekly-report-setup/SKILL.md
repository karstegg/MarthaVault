---
name: Weekly Report Setup
description: Automates steps 1-5 of weekly report generation - folder creation, email finding, and attachment downloading (max 300 chars)
---

# Weekly Report Setup Skill

Automates the first 5 steps of your weekly mining report workflow: creates week folders, finds weekly report emails from your contacts, downloads all attachments, and saves N2 email body for Claude to parse.

## When to Use This Skill

Use this skill at the **beginning of each week** when you're ready to start the weekly report generation process. It handles:
- Creating the Week XX folder
- Finding emails from N2, N3, Gloria, and Shafts & Winders contacts
- Downloading the Epiroc BEV report email
- Retrieving all file attachments (skips inline images)
- Saving N2 email body for Claude to parse into HEAL format

**Time Saved**: ~15-20 minutes of manual email searching and attachment downloading per week

## Usage

### Auto-Detect Current Week (with Confirmation)
```bash
/weekly-report-setup
```

The skill will:
1. Calculate the current fiscal week (Week 1 = July 1, 2025)
2. Show you the week dates
3. Ask for confirmation before proceeding
4. Search for emails from that week

**Example output:**
```
Detected Week 18 (Oct 27 - Nov 02, 2025)
Proceed? (Y/n): y
```

### Specify Week Manually (No Prompt)
```bash
/weekly-report-setup --week=18
```

Skips confirmation and directly processes Week 18.

## Prerequisites

**Before running:**

1. ✅ **Outlook must be open** - The skill uses Outlook COM API and requires an active Outlook instance
2. ✅ **Python 3.7+** installed with pywin32 package
3. ✅ **Windows operating system** - COM API only works on Windows
4. ✅ **Base folder exists** - `Weekly Reports` folder in your OneDrive

**If pywin32 is missing:**
```bash
pip install pywin32 --upgrade
```

## Setup Process

### What Happens When You Run the Skill

```
WEEKLY REPORT SETUP - Steps 1-5 Automation
============================================

[1/5] Determining Week Number
  Week dates: Mon, Oct 27 - Sun, Nov 02, 2025
  Report send date (Friday): Fri, Oct 31, 2025

[2/5] Creating Week 18 folder
  ✓ Week 18 folder ready: ....\Weekly Reports\Week 18

[3/5] Searching for weekly report emails
  Searching for N2 Report...
    From: Sikele Nzuza
    ✓ Found: N2 Weekly Report October 23-25
    Date: 2025-10-26 14:30:00
    Downloading 1 attachment(s)
    ✓ Downloaded: N2 Eng Report Week 17 Oct -23 Oct 25.xlsx

  [Similar for N3, Gloria, S&W, and Epiroc...]

[4/5] Saving N2 email body for Claude to parse...
  ✓ Saved N2 email body: N2 Email Body - Week18.txt
    → Claude will parse this to create N2 HEAL Page Week18.txt

[5/5] Setup Summary
  Week folder: ....\Weekly Reports\Week 18
  Files downloaded: 8
  ✓ Setup complete!
```

## Email Search Logic

The skill **recursively searches all Inbox subfolders** (up to 3 levels deep) and looks for emails based on **dual sender matching** (name OR email address, case-insensitive) with **subject keyword filtering**:

| Site | Contact | Email | Subject Keywords | Date Range |
|------|---------|-------|------------------|------------|
| N2 | Sikelela Nzuza | Sikelela.Nzuza@assmang.co.za | "weekly report", "eng report", "nch2", "n2" | Friday→Monday |
| N3 | Sello Sease | Sello.Sease@assmang.co.za | "weekly report", "eng report", "nch3", "n3" | Friday→Monday |
| Gloria | Sipho Dubazane | Sipho.Dubazane@assmang.co.za | "weekly report", "eng report", "gloria" | Friday→Monday |
| Shafts & Winders | Xavier Petersen | Xavier.Petersen@assmang.co.za | "weekly report", "shafts", "winders", "s&w" | Friday→Monday |
| Epiroc BEV | Phillip Moller | phillip.moller@epiroc.com | "brmo weekly report", "weekly report", "bev" | Friday→Monday |

**Search Strategy**:
- **Recursively searches Inbox + all subfolders** (up to 3 levels deep)
- **Date range**: Friday of the report week through Monday (4-day window)
- **Dual matching**: Sender name OR email address (case-insensitive)
- **Subject filtering**: Must contain at least one keyword from the list
- **Optimization**: Uses Outlook Restrict() for 10-100x faster searching
- Takes the most recent email from each sender that matches all criteria

## Output Files

All files are downloaded to: `Week XX/` folder in your Weekly Reports directory

### Downloaded Attachments
Attachments are saved with **original filenames** preserved:
- `N2 Eng Report Week XX Oct -23 Oct XX.xlsx`
- `N3 Eng Report Week XX Oct -XX Oct XX.xlsx`
- `Gloria Eng Report Week XX-23 Oct 2025.xlsx`
- `Weekly Report Shafts and Winders 2025_XX_XX-XXOct2025.xlsx`
- `BRMO weekly report LIVE XX October 2025 - XX October 2025.pdf`
- `Heal N3 week XX - 23 Oct 2025.pptx`
- `Gloria HEAL page (XXX).pptx`
- `SHAFTS AND WINDERS_HEAL_XX_WEEK_XX-XXOct2025.pptx`

### N2 HEAL Extraction (Two-Step Process)

**Step 1 - Automatic (Python Script)**:
- Saves raw email body to: `N2 Email Body - WeekXX.txt`

**Step 2 - Manual Request (Ask Claude)**:
- Tell Claude: "Parse the N2 email body for Week XX and create the HEAL page"
- Claude creates: `N2 HEAL Page WeekXX.txt` with formatted sections:
  - Highlight
  - Emerging Issues
  - Actions
  - Lowlights
- Claude automatically deletes: `N2 Email Body - WeekXX.txt` (cleanup)

## Validation & Error Handling

### Success Indicators ✓
- All emails found and attachments downloaded
- Inline images skipped (not downloaded)
- N2 email body saved for Claude parsing
- Week folder created successfully

### Warnings ⚠
- **Missing Email**: If an expected email isn't found, the skill notes it but continues
  - Example: "⚠ Missing: Gloria Report"
  - Skill does NOT stop - you can download that file manually later
- **No Attachments**: If an email has no attachments, it's noted but process continues
- **Inline Images Skipped**: "ℹ Skipped X inline image(s)" - this is normal and expected
- **Epiroc Inline PDF**: If Epiroc PDF is marked as inline, standard filtering will skip it
  - Message: "ℹ Skipped 2 inline image(s)"
  - Workaround: Use manual COM API to force download (see Troubleshooting section)

### Error Recovery

**If Outlook connection fails:**
- Make sure Outlook is open
- Check that you're on a Windows PC
- Verify pywin32 is installed: `pip install pywin32 --upgrade`

**If email not found:**
- The skill searches 10 days back - emails older than that won't be found
- Check sender name spelling matches exactly (case-insensitive)
- Download the file manually and place in Week XX folder

**If attachment download fails:**
- Outlook may have temporarily locked the file
- Try running the skill again
- Or download manually from Outlook

## Next Steps After Running

✓ **Skill completes Step 5** - All emails and attachments are ready

**Continue with Steps 6-12** - Run extraction skills in this order:

1. **Extract Primary Equipment Data**
   ```bash
   /extract-primary-equipment n2 18
   /extract-primary-equipment n3 18
   /extract-primary-equipment gloria 18
   ```

2. **Extract Maintenance Compliance**
   ```bash
   /extract-maintenance-compliance n2 18
   /extract-maintenance-compliance n3 18
   /extract-maintenance-compliance gloria 18
   ```

3. **Extract BEV Data**
   ```bash
   /extract-bev --week=18
   ```

4. **Extract Epiroc BEV Report**
   ```bash
   /extract-epiroc-bev-report --week=18
   ```

5. **Extract HEAL Pages**
   ```bash
   /extract-pptx-heal n3 18
   /extract-pptx-heal gloria 18
   /extract-pptx-heal shafts-winders 18
   ```

6. **Extract Shafts & Winders Data**
   ```bash
   /extract-shafts-winders 18
   ```

## Fiscal Week Calendar

**Week 1 Start Date**: July 1, 2025

The skill calculates weeks as:
- Week 1: Jul 01 - Jul 07, 2025
- Week 2: Jul 08 - Jul 14, 2025
- Week 17: Oct 20 - Oct 26, 2025
- Week 18: Oct 27 - Nov 02, 2025
- ... and so on

Each Friday is the email send date for the following week's reports.

## Common Issues & Troubleshooting

### "Error connecting to Outlook"
- **Cause**: Outlook is not open or not installed
- **Solution**: Open Microsoft Outlook and try again

### "No contacts found matching 'Sikele Nzuza'"
- **Cause**: Sender name doesn't match exactly (case-insensitive matching still requires correct spelling)
- **Solution**: Verify the contact name in Outlook matches the expected name

### "Detected Week 17... but I need Week 18"
- **Cause**: Fiscal calendar calculation based on today's date
- **Solution**: Use manual week: `/weekly-report-setup --week=18`

### "N2 Email Body file is still in the folder"
- **Cause**: Claude hasn't been asked to parse it yet
- **Solution**: Tell Claude "Parse the N2 email body for Week XX" - Claude will create the HEAL page and delete the intermediate file

### Email found but attachments not downloading
- **Cause**: Outlook file locking or permissions issue
- **Solution**: Close and reopen Outlook, then try skill again

### "Epiroc email found but PDF skipped as inline image"
- **Cause**: Outlook classifies PDF attachments as "inline" if they're referenced in email body, skill filters these out
- **Workaround (Week 21)**: Use manual COM API script to force download all attachments regardless of classification
- **Solution (Week 22+)**: Enhanced skill will attempt unfiltered download if standard download fails
- **Known Issue**: Temporary Outlook image file (Outlook-jxnzcdic.png) may be downloaded - safe to delete
- **Status**: ✅ Fix planned for Week 22+ - currently requires manual intervention

## FAQ

**Q: What if I miss an email?**
A: The skill continues even if emails are missing. You can download those files manually later and place them in the Week XX folder.

**Q: Can I run this for past weeks?**
A: Yes, use `--week=16` to specify a past week number. The skill will search the last 10 days for emails.

**Q: Does this send any emails?**
A: No, this skill only downloads and extracts. It never sends anything.

**Q: How do I get the N2 HEAL page created?**
A: After the script finishes, tell Claude "Parse the N2 email body for Week XX and create the HEAL page". Claude will read the raw email body, extract the HEAL sections, and create the formatted file automatically.

**Q: How long does this take?**
A: Usually 2-5 minutes depending on email size and your internet speed.

## Technical Details

For implementation details, see `reference.md` in the skill directory.
