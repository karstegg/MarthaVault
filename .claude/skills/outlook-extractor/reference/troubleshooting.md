# Outlook Extractor - Troubleshooting Guide

## Common Issues & Solutions

### 1. "Error connecting to Outlook"

**Error Message:**
```
✗ Error connecting to Outlook: [COM error]
```

**Causes:**
- Outlook not running
- Outlook crashed or hung
- Windows COM layer issue

**Solutions:**

Step 1: Verify Outlook is running
```bash
# Check Windows Task Manager for "OUTLOOK.EXE"
# Or look for Outlook window on screen
```

Step 2: If not running, open Outlook
```
- Click Start menu
- Search for "Outlook"
- Launch Microsoft Outlook
```

Step 3: If already running, restart Outlook
```
- Close Outlook completely
- Wait 5 seconds
- Reopen Outlook
- Try script again
```

Step 4: Restart Windows if COM layer is broken
```
- Save all work
- Restart computer
- Open Outlook before running script
```

**Prevention:**
- Always keep Outlook running while using this skill
- Close and reopen Outlook if you experience issues

---

### 2. "Invalid recipient email"

**Error Message:**
```
✗ Error sending email: [Recipient not found or invalid]
```

**Causes:**
- Typo in email address
- Email address not in Outlook's address book
- Invalid email format

**Solutions:**

Step 1: Verify email format
```bash
# CORRECT: user@company.com
# WRONG: user@company (missing domain)
# WRONG: user.company.com (missing @)
# WRONG: user @company.com (space in email)
```

Step 2: Check Outlook address book
```
- In Outlook, go to "People" tab
- Search for recipient name
- Confirm email address matches
```

Step 3: Use full email addresses
```bash
# BAD - relies on Outlook knowing abbreviation:
--to "xavier"

# GOOD - explicit full address:
--to "xavier.petersen@company.com"
```

Step 4: For external recipients, add to Contacts first
```
- In Outlook, go to "People" tab
- Add contact with correct email
- Try sending again
```

**Example of correct usage:**
```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --subject "Test" \
  --body "Test message"
```

---

### 3. "Attachment not found"

**Error Message:**
```
✗ Error sending email: Attachment not found: /path/to/file
```

**Causes:**
- File path doesn't exist
- Using relative path instead of absolute path
- File was moved or deleted

**Solutions:**

Step 1: Use absolute file paths
```bash
# WRONG - relative path:
--attachment "Reports/quarterly.pdf"

# CORRECT - absolute path:
--attachment "C:\Users\10064957\Documents\Reports\quarterly.pdf"
```

Step 2: Verify file exists
```bash
# In File Explorer, navigate to folder
# Confirm file is there
# Right-click file → Properties → Full path
# Copy exact path into command
```

Step 3: Check for spaces in path
```bash
# If path has spaces, ensure it's quoted:
--attachment "C:\Users\10064957\My Documents\file name.pdf"
```

Step 4: Use UNC paths for network files
```bash
# Network drive file:
--attachment "\\server\share\folder\file.pdf"
```

**Correct example:**
```bash
python outlook_extractor.py send-email \
  --to "user@company.com" \
  --subject "Report" \
  --body "Attached report" \
  --attachment "C:\Reports\Q4_2025.pdf"
```

---

### 4. Email extraction returns 0 emails

**Symptom:**
```
Found 0 emails
```

But you can see emails in Outlook inbox.

**Causes:**
- Date filter is too restrictive
- Date range doesn't match current emails
- Timezone comparison failing (historical bug)

**Solutions:**

Step 1: Check date range
```bash
# Try extracting from last 90 days:
python outlook_extractor.py emails --days 90 --limit 50

# Try extracting from last 365 days:
python outlook_extractor.py emails --days 365 --limit 50
```

Step 2: Increase limit dramatically
```bash
# Try getting more items:
python outlook_extractor.py emails --days 30 --limit 1000
```

Step 3: Extract all without date filtering
```bash
# Query all via the API:
python outlook_extractor.py emails --days 3650 --limit 10000
```

