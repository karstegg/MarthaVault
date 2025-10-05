---
Status:: Draft
Priority:: Med
Assignee:: Greg
DueDate:: 
Tags:: #year/2025 #note #site/nchwaning2
---

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