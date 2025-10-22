# Rule: Obsidian Tasks Integration

## Task Status Types

Use these checkbox symbols for task states:

- `[ ]` - Todo (not started)
- `[/]` - In Progress (actively working)
- `[-]` - Cancelled (won't complete)
- `[x]` - Done (completed)

## Task Format

```markdown
- [ ] Task description #task #priority/level #year/2025 📅 YYYY-MM-DD
```

## Priority Levels with Emojis

- `#priority/critical` 🔴 - Immediate action required
- `#priority/high` 🟡 - Important, near-term
- `#priority/medium` 🟢 - Standard priority
- `#priority/low` ⚪ - Nice to have

## Task Management Rules

### Master List
**Mirror every checkbox task** into `tasks/master_task_list.md`

This is the source of truth for all tasks across the vault.

### Complex Tasks
Create dedicated files with sub-tasks for complex work:

```markdown
# Project: BEV Fire Safety Review

- [ ] Main task: Complete BEV fire safety review
  - [ ] Sub-task 1: Review procedures with Kishore
  - [ ] Sub-task 2: Update documentation
  - [ ] Sub-task 3: Submit to DMR
```

### Status Sync
Keep checkbox states synchronized across files:
- If task appears in multiple places, update all instances
- Master task list is the authoritative source

### Assignee
Use front-matter for assignment:

```yaml
---
Assignee:: [[Lastname, Firstname]]
---
```

### Due Dates
Two formats supported:

1. **Inline emoji**: `📅 YYYY-MM-DD`
2. **Obsidian format**: `due: YYYY-MM-DD`

Example:
```markdown
- [ ] Review BEV procedures #task #priority/high 📅 2025-10-20
```

### Required Tags
Always include:
- `#task` - Identifies as task
- `#year/2025` - Year organization
- Project/site tags for filtering (e.g., `#BEV`, `#site/Nchwaning2`)

## Task Organization

### By Priority
- **Urgent** (🔴/🟡) - Critical and high priority tasks
- **Standard** (🟢) - Medium priority tasks
- **Low** (⚪) - Nice to have tasks

### By Project
Group tasks by project tags:
- `#BEV` - BEV-related tasks
- `#capital_application` - Capital project tasks
- `#maintenance` - Maintenance tasks

### By Person
Group tasks by assignee:
- `Assignee:: [[Gregory Karsten]]`
- `Assignee:: [[Sipho Dubazane]]`

### By Timeline
- **Today** - Due today
- **This week** - Due within 7 days
- **This month** - Due within 30 days
- **Overdue** - Past due date

## Windsurf Limitations

⚠️ **Note**: Some Obsidian Tasks features may not work in Windsurf:

**Will NOT work**:
- ❌ Obsidian Tasks query blocks (```tasks ... ```)
- ❌ Dynamic task views and dashboards
- ❌ Automatic task filtering in UI
- ❌ Calendar integration for due dates

**WILL work**:
- ✅ Checkbox status symbols
- ✅ Task formatting with emojis
- ✅ Due date notation (as text)
- ✅ Tag-based organization
- ✅ Manual task list maintenance
- ✅ Search for tasks by tag/priority

## Workarounds for Windsurf

Since dynamic queries don't work, use:

1. **Manual filtering**: Search for tags like `#task #priority/high`
2. **File organization**: Keep related tasks in project folders
3. **Master list**: Use `tasks/master_task_list.md` as single source
4. **Search**: Use Windsurf's search for task discovery

## Common Task Patterns

### Daily Tasks
```markdown
- [ ] Review inbox #task #priority/medium 📅 2025-10-15
- [ ] Check WhatsApp messages #task #priority/high 📅 2025-10-15
```

### Project Tasks
```markdown
- [ ] Complete BEV fire safety review #task #BEV #priority/critical 📅 2025-10-20
  - Assignee: [[Gregory Karsten]]
  - Project: [[BEV Fire Safety Program]]
```

### Recurring Tasks
```markdown
- [ ] Weekly team meeting prep #task #recurring #priority/medium 📅 2025-10-18
```

### Personal Tasks
```markdown
- [ ] Review personal development goals #task #personal #priority/low 📅 2025-10-31
```

## Integration with Workflows

**`/task` workflow**:
- Creates task in master list
- Applies `#task` and `#year/2025` tags
- Formats with proper syntax

**`/triage` workflow**:
- Extracts checkboxes from notes
- Mirrors to master task list
- Preserves formatting and tags

## Best Practices

1. **Always use master list** - Single source of truth
2. **Update status consistently** - Keep all instances in sync
3. **Use priority tags** - Enable filtering and sorting
4. **Set due dates** - Track deadlines
5. **Assign ownership** - Clear responsibility
6. **Link to projects** - Provide context
7. **Use emojis** - Visual priority indicators
