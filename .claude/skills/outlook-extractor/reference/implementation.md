# Outlook Extractor - Technical Implementation Reference

## Architecture Overview

The outlook-extractor skill provides programmatic access to Microsoft Outlook through the Windows Component Object Model (COM) API, specifically using the `pywin32` library's `win32com.client` interface.

```
User Request
    ↓
SKILL.md (instructions loaded)
    ↓
Python Script (outlook_extractor.py)
    ↓
win32com.client (COM bridge)
    ↓
Outlook.Application (COM object)
    ↓
MAPI Namespace (mail data access)
    ↓
Outlook Data (Inbox, Calendar, Contacts)
    ↓
JSON Output
```

## COM API Fundamentals

### Component Object Model (COM)

COM is Windows' native interface for inter-process communication. Outlook exposes itself as a COM object that can be controlled programmatically.

**Key Classes:**
- `Outlook.Application` - Main Outlook application object
- `Namespace` - Access to MAPI data stores
- `MailItem` - Individual email messages
- `AppointmentItem` - Calendar events/meetings
- `ContactItem` - Contact records

### MAPI (Messaging Application Programming Interface)

MAPI is the underlying protocol for mail access. The namespace represents the MAPI namespace which provides access to:
- Inbox (folder ID 6)
- Calendar (folder ID 9)
- Contacts (folder ID 10)
- Other folders as needed

**Folder Constants:**
```python
6  = Inbox
9  = Calendar
10 = Contacts
```

## Email Extraction Process

### Step 1: Connection
```python
outlook = win32com.client.GetActiveObject("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
```

This establishes a connection to the running Outlook instance. `GetActiveObject` ensures we connect to an already-running Outlook rather than creating a new instance.

### Step 2: Folder Access
```python
inbox = namespace.GetDefaultFolder(6)
items = inbox.Items
items.Sort("[ReceivedTime]", False)  # Sort by received time, descending
```

The Items collection represents all messages in the folder.

### Step 3: Date Filtering

**Challenge**: Inbox may contain thousands of emails. Need efficient filtering.

**Solution**: Iterate through sorted collection and apply date filter:

```python
cutoff_date = datetime.now() - timedelta(days=days_back)

for item in items:
    received_time = item.ReceivedTime

    # Normalize timezone (critical fix)
    if received_time.tzinfo is not None:
        received_time = received_time.replace(tzinfo=None)
    if cutoff_date.tzinfo is not None:
        cutoff_date = cutoff_date.replace(tzinfo=None)

    # Skip older emails, continue checking newer ones
    if received_time < cutoff_date:
        continue  # BUG FIX: Was 'break' which terminated loop prematurely
```

**Important Bug History**: Original code used `break` which terminated the entire loop when encountering an old email. This was wrong because:
1. Email collections aren't always perfectly sorted
2. When timezone comparison fails, `break` stops checking all remaining items
3. Should use `continue` to skip individual items and keep checking

### Step 4: Data Extraction

For each qualifying email:
```python
email_data = {
    'From': item.SenderName,
    'Subject': item.Subject,
    'ReceivedTime': str(item.ReceivedTime),
    'Unread': item.Unread,
    'Attachments': item.Attachments.Count
}
```

### Step 5: Output

Save to JSON file for further processing:
```python
with open('outlook_emails.json', 'w', encoding='utf-8') as f:
    json.dump(emails, f, indent=2, ensure_ascii=False)
```

## Calendar Event Extraction

Similar process to emails:

```python
calendar = namespace.GetDefaultFolder(9)
items = calendar.Items
items.Sort("[Start]")

now = datetime.now()
cutoff_date = now + timedelta(days=days_ahead)

for item in items:
    # Only future events within range
    if item.Start < now or item.Start > cutoff_date:
        continue

    event_data = {
        'Subject': item.Subject,
        'Start': str(item.Start),
        'End': str(item.End),
        'Location': item.Location,
        'Organizer': item.Organizer
    }
```

**Key Difference from Emails**: Calendar uses forward-looking date filter (next N days) vs backward-looking for emails (last N days).

## Email Sending Process

### Step 1: Create MailItem
```python
mail = self.outlook.CreateItem(0)  # 0 = MailItem
```

### Step 2: Set Importance (Priority)
```python
priority_map = {'low': 5, 'normal': 3, 'high': 2}
mail.Importance = priority_map.get(priority.lower(), 3)
```

Outlook uses numeric importance levels:
- 2 = High priority
- 3 = Normal priority
- 5 = Low priority

