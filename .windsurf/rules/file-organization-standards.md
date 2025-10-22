# Rule: File Organization Standards

## Folder Structure

### Core Directories
- **`00_Inbox/`**: Temporary landing zone for unprocessed items
- **`tasks/`**: Task management with `master_task_list.md` as source of truth
- **`projects/`**: Active projects with sub-folders per project
- **`people/`**: Personnel profiles and contact information
- **`personal/`**: Non-work items and personal development
- **`IDEAS/`**: Future concepts, innovations, strategic thinking
- **`reference/`**: Standards, equipment databases, terminology
- **`media/`**: Documents, images, recordings organized by type and year
- **`Schedule/`**: Calendar events and meeting notes
- **`Archive/`**: Completed or inactive items

### File Naming Conventions

**Date-Prefixed Files**:
```
YYYY-MM-DD - Descriptive Title.md
```

**Examples**:
- `2025-10-15 - Weekly Team Meeting.md`
- `2025-08-27 - Drill Rig Capital Application.md`

**Media Files**:
```
YYYY-MM-DD_HHMM_description.ext
```

**Examples**:
- `2025-09-06_1527_clutch_work.jpg`
- `2025-10-15_0830_safety_briefing.mp4`

### Front Matter Standards

Every note should include YAML front matter:

```yaml
---
Status:: #status/active | #status/complete | #status/urgent | #status/new
Priority:: Low | Med | High
Assignee:: Greg | Sipho | Xavier | SK | Simon
DueDate:: YYYY-MM-DD
Tags:: #task #project_name #year/2025 #context
---
```

**Status Values**:
- `#status/new` - Just created, needs triage
- `#status/active` - Currently being worked on
- `#status/urgent` - Requires immediate attention
- `#status/complete` - Finished
- `#status/blocked` - Waiting on dependencies

**Priority Values**:
- `Low` - Can wait, no immediate deadline
- `Med` - Normal priority, standard workflow
- `High` - Important, needs attention soon

### Tagging Conventions

**Always Include**:
- Year tag: `#year/2025`
- Content type: `#task`, `#meeting`, `#idea`, `#decision`
- Project/context: `#BEV`, `#Nchwaning_2`, `#capital_application`

**Personnel Tags**:
- Use full names: `#Gregory_Karsten`, `#Sipho_Dubazane`
- Or wiki-links: `[[Gregory Karsten]]`, `[[Sipho Dubazane]]`

**Location Tags**:
- `#Nchwaning_2`, `#Nchwaning_3`, `#Gloria`, `#Shafts_Winders`
- Or wiki-links: `[[Nchwaning 2]]`, `[[Gloria Mine]]`

### Task Management

**Master Task List**:
- Location: `tasks/master_task_list.md`
- Source of truth for all tasks
- Individual task files can exist in project folders
- Tasks must be mirrored in master list

**Task Format**:
```markdown
- [ ] Task description with context
  - Assignee: Greg
  - Due: 2025-10-20
  - Priority: High
  - Project: [[BEV Fire Safety]]
```

### Media Organization

**Structure**:
```
media/
├── images/
│   └── YYYY/
│       └── YYYY-MM-DD_HHMM_description.jpg
├── audio/
│   └── YYYY/
│       └── YYYY-MM-DD_HHMM_description.mp3
├── video/
│   └── YYYY/
│       └── YYYY-MM-DD_HHMM_description.mp4
└── documents/
    └── YYYY/
        └── YYYY-MM-DD_description.pdf
```

### Calendar Events

**Location**: `Schedule/YYYY-MM-DD - Event Title.md`

**Format**:
```yaml
---
title: Event Title
allDay: true
date: YYYY-MM-DD
completed: null
---

## Event Details
[Content here]

**Source**: [[source note title]]
```

## Separation of Concerns

**MarthaVault Contains**:
- Task management and personal productivity
- Project organization and documentation
- Knowledge base (people, reference, ideas)
- Media archive

**ProductionReports Repository Contains** (separate):
- Equipment databases and structured data
- Automation workflows and GitHub Actions
- External integrations and API connections
- Daily production report processing

**Never mix**: Production automation belongs in ProductionReports, not MarthaVault.

## Triage Process

Files in `00_Inbox/` should be processed regularly:
1. Analyze intent (meeting, task, idea, media)
2. Scan for dates and create calendar events if needed
3. Move to appropriate folder
4. Rename with proper convention
5. Add/update front matter
6. Mirror tasks to master_task_list.md
7. Link calendar events to source notes

## Best Practices

1. **One note per topic** - Don't create mega-documents
2. **Use wiki-links liberally** - `[[Person Name]]`, `[[Project Name]]`
3. **Tag consistently** - Follow established conventions
4. **Date everything** - Use YYYY-MM-DD format
5. **Keep inbox empty** - Process items regularly via `/triage`
6. **Update master task list** - Keep it synchronized
7. **Archive completed work** - Move to Archive/ when done
