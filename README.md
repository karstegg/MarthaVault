# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **MarthaVault**, an Obsidian vault designed as a back-office AI assistant system. The vault operates through Claude Code with two distinct modes:

- **AUTONOMOUS mode**: Natural language prompts trigger intelligent file creation/editing with automatic folder placement, tagging, and linking
- **EXECUTOR mode**: Slash commands (`/task`, `/triage`, `/new-note`) run exact instructions from the `.claude/commands/` directory

## Architecture

### Folder Structure
```
00_inbox/          # Drop-zone for raw notes (triage destination)
projects/          # One sub-folder per project (created on demand)
tasks/             # Contains master_task_list.md (central task registry)
people/            # One note per person
media/             # Obsidian attachments
.claude/commands/  # Slash command definitions
```

### Core Files
- `claude.md.md` - Main constitution/rules (Version 0.1)
- `.claude/commands/*.md.md` - Slash command implementations
- `tasks/master_task_list.md` - Master task registry (bidirectional sync with individual task files)

## Key Operational Rules

### File Naming Convention
All files use format: `YYYY-MM-DD – Descriptive Title.md`

### Front-Matter Template
Every new file starts with:
```yaml
Status:: #status/new
Priority:: #priority/medium
Assignee::
DueDate::
```

### Tagging System
1. Primary tag: `#meeting`, `#task`, `#idea`, or `#decision`
2. Year tag: `#year/2025`
3. Context tags: project names, systems, etc.
4. Maintain canonical tag list in `/tags.md`

### Task Management
- All checkbox tasks mirror to `tasks/master_task_list.md`
- Bidirectional sync between individual files and master list
- Person assignments create `people/<Name>.md` if needed

## Slash Commands

### `/task $ARGUMENTS`
Appends task to master_task_list.md with `#task` and `#year/2025` tags

### `/triage`
Processes all files in `00_inbox/`, moving them to appropriate folders based on content analysis and adding missing metadata

### `/new-note $ARGUMENTS`
Creates structured notes with automatic project folder placement and proper tagging based on parsed front-matter hints

## Assignment Logic
Detects phrases like "for Jane Smith", "John to...", "ask Bob to..." and automatically:
- Sets `Assignee:: [[Person Name]]`
- Creates person note in `people/` if missing

## Safety Rules
- Auto-accept file create/move/edit operations
- Always ask before deleting files
- Never overwrite existing files (append numeric suffix)
- Current date context: 2025-07-29