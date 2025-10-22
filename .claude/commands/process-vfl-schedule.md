# Process VFL Schedule

Extract VFL schedule from PDF, identify Greg's weeks, and create both Obsidian and Outlook calendar events.

## Task

You are processing a VFL (Visible Felt Leadership) schedule PDF. Follow these steps systematically:

### Step 1: Locate VFL PDF

Search for VFL schedule PDF in these locations (in order):
1. `00_Inbox/VFL Schedule*.pdf`
2. Any file path provided as argument to this command
3. Recently extracted Outlook email attachments (check for VFL schedule in email extraction results)

If multiple files found, use the most recent one by date.

### Step 2: Read and Parse PDF

Use the Read tool to open the VFL schedule PDF. The PDF contains:
- 5 columns (Areas): N2, N3, Gloria, Surface Plant, Black Rock
- 4-5 rows (Weekly rotations)
- Each cell contains: VFL Champion, Focus Topic, Team Members (6 names)

Extract ALL data from the PDF:
- Identify the month covered (from filename or PDF content)
- For each week, extract date, area, champion, focus topic, team members

### Step 3: Identify Greg's Weeks

Search for "Greg" (case-insensitive) in ALL team member lists across all weeks and areas.

For each week Greg appears:
- Record the exact date
- Record the area
- Record the VFL Champion name
- Record the focus topic
- Record ALL team member names (including Greg)

### Step 4: Create Obsidian Calendar Events

For EACH week Greg is scheduled, create a markdown file:

**Filename:** `Schedule/YYYY-MM-DD - VFL [Area].md`

**Content Template:**
```markdown
---
title: VFL - [Area]
allDay: false
date: YYYY-MM-DD
startTime: "08:00"
endTime: "17:00"
completed: null
---

# VFL - [Area]

**VFL Champion**: [Champion Name]
**Focus Topic**: [Focus Topic]
**Area**: [Area Name]
**Time**: 08:00 - 17:00 (Full Day)

**Team Members**: [Name1], [Name2], [Name3], [Name4], [Name5], [Name6]

**Tags**: #VFL #SHEQ #[AreaTag] #year/2025
```

**Note:** VFL events are all-day (08:00-17:00) but use `allDay: false` with explicit `startTime` and `endTime` to ensure proper calendar display.

**Area Tags:**
- N2 → `#site/Nchwaning2`
- N3 → `#site/Nchwaning3`
- Gloria → `#site/Gloria`
- Surface Plant → `#SurfacePlant`
- Black Rock → `#BlackRock`

### Step 5: Create Outlook Calendar Events

For EACH week Greg is scheduled, create an Outlook meeting using the outlook-extractor skill.

**Important:** Claude should automatically recognize the need to create Outlook meetings and invoke the outlook-extractor skill without manual prompting.

**Meeting Details:**
- Subject: `VFL - [Area]: [Focus Topic]`
- Start: `YYYY-MM-DD 08:00` (SAST local time)
- End: `YYYY-MM-DD 17:00` (SAST local time)
- Location: `[Area]`
- Body:
  ```
  VFL Champion: [Name]
  Focus Topic: [Topic]
  Area: [Area]

  Team Members: [Complete list]
  ```

Use the outlook-extractor skill's create-meeting command with these parameters.

### Step 6: Move PDF to Archive

1. Check if PDF already exists in `reference/SHEQ/VFL_Schedules/`
2. If duplicate in inbox, delete the inbox copy
3. If new file, move to `reference/SHEQ/VFL_Schedules/VFL Schedule - [Month] [Year].pdf`
4. Ensure proper naming convention

### Step 7: Create Processing Summary

Create a summary file: `00_Inbox/VFL_[Month]_Processing_Summary.md`

**Content:**
```markdown
# VFL Schedule Processing Summary - [Month] [Year]

**Processed:** [Timestamp]
**PDF File:** [Original filename]
**Moved to:** reference/SHEQ/VFL_Schedules/[new filename]

## Greg's Schedule

| Date | Area | Champion | Focus Topic | Team |
|------|------|----------|-------------|------|
| [Date] | [Area] | [Name] | [Topic] | [Members] |

## Events Created

### Obsidian Calendar
- [ ] Schedule/YYYY-MM-DD - VFL [Area].md
- [ ] Schedule/YYYY-MM-DD - VFL [Area].md
- [ ] Schedule/YYYY-MM-DD - VFL [Area].md

### Outlook Calendar
- [ ] VFL - [Area]: [Topic] ([Date])
- [ ] VFL - [Area]: [Topic] ([Date])
- [ ] VFL - [Area]: [Topic] ([Date])

## Status
✅ Processing completed successfully
Total events created: [N] Obsidian + [N] Outlook = [2N] total
```

### Step 8: Report Results

Provide a brief summary to the user:
- Number of weeks Greg is scheduled
- Dates and areas
- Confirmation that all calendar events created
- Location of processing summary

## Quality Checks

Before completing, verify:
- ✅ Greg found in at least one team list
- ✅ All dates are valid and properly formatted
- ✅ Both Obsidian AND Outlook events created for each week
- ✅ PDF moved to proper location
- ✅ No duplicate events created

## Error Handling

If errors occur:
- Log the error in processing summary
- Continue with remaining events if possible
- Report partial success to user
- Do not delete PDF until processing confirmed successful

## Notes

- This command can be triggered automatically by hooks when VFL PDFs arrive
- Uses Claude's native PDF reading (Read tool) - no external libraries needed
- Leverages outlook-extractor skill for Outlook integration
- All times in SAST (UTC+2)
- VFL events are always all-day events (08:00-17:00)

---

**Tags:** #VFL #SHEQ #automation #calendar #year/2025
