# Sync Outlook Calendar (Two-Way)

Synchronize calendar events between Obsidian and Outlook for the current month. This is a **two-way sync**:
- Outlook → Obsidian (meetings created in Outlook appear in vault)
- Obsidian → Outlook (events created in vault appear in Outlook)

## Task

You are performing a two-way calendar synchronization between Obsidian vault and Microsoft Outlook for the current month.

### Step 1: Determine Sync Window

Calculate the current month range:
- Start date: First day of current month (YYYY-MM-01)
- End date: Last day of current month (YYYY-MM-DD)
- Use today's date from system environment

### Step 2: Extract Outlook Calendar Events

Use the outlook-extractor skill to retrieve current month's Outlook events:

**Standard sync (from today forward):**
```bash
python ~/.claude/skills/outlook-extractor/scripts/outlook_extractor.py calendar --days 30 --limit 200
```

**Mid-week sync (include events from Monday of current week):**
```bash
python ~/.claude/skills/outlook-extractor/scripts/outlook_extractor.py calendar --days 30 --limit 200 --from-week-start
```

**When to use `--from-week-start`:**
- Syncing on Wednesday/Thursday but need Monday/Tuesday events
- After missing sync earlier in the week
- Getting full week context for reporting

This creates `outlook_calendar.json` with all Outlook events.

Parse the JSON to extract for each event:
- Subject
- Start date/time (convert from UTC to SAST if needed)
- End date/time
- Location
- Body/description
- Attendees (if available)
- All-day flag

**Technical Note:** outlook-extractor automatically:
- Searches ALL Outlook stores (shared calendars, delegated access)
- Excludes Archives and student accounts
- Expands recurring events into individual occurrences
- Handles recurring event exceptions (rescheduled/deleted meetings)

See [outlook-extractor/reference.md](~/.claude/skills/outlook-extractor/reference.md) for implementation details.

### Step 3: Extract Obsidian Calendar Events

Search for all calendar event files in `Schedule/` folder for the current month:

Use Glob: `Schedule/YYYY-MM-*.md`

For each event file found, use Read tool to extract:
- `title` from frontmatter
- `date` from frontmatter (YYYY-MM-DD)
- `allDay` from frontmatter
- Event details from body
- Location (if specified in body)
- Any additional metadata

### Step 4: Two-Way Comparison

Build two lists:

**List A: Outlook events not in Obsidian**
- For each Outlook event, check if matching Obsidian file exists
- Match criteria:
  - Same date (YYYY-MM-DD)
  - Similar subject/title (fuzzy match, case-insensitive)
- Mark as "needs Obsidian creation" if no match

**List B: Obsidian events not in Outlook**
- For each Obsidian event, check if matching Outlook event exists
- Match criteria:
  - Same date
  - Similar title
- Mark as "needs Outlook creation" if no match

**Matching Logic:**
```
Outlook: "Team Meeting with Xavier" on 2025-10-22
Obsidian: "2025-10-22 - Team Meeting with Xavier.md"
→ MATCH ✅

Outlook: "VFL - Black Rock" on 2025-10-21
Obsidian: "2025-10-21 - VFL Black Rock.md"
→ MATCH ✅ (ignore punctuation differences)

Outlook: "Board Meeting" on 2025-10-25
Obsidian: (nothing on 2025-10-25)
→ NO MATCH - needs Obsidian creation ➕
```

### Step 5A: Sync Outlook → Obsidian (Create Missing Obsidian Events)

For each Outlook event in List A (not in Obsidian):

**Create Obsidian markdown file:**

**Filename:** `Schedule/YYYY-MM-DD - [Event Subject].md`

**Content Template for All-Day Events:**
```markdown
---
title: [Event Subject]
allDay: true
date: YYYY-MM-DD
completed: null
---

# [Event Subject]

**Location:** [Location from Outlook]
**Attendees:** [List of attendees if available]

**Details:**
[Event body/description from Outlook]

**Tags:** #meeting #outlook-sync #year/2025
```

