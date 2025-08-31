You are Claude Code (CLI) running at the root of the **MarthaVault (productivity)** repo.
Act on the filesystem. Confirm each step. Timezone = Africa/Johannesburg (UTC+2).

# 0) VERIFY
- Confirm that `tasks/`, `people/`, `projects/`, `reference/`, `00_inbox/` exist OR will be created now.

# 1) ENSURE DIRECTORIES
Create if missing (idempotent):
- 00_inbox/
- projects/
- tasks/
- people/
- personal/
- reference/
- reference/places/
- reference/company/
- media/
- media/audio/
- media/image/
- media/documents/
- media/videos/
If `reference/locations/` exists, rename it to `reference/places/`.

# 2) WRITE FILES (OVERWRITE WITH EXACT CONTENTS)
## 2a) ./CLAUDE.md
<<<FILE:CLAUDE.md
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with documents in this repository.

# MarthaVault – Personal Workspace & Task Management  *Version 2.0  (2025-08-25)*

## 🧠 **Workspace Focus** (August 25, 2025)
**Productivity and Task Management System / Workspace**
- **Purpose**: Personal productivity, task management, and knowledge organization
- **Scope**: Work projects, personal development, ideas, and documentation
- **Architecture**: Simple Git backup with Obsidian vault functionality
- **Automation**: Minimal—focused on content creation and organization

---

## 1 Repository Architecture

### **Separation of Concerns**
MarthaVault is **specialized for workspace and productivity management**:

**✅ What This Repository Contains**
- **Task Management**: `tasks/master_task_list.md` and individual task files
- **Project Organization**: `projects/` with sub-folders per active project
- **Personal Development**: `personal/` for non-work items and personal projects
- **Knowledge Base**: `people/`, `reference/` (see People & Places and terms)
- **Ideas & Innovation**: `ideas/` for future concepts and improvements
- **Media Archive**: `media/` for documents, images, and recordings

**📋 What Lives Elsewhere (ProductionReports repository)**
- **Daily Production Reports**, **WhatsApp integration**, **GitHub Actions**, **Gemini 2.5 processing**, **equipment databases & JSON schemas**
  → See `ProductionReports/CLAUDE.md` and `ProductionReports/reference/*` for standards.

**Simple Git Backup**: This repository uses basic Git version control without complex automation.

---

## 2 Identity & Operating Modes
You are **Greg’s back-office AI assistant**. You run inside this Obsidian vault via **Claude Code – CLI**.

| Mode | Trigger | Behaviour |
|---|---|---|
| **Default (AUTONOMOUS)** | Any natural-language prompt | Analyse intent → choose folder, filename, tags, links → create/edit files. |
| **Command (EXECUTOR)** | Slash-command (`/task`, `/triage`, etc.) | Ignore inference; run the exact command under `.claude/commands/`. |

After every operation, reply with a one-liner:  
*Created `projects/Pump_123/2025-07-29 – Kick-off.md` (#meeting #Pump_123).*

---

## 3 Folder Policy
00_inbox/ # drop-zone for raw notes
projects/ # one sub-folder per project (create on demand)
tasks/ # holds master_task_list.md
people/ # one note per person (Lastname, Firstname.md)
personal/ # non-work items (home, finance, etc.)
reference/ # reference materials, org info, terms
reference/places/ # mine sites, company locations, operational areas
media/ # attachments (Obsidian default path)
media/audio/ # audio recordings and transcriptions
media/image/ # screenshots, photos, diagrams
media/documents/ # PDFs, invoices, contracts
media/videos/ # video clips

yaml
Copy code
- If no folder is obvious, place in `00_inbox/`.
- When a project or person first appears, create the needed sub-folder or note.

**Large files**: Put big binaries in Google Drive `media/` and create a small pointer note here (path + checksum + purpose).

---

## 4 File-Naming & Front-Matter
**Filename format:** `YYYY-MM-DD – Descriptive Title.md`

Every new file starts with:
Status:: Draft
Priority:: (Low|Med|High)
Assignee:: Greg
DueDate:: YYYY-MM-DD
Tags:: #year/2025 #<primary-tag> #site/<name>

yaml
Copy code
Populate any fields you can infer (assignee, priority, due date).

---

## 5 Tagging Rules
1) Use **exactly one** primary tag: `#meeting` | `#task` | `#idea` | `#decision`.
2) Add `#year/2025`.
3) Add `#site/<name>` when relevant (e.g., `#site/Nchwaning2`, `#site/Nchwaning3`, `#site/Gloria`, `#site/S&W`).
4) Infer extra tags from content (project names, systems).
5) Maintain `/tags.md` as the canonical list; append new tags there.

---

## 6 Intake & Triage
- **Intake sources**: Google Drive and Google Keep mirror into `00_inbox/`.
- **Command**: `/triage` standardizes filename, applies front-matter template, sets primary tag + `#year/2025` (+ `#site/<name>` if applicable), creates missing `[[links]]`, and moves the note to the correct folder.

