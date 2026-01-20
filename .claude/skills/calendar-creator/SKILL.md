---
name: Calendar Event Creator
description: Create Obsidian calendar events with correct YAML frontmatter. Prevents calendar display issues.
---

# Calendar Event Creator

Generate properly formatted calendar events for Obsidian Full Calendar plugin.

## When to Use This Skill

Invoke when:
- Creating a calendar event in Schedule/
- User asks to add something to the calendar
- Fixing a malformed calendar event

---

## File Location & Naming

**Folder:** `Schedule/`
**Filename:** `YYYY-MM-DD - Event Title.md`

---

## YAML Frontmatter Templates

### All-Day Event
```yaml
---
title: Event Title
allDay: true
date: 2025-12-17
completed: null
---
```

### Timed Event (CRITICAL FORMAT)
```yaml
---
title: Meeting Title
allDay: false
date: 2025-12-17
startTime: "14:00"
endTime: "15:30"
completed: null
---
```

---

## Critical Rules

| Rule | Correct | Wrong |
|------|---------|-------|
| Times MUST be quoted | `"14:00"` | `14:00` or `840` |
| 24-hour format | `"14:00"` | `"2:00 PM"` |
| Required for timed | `startTime` + `endTime` | Omitting either |
| No placeholders | Valid time or omit | `null`, `--`, `TBD` |

**A single malformed time breaks the ENTIRE calendar display.**

---

## Quick Examples

**Morning meeting:**
```yaml
---
title: Engineering Standup
allDay: false
date: 2025-12-17
startTime: "08:00"
endTime: "08:30"
completed: null
---
```

**Deadline/reminder (all-day):**
```yaml
---
title: DMR Report Due
allDay: true
date: 2025-12-20
completed: null
---
```

**Multi-hour workshop:**
```yaml
---
title: BEV Safety Training
allDay: false
date: 2025-12-18
startTime: "09:00"
endTime: "12:00"
completed: null
---
```

---

## Timezone

All times in **SAST (Africa/Johannesburg, UTC+2)**.

Weekdays only for work events. Move weekend deadlines to preceding Friday.

---

## Calendar Sync

Events auto-sync to Outlook via SessionStart hook. Manual sync: `/sync-outlook-calendar`

See: `reference/claude-code/2025-10-21 – Calendar Automation System.md`
