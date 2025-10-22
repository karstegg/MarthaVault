---
description: Create a quick note in 00_Inbox/ for later triage
---

# /quick-note

Create a quick note in `00_Inbox/` for later processing via `/triage`.

## Usage

```
/quick-note [content]
```

## Process

1. **Generate filename**: `YYYY-MM-DD_HHMM - Quick Note.md`

2. **Create file** in `00_Inbox/` with:
   ```yaml
   ---
   Status:: #status/new
   Priority:: Med
   Assignee:: Greg
   DueDate::
   Tags:: #quick_note #year/2025
   ---
   
   [content]
   ```

3. **Confirm** in chat: `Quick note created → 00_Inbox/YYYY-MM-DD_HHMM - Quick Note.md`

## Example

**Input**: `/quick-note Need to follow up with Sipho about N3 blast counts`

**Output**: Creates `00_Inbox/2025-10-15_1430 - Quick Note.md`:
```markdown
---
Status:: #status/new
Priority:: Med
Assignee:: Greg
DueDate::
Tags:: #quick_note #year/2025
---

Need to follow up with Sipho about N3 blast counts
```

**Confirmation**: `Quick note created → 00_Inbox/2025-10-15_1430 - Quick Note.md`

## Notes

- Quick notes are meant to be temporary
- Process them with `/triage` to move to proper location
- Add proper context and tags during triage
