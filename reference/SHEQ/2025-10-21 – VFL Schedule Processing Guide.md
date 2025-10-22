---
Status:: Reference
Priority:: Medium
Tags:: #reference #VFL #SHEQ #schedule #process #year/2025
Created:: 2025-10-21
---

# VFL Schedule Processing Guide

## Overview

This document describes the process for handling VFL (Visible Felt Leadership) schedule PDFs when they arrive monthly. This ensures calendar events are created correctly and files are stored in the proper location.

**VFL Program:** Monthly rotating schedule of leadership visits across mine sites focusing on safety and operational excellence.

---

## File Storage Locations

### VFL Schedule PDFs
**Location:** `reference/SHEQ/VFL_Schedules/`

**Naming Convention:** `VFL Schedule - [Month] [Year].pdf`

**Examples:**
- `VFL Schedule - Aug 2025.pdf`
- `VFL Schedule - Oct 2025.pdf`
- `VFL Schedule - Sep 2025.pdf`

### Calendar Events
**Location:** `Schedule/`

**Naming Convention:** `YYYY-MM-DD - VFL [Area] [Focus].md`

**Examples:**
- `2025-10-21 - VFL Black Rock.md`
- `2025-11-04 - VFL Nchwaning 3.md`
- `2025-10-07 - VFL Surface Plant.md`

---

## VFL Schedule Structure

### Mine Areas Covered
1. **N2** (Nchwaning 2)
2. **N3** (Nchwaning 3)
3. **Gloria**
4. **Surface Plant**
5. **Black Rock**

### VFL Champions (by Area)
- **N2:** James Collins
- **N3:** Johan Jooste
- **Gloria:** Wandile Kwinana
- **Surface Plant:** Michael Bester
- **Black Rock:** Roelie Prinsloo / Zol de Beer (alternating)

### Focus Topics Rotation
- Procedures
- Legal Compliance
- Training
- Housekeeping
- Contractor Management
- Change Management
- Risk Assessment
- Incident Reporting
- Occupational Hygiene
- Emergency Preparedness

### Schedule Format
- **Frequency:** Weekly rotations
- **Duration:** Typically 5 weeks per month covering different focus areas
- **Team Size:** 6 members per area per week
- **Format:** PDF with 5 rows (one per week) × 5 columns (one per area)

---

## Processing Workflow

### Step 1: Receive VFL Schedule
1. New VFL schedule arrives (typically via email or shared drive)
2. PDF placed in `00_Inbox/` for triage
3. Filename usually: `VFL Schedule - [Month] [Year].pdf`

### Step 2: Review Schedule Content
1. Open PDF to identify:
   - Month covered (e.g., October 2025)
   - Number of weeks (typically 4-5)
   - All team member names per week per area
2. **Critical:** Identify which weeks Greg is scheduled
3. Extract for each of Greg's weeks:
   - Date
   - Area
   - VFL Champion
   - Focus Topic
   - Team members list

### Step 3: File Storage
1. Check if PDF already exists in `reference/SHEQ/VFL_Schedules/`
2. If duplicate in inbox, delete inbox copy
3. If new file, move to `reference/SHEQ/VFL_Schedules/`
4. Verify naming convention matches: `VFL Schedule - [Month] [Year].pdf`

### Step 4: Create Calendar Events

#### For Each Week Greg is Scheduled:

**A. Vault Calendar Event (Obsidian)**

Create markdown file in `Schedule/` folder:

**Filename:** `YYYY-MM-DD - VFL [Area].md`

**Content Template:**
```markdown
---
title: VFL - [Area]
allDay: true
date: YYYY-MM-DD
completed: null
---

# VFL - [Area]

**VFL Champion**: [Champion Name]
**Focus Topic**: [Topic]
**Area**: [Area Name]

**Team Members**: [Name1], [Name2], [Name3], [Name4], [Name5], [Name6]

**Tags**: #VFL #SHEQ #[AreaTag] #year/2025
```

**Area Tags:**
- N2: `#site/Nchwaning2`
- N3: `#site/Nchwaning3`
- Gloria: `#site/Gloria`
- Surface Plant: `#SurfacePlant`
- Black Rock: `#BlackRock`

**B. Outlook Calendar Event**

Use the `outlook-extractor` skill to create Outlook meeting:

```bash
# Claude should automatically invoke when you say:
"Add the VFL events to my Outlook calendar"

# Manual command (if needed):
python ~/.claude/skills/outlook-extractor/scripts/outlook_extractor.py create-meeting \
  --subject "VFL - [Area]: [Focus Topic]" \
  --start "YYYY-MM-DD 08:00" \
  --end "YYYY-MM-DD 17:00" \
  --location "[Area]" \
  --body "VFL Champion: [Name]\nFocus Topic: [Topic]\nArea: [Area]\n\nTeam Members: [List]"
```

**Important Notes:**
- Use **local SAST time** (UTC+2) for meeting times
- Standard VFL day: 08:00 - 17:00 (full day event)
- Location: Set to mine area name
- Body: Include all relevant details (champion, topic, team)

---

## October 2025 Example

### Schedule Received
**File:** `VFL Schedule - Oct 2025.pdf`
**Location:** `00_Inbox/` → moved to `reference/SHEQ/VFL_Schedules/`

### Greg's Schedule Identified

