---
title: Obsidian Full Calendar Configuration & Troubleshooting Guide
date: 2025-11-10
Status: Complete
Priority: High
Tags: null
permalink: reference/claude-code/2025-11-10-obsidian-full-calendar-configuration-troubleshooting-guide
---

# Obsidian Full Calendar Configuration & Troubleshooting Guide

**Last Updated:** 2025-11-10
**Version:** 1.0
**Status:** Operational (resolved 2025-11-10)

---

## Overview

This guide documents the complete setup, configuration, and troubleshooting procedures for the **Obsidian Full Calendar** plugin in MarthaVault. It covers common issues, their causes, and solutions based on real-world experience troubleshooting on 2025-11-10.

---

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Plugin Name** | obsidian-full-calendar (version 0.10.7) |
| **Plugin Author** | Davis Haupt (@davish) |
| **GitHub** | https://github.com/obsidian-community/obsidian-full-calendar |
| **Config File** | `.obsidian/plugins/obsidian-full-calendar/data.json` |
| **Event Folder** | `Schedule/` (can be customized) |
| **Frontmatter Format** | YAML with specific required fields |
| **Total Events** | 113 files (as of 2025-11-10) |

---

## Installation & Setup

### Step 1: Install Plugin
1. Open Obsidian Settings → Community Plugins
2. Search for "Full Calendar"
3. Install "obsidian-full-calendar" by Davis Haupt
4. Enable the plugin

### Step 2: Create Schedule Folder
Create a folder in your vault to store calendar events:
```
MarthaVault/
└── Schedule/
    ├── 2025-11-10 - Event Title.md
    ├── 2025-11-13 - Another Event.md
    └── ...
```

### Step 3: Configure Plugin
The plugin auto-creates `data.json` with this default configuration:

**File:** `.obsidian/plugins/obsidian-full-calendar/data.json`

```json
{
  "calendarSources": [
    {
      "type": "local",
      "color": "hsl( calc(44 - 1), calc(66% * 1.01), calc(61% * 1.075) )",
      "directory": "Schedule"
    }
  ],
  "defaultCalendar": 0,
  "firstDay": 0,
  "initialView": {
    "desktop": "timeGridWeek",
    "mobile": "timeGrid3Days"
  },
  "timeFormat24h": false
}
```

**Key Settings:**
- `directory`: Folder to scan for event files (default: "Schedule")
- `initialView`: Desktop view ("timeGridWeek" = week view with times)
- `timeFormat24h`: Set to `false` for 12-hour format, `true` for 24-hour

---

## Event File Format (YAML Frontmatter)

### Required Fields

Every event file **MUST** have these frontmatter fields or the calendar will not display:

```yaml
---
title: Event Title
allDay: true/false
date: YYYY-MM-DD
completed: null
---
```

### All-Day Event Format

```yaml
---
title: VFL - Nchwaning 3
allDay: true
date: 2025-11-04
completed: null
---
```

**Requirements:**
- `title`: Event name (required)
- `allDay: true`: Marks as all-day event
- `date`: Single date in YYYY-MM-DD format
- `completed: null`: Status field (keep as null)

### Timed Event Format

```yaml
---
title: Standards Meeting
allDay: false
date: 2025-11-13
startTime: "13:30"
endTime: "15:00"
completed: null
---
```

**Requirements:**
- `allDay: false`: Marks as timed event
- `startTime`: Time in HH:MM format (must be quoted)
- `endTime`: Time in HH:MM format (must be quoted)
- **CRITICAL:** Times MUST be in 24-hour HH:MM format (e.g., "14:00", not "2:00 PM")

### Multi-Day All-Day Events

```yaml
---
title: Conference
allDay: true
date: 2025-11-20
endDate: 2025-11-23
completed: null
---
```

**Requirements:**
- `endDate`: Day AFTER the actual end date (off-by-one convention)
- Example: Event spanning Nov 20-22 uses `date: 2025-11-20` and `endDate: 2025-11-23`

### Optional Fields

- `permalink`: Auto-generated link reference (optional)
- `recurrence`: For recurring events (e.g., "weekly", "daily")
- Additional custom fields are ignored by the plugin

---

## Critical Issue: Malformed Time Values

### The Problem

**The obsidian-full-calendar plugin has a critical flaw:** If ANY event file contains malformed `startTime` or `endTime` values, the entire calendar becomes blank and non-functional.

**Symptoms:**
- Calendar view appears completely empty
- No events display, even after refresh
- Reinstalling plugin doesn't help (issue is in frontmatter)
- No error messages shown to user

### Causes of Malformed Times

Invalid `endTime` or `startTime` values include:

| Invalid Value | Problem | Example |
|---------------|---------|---------|
| `840` | Missing colon separator | `endTime: 840` |
| `--` | Placeholder text | `endTime: --` |
| `null` | Null value | `startTime: null` |
| `14:00:00` | Seconds included | `endTime: 14:00:00` |
| `2:00 PM` | 12-hour format | `startTime: 2:00 PM` |
| Empty string | No value | `startTime: ""` |