**Content Template for Timed Events:**
```markdown
---
title: [Event Subject]
allDay: false
date: YYYY-MM-DD
startTime: "[HH:MM]"
endTime: "[HH:MM]"
completed: null
---

# [Event Subject]

**Time:** [Start Time] - [End Time]
**Location:** [Location from Outlook]
**Attendees:** [List of attendees if available]

**Details:**
[Event body/description from Outlook]

**Tags:** #meeting #outlook-sync #year/2025
```

**CRITICAL:** For timed events, `startTime` and `endTime` must be in quotes and in HH:MM format, or events won't display in Obsidian calendar plugins.

**Special handling:**
- If all-day event: Set `allDay: true`, omit time details
- If recurring: Add `#recurring` tag
- If has attendees: List them in body
- Preserve Outlook formatting as much as possible

### Step 5B: Sync Obsidian → Outlook (Create Missing Outlook Events)

For each Obsidian event in List B (not in Outlook):

**Extract event details from Obsidian file:**
- Title from frontmatter
- Date from frontmatter or filename
- Check if all-day event
- Parse body for time, location, details

**Determine event timing:**
- If `allDay: true` → Use 08:00-17:00 SAST
- If time specified in body → Parse and use
- Default: 08:00-17:00 SAST for all-day events

**Create Outlook meeting using outlook-extractor:**

Execute: `python ~/.claude/skills/outlook-extractor/scripts/outlook_extractor.py create-meeting --subject "[Title]" --start "YYYY-MM-DD HH:MM" --end "YYYY-MM-DD HH:MM" --location "[Location]" --body "[Details]"`

**Important:** Use SAST local time (what you see in Outlook UI)

### Step 6: Handle Special Event Types

**VFL Events:**
- Always 08:00-17:00 (all-day)
- Location: Area name (from event details)
- Body: Include VFL Champion, Focus Topic, Team Members
- Tags: `#VFL #SHEQ`

**Meetings:**
- Use specified times if available in body
- Location from event details
- Include attendees if listed
- Tags: `#meeting`

**Task Deadlines:**
- If event represents a task deadline: create all-day reminder
- Tags: `#task #deadline`

**Recurring Events:**
- Check for `#recurring` tag
- Handle first occurrence only (avoid creating duplicates)
- Note in sync summary

### Step 7: Create Sync Summary

Create summary file: `Schedule/_Sync_Summary_YYYY-MM.md`

**Content:**
```markdown
# Calendar Sync Summary - [Month] [Year]

**Sync Date:** [Timestamp]
**Sync Type:** Two-Way (Outlook ↔ Obsidian)
**Month Covered:** [Month] [Year]

## Sync Statistics

- Outlook events scanned: [N]
- Obsidian events scanned: [N]
- Events already in sync: [N]
- Events created in Obsidian: [N]
- Events created in Outlook: [N]
- Events skipped: [N]
- Errors: [N]

## Outlook → Obsidian (Created in Vault)

### New Events Added ➕
- [YYYY-MM-DD] [Event Title] → Schedule/YYYY-MM-DD - [Title].md
- [YYYY-MM-DD] [Event Title] → Schedule/YYYY-MM-DD - [Title].md

### Skipped (Already Exists) ⏭️
- [Event title] - [Date]

## Obsidian → Outlook (Created in Outlook)

### New Events Added ➕
- [YYYY-MM-DD] [Event Title] → Outlook meeting created
- [YYYY-MM-DD] [Event Title] → Outlook meeting created

### Skipped (Already Exists) ⏭️
- [Event title] - [Date]

## Already in Sync ✅
- [Event title] - [Date]
- [Event title] - [Date]

## Errors ❌
- [Event title] - [Date] → Error: [Description]

## Summary
✅ Sync completed successfully
- Total events in sync: [N]
- New Obsidian files: [N]
- New Outlook events: [N]
```

### Step 8: Report Results

Provide a concise summary to the user:

```
Two-way calendar sync completed for [Month] [Year]:

Outlook → Obsidian:
  ✅ [N] events already in vault
  ➕ [N] new events added to vault

Obsidian → Outlook:
  ✅ [N] events already in Outlook
  ➕ [N] new events added to Outlook

Total events in sync: [N]

Summary: Schedule/_Sync_Summary_YYYY-MM.md
```