Step 4: Check if emails are archived
```
- In Outlook, verify you're viewing "Inbox"
- Not "All Mail" or Archive folder
- Right-click folder → Folder properties → item count
```

Step 5: Verify Outlook sync
```
- Check Outlook → File → Account Settings → Data Files
- Verify inbox OST file is present and recent
- File → Options → Advanced → Outlook data files
```

**Historical Note:** Earlier versions had a bug where `break` instead of `continue` would terminate the loop prematurely on date comparison errors. This is fixed in the current version.

---

### 5. Calendar extraction shows no events

**Symptom:**
```
Found 0 events
```

But calendar has meetings in Outlook.

**Causes:**
- Looking ahead when meetings are in past
- Date range doesn't match
- Meetings not saved properly

**Solutions:**

Step 1: Verify current date
```bash
# Check your system date:
# Windows: Show date/time in system tray

# Outlook meetings in past won't show
# Must specify future date range
```

Step 2: Increase lookahead period
```bash
# Default is 7 days:
python outlook_extractor.py calendar --days 7 --limit 100

# Try 30 days:
python outlook_extractor.py calendar --days 30 --limit 100

# Try 365 days:
python outlook_extractor.py calendar --days 365 --limit 100
```

Step 3: Refresh Outlook calendar
```
- In Outlook, go to Calendar tab
- Press Ctrl+Shift+U (refresh)
- Try extraction again
```

Step 4: Check calendar visibility
```
- In Outlook, verify calendar is visible
- Not hidden or minimized
- Meetings appear in calendar view
```

---

### 6. pywin32 module not found

**Error Message:**
```
ModuleNotFoundError: No module named 'win32com'
```

**Cause:** pywin32 not installed

**Solution:**

Step 1: Install pywin32
```bash
pip install pywin32 --upgrade
```

Step 2: Verify installation
```bash
python -c "import win32com.client; print('✓ Installed')"
```

Step 3: If still fails, check Python path
```bash
# Verify correct Python version:
python --version

# Should be 3.7 or higher
# If you have multiple Python installations, ensure using correct one
```

Step 4: Use absolute path to Python if needed
```bash
# Find Python installation:
where python

# Use full path:
C:\Users\10064957\AppData\Local\Programs\Python\Python311\python.exe outlook_extractor.py emails
```

---

### 7. "Unicode encoding error" on Windows console

**Error Message:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Cause:** Windows console using cp1252 encoding instead of UTF-8

**Solution:**

The script handles this automatically:
```python
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')  # Change to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
```

If you still see errors:

Step 1: Manually set console encoding
```bash
chcp 65001
python outlook_extractor.py emails
```

Step 2: Use PowerShell instead of Command Prompt
```
- Right-click Start menu
- Select "Windows PowerShell (Admin)"
- Run script from there
```

---

### 8. "Meeting not visible in Outlook"

**Symptom:**
```
✓ Meeting created successfully
```

But meeting doesn't appear in calendar.

**Causes:**
- Calendar needs refresh
- Meeting created in wrong calendar
- Outlook needs restart

**Solutions:**

Step 1: Refresh calendar
```
- In Outlook, go to Calendar tab
- Press Ctrl+Shift+U (or F9)
- Wait 5 seconds for refresh
```

Step 2: Check calendar selection
```
- Look at left sidebar in Outlook
- Verify your calendar is checked (blue checkmark)
- All calendars should be visible
```

Step 3: Restart Outlook
```
- Close Outlook
- Wait 10 seconds
- Reopen Outlook
- Check calendar
```

Step 4: Check dates carefully
```
# Make sure meeting date is correct:
python outlook_extractor.py calendar --days 365 | grep "Meeting Title"

# If not found, meeting was created for different date
```

---

### 9. "Email appears in draft, not sent"

**Symptom:**
```
✓ Email sent successfully
```

But email is in Drafts folder, not Sent.

**Cause:** Email object not fully sent (rare race condition)

**Solution:**

Step 1: Check Drafts folder
```
- In Outlook, open Drafts folder
- Look for your email
- Right-click → Send (if needed)
```

Step 2: Restart Outlook and retry
```
- Close Outlook
- Reopen
- Send email again
```