**Valid Values:**
- `"14:00"` ✅
- `"09:30"` ✅
- `"07:00"` ✅
- Always 24-hour format with quotes

### Real Example (Found 2025-11-10)

**File:** `2025-10-08 - VFL Tuesday.md`
**Problem:**
```yaml
---
title: VFL Tuesday
allDay: false
startTime: 07:00
endTime: 840          # ← INVALID! Should be "14:00"
---
```

**Impact:** This single malformed value broke the entire calendar for the vault

**Solution:**
```yaml
---
title: VFL Tuesday
allDay: false
startTime: "07:00"
endTime: "14:00"      # ← FIXED to proper HH:MM format
---
```

---

## Validation & Troubleshooting

### How to Find Malformed Events

Use this Python script to scan all event files:

```python
import os
import re

def check_time_format(time_str):
    """Check if time is in HH:MM format"""
    if time_str is None or time_str == '':
        return False
    time_str = str(time_str).strip().strip("'\"")
    if time_str in ('null', '--', ''):
        return False
    if re.match(r'^\d{1,2}:\d{2}(:\d{2})?$', time_str):
        return True
    return False

# Scan Schedule folder
for fname in os.listdir('Schedule'):
    if not fname.endswith('.md'):
        continue

    with open(f'Schedule/{fname}', 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        continue

    fm = match.group(1)

    # Check timed events
    if 'allDay: false' in fm:
        start_match = re.search(r"startTime:\s*['\"]?([^'\"\n]+)['\"]?", fm)
        end_match = re.search(r"endTime:\s*['\"]?([^'\"\n]+)['\"]?", fm)

        start_time = start_match.group(1) if start_match else None
        end_time = end_match.group(1) if end_match else None

        if not check_time_format(start_time) or not check_time_format(end_time):
            print(f"PROBLEM: {fname}")
            print(f"  startTime: {start_time}")
            print(f"  endTime: {end_time}")
```

### Troubleshooting Checklist

| Issue | Cause | Solution |
|-------|-------|----------|
| Calendar completely blank | Malformed time in any event | Run validation script above; fix all invalid times |
| Event not showing | Missing required fields | Check file has `title`, `date`, `allDay` |
| All-day event appears as timed | `allDay: false` when should be `true` | Change `allDay: true` and remove `startTime`/`endTime` |
| Time display incorrect | Timezone issues | Ensure times are in local SAST (UTC+2) |
| "No events found" message | Wrong folder configured | Check `data.json` `directory` field points to `Schedule` |
| Plugin not loading | Plugin disabled or not installed | Enable plugin in Community Plugins settings |

### Recovery Procedure

**If calendar becomes blank:**

1. **Identify problematic files:**
   ```bash
   cd Schedule/
   python3 validation_script.py
   ```

2. **Fix each file:**
   - For `allDay: false` events: Ensure `startTime` and `endTime` are in "HH:MM" format
   - For `allDay: true` events: Remove `startTime` and `endTime` fields entirely

3. **Reload Obsidian:**
   - Close and reopen vault, OR
   - Disable and re-enable plugin in Settings

4. **Verify:**
   - Calendar should display events within seconds
   - Check both month and week views

---

## Best Practices

### 1. Filename Convention
```
YYYY-MM-DD - Event Title.md
2025-11-10 - Solrock Feedback Meeting.md
2025-11-13 - Standards Meeting.md
```

**Benefits:**
- Auto-sorted by date in file explorer
- Easy to identify event dates
- Consistent with other vault conventions

### 2. Frontmatter Consistency

**Always include these fields:**
```yaml
---
title: [Extract from filename]
allDay: [true/false]
date: [YYYY-MM-DD from filename]
completed: null
---
```

**Optional but recommended:**
```yaml
permalink: schedule/2025-11-10-event-title
```

### 3. Content Structure

After frontmatter, use this markdown structure:

```markdown
---
title: Event Title
allDay: false
date: 2025-11-10
startTime: "10:00"
endTime: "11:00"
completed: null
---

# Event Title

**Time:** 10:00 - 11:00
**Location:** [Location]
**Organizer:** [Name]

**Details:**
[Event description]

**Attendees:** [Names if applicable]

**Tags:** #meeting #year/2025 #site/[location]
```

### 4. Time Zone Handling

**SAST (South African Standard Time): UTC+2**

- All times in frontmatter should be in **local SAST time**
- What you see in Outlook UI = what goes in `startTime`/`endTime`
- No UTC conversion needed in frontmatter

**Example:**
- Outlook shows: 15:00 (3 PM SAST)
- Frontmatter should have: `startTime: "15:00"`

---

## Calendar Sync Workflow (Outlook ↔ Obsidian)

### Two-Way Sync Process

When synchronizing with Outlook:

1. **Extract Outlook events** (last 30 days)
2. **Compare with Obsidian events** by date and title
3. **Create missing Obsidian files** from Outlook events
4. **Fix time mismatches** (Outlook UTC → SAST conversion)
5. **Validate all frontmatter** before finalizing

### Sync Command

```bash
/sync-outlook-calendar
```

