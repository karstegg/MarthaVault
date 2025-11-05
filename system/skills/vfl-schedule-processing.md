---
'Status:': Active
'Priority:': System
'Assignee:': Claude Code
'DueDate:': null
'Tags:': null
permalink: system/skills/vfl-schedule-processing
---

# Skill: VFL Schedule Processing

**Skill Name**: `vfl-schedule-processing`
**Category**: SHEQ Operations
**Frequency**: Monthly
**Owner**: [[Gregory Karsten]]
**Created**: 2025-10-09

---

## Purpose

Process monthly VFL (Visible Felt Leadership) schedules when received:
1. Archive PDF schedule in proper location
2. Extract Greg's weekly VFL assignments
3. Create calendar events for each assignment
4. Maintain historical schedule archive

---

## Trigger Patterns

**File Detection**:
- PDF filename contains "VFL Schedule"
- Usually arrives in `00_Inbox/`
- Monthly occurrence (beginning of each month)

**User Instructions**:
- "Process the VFL schedule"
- "Add VFL to my calendar"
- During `/triage` when VFL PDF detected

---

## Standard Workflow

### Step 1: Archive Schedule
```
Destination: reference/SHEQ/VFL_Schedules/
Naming: "VFL Schedule - <MMM YYYY>.pdf"
Example: "VFL Schedule - Oct 2025.pdf"
```

### Step 2: Extract Content
Read PDF and identify:
- 5 weekly schedules (covering ~5 weeks)
- 5 mine areas: Nchwaning 2, Nchwaning 3, Gloria, Surface Plant, Black Rock
- VFL Champions per area
- Focus topics per week
- Team member assignments

### Step 3: Identify Greg's Assignments
Search for "Greg" in team member lists across all weeks and areas.

**Extract for each occurrence**:
- Date (week starting date)
- Area (N2, N3, Gloria, Surface Plant, Black Rock)
- VFL Champion
- Focus Topic
- Other team members

### Step 4: Create Calendar Events
For each Greg assignment, create:

```markdown
File: Schedule/<YYYY-MM-DD> - VFL <Area>.md

---
title: VFL - <Area>
allDay: true
date: YYYY-MM-DD
completed: null
---

# VFL - <Area>

**VFL Champion**: <Champion Name>
**Focus Topic**: <Topic>
**Area**: <Area Name>

**Team Members**: <List all team members for this week/area>

**Tags**: #VFL #SHEQ #<site-tag> #year/2025
```

**Site Tag Mapping**:
- Nchwaning 2 → `#site/Nchwaning2`
- Nchwaning 3 → `#site/Nchwaning3`
- Gloria → `#site/Gloria`
- Surface Plant → `#SurfacePlant`
- Black Rock → `#site/BlackRock`

---

## Example Output

### Input
VFL Schedule PDF for October 2025 showing:
- Week of Oct 7: Greg assigned to Surface Plant (Michael Bester, Housekeeping)
- Week of Oct 21: Greg assigned to Surface Plant (Michael Bester, Housekeeping)
- Week of Nov 4: Greg assigned to Nchwaning 3 (Johan Jooste, Procedures)

### Output
Created calendar events:
1. `Schedule/2025-10-07 - VFL Surface Plant.md`
2. `Schedule/2025-10-21 - VFL Surface Plant.md`
3. `Schedule/2025-11-04 - VFL Nchwaning 3.md`

Archived: `reference/SHEQ/VFL_Schedules/VFL Schedule - Oct 2025.pdf`

---

## Quality Checks

**Before completing**:
- ✅ All Greg assignments extracted (check all 5 weeks)
- ✅ Calendar events created with proper front-matter
- ✅ Site tags correctly applied
- ✅ VFL Champion and Focus Topic captured
- ✅ PDF archived in proper location
- ✅ Filename follows naming convention

**Edge Cases**:
- Greg not assigned any week → No calendar events, just archive PDF
- Greg assigned multiple areas same week → Create separate event for each
- Schedule spans into next month → Use week-starting date for event

---

## Success Criteria

**Complete when**:
1. PDF archived in `reference/SHEQ/VFL_Schedules/`
2. All Greg assignments converted to calendar events
3. Calendar events properly formatted and tagged
4. User confirmation received

**User Notification**:
```
✅ Processed VFL Schedule for <Month YYYY>
📅 Created <N> calendar events for Greg's assignments:
   - <Date>: VFL - <Area> (Focus: <Topic>)
   - <Date>: VFL - <Area> (Focus: <Topic>)
📁 Archived: reference/SHEQ/VFL_Schedules/VFL Schedule - <MMM YYYY>.pdf
```

---

## Related Entities

**People**:
- [[Gregory Karsten]] - Primary user
- VFL Champions: [[James Collins]], [[Johan Jooste]], [[Kwinana, Wandile]], [[Michael Bester]], [[Prinsloo, Roelie]], [[de Beer, Zol]]

**Business Process**: VFL Program (Visible Felt Leadership)

**Sites**: [[reference/places/Nchwaning 2]], [[reference/places/Nchwaning 3]], [[reference/places/Gloria Mine]], Black Rock, Surface Plant

**Tags**: #VFL #SHEQ #year/2025

---

## Future Enhancements (Phase 3+)

**Automated Detection**:
- Watch `00_Inbox/` for VFL PDF arrivals
- Auto-trigger processing when detected
- Confidence threshold: 0.85+ for auto-execution

**Predictive Scheduling**:
- Learn Greg's typical VFL patterns (areas, frequency)
- Pre-populate calendar placeholders before schedule arrives
- Alert if expected schedule hasn't arrived by month-start

**Team Coordination**:
- Extract full team schedules (not just Greg)
- Create team member assignment summaries
- WhatsApp notifications to team members

---

#system #skill #SHEQ #VFL #automation #calendar #year/2025