Step 3: Check Outlook Offline Status
```
- Verify Outlook is not in "Offline" mode
- Check status bar at bottom of Outlook window
- Should show "Online"
```

---

### 10. "Outlook crashes when sending email"

**Symptom:**
```
✓ Email sent successfully
```

Then Outlook crashes.

**Causes:**
- Large attachment size
- Corrupted attachment file
- Outlook memory issue

**Solutions:**

Step 1: Check attachment size
```
# Outlook can have issues with files >100MB
# Use smaller files or split large files

# Check file size:
# Right-click file → Properties → Size
```

Step 2: Try sending without attachment first
```bash
python outlook_extractor.py send-email \
  --to "user@company.com" \
  --subject "Test" \
  --body "Testing"

# If that works, issue is with attachment
```

Step 3: Repair Outlook
```
- Close Outlook completely
- Windows Start → Settings
- Apps → Apps & Features
- Find "Microsoft Office"
- Click → Modify
- Select "Quick Repair" or "Online Repair"
- Wait for repair to complete
- Restart Outlook
```

Step 4: Restart Windows
```
- If crashes continue, restart your computer
- This clears COM state
```

---

### 11. "Permission denied" errors

**Error Message:**
```
Error: Permission denied
```

**Causes:**
- Outlook running in restricted mode
- File permission issue on attachment
- Antivirus blocking

**Solutions:**

Step 1: Check Outlook restricted mode
```
- Close Outlook
- Restart computer
- Reopen Outlook normally
- Try script again
```

Step 2: Check file permissions
```
- Right-click attachment file
- Properties → Security → Edit
- Ensure your user has "Full Control"
- Click Apply
```

Step 3: Disable antivirus temporarily
```
- Some antivirus software blocks COM API
- Temporarily disable to test
- If script works, add to antivirus whitelist
```

Step 4: Use administrator command prompt
```
- Right-click Command Prompt
- Select "Run as administrator"
- Run script from there
```

---

## Performance Optimization

### Slow email extraction?

**Tips to speed up:**
```bash
# 1. Reduce date range:
python outlook_extractor.py emails --days 7 --limit 50

# 2. Reduce limit:
python outlook_extractor.py emails --days 30 --limit 20

# 3. Close other apps:
# Free up RAM by closing browser, IDE, etc

# 4. Archive old emails:
# Move emails older than 2 years to archive
# Makes active inbox smaller
```

### Slow calendar extraction?

```bash
# 1. Reduce days ahead:
python outlook_extractor.py calendar --days 7 --limit 50

# 2. Archive past meetings:
# Delete old meetings from calendar
```

---

## Diagnostic Commands

### Check Outlook connection:
```bash
python -c "import win32com.client; o = win32com.client.GetActiveObject('Outlook.Application'); print('✓ Connected'); print(f'Version: {o.Version}')"
```

### List all Outlook folders:
```python
import win32com.client
o = win32com.client.GetActiveObject('Outlook.Application')
ns = o.GetNamespace('MAPI')
for folder in ns.Folders:
    print(folder.Name, folder.Items.Count)
```

### Check specific folder item count:
```python
import win32com.client
o = win32com.client.GetActiveObject('Outlook.Application')
ns = o.GetNamespace('MAPI')
inbox = ns.GetDefaultFolder(6)
print(f'Inbox items: {inbox.Items.Count}')
```

---

## When to Escalate

If you've tried all steps above and issue persists:

1. **Note the exact error message**
2. **Save the command you ran**
3. **Note your Outlook version**
4. **Note your Windows version**
5. **Contact IT support with this information**

Provide details like:
```
Issue: Email extraction returns 0 results
Outlook Version: 2021 (Build 16.0.14326.2024)
Windows: Windows 10 Pro (Build 19045)
Command: python outlook_extractor.py emails --days 7 --limit 50
Error: None (runs but shows 0 emails)
Actions Tried: Restarted Outlook, verified inbox has emails, tried --days 90
```

---

## Related Documentation

- See `implementation.md` for technical architecture details
- See `SKILL.md` for command reference and examples
- See `scripts/outlook_extractor.py` source code comments for implementation details
