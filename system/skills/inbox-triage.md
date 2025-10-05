---
Status:: Active
Priority:: System
Assignee:: Claude Code
Tags:: #year/2025 #system #skill #workflow #triage
---

# Skill Card: Inbox → Triage Workflow

**Skill Name**: `inbox-triage`
**Trigger**: `/triage` command OR inbox items present (00_inbox/ folder)
**Confidence Threshold**: 0.75
**Success Rate**: TBD (Phase 3 tracking)

---

## Workflow Steps

### Step 1: Read Inbox Items
```
Tool: Glob("00_inbox/*.md")
Action: List all unprocessed files in inbox
```

### Step 2: Analyze Content
For each file:
- Read file content
- Identify content type (meeting, task, idea, decision, person, project)
- Assess urgency (deadline mentions, "URGENT", priority keywords)
- Extract key entities (people names, project names, site names)
- Determine organizational context

### Step 3: Apply Tags
Add front-matter if missing:
```yaml
---
Status:: Draft
Priority:: (Low|Med|High|Critical)
Assignee:: (inferred from content)
DueDate:: (if mentioned)
Tags:: #year/2025 #<primary-tag> #site/<name> #<project>
---
```

**Primary Tag Rules**:
- Meeting mentions/outcomes → `#meeting`
- Action items/to-do → `#task`
- Concepts/future possibilities → `#idea`
- Approval/commitment/choice → `#decision`

**Site Tag Rules**:
- "Nchwaning 2" | "N2" → `#site/Nchwaning2`
- "Nchwaning 3" | "N3" → `#site/Nchwaning3`
- "Gloria" → `#site/Gloria`
- "Shafts & Winders" | "S&W" → `#site/S&W`

### Step 4: Create Wikilinks
Scan for:
- **People**: Names → Create `[[Lastname, Firstname]]` links
  - Check if person file exists in people/
  - Create stub if missing
- **Projects**: Project keywords → Create `[[projects/ProjectName/]]` links
  - Check if project folder exists
  - Create folder structure if missing
- **Places**: Site mentions → Create `[[reference/places/SiteName]]` links

### Step 5: Standardize Filename
Format: `YYYY-MM-DD – Descriptive Title.md`
- Use date from content or today's date
- Create descriptive title (3-7 words)
- Handle duplicate filenames (append _2, _3, etc.)

### Step 6: Move to Appropriate Folder
**Routing Logic**:
```
Meeting notes → Schedule/ (if future event) OR people/ (if person-specific)
Tasks → tasks/ (if standalone) OR projects/ (if project-specific)
Ideas → IDEAS/
Decisions → projects/ (context-dependent)
People info → people/
Project updates → projects/[ProjectName]/
Equipment/technical → Operations/ or reference/
```

### Step 7: Extract Actionable Tasks
Scan for action items:
- Lines starting with `- [ ]` (checkbox)
- Phrases: "need to", "must", "action:", "follow up", "TODO"
- Deadline mentions: "by Friday", "end of month", "ASAP"

For each task found:
- Add to `tasks/master_task_list.md`
- Format: `- [ ] Task description #tags 📅 YYYY-MM-DD`
- Include assignee, priority, project link

---

## Success Criteria

✅ **File Successfully Triaged**:
- Front-matter complete with all required fields
- At least one primary tag applied
- Site tag if applicable
- Filename standardized (YYYY-MM-DD format)
- Wikilinks created for people/projects/places
- File moved from 00_inbox/ to appropriate folder
- Action items extracted to master_task_list.md

---

## Example Execution

**Input** (00_inbox/meeting notes.md):
```markdown
Had a meeting with Sipho about the BEV fire safety audit.
Need to schedule FireRisk engineer visit by end of October.
Gloria mine needs temperature monitors installed ASAP.
```

**Output** (projects/BEV/2025-10-05 – BEV Fire Safety Meeting with Sipho.md):
```markdown
---
Status:: processed
Priority:: High
Assignee:: Greg Karsten
DueDate:: 2025-10-31
Tags:: #year/2025 #meeting #BEV #fire-safety #site/Gloria
---

# BEV Fire Safety Meeting with Sipho

Had a meeting with [[Sipho Dubazane]] about the [[projects/BEV/]] fire safety audit.

## Action Items
- [ ] Schedule FireRisk engineer visit by end of October 📅 2025-10-31
- [ ] Install temperature monitors at [[reference/places/Gloria Mine]] ASAP 📅 2025-10-15

#meeting #BEV #fire-safety #year/2025 #site/Gloria
```

**Also Added to tasks/master_task_list.md**:
```markdown
- [ ] Schedule FireRisk engineer visit #BEV #fire-safety #priority/high 📅 2025-10-31
- [ ] Install temperature monitors at Gloria #BEV #fire-safety #site/Gloria #priority/critical 📅 2025-10-15
```

---

## Confidence Scoring Factors

**High Confidence (≥0.75)**:
- Clear content type (meeting, task, etc.)
- Obvious folder destination
- Known people/project names
- Standard date format present

**Low Confidence (<0.75)**:
- Ambiguous content type
- Multiple possible destinations
- Unknown entities (new people/projects)
- Missing critical context

**Action on Low Confidence**:
- Ask user for clarification
- Provide options with rationale
- Learn from user choice for future

---

## Learning Integration (Phase 3)

Track user edits after triage:
- Which folder assignments get changed?
- Which tags get added/removed?
- Which wikilinks get corrected?
- Patterns to strengthen/decay

**Feedback Loop**:
```
User Edit → Pattern Recognition → Confidence Adjustment
     ↓              ↓                    ↓
  Deviation    Update Skill Card    Future Improvement
```

---

## Related Skills

- [[system/skills/daily-note-creation.md]] - Create structured daily notes
- [[system/skills/meeting-notes-processing.md]] - Meeting-specific processing
- [[system/skills/task-extraction.md]] - Extract tasks from any content

---

#skill #inbox #triage #workflow #automation #year/2025
