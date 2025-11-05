---
Status: Active
Priority: High
Tags: null
LastUpdated: 2025-11-05
permalink: reference/obsidian-kanban-plugin-setup
---

# Obsidian Kanban Plugin - Setup Guide

**Author**: MarthaVault System  
**Created**: 2025-11-05  
**Plugin Version**: Obsidian Kanban 2.0.51+  

---

## What It Is

The **Obsidian Kanban Plugin** transforms markdown files into interactive Kanban boards with drag-and-drop columns and cards. Perfect for task management, project tracking, and workflow visualization.

---

## Installation

1. Open Obsidian → Settings → Community Plugins
2. Search for "Kanban" by mgmeyers
3. Install and enable
4. Restart Obsidian

**Current Status**: ✅ Installed in MarthaVault

---

## Correct File Format

### Minimal Working Example

```markdown
---
kanban-plugin: basic
---

# Your Board Title

## Column 1 Header

- Task or card 1
- Task or card 2
- Task or card 3

## Column 2 Header

- Another task
- With details

## Column 3 Header

- Completed item
```

### Key Rules

✅ **MUST HAVE:**
- YAML frontmatter with `kanban-plugin: basic`
- Markdown headers (`##`) for columns
- Bullet points (`-`) for cards

❌ **DO NOT USE:**
- Triple backticks (` ``` `) around the kanban
- Complex formatting in headers
- Task checkbox format for cards (unless using Tasks integration)

---

## Card Format Options

### Simple Card
```
- Task name
```

### Card with Tags
```
- Task name #tag1 #tag2
```

### Card with Due Date
```
- Task name 📅 2025-11-05
```

### Card with Tags + Date
```
- Task name #priority/high #BEV 📅 2025-11-15
```

### Card with Link
```
- [[Reference Note]] - Task description
```

---

## Columns Structure

Each `## Header` becomes a column. Standard workflow:

| Column | Purpose | Color |
|--------|---------|-------|
| **CRITICAL & OVERDUE** | Do immediately | 🔴 Red |
| **HIGH PRIORITY** | This week | 🟡 Yellow |
| **IN PROGRESS** | Currently working on | 🔵 Blue |
| **COMPLETED** | Done | 🟢 Green |
| **BACKLOG** | Future work | ⚪ Gray |

---

## Using the Board

### Drag & Drop
- Drag cards **left/right** between columns
- Drag cards **up/down** within columns to reorder
- Changes save automatically to the markdown file

### Add Cards
- Click **+ Add a card** at bottom of any column
- Type card text
- Press Enter

### Edit Cards
- Click card to open details panel
- Edit title, add description, tags, due date
- Click save or press Escape

### Archive Cards
- Right-click card → **Archive**
- Or drag to "Completed" or "Backlog"

### Settings (Right-click board header)
- **Open board settings** → customize appearance
- **Archive completed cards** → hide done items
- **Add a list** → create new column
- **Search** → find specific cards

---

## Tag Configuration

### Priority Tags (Recommended)
```
#priority/critical   - Do now (🔴)
#priority/high       - This week (🟡)
#priority/medium     - Next 2 weeks (🟢)
#priority/low        - Backlog (⚪)
```

### Project Tags
```
#BEV          - Battery Electric Vehicle
#capital      - Capital expenditure
#recruitment  - Personnel/hiring
#fire-safety  - Safety compliance
```

### Site Tags
```
#site/Nchwaning2
#site/Nchwaning3
#site/Gloria
#site/S&W
```

---

## Common Mistakes & Fixes

### ❌ Problem: Board shows as markdown list, not Kanban

**Causes:**
- Missing `kanban-plugin: basic` in frontmatter
- Using backticks (` ``` `) around content
- Headers using `#` instead of `##`

**Fix:**
```yaml
---
kanban-plugin: basic
---

# Title

## Column 1
- Card 1
```

### ❌ Problem: Cards not showing

**Causes:**
- Using complex formatting in card text
- Headers at wrong level
- File not recognized as Kanban

**Fix:**
- Keep card text simple
- Use `##` for columns (not `#` or `###`)
- Right-click → "Open as Kanban"

### ❌ Problem: Can't drag cards

**Causes:**
- Board in read-only mode
- Plugin needs reload
- Card text has line breaks

**Fix:**
- Restart Obsidian
- Check file permissions
- Keep card text on single line

---

## Advanced: Integrating with Tasks Plugin

If using **Obsidian Tasks** plugin:

```
## To Do

- [ ] Task 1 #priority/high 📅 2025-11-05
- [ ] Task 2 #priority/medium 📅 2025-11-12

## Done

- [x] Completed task
```

Kanban shows checkboxes that sync with Tasks plugin.

---

## MarthaVault Implementation

**File Location**: `tasks/Tasks Kanban Board.md`

**Columns**:
1. CRITICAL & OVERDUE (5 items)
2. HIGH PRIORITY (8 items)
3. IN PROGRESS (5 items)
4. COMPLETED (4 items)
5. BACKLOG (medium priority tasks)

**Sync Strategy**:
- Kanban board for visual management
- `master_task_list.md` for authoritative source
- Changes sync bidirectionally

**Usage**:
- Drag tasks to "IN PROGRESS" when starting
- Move to "COMPLETED" when done
- Keep "CRITICAL & OVERDUE" empty by working through items
- Add new cards directly or from master list

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New card | **Shift + Enter** |
| Close card details | **Escape** |
| Search board | **Ctrl/Cmd + F** |
| Archive card | **Right-click** → Archive |

---

## Performance Tips

✅ **Do This:**
- Keep columns to 5-8 items max for speed
- Archive old completed items regularly
- Use backlog column for future work

❌ **Avoid:**
- 100+ cards in single board (split to multiple files)
- Heavy formatting in card text
- Nested bullet lists (keep flat structure)

---

## Resources

- **Official Docs**: https://publish.obsidian.md/kanban/
- **GitHub**: https://github.com/mgmeyers/obsidian-kanban
- **Plugin Community**: Obsidian Discord #kanban

---

## Related Files

- [[tasks/Tasks Kanban Board.md]] - Working board implementation
- [[tasks/master_task_list.md]] - Authoritative task source
- [[Dashboard.md]] - Main dashboard with board link

---

**Last Updated**: 2025-11-05  
**Status**: ✅ Verified working in MarthaVault  
**Next Review**: 2025-12-01