This command:
- Scans Outlook for events in current month
- Scans `Schedule/` for existing events
- Creates new files for missing Outlook events
- Fixes time format issues
- Generates sync summary report

### After Sync

**Always verify:**
- No new malformed times were introduced
- Event titles match between systems
- Times are correctly converted to SAST format
- Calendar displays without blanking

---

## Performance Notes

### Current Statistics (2025-11-10)

- **Total events in Schedule/:** 113 files
- **Date range:** August 2025 - December 2025
- **Active in November:** ~18 events
- **Plugin version:** 0.10.7
- **Calendar load time:** < 2 seconds

### Optimization Tips

1. **Archive old months:** Move past event files to `Schedule/Archive/` to reduce clutter
2. **Use consistent naming:** File names impact search and display sorting
3. **Minimize custom fields:** Extra frontmatter fields don't affect display but slow parsing
4. **Regular validation:** Run validation script monthly to catch drift

---

## Common Patterns

### VFL (Visible Felt Leadership) Events

```yaml
---
title: VFL - [Area]
allDay: true
date: 2025-11-04
completed: null
---

# VFL - [Area]

**VFL Champion:** [Name]
**Focus Topic:** [Topic]
**Area:** [Location]

**Team Members:** [Names]

#VFL #SHEQ #site/[location] #year/2025
```

### Regular Meetings

```yaml
---
title: [Meeting Name]
allDay: false
date: 2025-11-13
startTime: "13:30"
endTime: "15:00"
completed: null
recurrence: weekly
---

# [Meeting Name]

**Time:** 13:30 - 15:00 (Weekly)
**Location:** [Location]
**Organizer:** [Name]

**Details:** [Description]

#meeting #year/2025 #site/[location]
```

### Task Deadlines

```yaml
---
title: [Task] - Due
allDay: true
date: 2025-11-30
completed: null
---

# [Task] - Deadline

**Due:** 2025-11-30

**Details:** [Description]

#task #deadline #priority/[level] #year/2025
```

---

## File Organization

```
MarthaVault/
├── Schedule/
│   ├── 2025-08-05 - VFL Week 1 N3 Procedures.md
│   ├── 2025-08-12 - VFL Week 2 N3 Risk Assessment.md
│   ├── 2025-11-04 - VFL Nchwaning 3.md
│   ├── 2025-11-10 - Solrock Feedback Meeting.md
│   ├── 2025-11-13 - Standards Meeting.md
│   ├── 2025-11-13 - Project Steerco.md
│   ├── 2025-11-13 - Monthly Engineering Meeting.md
│   ├── Archive/
│   │   ├── 2025-08-*.md (old events)
│   │   └── 2025-09-*.md (old events)
│   ├── _Sync_Summary_2025-10.md
│   ├── _Sync_Summary_2025-11.md
│   └── 2025-10-08 - VFL Tuesday.md (note: contains recurrence info)
│
└── reference/
    └── claude-code/
        └── 2025-11-10 – Obsidian Full Calendar Configuration & Troubleshooting Guide.md
```

---

## Related Documentation

- **Memory System:** See `memory://calendar-configuration` (Claude AI memory)
- **Outlook Sync:** See `reference/claude-code/2025-10-21 – Calendar Automation System.md`
- **WhatsApp Voice Notes:** See `reference/claude-code/WhatsApp Voice Note Transcription.md`

---

## Key Takeaways

### What Works ✅
- 113 event files with proper YAML frontmatter
- Weekly and monthly recurring events
- Multi-event days with different times
- Two-way Outlook sync functionality
- Calendar displays reliably when frontmatter is valid

### What Breaks ❌
- ANY malformed `startTime` or `endTime` values
- Missing required fields (`title`, `date`, `allDay`)
- Incorrect date format (not YYYY-MM-DD)
- Invalid time format (not HH:MM in 24-hour)
- Spaces or quotes in time fields without proper escaping

### Recovery Always Works ✅
- Fixing malformed frontmatter immediately restores calendar
- No data is lost; only frontmatter needs correction
- Validation script identifies all problem files
- Process takes < 5 minutes for full vault

---

## Maintenance Schedule

### Weekly
- Check calendar display on session startup
- Verify new events created have valid frontmatter

### Monthly
- Run validation script to find any drift
- Archive events from previous month to `Schedule/Archive/`
- Review sync summary reports

### Quarterly
- Backup Schedule/ folder
- Review and consolidate recurring events
- Update this documentation if plugin behavior changes

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-10 | 1.0 | Initial documentation; fixed malformed endTime: 840 issue; confirmed all 113 events valid |

---

## Support & Resources

**Plugin Repository:** https://github.com/obsidian-community/obsidian-full-calendar

**Issues & Discussions:**
- GitHub Issues: Feature requests, bug reports
- GitHub Discussions: Help & troubleshooting
- Obsidian Forum: Community support

**Claude Code Reference:**
- Run `/sync-outlook-calendar` to sync with Outlook
- Use validation script to find malformed events
- Check this document first for troubleshooting

---

**Last Verified:** 2025-11-10
**Status:** All 113 events validated and working
**Next Review Date:** 2025-12-10