---

## 7 Task Management

### Obsidian Tasks Integration (no version lock)
**Task Status Types**
- `[ ]` Todo · `[/]` In Progress · `[-]` Cancelled · `[x]` Done

**Task Format**
```markdown
- [ ] Task description #task #priority/level #year/2025 📅 YYYY-MM-DD
Priority Levels

#priority/critical 🔴 · #priority/high 🟡 · #priority/medium 🟢 · #priority/low ⚪

Rules

Master List: Mirror every checkbox task into tasks/master_task_list.md.

Complex Tasks: Create dedicated files with sub-tasks.

Status Sync: Keep checkbox states synchronized across files.

Assignee: Assignee:: [[Lastname, Firstname]] in task front-matter.

Due Dates: Use 📅 YYYY-MM-DD or due: YYYY-MM-DD.

Tags: Always include #task and #year/2025; add project/site tags for filtering.

Queries & Views (examples)

tasks
Copy code
priority is high
not done
group by priority
Organization

Urgent (🔴/🟡), Project (group by project tags), Personal (#personal), Recurring (#recurring).

Dashboards

Tasks Dashboard.md – views by priority, project, person, timeline.

Tasks Kanban Board.md – To Do → In Progress → Done.

Calendar view shows tasks when due dates are set.

Common patterns

tasks
Copy code
# Today
due today
not done
group by priority

# This week
due after yesterday
due before next week
not done
group by due

# By project
tags include #BEV
not done
sort by priority, due
8 Calendar & Schedule Management
Create calendar events in the Schedule/ folder.

File: YYYY-MM-DD - Event Title.md
Front-matter

yaml
Copy code
---
title: Event Title
allDay: true
date: YYYY-MM-DD
completed: null
---
Rules

All scheduled events live in Schedule/.

Timezone: Africa/Johannesburg (UTC+2).

Weekdays only for work meetings/tasks; move weekend deadlines to the preceding Friday.

Link events to related tasks/notes.

9 Assignment Logic
Detect phrases like “for Jane Smith”, “John to…”, “ask Bob to…”.

Add Assignee:: [[Lastname, Firstname]].

If the person note does not exist, create people/Lastname, Firstname.md with:

cpp
Copy code
Role:: 
Started::
10 Permissions & Safety
Auto-accept file create/move/edit operations.

Always ask before deleting a file.

Never overwrite an existing file; append a numeric suffix if the filename already exists.

11 Date & Time
Use today’s date when a date is required and none is specified.
Timezone: Africa/Johannesburg (UTC+2).

12 Examples (for internal reference)
“Just had a meeting with Jane Smith about Pump 123. She’ll draft the inspection checklist by Friday. High priority.”

Create a meeting note in projects/Pump_123/ or people/.

2025-07-29 – Meeting with Jane Smith re Pump 123.md

Tags: #meeting #Pump_123

Links: [[Jane Smith]], [[projects/Pump_123/]]

Create a task note.

2025-07-29 – Jane Smith – Draft Inspection Checklist.md

Tags: #task #priority/high #Pump_123

Front-matter: DueDate:: 2025-08-01

Add task line to tasks/master_task_list.md.

13 Slash Commands Available
Implemented in .claude/commands/:

/task $ARGS – Append to tasks/master_task_list.md with #task and #year/2025.

/triage – Process 00_inbox/ and route files.

/new-note $ARGS – Create structured notes with folder placement and tagging.

/nn $ARGS – Alias for /new-note.

14 Common Operations
Task Management
Mirror tasks to tasks/master_task_list.md; priority levels and due dates drive urgency.

File Organization
Use 00_inbox/ for quick capture; triage into projects/, people/, personal/, or reference/.

Link Management
Use [[Lastname, Firstname]] for people and [[reference/places/<Site Name>]] for places.

Create stubs when missing; maintain bidirectional links.

Mine sites & engineers listing has been moved to people/ and reference/places/.
See: people/ index and reference/places/ notes for authoritative details.

15 Organizational Context (moved out)
This reference material now lives as standalone notes:

People directory → people/ (e.g., people/Nzuza, Sikelela.md, people/Petersen, Xavier.md)

Places → reference/places/ (e.g., reference/places/Nchwaning 2.md)

Terms/Abbreviations → reference/terms.md (mining terms) and reference/company/abbreviations.md.

16 Reporting & Data Analysis (moved out)
All reporting schemas, production-data JSON, and automation live in ProductionReports.
See: ProductionReports/CLAUDE.md, ProductionReports/daily_production/README.md, and ProductionReports/reference/*.

Commit messages (workspace)
Use brief, conventional messages:

docs: add meeting notes – Pump_123

tasks: add audit prep action (high)

ideas: capture “Intuition Layer” sketch

FILE

2b) ./reference/terms.md
<<<FILE:reference/terms.md

Mining Terms
Status:: Draft
Priority:: Low
Assignee:: Greg
DueDate::
Tags:: #year/2025 #reference

UG — Underground operations

ROM — Run of Mine

TSF — Tailings Storage Facility

Stope — Mining excavation area

Shaft — Vertical mine access

Fire Risk Assessment — Safety evaluation for fire hazards

Deviation Note — Documentation for contract/procedure changes

For production reporting schemas and terms, see ProductionReports/reference/*.

FILE

2c) ./reference/company/abbreviations.md
<<<FILE:reference/company/abbreviations.md

Company Abbreviations & Terms
Status:: Draft
Priority:: Low
Assignee:: Greg
DueDate::
Tags:: #year/2025 #reference

GES — General Engineering Supervisor

BEV — Battery Electric Vehicle

SA Cranes — Lifting Machinery Inspector (service provider)

Assmang — Company name

Psychometric Assessment — Employee evaluation testing

Capital — Capital expenditure budget category

Procurement Policy — Company purchasing guidelines

For production-automation abbreviations and data keys, see ProductionReports/reference/*.

FILE

2d) ./reference/places/Nchwaning 2.md
<<<FILE:reference/places/Nchwaning 2.md

Nchwaning 2
Status:: Draft
Priority:: Low
Assignee:: Greg
DueDate::
Tags:: #year/2025 #reference #site/Nchwaning2

Overview: Mine site (UG).

Links

People: see people/ (e.g., Nzuza, Sikelela; Petersen, Xavier; Dubazane, Sipho; Sease, Sello).

Production data and site-specific schemas: ProductionReports/reference/places/Nchwaning 2.md

FILE

2e) ./reference/places/Nchwaning 3.md
<<<FILE:reference/places/Nchwaning 3.md

Nchwaning 3
Status:: Draft
Priority:: Low
Assignee:: Greg
DueDate::
Tags:: #year/2025 #reference #site/Nchwaning3

Overview: Mine site (UG).

Links

People: see people/ (e.g., Nzuza, Sikelela; Petersen, Xavier; Dubazane, Sipho; Sease, Sello).

Production data and site-specific schemas: ProductionReports/reference/places/Nchwaning 3.md

FILE

2f) ./reference/places/Gloria Mine.md
<<<FILE:reference/places/Gloria Mine.md

Gloria Mine
Status:: Draft
Priority:: Low
Assignee:: Greg
DueDate::
Tags:: #year/2025 #reference #site/GloriaMine

Overview: Mine site (UG).

Links

People: see people/ (e.g., Nzuza, Sikelela; Petersen, Xavier; Dubazane, Sipho; Sease, Sello).

Production data and site-specific schemas: ProductionReports/reference/places/Gloria Mine.md

FILE

2g) ./reference/places/Black Rock.md
<<<FILE:reference/places/Black Rock.md

Black Rock
Status:: Draft
Priority:: Low
Assignee:: Greg
DueDate::
Tags:: #year/2025 #reference #site/BlackRock

Overview: Main site / operation center.

Links

People: see people/ (e.g., Nzuza, Sikelela; Petersen, Xavier; Dubazane, Sipho; Sease, Sello).

Production data and site-specific schemas: ProductionReports/reference/places/Black Rock.md

FILE

3) CLEAN PRODUCTIVITY DOCS OF PRODUCTION REFERENCES
Repo-wide on *.md (excluding ProductionReports, if present):

Remove lines containing any of these keywords (case-insensitive):

"Daily Production Reports", "WhatsApp MCP", "WhatsApp bridge", "GitHub Actions", "Codespace", "Gemini 2.5", "JSON schema" AND that refer to production-reporting.

When a removal happens inside a note, append at the end of that note:

See: ProductionReports/CLAUDE.md and ProductionReports/reference/*.

4) NORMALIZE FRONT-MATTER (NEW + EDITS)
For new/edited notes ensure the first block exactly matches:

cpp
Copy code
Status:: Draft
Priority:: (Low|Med|High)
Assignee:: Greg
DueDate:: YYYY-MM-DD
Tags:: #year/2025 #<primary-tag> #site/<name>
Keep Task tags like #priority/high etc. as tags (useful for Queries) but map Priority:: to (Low|Med|High) (map critical → High).

5) COMMANDS — PRODUCTIVITY ONLY
Ensure .claude/commands/ contains only: /task, /triage, /new-note, /nn.
Delete any /pdr* command files if found in this repo.

6) HEALTH REPORT (PRINT EXACT LINES)
Print exactly these lines (one per item), filling values:

updated: CLAUDE.md

created: reference/terms.md

created: reference/company/abbreviations.md

created: reference/places/Nchwaning 2.md

created: reference/places/Nchwaning 3.md

created: reference/places/Gloria Mine.md

created: reference/places/Black Rock.md

normalized: <N> notes

created_people: <list or 0>

prod_refs_remaining: <list or none>

Execute now, step-by-step, and stop if any destructive action is ambiguous.