### Step 3: Add Recipients
```python
# TO recipients
for to_email in to_list:
    mail.Recipients.Add(to_email)

# CC recipients
for cc_email in cc_list:
    recipient = mail.Recipients.Add(cc_email)
    recipient.Type = 2  # 2 = CC

# BCC recipients
for bcc_email in bcc_list:
    recipient = mail.Recipients.Add(bcc_email)
    recipient.Type = 3  # 3 = BCC
```

Recipient types in Outlook:
- 1 = To
- 2 = CC
- 3 = BCC

### Step 4: Add Content
```python
mail.Subject = subject
mail.Body = body
```

### Step 5: Add Attachments
```python
if attachment:
    # Validate file exists first
    if not os.path.exists(attachment):
        raise FileNotFoundError(f"Attachment not found: {attachment}")

    mail.Attachments.Add(attachment)
```

File path must be absolute path.

### Step 6: Resolve and Send
```python
mail.Recipients.ResolveAll()  # Validate all recipients
mail.Send()
```

ResolveAll() ensures all recipient addresses are valid and known to Outlook's address book.

## Meeting Creation Process

### Step 1: Create AppointmentItem
```python
meeting = self.outlook.CreateItem(1)  # 1 = AppointmentItem
```

### Step 2: Set Basic Properties
```python
meeting.Subject = subject
meeting.Start = start_time
meeting.End = end_time
meeting.Location = location
```

### Step 3: Add Body/Notes
```python
if body:
    meeting.Body = body
```

### Step 4: Add Attendees
```python
for attendee_email in attendee_list:
    meeting.Recipients.Add(attendee_email)

meeting.Recipients.ResolveAll()
```

### Step 5: Save
```python
meeting.Save()
```

Important: Use `Save()` not `Send()` for appointments unless sending meeting invitations.

## Meeting Deletion Process

### Step 1: Access Calendar
```python
calendar = self.namespace.GetDefaultFolder(9)  # 9 = Calendar
items = calendar.Items
```

### Step 2: Find the Meeting
```python
for item in items:
    if item.Subject == subject:
        # Verify it's the right one by checking start time
        item_start = item.Start
        if item_start.tzinfo is not None:
            item_start = item_start.replace(tzinfo=None)

        if item_start == start_time.replace(tzinfo=None):
            # Found the right meeting
            break
```

**Important**: Use both subject AND start time for matching to ensure we delete the correct meeting. Same subject can occur multiple times at different times.

### Step 3: Delete the Item
```python
item.Delete()
```

This removes the appointment from the calendar immediately.

### Step 4: Error Handling
If meeting not found:
```python
print(f"✗ Meeting not found: {subject} at {start_time}")
return False
```

**Why match on both fields:**
- Subject alone: Could match multiple meetings with same name
- Time alone: Could match meetings with different names but same time
- Both: Uniquely identifies the exact meeting to delete

## Timezone Handling

### The Problem

Outlook's COM API returns timezone-aware datetime objects (with UTC offset), while Python's `datetime.now()` returns naive objects (no timezone info).

```python
# Outlook returns this:
2025-10-20T09:30:00+00:00  # Timezone-aware

# Python's datetime.now() returns this:
2025-10-20T09:30:00  # Timezone-naive

# Comparison raises error:
if received_time < cutoff_date:  # ValueError!
    pass
```

### The Solution

Normalize both sides to naive datetime objects before comparison:

```python
def normalize_datetime(dt):
    """Remove timezone info for comparison"""
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

# Usage:
received_time = normalize_datetime(item.ReceivedTime)
cutoff_date = normalize_datetime(cutoff_date)

if received_time < cutoff_date:  # Now safe
    continue
```

This approach works because:
1. Outlook stores times in UTC
2. We're doing local comparisons (same timezone throughout)
3. Stripping timezone info preserves the absolute time correctly

## Performance Characteristics

### Email Extraction

