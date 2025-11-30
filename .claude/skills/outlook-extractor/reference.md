# Outlook Extractor - Technical Reference

**Version:** 2.0
**Last Updated:** 2025-11-10
**Purpose:** Technical deep-dive into Outlook calendar extraction implementation

This document provides implementation details for developers and technical troubleshooting. For user-facing documentation, see [SKILL.md](SKILL.md).

---

## Table of Contents

1. [Store Enumeration & Calendar Discovery](#store-enumeration--calendar-discovery)
2. [Recurring Event Expansion](#recurring-event-expansion)
3. [Recurring Event Exceptions](#recurring-event-exceptions)
4. [Parameter Reference](#parameter-reference)
5. [Implementation Details](#implementation-details)
6. [Troubleshooting](#troubleshooting)

---

## Store Enumeration & Calendar Discovery

### Overview

The outlook-extractor skill searches **ALL** Outlook stores (accounts/folders) to find calendar events, not just the default calendar. This is critical for accessing shared/delegated calendars like `Gregory.Karsten@assmang.co.za`.

### Discovery Process

**Step 1: Enumerate All Stores**
```python
stores = namespace.Stores
for store_idx in range(stores.Count):
    store = stores.Item(store_idx + 1)  # COM indexing starts at 1
```

**Step 2: Filter Excluded Stores**
```python
# Skip Archives and student accounts
if 'Archives' in store.DisplayName or 'student' in store.DisplayName.lower():
    continue
```

**Step 3: Find Calendar Folders**
```python
root_folder = store.GetRootFolder()
folders = root_folder.Folders

for folder in folders:
    # Check if folder is appointment type (DefaultItemType = 1)
    if hasattr(folder, 'DefaultItemType') and folder.DefaultItemType == 1:
        # Only process folders named "Calendar" (exclude subfolders)
        if folder.Name == 'Calendar':
            calendars_to_check.append(folder)
```

### Example Stores Discovered

In a typical corporate Outlook setup:

| Store Name | Type | Included? | Notes |
|------------|------|-----------|-------|
| `Gregory.Karsten` | Shared Calendar | ✅ Yes | Primary shared calendar |
| `gregory.karsten@assmang.co.za` | Mailbox | ✅ Yes | Personal mailbox calendar |
| `Archives` | Archive | ❌ No | Historical data excluded |
| `student@university.ac.za` | Test Account | ❌ No | Student account excluded |

### Exclusion Logic

**Why Exclude Archives?**
- Contains historical emails/events not relevant for current sync
- Significantly slows down enumeration
- Creates duplicate events from past

**Why Exclude Student Accounts?**
- Test/development accounts
- Not part of production workflow
- May contain irrelevant test data

### Fallback Behavior

If store enumeration fails (rare), the system falls back to:
```python
calendar = namespace.GetDefaultFolder(9)  # olFolderCalendar = 9
```

This ensures basic functionality even if advanced enumeration fails.

### Key Code Location

**File:** `outlook_extractor.py`
**Lines:** 200-230
**Method:** `get_calendar_events()`

---

## Recurring Event Expansion

### Overview

Recurring events in Outlook are stored as a single master item with a recurrence pattern. To display individual occurrences (e.g., "every Tuesday at 10:00"), we must **expand** the pattern into discrete events.

### Pattern Types

Outlook supports these recurrence types:

| Type | Enum Value | Description | Example |
|------|------------|-------------|---------|
| `olRecursDaily` | 0 | Daily with interval | Every 2 days |
| `olRecursWeekly` | 1 | Weekly on specific days | Every Monday & Friday |
| `olRecursMonthly` | 2 | Monthly by date | 15th of each month |
| `olRecursMonthNth` | 3 | Monthly by day | 2nd Tuesday of each month |
| `olRecursYearly` | 5 | Yearly by date | July 4th every year |
| `olRecursYearNth` | 6 | Yearly by day | Last Friday in December |

### Expansion Algorithm

**Step 1: Detect Recurring Event**
```python
if hasattr(item, 'IsRecurring') and item.IsRecurring:
    pattern = item.GetRecurrencePattern()
```

**Step 2: Extract Pattern Properties**
```python
pattern_start = pattern.PatternStartDate  # First occurrence
pattern_end = pattern.PatternEndDate      # Last occurrence (if finite)
recurrence_type = pattern.RecurrenceType  # Pattern type enum
interval = pattern.Interval               # Frequency multiplier
```

**Step 3: Calculate Occurrences Within Date Range**
```python
occurrence_date = pattern_start
while occurrence_date <= cutoff_date:
    # Skip if date is in deleted_dates (cancelled occurrences)
    if occurrence_date.date() in deleted_dates:
        occurrence_date = calculate_next_occurrence(occurrence_date, pattern)
        continue

    # Calculate datetime for this occurrence
    occurrence_start = datetime.combine(occurrence_date, item.Start.time())
    occurrence_end = datetime.combine(occurrence_date, item.End.time())

    # Check if occurrence is in our date range
    if occurrence_end >= start_date and occurrence_start <= cutoff_date:
        events.append({
            'Subject': item.Subject,
            'Start': str(occurrence_start),
            'End': str(occurrence_end),
            'Location': item.Location,
            'Organizer': item.Organizer
        })

    # Calculate next occurrence
    occurrence_date = calculate_next_occurrence(occurrence_date, pattern)
```

**Step 4: Calculate Next Occurrence by Pattern Type**
```python
def calculate_next_occurrence(current_date, pattern):
    if pattern.RecurrenceType == 0:  # Daily
        return current_date + timedelta(days=pattern.Interval)
    elif pattern.RecurrenceType == 1:  # Weekly
        return current_date + timedelta(weeks=pattern.Interval)
    elif pattern.RecurrenceType == 2:  # Monthly
        return current_date + timedelta(days=30 * pattern.Interval)  # Approximation
    elif pattern.RecurrenceType == 3:  # MonthNth
        return current_date + timedelta(days=30 * pattern.Interval)
    elif pattern.RecurrenceType == 5:  # Yearly
        return current_date + timedelta(days=365 * pattern.Interval)
    elif pattern.RecurrenceType == 6:  # YearNth
        return current_date + timedelta(days=365 * pattern.Interval)
```

### Example: Weekly Recurring Event

**Master Event:**
- Subject: "CAS L9 Activation Meeting"
- Pattern: Weekly, every Tuesday
- Start: Oct 28, 2025, 10:30 AM
- End: Oct 28, 2025, 11:00 AM
- Pattern Start: Oct 28, 2025
- Pattern End: Dec 31, 2025

**Expanded Occurrences (for Nov 10-22):**
- Nov 11, 2025 10:30-11:00 (Tuesday)
- Nov 18, 2025 10:30-11:00 (Tuesday)

**Skipped Occurrences:**
- Oct 28, Nov 4: Before sync date range
- Nov 25, Dec 2, etc.: After sync date range

### Key Code Location

**File:** `outlook_extractor.py`
**Lines:** 280-400
**Method:** `get_calendar_events()` - recurring event expansion loop

---

## Recurring Event Exceptions

### Overview

**Recurring event exceptions** are modifications to specific occurrences of a recurring event. This is one of the most critical and complex aspects of calendar sync.

### Types of Exceptions

1. **Rescheduled Occurrences**: Meeting moved to different time/date
2. **Deleted Occurrences**: Meeting cancelled/declined for that date
3. **Modified Occurrences**: Changed subject, location, or attendees for one instance

### The Problem

**Without exception handling:**
- Rescheduled meetings don't appear at new time
- Deleted/declined meetings still appear (ghost events)
- Modified meeting details don't sync

**Example:**
```
Base Pattern: Weekly team meeting, Fridays 10:00-11:00
Exception 1: Nov 10 rescheduled to Monday 14:00-15:00
Exception 2: Nov 17 cancelled (user declined)

Without exception handling:
❌ Nov 10 Friday 10:00-11:00 (wrong - actually Monday 14:00)
❌ Nov 17 Friday 10:00-11:00 (wrong - meeting was cancelled)
✅ Nov 24 Friday 10:00-11:00 (correct - normal occurrence)
```

### Exception Handling Process

#### Step 1: Get Pattern Exceptions
```python
try:
    pattern = item.GetRecurrencePattern()
    exceptions = pattern.Exceptions
except:
    # No recurring pattern or no exceptions
    pass
```

#### Step 2: Track Deleted/Declined Occurrences
```python
deleted_dates = set()

for exc_idx in range(exceptions.Count):
    exc = exceptions.Item(exc_idx + 1)  # COM indexing starts at 1

    # Check if this occurrence was deleted/declined
    if exc.Deleted:
        deleted_dates.add(exc.OriginalDate.date())
        continue  # Skip this exception - it's deleted
```

**Critical:** The `deleted_dates` set prevents creating events for cancelled occurrences later in the expansion loop.

#### Step 3: Process Rescheduled Occurrences
```python
for exc_idx in range(exceptions.Count):
    exc = exceptions.Item(exc_idx + 1)

    if exc.Deleted:
        continue  # Already handled in Step 2

    # Get the rescheduled appointment details
    if hasattr(exc, 'AppointmentItem'):
        appt = exc.AppointmentItem
        exc_start = appt.Start
        exc_end = appt.End

        # Normalize timezone (remove tzinfo)
        if exc_start.tzinfo is not None:
            exc_start = exc_start.replace(tzinfo=None)
        if exc_end.tzinfo is not None:
            exc_end = exc_end.replace(tzinfo=None)

        # Check if this rescheduled occurrence is in our date range
        if exc_end >= start_date and exc_start <= cutoff_date:
            event_data = {
                'Subject': appt.Subject,
                'Start': str(exc_start),      # Use rescheduled time
                'End': str(exc_end),          # Use rescheduled time
                'Location': appt.Location,
                'Organizer': appt.Organizer if hasattr(appt, 'Organizer') else item.Organizer
            }

            # Avoid duplicates
            if not any(e['Subject'] == event_data['Subject'] and
                      e['Start'] == event_data['Start'] for e in events):
                events.append(event_data)
```

#### Step 4: Expand Base Pattern (Skip Deleted Dates)
```python
occurrence_date = pattern.PatternStartDate

while occurrence_date <= cutoff_date:
    # CRITICAL: Skip this occurrence if it was deleted/declined
    occurrence_date_only = occurrence_date.date() if isinstance(occurrence_date, datetime) else occurrence_date

    if occurrence_date_only in deleted_dates:
        # Move to next occurrence without creating event
        occurrence_date = calculate_next_occurrence(occurrence_date, pattern)
        continue

    # Normal occurrence processing...
    occurrence_start = datetime.combine(occurrence_date, item.Start.time())
    occurrence_end = datetime.combine(occurrence_date, item.End.time())

    if occurrence_end >= start_date and occurrence_start <= cutoff_date:
        events.append({
            'Subject': item.Subject,
            'Start': str(occurrence_start),
            'End': str(occurrence_end),
            'Location': item.Location,
            'Organizer': item.Organizer
        })

    occurrence_date = calculate_next_occurrence(occurrence_date, pattern)
```

### Complete Example: Emergency Preparedness Meeting

**Base Pattern:**
- Subject: "Emergency Preparedness - Monthly Meeting"
- Pattern: Monthly, every 2nd Friday
- Time: 16:00-17:00 SAST
- Pattern Start: Oct 11, 2025 (Friday)

**Exceptions:**
- **Exception 1 (Nov 8)**: Original date, deleted (user declined)
- **Exception 2 (Nov 10)**: Rescheduled to Monday 14:00-15:00 (people unavailable on Friday)

**Processing:**

1. **Get exceptions**:
   - Exception 1: `exc.Deleted = True`, `OriginalDate = Nov 8`
   - Exception 2: `exc.Deleted = False`, `AppointmentItem.Start = Nov 10 14:00`

2. **Build deleted_dates set**:
   - `deleted_dates = {Nov 8}`

3. **Process rescheduled exception**:
   - Create event: Nov 10 Monday 14:00-15:00

4. **Expand base pattern**:
   - Oct 11 Friday: Before date range, skip
   - **Nov 8 Friday**: In `deleted_dates`, **SKIP** (no event created)
   - Dec 13 Friday: After date range, skip

**Result:**
- ✅ Nov 10 Monday 14:00-15:00 (rescheduled exception)
- ❌ Nov 8 Friday 16:00-17:00 (correctly skipped - was declined)

### Critical Implementation Details

**Type Checking for Date Comparison:**
```python
# COM API sometimes returns datetime, sometimes date object
occurrence_date_only = occurrence_date.date() if isinstance(occurrence_date, datetime) else occurrence_date

if occurrence_date_only in deleted_dates:
    # Skip this occurrence
```

**Why This Matters:**
- `deleted_dates` contains `date` objects
- `occurrence_date` may be `datetime` object
- Comparison fails without normalization: `datetime(2025-11-08 16:00) != date(2025-11-08)`

**Duplicate Prevention:**
```python
# Check if event already exists before adding
if not any(e['Subject'] == event_data['Subject'] and
          e['Start'] == event_data['Start'] for e in events):
    events.append(event_data)
```

### Debugging Recurring Event Issues

**Symptom:** Meeting appears when it should be deleted/declined

**Check:**
1. Is `exc.Deleted` being checked?
2. Is `deleted_dates` set being populated?
3. Is date comparison working (datetime vs date type issue)?
4. Is `deleted_dates` check happening BEFORE creating occurrence?

**Symptom:** Rescheduled meeting appears at wrong time

**Check:**
1. Is `exc.AppointmentItem` being accessed?
2. Are we using `appt.Start` and `appt.End` (rescheduled times)?
3. Is timezone normalization happening correctly?

### Key Code Location

**File:** `outlook_extractor.py`
**Lines:** 289-358
**Method:** `get_calendar_events()` - exception handling section

---

## Parameter Reference

### `--days N`

**Purpose:** Number of days ahead to check for events

**Default:** `7`

**Usage:**
```bash
python outlook_extractor.py calendar --days 30
```

**Example:**
- Today: Nov 10
- `--days 7`: Extract events Nov 10 - Nov 17
- `--days 30`: Extract events Nov 10 - Dec 10

---

### `--limit N`

**Purpose:** Maximum number of events to return

**Default:** `20`

**Usage:**
```bash
python outlook_extractor.py calendar --limit 200
```

**Notes:**
- Set higher for full calendar sync
- Set lower for quick checks
- No performance impact (filtering happens after extraction)

---

### `--from-week-start`

**Purpose:** Include events from Monday of current week, not just from today forward

**Default:** `False` (start from today)

**Usage:**
```bash
python outlook_extractor.py calendar --days 30 --from-week-start
```

**When to Use:**
- Syncing on Wednesday but need Monday/Tuesday events
- Getting full week context for reporting
- After missing sync on Monday/Tuesday
- Reviewing what happened earlier in the week

**Behavior:**
1. Calculate current weekday: `now.weekday()` (0=Monday, 6=Sunday)
2. Calculate days since Monday: `days_since_monday`
3. Set start to Monday 00:00:00: `now - timedelta(days=days_since_monday)`
4. Extract events from Monday through `today + days_ahead`

**Example:**

**Scenario 1: Without `--from-week-start`**
```bash
# Today: Wednesday, Nov 13
python outlook_extractor.py calendar --days 7

# Extracts: Nov 13 (Wed) → Nov 20 (Wed)
# Missing: Nov 11 (Mon) and Nov 12 (Tue) events
```

**Scenario 2: With `--from-week-start`**
```bash
# Today: Wednesday, Nov 13
python outlook_extractor.py calendar --days 7 --from-week-start

# Extracts: Nov 11 (Mon) → Nov 20 (Wed)
# Includes: All events from start of week
```

**Implementation:**
```python
if from_week_start:
    days_since_monday = now.weekday()  # 0=Mon, 1=Tue, ..., 6=Sun
    week_start = now - timedelta(days=days_since_monday)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = week_start
else:
    start_date = now
```

**Key Code Location:**
**File:** `outlook_extractor.py`
**Lines:** 183-193
**Method:** `get_calendar_events()`

---

## Implementation Details

### Timezone Handling

**Outlook COM API:** Returns times in UTC (UTC+0)
**Display in Outlook UI:** Converted to local time (SAST UTC+2) by Windows
**MarthaVault:** All times stored in SAST (UTC+2)

**Conversion:**
```python
# Outlook COM returns: 2025-11-10 12:00:00 UTC
# Display as: 2025-11-10 14:00:00 SAST (UTC+2)
```

**Timezone Normalization:**
```python
if exc_start.tzinfo is not None:
    exc_start = exc_start.replace(tzinfo=None)
```

**Why:** COM API sometimes includes timezone info, sometimes doesn't. Normalize to naive datetime for consistency.

---

### Performance Characteristics

**Store Enumeration:**
- Time: ~200ms per store
- Impact: Negligible for 2-5 stores
- Optimization: Store exclusion (Archives) reduces load

**Recurring Event Expansion:**
- Time: ~10ms per recurring event
- Impact: Linear with number of recurring events
- Optimization: Break loop when occurrence_date > cutoff_date

**Exception Processing:**
- Time: ~5ms per exception
- Impact: Minimal (most events have 0-2 exceptions)

**Total Extraction Time:**
- Small calendar (20 events): ~500ms
- Medium calendar (100 events): ~2s
- Large calendar (500 events): ~10s

---

## Troubleshooting

### Issue: No events extracted

**Check:**
1. Is Outlook running?
2. Is default calendar populated?
3. Are all stores showing as "Archives" or "student" (excluded)?
4. Is date range correct (past events not included unless `--from-week-start`)?

**Debug:**
```bash
python outlook_extractor.py calendar --days 30 --limit 500 --from-week-start
```

---

### Issue: Recurring events appear once or not at all

**Check:**
1. Is `item.IsRecurring` property being checked?
2. Is `GetRecurrencePattern()` succeeding?
3. Is pattern start date within extraction range?
4. Are occurrences being calculated correctly?

**Debug:**
Look for log output: "Recurring event: [Subject], expanding..."

---

### Issue: Deleted meeting still appears

**Check:**
1. Is exception handling enabled?
2. Is `exc.Deleted` being checked?
3. Is `deleted_dates` set populated?
4. Is date comparison working (datetime vs date type)?

**Critical Fix:**
```python
# Ensure type compatibility
occurrence_date_only = occurrence_date.date() if isinstance(occurrence_date, datetime) else occurrence_date
if occurrence_date_only in deleted_dates:
    continue  # Skip this occurrence
```

---

### Issue: Rescheduled meeting appears at wrong time

**Check:**
1. Is `exc.AppointmentItem` being accessed?
2. Are exception times being used instead of base pattern times?
3. Is timezone normalization correct?

**Debug:**
Log exception details:
```python
print(f"Exception: {exc.AppointmentItem.Subject}")
print(f"  Original: {exc.OriginalDate}")
print(f"  Rescheduled: {exc.AppointmentItem.Start}")
```

---

## Related Documentation

- **User Guide:** [SKILL.md](SKILL.md)
- **System Architecture:** `reference/claude-code/2025-10-21 – Calendar Automation System.md`
- **Obsidian Plugin Config:** `reference/claude-code/2025-11-10 – Obsidian Full Calendar Configuration.md`
- **Sync Command:** `.claude/commands/sync-outlook-calendar.md`

---

## Version History

**v2.0 (2025-11-10)**
- Added store enumeration with Archives/student exclusion
- Implemented recurring event expansion
- Added recurring event exception handling (rescheduled & deleted)
- Added `--from-week-start` parameter
- Comprehensive documentation of all features

**v1.0 (2025-10-21)**
- Initial implementation
- Basic calendar extraction
- Single store support
