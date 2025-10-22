# Rule: Calendar & Schedule Management

## Calendar Event Location

All scheduled events live in the `Schedule/` folder.

## File Format

**Filename**: `YYYY-MM-DD - Event Title.md`

**Front-matter**:
```yaml
---
title: Event Title
allDay: true
date: YYYY-MM-DD
completed: null
---
```

## Event Creation Rules

### When to Create Events

Create calendar events when:
- Meetings are scheduled
- Deadlines are set
- Important dates are mentioned in notes
- Recurring events occur (weekly meetings, monthly reviews)

### Event Types

**Meetings**:
```yaml
---
title: Weekly Team Meeting
allDay: false
date: 2025-10-18
startTime: "09:00"
endTime: "10:00"
completed: null
---
```

**Deadlines**:
```yaml
---
title: BEV Fire Safety Review Due
allDay: true
date: 2025-10-20
completed: null
---
```

**All-day Events**:
```yaml
---
title: Site Visit - Nchwaning 2
allDay: true
date: 2025-10-22
completed: null
---
```

## Timezone Handling

**Default timezone**: Africa/Johannesburg (UTC+2)

All times are in South African Standard Time unless explicitly stated otherwise.

## Weekend Deadline Rules

**Move weekend deadlines to Friday**:
- If due date falls on Saturday → Move to Friday
- If due date falls on Sunday → Move to Friday

**Example**:
- Original: Due 2025-10-19 (Saturday)
- Adjusted: Due 2025-10-18 (Friday)

**Reason**: Work meetings and tasks are weekdays only.

## Event Linking

**Link events to related content**:

```markdown
---
title: Meeting with Sipho - Gloria Site Review
allDay: false
date: 2025-10-17
startTime: "14:00"
endTime: "15:00"
completed: null
---

## Attendees
- [[Gregory Karsten]]
- [[Sipho Dubazane]]

## Related
- **Project**: [[Gloria Mine Operations]]
- **Source**: [[2025-10-15 - Gloria Site Issues Discussion]]

## Agenda
1. Review current site status
2. Discuss maintenance priorities
3. Plan next quarter activities
```

## Integration with Triage

During `/triage`, when dates are detected:

1. **Scan content** for date mentions
2. **Create calendar event** in `Schedule/` folder
3. **Use proper format** with front-matter
4. **Link to source note**: `**Source**: [[note title]]`

**Example**:
If note mentions "Meeting with John on October 20th":
- Create: `Schedule/2025-10-20 - Meeting with John.md`
- Add source link in event file
- Add event reference in original note

## Event Status Tracking

**Completed events**:
```yaml
completed: 2025-10-15
```

**Cancelled events**:
```yaml
completed: null
cancelled: true
```

**Rescheduled events**:
- Create new event with new date
- Mark old event as cancelled
- Link between old and new events

## Recurring Events

**Weekly meetings**:
```markdown
---
title: Weekly Engineering Sync
allDay: false
date: 2025-10-18
startTime: "10:00"
endTime: "11:00"
completed: null
recurring: weekly
---

**Recurrence**: Every Friday at 10:00
**Next occurrence**: 2025-10-25
```

**Monthly reviews**:
```markdown
---
title: Monthly Performance Review
allDay: true
date: 2025-10-31
completed: null
recurring: monthly
---

**Recurrence**: Last day of each month
**Next occurrence**: 2025-11-30
```

## Calendar Views

⚠️ **Windsurf Limitation**: Calendar views may not work as in Obsidian.

**Workarounds**:
- Use file explorer to browse `Schedule/` by date
- Search for events: `path:Schedule/ date:2025-10`
- Manually maintain event lists

## Best Practices

1. **Always use YYYY-MM-DD format** - Sortable, unambiguous
2. **Include time when relevant** - Meetings need start/end times
3. **Link to source notes** - Provide context
4. **Link to attendees** - Track who's involved
5. **Update completion status** - Mark events as done
6. **Handle weekends** - Move work deadlines to Friday
7. **Document recurring patterns** - Note recurrence rules

## Integration with Tasks

**Events with associated tasks**:

```markdown
---
title: Capital Application Deadline
allDay: true
date: 2025-10-25
completed: null
---

## Related Tasks
- [ ] Complete financial analysis #task #priority/high 📅 2025-10-23
- [ ] Draft executive summary #task #priority/high 📅 2025-10-24
- [ ] Submit application #task #priority/critical 📅 2025-10-25

**Source**: [[projects/Capital/Generator Procurement]]
```

## Common Event Patterns

**Site visits**:
```
Schedule/2025-10-22 - Site Visit Nchwaning 3.md
```

**Meetings**:
```
Schedule/2025-10-18 - Weekly Team Meeting.md
```

**Deadlines**:
```
Schedule/2025-10-25 - Capital Application Due.md
```

**Reviews**:
```
Schedule/2025-10-31 - Monthly Performance Review.md
```