- **Inbox with 8,813 items**: ~2-3 seconds for `--limit 50 --days 1`
- **Bottleneck**: COM API iteration is sequential (can't parallelize)
- **Optimization**: Sort descending by date, break early when possible

### Calendar Extraction

- **100 events**: <1 second
- **1,000 events**: 2-3 seconds
- **Bottleneck**: Fewer items to iterate, generally faster

### Email Sending

- **Simple email**: <2 seconds
- **With attachment**: 2-5 seconds (file I/O dependent)

### Meeting Creation

- **Simple meeting**: <1 second
- **With many attendees**: Still <1 second (recipients resolved async)

## Error Handling Strategy

### Connection Errors
```python
try:
    outlook = win32com.client.GetActiveObject("Outlook.Application")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

**Cause**: Outlook not running
**Solution**: Ensure Outlook is open before running

### Recipient Resolution Errors
```python
try:
    mail.Recipients.ResolveAll()
except Exception as e:
    print(f"Invalid recipient: {e}")
```

**Cause**: Invalid email address or not in address book
**Solution**: Validate email format, check address book

### Attachment Errors
```python
if not os.path.exists(attachment):
    raise FileNotFoundError(f"Attachment not found: {attachment}")
```

**Cause**: File path doesn't exist or is relative path
**Solution**: Use absolute file path, verify file exists

### Date Comparison Errors
```python
# Normalize timezone before comparison
if dt.tzinfo is not None:
    dt = dt.replace(tzinfo=None)
```

**Cause**: Comparing timezone-aware and naive datetimes
**Solution**: Normalize both to naive before comparison

## Known Issues & Workarounds

### Issue 1: Email Extraction Returns 0 Results

**Symptoms**: Extraction shows "Found 0 emails" despite visible emails

**Root Cause**: Date filtering logic terminates loop prematurely

**Workaround**: Ensure using `continue` not `break` for date filtering

**Status**: Fixed in current version

### Issue 2: Calendar vs Email Sync Mismatch

**Symptoms**: Calendar shows current events but emails appear old

**Root Cause**: Different sync paths in Outlook's cache

**Workaround**: Check Exchange account settings for sync range

**Note**: Not a code issue, Outlook configuration issue

### Issue 3: Unicode Encoding on Windows Console

**Symptoms**: UTF-8 characters display as garbage or errors

**Workaround**:
```python
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')
```

## Testing Coverage

### What's Tested

✅ Email extraction with date filtering
✅ Calendar event extraction
✅ Contact extraction
✅ Email sending with CC/BCC/attachments
✅ Meeting creation with attendees
✅ Timezone handling
✅ File attachment validation
✅ Error handling for missing Outlook

### Test Scenarios

1. **Empty inbox**: Returns empty list gracefully
2. **Large inbox (8,813 items)**: Extracts successfully with date filter
3. **Invalid email addresses**: Shows error, continues with valid ones
4. **Missing attachment file**: Returns error before sending
5. **Outlook not running**: Returns clear error message
6. **Old Python version**: Shows pywin32 installation requirement

## Future Enhancement Opportunities

1. **Parallel Processing**: Use threading to process multiple items faster
2. **Search API**: Use Outlook's search rather than iteration
3. **HTML Email Support**: Set mail.HTMLBody instead of Body
4. **Email Scheduling**: Set mail.DeferredDeliveryTime for delayed send
5. **Recurring Meetings**: Set AppointmentItem recurrence patterns
6. **Read Receipts**: Set mail.ReadReceiptRequested
7. **Auto-Signature**: Include mail.HTMLBody with signature
8. **Batch Operations**: Process multiple operations in single connection

## Architecture Decisions

### Why pywin32 over other libraries?

- **Official**: Microsoft-supported COM bridge
- **Comprehensive**: Full access to Outlook object model
- **Reliable**: Long-standing library (stable APIs)
- **Alternative**: Python-UNO (LibreOffice), but less suitable for Outlook

### Why JSON output vs direct database?

- **Portable**: JSON works across all platforms
- **Flexible**: Can pipe to other tools
- **Debuggable**: Human-readable format
- **Stateless**: No side effects from extraction

### Why sync vs async execution?

- **Simplicity**: Easier to debug and troubleshoot
- **Predictability**: No race conditions
- **COM API**: Not thread-safe anyway
- **Performance**: Adequate for typical use cases

## Debugging Tips

### Enable detailed error messages:
```python
import traceback

try:
    # COM operation
except Exception as e:
    traceback.print_exc()
    print(f"Detailed error: {e}")
```

### Print COM object properties:
```python
print(dir(item))  # List all properties
print(f"Property: {item.PropertyName}")  # Check specific property
```

### Use Outlook's UI to verify operations:
After sending email or creating meeting, check Outlook UI to confirm

### Check Windows Event Viewer:
Outlook COM errors sometimes logged in Windows Event Viewer

## Related Documentation

- See `SKILL.md` for user-facing commands and workflows
- See `troubleshooting.md` for common issues and solutions
- See `scripts/outlook_extractor.py` for implementation details
