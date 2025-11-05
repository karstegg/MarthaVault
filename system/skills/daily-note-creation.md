---
'Status:': Active
'Priority:': System
'Assignee:': Claude Code
'Tags:': null
permalink: system/skills/daily-note-creation
---

# Skill Card: Daily Note Creation

**Skill Name**: `daily-note-creation`
**Trigger**: `/nn` or `/new-note` command with daily context
**Confidence Threshold**: 0.80
**Success Rate**: TBD (Phase 3 tracking)

---

## Workflow Steps

### Step 1: Determine Note Type & Context
```
Analyze user request for:
- Date (specific date or "today")
- Content type (meeting, reflection, status update, planning)
- Folder destination (Daily/, Schedule/, projects/)
- Key topics/people/projects mentioned
```

### Step 2: Create Structured Note
**Template Selection**:
- **Daily Journal**: General daily note in Daily/
- **Meeting Note**: Specific meeting in Schedule/ or projects/
- **Project Update**: Progress note in projects/[ProjectName]/
- **Weekly Plan**: Planning note in Schedule/

### Step 3: Apply Front-Matter
```yaml
---
Status:: Draft
Priority:: Med (or inferred from context)
Assignee:: Greg Karsten
DueDate:: (if applicable)
Tags:: #year/2025 #<primary-tag> #<context-tags>
---
```

### Step 4: Populate Note Structure
**Daily Journal Format**:
```markdown
# Daily Note - YYYY-MM-DD

## Morning Review
- [ ] Check 00_inbox/ for new items
- [ ] Review tasks/master_task_list.md priorities
- [ ] Check Schedule/ for today's meetings
- [ ] Update project status

## Key Activities Today
-

## Decisions Made
-

## Action Items
- [ ]

## Evening Wrap-up
- Task statuses updated
- New tasks added to master list
- Tomorrow's priorities identified

## Notes & Observations
-
```

**Meeting Note Format**:
```markdown
# Meeting Title - YYYY-MM-DD

**Date**: YYYY-MM-DD
**Time**: HH:MM - HH:MM
**Location**:
**Attendees**: [[Person 1]], [[Person 2]]

## Agenda
1.
2.

## Discussion Points
### Topic 1


### Topic 2


## Decisions Made
-

## Action Items
- [ ] Task description | Assignee | Due Date

## Follow-up Required
-

#meeting #year/2025
```

### Step 5: Add Context Links
Auto-link to:
- **People**: Create `[[Lastname, Firstname]]` for attendees
- **Projects**: Link `[[projects/ProjectName/]]` for mentioned projects
- **Strategy**: Link to `[[strategy/ActivePhase.md]]` if strategic discussion
- **Previous notes**: Link to related daily notes or meeting series

### Step 6: Extract and Add Tasks
If action items present:
- Add to note as checkboxes
- Mirror to `tasks/master_task_list.md`
- Include assignee, due date, priority tags

---

## Success Criteria

✅ **Daily Note Successfully Created**:
- Proper filename format (YYYY-MM-DD – Title.md)
- Complete front-matter
- Appropriate template applied
- Wikilinks created for people/projects
- Placed in correct folder (Daily/ or Schedule/)
- Tasks extracted to master list if applicable

---

## Example Execution

**User Request**:
> "Create a daily note for today with focus on BEV fire safety and N3 GES recruitment"

**Output** (Daily/2025-10-05 – Daily Note.md):
```markdown
---
Status:: Active
Priority:: High
Assignee:: Greg Karsten
DueDate:: 2025-10-05
Tags:: #year/2025 #daily #BEV #recruitment #fire-safety
---

# Daily Note - October 5, 2025

## Focus of the Day
**Strategic Alignment**: [[strategy/FocusOfWeek.md]] - BEV Safety & Recruitment Closure

**Top Priorities**:
1. [[projects/BEV/]] Charging Bay 2 - Charger procurement finalization
2. [[tasks/2025-08-18 – Recruit N3 GES]] - Final candidate decision
3. Fire safety controls status review

## Morning Review
- [x] Check 00_inbox/ for new items
- [x] Review tasks/master_task_list.md priorities
- [x] Check Schedule/ for today's meetings
  - Kudumane Brakes Quarterly Meeting

## Key Activities Today
- BEV charger quote review and order placement
- Coordinate with [[Louisa Breet]] on N3 GES candidate offer
- Review FireRisk audit preparation status
- Capital vote closures progress check

## Meetings & Interactions
### Kudumane Brakes Quarterly Meeting
- Time: TBD
- Attendees: TBD
- Focus: Q3 brake system performance review

## Decisions Made
-

## Action Items
- [ ] Place BEV charger order by EOD #BEV #critical 📅 2025-10-05
- [ ] Finalize N3 GES candidate selection #recruitment #priority/high 📅 2025-10-05
- [ ] Review capital vote closure status with finance #capital 📅 2025-10-05

## Evening Wrap-up
- Task statuses updated: ___ / ___ completed
- New tasks added to master list: ___
- Tomorrow's top priorities:
  1.
  2.
  3.

## Notes & Observations
-

## Strategic Alignment
- **Fire Safety & Risk Mitigation**: BEV controls implementation ongoing
- **Team Capacity Building**: N3 GES recruitment in final stages
- **Capital Planning**: 2025 vote closures progressing

#daily #year/2025 #BEV #recruitment #fire-safety
```

---

## Confidence Scoring Factors

**High Confidence (≥0.80)**:
- Clear date specified (or "today")
- Obvious note type (daily, meeting, etc.)
- Known context (projects, people mentioned)
- Standard request pattern

**Low Confidence (<0.80)**:
- Ambiguous date ("sometime this week")
- Unclear note type
- Multiple possible interpretations
- Missing critical context

**Action on Low Confidence**:
- Ask clarifying questions
- Propose note structure for approval
- Learn from user edits

---

## Integration with Other Systems

**Daily Workflow Integration**:
```
Morning:
  Create Daily Note → Review Inbox (/triage) → Check Master Task List
                ↓
  Update Strategic Focus (FocusOfWeek.md) → Prioritize Tasks

Evening:
  Update Daily Note → Mark Tasks Complete → Archive Completed Items
                ↓
  Plan Tomorrow's Priorities → Update Strategy if Needed
```

**Memory System Integration**:
- Daily notes indexed in Basic Memory for `recent_activity()` queries
- Strategic focus linked via Graph Memory relations
- Task completion tracked for learning patterns

---

## Learning Integration (Phase 3)

Track user customization patterns:
- Which template sections get used vs deleted?
- Which links get added manually?
- Which tasks get rephrased?
- Time-of-day preferences?

**Adaptation**:
- Customize templates based on user preferences
- Learn preferred language/phrasing
- Adjust detail level
- Optimize structure

---

## Related Skills

- [[system/skills/inbox-triage.md]] - Process inbox items
- [[system/skills/meeting-notes-processing.md]] - Meeting-specific notes
- [[system/skills/task-extraction.md]] - Extract actionable tasks

---

#skill #daily-notes #workflow #automation #templates #year/2025