## Quality Checks

Before completing, verify:
- ✅ All current month events processed (both directions)
- ✅ Duplicate detection working correctly
- ✅ Times in SAST for Outlook events
- ✅ Obsidian files have proper frontmatter
- ✅ No duplicate events created
- ✅ Sync summary complete and accurate

## Duplicate Prevention (Critical)

**Before creating any event, check:**

**For Obsidian creation:**
1. File doesn't already exist: `Schedule/YYYY-MM-DD - [Title].md`
2. No similar title on same date (fuzzy match)
3. Check variations (punctuation, capitalization)

**For Outlook creation:**
1. Subject match (case-insensitive, ignore minor differences)
2. Date match (same day)
3. Time overlap check (if times specified)

**Skip creation if:**
- Exact match found
- Very similar event on same day (>80% title similarity)
- Event marked as synced in previous run

## Fuzzy Matching Algorithm

To avoid duplicates, use fuzzy matching:

```
Title variations that should MATCH:
- "VFL - Black Rock" ≈ "VFL Black Rock"
- "Team Meeting" ≈ "Team meeting"
- "Review Session" ≈ "Review session - Engineering"

Normalize before comparison:
- Remove punctuation (-, :, etc.)
- Lowercase
- Remove extra spaces
- Compare on same date
```

## Error Handling

**Common errors:**

1. **Outlook not running**
   - Error: "Can't connect to Outlook"
   - Solution: Prompt user to start Outlook, retry

2. **File write permissions**
   - Error: "Can't create Schedule/ file"
   - Solution: Check folder permissions, log error

3. **Network/API errors**
   - Error: "Outlook API timeout"
   - Solution: Retry once, then skip and log

4. **Malformed event data**
   - Error: "Can't parse date from event"
   - Solution: Use fallback values, log warning

**For all errors:**
- Log detailed error in sync summary
- Continue processing remaining events
- Report partial success to user
- Include troubleshooting hints

## Conflict Resolution

**If same event modified in both places:**
- Default: **Outlook wins** (since you primarily use Outlook)
- Obsidian version gets overwritten with Outlook data
- Log conflict in sync summary

**Future enhancement:**
- Implement last-modified timestamp comparison
- Allow user to choose conflict resolution strategy

## Performance Optimization

**Efficiency measures:**
- Batch read all Obsidian files at once (Glob + parallel Read)
- Single Outlook API call for all events
- Cache event lists to avoid redundant searches
- Process comparisons in memory before file operations

**Session start optimization:**
- Target completion: < 30 seconds
- Show progress: "Syncing calendars... (Outlook: 15 events, Obsidian: 12 events)"
- Skip verbose output during automated SessionStart trigger

## Configuration

**Sync Direction:** Two-way (Outlook ↔ Obsidian)
**Sync Window:** Current month only
**Trigger Frequency:**
- Automatic: SessionStart hook
- Manual: `/sync-outlook-calendar` command
- Automatic: PostToolUse hook (when Schedule/ files created)

**Scope:**
- Include: All calendar events in current month
- Exclude: Past months (historical), future months (>1 month out)

## Manual Usage

**Sync current month:**
```
/sync-outlook-calendar
```

**Sync specific month (future enhancement):**
```
/sync-outlook-calendar november
/sync-outlook-calendar 2025-11
```

**Force re-sync (ignore duplicates):**
```
/sync-outlook-calendar --force
```

## Notes

- Uses outlook-extractor personal skill for all Outlook operations
- All Outlook times in SAST (UTC+2) - no conversion needed
- Obsidian files use standard frontmatter format (compatible with calendar plugins)
- Sync summary archived for audit trail
- Safe to run multiple times (duplicate detection prevents issues)
- Two-way sync ensures single source of truth across both systems

## Related Commands

- `/process-vfl-schedule` - Specialized VFL schedule processing
- Outlook-extractor skill - Low-level Outlook operations
- SessionStart hook - Automatic trigger on Claude startup
- PostToolUse hook - Automatic trigger when Schedule/ modified

---

**Tags:** #calendar #sync #outlook #obsidian #automation #year/2025
