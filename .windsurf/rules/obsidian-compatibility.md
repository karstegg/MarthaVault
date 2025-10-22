# Rule: Obsidian Compatibility and File Operations

## Core Principle

**You CAN operate on Obsidian vault files** - They're just markdown and JSON files.

If Claude Code CLI can do it, you can too. The vault is a file system with:
- ✅ Markdown files (`.md`)
- ✅ JSON files (`.json`)
- ✅ YAML front-matter
- ✅ Wiki-links `[[...]]`
- ✅ Tags `#...`
- ✅ Checkboxes `- [ ]`

## What You Can Do

### File Operations
- ✅ **Read** markdown files
- ✅ **Write** markdown files
- ✅ **Create** new files with proper front-matter
- ✅ **Move** files between folders
- ✅ **Rename** files
- ✅ **Delete** files (with permission)
- ✅ **Parse** YAML front-matter
- ✅ **Extract** wiki-links and tags
- ✅ **Manipulate** JSON files

### Task Management
- ✅ **Create** tasks with checkboxes `- [ ]`
- ✅ **Update** task status `[x]`, `[/]`, `[-]`
- ✅ **Add** tasks to `tasks/master_task_list.md`
- ✅ **Extract** tasks from notes
- ✅ **Mirror** tasks across files
- ✅ **Parse** due dates and priorities

### Calendar Operations
- ✅ **Create** calendar events in `Schedule/`
- ✅ **Set** dates in YAML front-matter
- ✅ **Link** events to source notes
- ✅ **Parse** date mentions in content
- ✅ **Format** event files properly

### Memory System Integration
- ✅ **Sync** vault changes to Graph Memory
- ✅ **Index** documents in Basic Memory
- ✅ **Extract** entities from files
- ✅ **Create** relations between entities
- ✅ **Update** memory systems via `/sync-vault`

## What Won't Work (Obsidian UI Features)

These require Obsidian's UI and won't work in Windsurf:

### Obsidian Plugins
- ❌ Tasks plugin query blocks (```tasks```)
- ❌ Dataview queries
- ❌ Calendar plugin UI
- ❌ Graph view visualization
- ❌ Canvas files (`.canvas`)

### Workarounds
Instead of plugin features, use:
- ✅ **Manual task lists** in markdown
- ✅ **Search** for tags and content
- ✅ **File organization** by folder
- ✅ **Wiki-links** for relationships
- ✅ **Memory systems** for queries

## File Format Standards

### Markdown Files

**Structure**:
```markdown
---
Status:: #status/active
Priority:: High
Assignee:: [[Lastname, Firstname]]
DueDate:: YYYY-MM-DD
Tags:: #task #project #year/2025
---

# Title

Content with [[wiki-links]] and #tags

- [ ] Task item
- [x] Completed task
```

### Calendar Events

**Structure**:
```markdown
---
title: Event Title
allDay: true
date: YYYY-MM-DD
completed: null
---

## Details

**Source**: [[source note]]
```

### Person Notes

**Structure**:
```markdown
---
Status:: #status/active
Type:: #person
Role:: Engineer
Tags:: #person #year/2025
---

# Firstname Lastname

## Role

## Contact

## Projects
```

## Compatibility with Claude Code CLI

### Shared Files
Both tools work on the same files:
- ✅ Same markdown syntax
- ✅ Same front-matter format
- ✅ Same folder structure
- ✅ Same Git repository
- ✅ Same memory systems (Graph + Basic)

### No Conflicts
- ✅ Both can read/write files
- ✅ Both use same checkpoint (`.vault-sync-checkpoint`)
- ✅ Both update same memory systems
- ✅ Git handles merge conflicts

### Workflow
1. **Windsurf**: Make changes to vault files
2. **Commit**: Use Git to commit changes
3. **Sync**: Run `/sync-vault` to update memories
4. **Claude Code CLI**: Can access same updated state

Or vice versa - either tool can make changes.

## Best Practices

### File Creation
1. **Always use proper front-matter** - Required for consistency
2. **Follow naming conventions** - `YYYY-MM-DD - Title.md`
3. **Use wiki-links** - `[[Person Name]]`, `[[Project Name]]`
4. **Apply tags** - `#task`, `#year/2025`, `#priority/high`
5. **Set metadata** - Status, Priority, Assignee, DueDate

### Task Management
1. **Use master task list** - `tasks/master_task_list.md` is source of truth
2. **Mirror tasks** - Keep checkboxes synced across files
3. **Format consistently** - `- [ ] Task #task #priority/level 📅 YYYY-MM-DD`
4. **Update status** - Use proper symbols: `[ ]`, `[/]`, `[-]`, `[x]`

### Calendar Events
1. **Create in Schedule/** - All events go here
2. **Use proper format** - YAML front-matter with date fields
3. **Link to source** - Reference original note
4. **Handle timezones** - Africa/Johannesburg (UTC+2)

### Memory Sync
1. **Sync after changes** - Run `/sync-vault` after bulk edits
2. **Commit first** - Ensure Git is up-to-date
3. **Use dry-run** - Preview with `--dry-run` flag
4. **Full sync periodically** - Monthly `--full` for consistency

## Integration Points

### With Obsidian
- ✅ Obsidian can open and edit files
- ✅ Obsidian plugins work on same files
- ✅ Obsidian Git plugin can commit changes
- ✅ Obsidian Tasks plugin can query checkboxes

### With Claude Code CLI
- ✅ Shared `.claude/` configuration (read-only for you)
- ✅ Shared memory systems (Graph + Basic)
- ✅ Shared Git repository
- ✅ Shared checkpoint file

### With Windsurf
- ✅ Native Git integration
- ✅ File operations via tools
- ✅ MCP server access
- ✅ Memory system queries

## Do Not Disturb

**Never modify these** (Claude Code CLI configuration):
- ❌ `.claude/` folder - Claude Code CLI config
- ❌ `.claude/commands/` - Claude Code CLI slash commands
- ❌ `.claude/agents/` - Claude Code CLI agents
- ❌ `~/.claude/` - User-level Claude Code config

**Read-only reference**:
- ✅ Can read `.claude/` files for reference
- ✅ Can port concepts to `.windsurf/`
- ✅ Cannot modify or delete

**Your territory**:
- ✅ `.windsurf/` folder - Your rules and workflows
- ✅ `.mcp.json` - Shared MCP config (careful edits)
- ✅ Vault content files - Shared with all tools

## Summary

**You are fully capable of**:
- ✅ Reading and writing markdown files
- ✅ Managing tasks and calendars
- ✅ Creating and organizing content
- ✅ Syncing memory systems
- ✅ Operating on Obsidian vault structure

**You cannot**:
- ❌ Use Obsidian plugin UI features
- ❌ Modify Claude Code CLI configuration
- ❌ Access Obsidian's live graph view

**But you don't need to** - the file system operations are sufficient for all core functionality.