| Date | Area | Champion | Focus Topic | Team |
|------|------|----------|-------------|------|
| 07 Oct 25 | Surface Plant | Michael Bester | Housekeeping | Sello T, Greg, Evelyn, Molahlehi, Tshepo T, Wayne |
| 21 Oct 25 | Black Rock | Roelie Prinsloo | Incident Reporting | Sello T, Greg, Keitumetsi, Molahlehi, Humbelani, Chris R |
| 04 Nov 25 | Nchwaning 3 | Johan Jooste | Procedures | Johan V, Greg, Jerome, Anthony, Mothelo, Chris R |

### Calendar Events Created

**Vault Files:**
1. `Schedule/2025-10-07 - VFL Surface Plant.md`
2. `Schedule/2025-10-21 - VFL Black Rock.md`
3. `Schedule/2025-11-04 - VFL Nchwaning 3.md`

**Outlook Meetings:**
1. "VFL - Surface Plant: Housekeeping" - 07 Oct 2025, 08:00-17:00
2. "VFL - Black Rock: Incident Reporting" - 21 Oct 2025, 08:00-17:00
3. "VFL - Nchwaning 3: Procedures" - 04 Nov 2025, 08:00-17:00

---

## Quality Checks

### Before Finalizing
- ✅ Verify Greg's name appears in team list for each event created
- ✅ Confirm area, champion, and focus topic match PDF exactly
- ✅ Check all team member names spelled correctly
- ✅ Ensure dates are correct (day of week matches calendar)
- ✅ Validate no duplicate events created

### Common Errors to Avoid
- ❌ Creating events for weeks Greg is NOT scheduled
- ❌ Wrong area (e.g., Surface Plant instead of Black Rock)
- ❌ Wrong champion name
- ❌ Incorrect team member list
- ❌ Duplicate files in inbox and reference folder

---

## Troubleshooting

### Issue: Can't Find Greg's Name in Schedule
**Solution:** Double-check all areas for each week. Greg may be in different areas different weeks. Search for "Greg" in PDF.

### Issue: Team Member List Doesn't Match
**Symptom:** Vault calendar has different team than PDF
**Solution:** Re-read the correct column/row from PDF. Ensure you're reading the right week and area intersection.

### Issue: Calendar Event Already Exists
**Solution:** Check if event was created in previous processing. Update if needed rather than duplicate.

### Issue: Outlook Meeting Creation Fails
**Common Causes:**
- Outlook not running
- Python pywin32 library not installed
- Incorrect time format (use SAST local time)
- Missing required fields (subject, start time)

**Solution:** Verify Outlook is open, check skill prerequisites, use correct datetime format.

---

## Automation Potential

### Current Process
- Manual review of PDF required
- Manual identification of Greg's weeks
- Semi-automated calendar event creation

### Future Enhancements
Could create a skill to:
1. Parse VFL PDF automatically
2. Detect Greg's name in team lists
3. Extract all relevant data (date, area, champion, topic, team)
4. Auto-create both vault and Outlook events
5. Handle updates to existing schedules

**Skill Name:** `extract-vfl-schedule`
**Trigger:** "Process the VFL schedule for [month]"

---

## Historical Reference

### Schedule Archive
All VFL schedules stored in: `reference/SHEQ/VFL_Schedules/`

**Available:**
- August 2025
- September 2025
- October 2025

### Event History
All created VFL calendar events searchable by:
- Tag: `#VFL`
- Folder: `Schedule/`
- Date range: Filter by year/month
- Query: Search for "VFL" in vault

---

## Related Documentation

### VFL Program Context
- **Purpose:** Visible Felt Leadership - management presence at operational level
- **Goal:** Safety culture improvement, operational excellence, employee engagement
- **Frequency:** Weekly rotations across all mine areas
- **Participation:** Engineering management, site leadership, SHEQ personnel

### SHEQ Documentation
- SHEQ folder: `reference/SHEQ/`
- VFL schedules: `reference/SHEQ/VFL_Schedules/`
- Safety meetings: Tagged with `#SHEQ`
- Compliance tracking: Various SHEQ reports

### Calendar Management
- All scheduled events: `Schedule/` folder
- Obsidian Tasks integration: Use calendar view plugin
- Outlook sync: Manual via outlook-extractor skill
- Timezone: Always SAST (UTC+2)

---

## Template for New Month

When new VFL schedule arrives:

```markdown
## [Month] [Year] VFL Schedule

**Received:** [Date]
**File:** VFL Schedule - [Month] [Year].pdf
**Stored:** reference/SHEQ/VFL_Schedules/

**Greg's Schedule:**

| Date | Area | Champion | Focus | Team |
|------|------|----------|-------|------|
| [DD Mon YY] | [Area] | [Name] | [Topic] | [List] |
| [DD Mon YY] | [Area] | [Name] | [Topic] | [List] |
| [DD Mon YY] | [Area] | [Name] | [Topic] | [List] |

**Events Created:**
- [ ] Vault calendar: Schedule/YYYY-MM-DD - VFL [Area].md
- [ ] Outlook calendar: VFL - [Area]: [Topic]
- [ ] Verified team lists match PDF
- [ ] Confirmed dates and times correct
```

---

**Last Updated:** 2025-10-21
**Author:** Gregory Karsten (with Claude Code assistance)
**Next Review:** When next VFL schedule received (likely November 2025)
