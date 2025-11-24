---
'Status:': Reference
'Priority:': High
'Tags:': null
'Created:': 2025-10-21
permalink: reference/claude-code/2025-10-21-calendar-automation-system
---

# Calendar Automation System

## Overview

Automated calendar synchronization system for MarthaVault that maintains a unified calendar across Obsidian and Microsoft Outlook.

**Core Principle:** Single source of truth - events exist in BOTH places, always in sync.

---

## System Components

### 1. Slash Commands

#### `/sync-outlook-calendar`
**Purpose:** Two-way synchronization between Obsidian and Outlook
**Location:** `.claude/commands/sync-outlook-calendar.md`

**Functionality:**
- Outlook → Obsidian: Meetings created in Outlook appear in vault
- Obsidian → Outlook: Events created in vault appear in Outlook
- Syncs current month only
- Fuzzy matching to prevent duplicates
- Creates detailed sync summary report

**Manual Usage:**
```
/sync-outlook-calendar
```

#### `/process-vfl-schedule`
**Purpose:** Extract VFL schedule from PDF and create calendar events
**Location:** `.claude/commands/process-vfl-schedule.md`

**Functionality:**
- Reads VFL schedule PDF (uses Claude's native PDF reading)
- Identifies weeks where Greg is scheduled
- Creates Obsidian calendar events in `Schedule/`
- Creates Outlook calendar meetings
- Moves PDF to `reference/SHEQ/VFL_Schedules/`
- Generates processing summary

**Manual Usage:**
```
/process-vfl-schedule
```

### 2. Hooks (Automatic Triggers)

All hooks configured in: `.claude/settings.local.json`

#### SessionStart Hook
**Trigger:** When Claude Code session starts or resumes
**Action:** Executes `/sync-outlook-calendar`
**Purpose:** Sync all Outlook meetings into Obsidian on startup

**Configuration:**
```json
"SessionStart": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "/sync-outlook-calendar",
        "timeout": 60
      }
    ]
  }
]
```

**Behavior:**
- Runs automatically every time Claude Code starts
- Syncs current month events (two-way)
- Completes in < 60 seconds
- Ensures Obsidian calendar is up-to-date with Outlook

#### PostToolUse Hook #1: Schedule Event Sync
**Trigger:** When Claude creates/edits files in `Schedule/` folder
**Action:** Executes `/sync-outlook-calendar`
**Purpose:** Immediately sync new Obsidian events to Outlook

**Configuration:**
```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "bash -c 'if [[ \"$TOOL_INPUT\" =~ Schedule/ ]]; then echo \"/sync-outlook-calendar\"; fi'",
      "timeout": 30
    }
  ]
}
```

**Behavior:**
- Detects when Claude uses Write or Edit tool on Schedule/ files
- Automatically syncs to Outlook
- Ensures immediate two-way consistency

#### PostToolUse Hook #2: VFL Schedule Processing
**Trigger:** When VFL schedule PDF appears in `00_Inbox/`
**Action:** Executes `/process-vfl-schedule`
**Purpose:** Automatically process VFL schedules when they arrive

**Configuration:**
```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "bash -c 'if [[ \"$TOOL_INPUT\" =~ \"VFL Schedule\" ]] && [[ \"$TOOL_INPUT\" =~ \"00_Inbox\" ]]; then echo \"/process-vfl-schedule\"; fi'",
      "timeout": 30
    }
  ]
}
```

**Behavior:**
- Detects when VFL schedule PDF written to inbox
- Automatically extracts Greg's weeks
- Creates calendar events in both systems
- Moves PDF to archive

---

## Workflows

### Primary Workflow: Create Event via Claude

**User says:** "Create a meeting tomorrow at 2pm with Xavier about capital planning"

**What happens:**
1. ✅ Claude creates Obsidian event: `Schedule/2025-10-22 - Meeting with Xavier.md`
2. ✅ PostToolUse hook detects Write tool used on Schedule/ folder
3. ✅ Hook triggers `/sync-outlook-calendar`
4. ✅ Sync command creates matching Outlook meeting
5. ✅ **Result:** Event exists in BOTH Obsidian and Outlook immediately

**Time:** < 10 seconds total

### Secondary Workflow: Manual Obsidian Creation

**User manually creates/edits** event in Obsidian (outside Claude)

**What happens:**
1. ⏳ Event exists in Obsidian only (not detected immediately)
2. ⏳ User continues work in Obsidian
3. ✅ Next Claude Code session starts
4. ✅ SessionStart hook triggers `/sync-outlook-calendar`
5. ✅ Sync command detects new Obsidian event, creates in Outlook
6. ✅ **Result:** Event now in BOTH systems

**Time:** Synced on next session start (or manual `/sync-outlook-calendar`)

### Outlook-Driven Workflow: Schedule Meeting in Outlook

**User schedules meeting** in Outlook (normal workflow with invites, etc.)

**What happens:**
1. ✅ Event created in Outlook
2. ⏳ User starts Claude Code (or it's already running)
3. ✅ SessionStart hook triggers `/sync-outlook-calendar`
4. ✅ Sync command detects new Outlook event, creates in Obsidian
5. ✅ **Result:** Event appears in vault as `Schedule/YYYY-MM-DD - [Event].md`

**Time:** Synced on next session start

### VFL Schedule Workflow: PDF Arrives

**New VFL schedule PDF** arrives (email, shared drive, etc.)

**What happens:**
1. ✅ User places PDF in `00_Inbox/VFL Schedule - Oct 2025.pdf`
2. ✅ User says: "Process the VFL schedule" (or it auto-detects)
3. ✅ Claude executes `/process-vfl-schedule`
4. ✅ PDF parsed, Greg's weeks identified
5. ✅ Obsidian events created in `Schedule/`
6. ✅ PostToolUse hook detects Schedule/ writes
7. ✅ Outlook events created automatically
8. ✅ PDF moved to `reference/SHEQ/VFL_Schedules/`

**Time:** < 30 seconds total

---

## File Locations

### Slash Commands
```
.claude/commands/
├── process-vfl-schedule.md
└── sync-outlook-calendar.md
```

### Hook Configuration
```
.claude/settings.local.json
└── hooks: { SessionStart, PostToolUse }
```

### Calendar Events (Obsidian)
```
Schedule/
├── 2025-10-21 - VFL Black Rock.md
├── 2025-10-22 - Meeting with Xavier.md
├── 2025-10-25 - Board Meeting.md
└── _Sync_Summary_2025-10.md (sync report)
```

### VFL Schedules (Archive)
```
reference/SHEQ/VFL_Schedules/
├── VFL Schedule - Aug 2025.pdf
├── VFL Schedule - Sep 2025.pdf
└── VFL Schedule - Oct 2025.pdf
```

### Outlook Integration (Skill)
```
~/.claude/skills/outlook-extractor/
└── scripts/outlook_extractor.py
```

---

## Event Formats

### Obsidian Calendar Event

**Filename:** `Schedule/YYYY-MM-DD - Event Title.md`

**Template:**
```markdown
---
title: Event Title
allDay: true
date: YYYY-MM-DD
completed: null
---

# Event Title

**Time:** HH:MM - HH:MM (if not all-day)
**Location:** Location name

**Details:**
Event description and context

**Tags:** #meeting #category #year/2025
```

### Outlook Calendar Event

Created via outlook-extractor skill:
- Subject: Event title
- Start: YYYY-MM-DD HH:MM (SAST local time)
- End: YYYY-MM-DD HH:MM
- Location: Location field
- Body: Full details from Obsidian event
- Timezone: SAST (UTC+2)

---

## Duplicate Prevention

### Fuzzy Matching Algorithm

Events are considered **duplicates** if:
1. Same date (YYYY-MM-DD)
2. Similar title (normalized comparison)

**Title normalization:**
- Remove punctuation (-, :, ., etc.)
- Convert to lowercase
- Remove extra spaces
- Ignore "the", "a", "an"

**Examples of matches:**
```
"VFL - Black Rock" ≈ "VFL Black Rock"
"Team Meeting" ≈ "team meeting"
"Review Session: Capital" ≈ "Review Session Capital"
```

**Match threshold:** 80% similarity on same date

### Duplicate Handling

**Before creating any event:**
1. ✅ Search for existing event on same date
2. ✅ Normalize titles and compare
3. ✅ If match found, skip creation
4. ✅ Log in sync summary

**Result:** No duplicates even with multiple sync runs

---

## Sync Summary Reports

### Location
`Schedule/_Sync_Summary_YYYY-MM.md`

### Contents
- Sync timestamp
- Events scanned (Outlook and Obsidian)
- Events already in sync
- New events created (both directions)
- Events skipped (duplicates)
- Errors encountered
- Summary statistics

### Example
```markdown
# Calendar Sync Summary - October 2025

**Sync Date:** 2025-10-21 08:00:00
**Sync Type:** Two-Way (Outlook ↔ Obsidian)

## Sync Statistics
- Outlook events scanned: 15
- Obsidian events scanned: 12
- Events already in sync: 10
- Events created in Obsidian: 5
- Events created in Outlook: 2

✅ Sync completed successfully
```

---

## Troubleshooting

### Issue: "Outlook not running"
**Error:** Can't connect to Outlook API
**Solution:**
1. Start Microsoft Outlook
2. Retry sync command
3. Check outlook-extractor skill prerequisites

### Issue: "Duplicate events created"
**Symptom:** Same event appears multiple times
**Solution:**
1. Check sync summary for match details
2. Verify fuzzy matching is working
3. Manually delete duplicates
4. Run sync again (should skip duplicates)

### Issue: "Hook not triggering"
**Symptom:** Events created but not synced automatically
**Solution:**
1. Check `.claude/settings.local.json` hook configuration
2. Verify JSON syntax is valid
3. Restart Claude Code session
4. Test with manual slash command first

### Issue: "Times incorrect in Outlook"
**Symptom:** Event times off by hours
**Solution:**
1. Verify using SAST (UTC+2) times
2. Check Outlook timezone settings
3. Ensure not converting UTC unnecessarily
4. All times should be local SAST

### Issue: "VFL schedule not processing"
**Symptom:** PDF in inbox but no events created
**Solution:**
1. Manually run `/process-vfl-schedule`
2. Check PDF format matches expected structure
3. Verify Greg's name appears in team lists
4. Review processing summary for errors

---

## Configuration

### Hook Timeouts
- SessionStart: 60 seconds
- PostToolUse (Schedule sync): 30 seconds
- PostToolUse (VFL processing): 30 seconds

### Sync Window
- Current month only (first day to last day)
- Can be extended via command arguments (future)

### Event Types Handled
- ✅ All-day events (allDay: true)
- ✅ Timed events (specific start/end)
- ✅ Recurring events (all occurrences expanded)
- ✅ Recurring event exceptions (rescheduled/deleted occurrences)
- ✅ Events with attendees
- ✅ Events with locations
- ✅ VFL schedule events
- ✅ Shared/delegated calendars

### Excluded from Sync
- Past months (historical events)
- Far future events (> 2 months out)
- Completed events (completed: true)
- Explicitly marked as local-only
- Archive calendars
- Student/test accounts

---

## Advanced Calendar Extraction Features

### Store Enumeration & Multi-Calendar Support

**Problem:** Default Outlook calendar API only accesses the default calendar, missing shared/delegated calendars like `Gregory.Karsten@assmang.co.za`.

**Solution:** outlook-extractor skill enumerates **all** Outlook stores (accounts/folders) to find calendar events.

**Process:**
1. Enumerate all stores: `namespace.Stores`
2. Filter out excluded stores (Archives, student accounts)
3. Search each store for Calendar folders
4. Extract events from all discovered calendars

**Benefit:** Captures events from:
- Shared calendars (e.g., Gregory.Karsten)
- Delegated access calendars
- Multiple mailboxes

**Technical Details:** See [outlook-extractor/reference.md](~/.claude/skills/outlook-extractor/reference.md#store-enumeration--calendar-discovery)

---

### Recurring Event Expansion

**Problem:** Recurring events stored as single master item with pattern, need individual occurrences for sync.

**Solution:** outlook-extractor expands recurring patterns into discrete events within date range.

**Supported Patterns:**
- Daily (every N days)
- Weekly (specific days of week)
- Monthly (by date or by day)
- Yearly (by date or by day)

**Example:**
```
Master Event: "CAS L9 Meeting" - Weekly, every Tuesday 10:30-11:00
Date Range: Nov 10-22, 2025

Expanded Occurrences:
- Nov 11, 2025 10:30-11:00
- Nov 18, 2025 10:30-11:00
```

**Technical Details:** See [outlook-extractor/reference.md](~/.claude/skills/outlook-extractor/reference.md#recurring-event-expansion)

---

### Recurring Event Exceptions

**Problem:** Rescheduled or cancelled occurrences of recurring events must be handled separately from base pattern.

**Solution:** outlook-extractor processes exceptions to override base pattern.

**Exception Types:**
1. **Rescheduled occurrences:** Meeting moved to different time/date
2. **Deleted occurrences:** Meeting cancelled/declined for that date
3. **Modified occurrences:** Changed subject/location for one instance

**Example:**
```
Base Pattern: Weekly team meeting, Fridays 10:00-11:00
Exception 1: Nov 10 rescheduled to Monday 14:00-15:00
Exception 2: Nov 17 cancelled (declined)

Result:
- Nov 10 Monday 14:00-15:00 ✅ (rescheduled)
- Nov 17 Friday 10:00-11:00 ❌ (skipped - deleted)
- Nov 24 Friday 10:00-11:00 ✅ (normal occurrence)
```

**Technical Details:** See [outlook-extractor/reference.md](~/.claude/skills/outlook-extractor/reference.md#recurring-event-exceptions)

---

### Mid-Week Sync Support

**Problem:** Syncing on Wednesday doesn't include Monday/Tuesday events by default.

**Solution:** `--from-week-start` parameter includes events from Monday of current week.

**Usage:**
```bash
python outlook_extractor.py calendar --days 30 --from-week-start
```

**When to Use:**
- Syncing mid-week but need full week context
- After missing sync on Monday/Tuesday
- Reviewing what happened earlier in the week

**Example:**
```
Today: Wednesday, Nov 13
Without flag: Extracts Nov 13 → Dec 13
With flag: Extracts Nov 11 (Monday) → Dec 13
```

**Technical Details:** See [outlook-extractor/reference.md](~/.claude/skills/outlook-extractor/reference.md#--from-week-start)

---

## Performance

### SessionStart Sync
**Target:** < 30 seconds
**Typical:** 15-20 seconds
**Factors:**
- Number of Outlook events (scales linearly)
- Number of Obsidian events
- Network latency to Outlook API

### PostToolUse Sync
**Target:** < 10 seconds
**Typical:** 5-8 seconds
**Factors:**
- Single event sync vs. full month
- Outlook API response time

### VFL Processing
**Target:** < 30 seconds
**Typical:** 20-25 seconds
**Factors:**
- PDF complexity
- Number of weeks Greg is scheduled
- Outlook API for multiple events

---

## Future Enhancements

### Planned Features
1. **Conflict resolution** - Handle events modified in both systems
2. **Two-way updates** - Detect changes, not just creation
3. **Event deletion sync** - Delete from one, delete from both
4. **Multi-month sync** - Sync broader date ranges
5. **Attendee management** - Sync attendee lists from Outlook
6. **Recurring event support** - Full recurring series handling
7. **Email extraction integration** - Auto-process VFL from email attachments

### Potential Optimizations
1. **Incremental sync** - Only sync changed events
2. **Cache optimization** - Reduce API calls
3. **Parallel processing** - Create multiple events simultaneously
4. **Background sync** - Continuous filesystem watching

---

## Technical Details

### Dependencies
- **outlook-extractor skill** - Personal skill in `~/.claude/skills/`
- **Python 3.7+** - For outlook_extractor.py script
- **pywin32 library** - Windows COM API for Outlook
- **Microsoft Outlook** - Must be installed and running
- **Claude Code** - Hooks and slash commands

### Tools Used
- **Read tool** - PDF parsing, file reading
- **Write tool** - Creating Obsidian markdown files
- **Edit tool** - Modifying existing events (future)
- **Bash tool** - File operations (move, copy, delete)
- **outlook-extractor skill** - All Outlook operations

### Timezone Handling
- **Obsidian:** Dates only (YYYY-MM-DD), times in body text
- **Outlook:** Full datetime with timezone (SAST UTC+2)
- **Conversion:** Always use local SAST time, no UTC conversion
- **Display:** All times shown in SAST (what user sees in Outlook UI)

### Security
- **Hooks run automatically** - Review hook commands before enabling
- **Outlook credentials** - Uses Windows integrated auth
- **File permissions** - Hooks inherit Claude Code permissions
- **No external APIs** - All local (Outlook COM, filesystem)

---

## Testing

### Test SessionStart Hook
1. Restart Claude Code
2. Observe console for sync message
3. Check `Schedule/_Sync_Summary_YYYY-MM.md`
4. Verify Outlook events appeared in Obsidian

### Test PostToolUse Hook (Schedule)
1. Ask Claude: "Create a test meeting tomorrow at 3pm"
2. Verify Obsidian file created: `Schedule/YYYY-MM-DD - Test Meeting.md`
3. Check if hook triggered (should see sync activity)
4. Open Outlook, verify meeting exists

### Test VFL Processing
1. Place test VFL PDF in `00_Inbox/`
2. Run: `/process-vfl-schedule`
3. Verify Greg's weeks identified correctly
4. Check Schedule/ for VFL events
5. Check Outlook for VFL meetings
6. Verify PDF moved to `reference/SHEQ/VFL_Schedules/`

### Test Manual Sync
1. Manually create event in Obsidian (outside Claude)
2. Run: `/sync-outlook-calendar`
3. Verify event created in Outlook
4. Check sync summary for details

---

## Related Documentation

### Internal References
- [Agent Skills System Reference](./2025-10-21 – Agent Skills System Reference.md)
- [VFL Schedule Processing Guide](../SHEQ/2025-10-21 – VFL Schedule Processing Guide.md)
- Project CLAUDE.md: Main vault instructions
- User CLAUDE.md: Global user settings

### External References
- [Claude Code Hooks Guide](https://docs.claude.com/en/docs/claude-code/hooks-guide.md)
- [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills.md)
- [Anthropic Agent Skills](https://www.anthropic.com/news/skills)

---

**Last Updated:** 2025-10-21
**Author:** Gregory Karsten (with Claude Code assistance)
**Status:** Active - Production use
**Next Review:** When hooks fail or need adjustment