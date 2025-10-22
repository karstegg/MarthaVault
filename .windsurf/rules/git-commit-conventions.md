# Rule: Git Commit Conventions

## Commit Message Format

Use conventional commit format:

```
type: brief description
```

## Commit Types

- **docs:** - Documentation, meeting notes, reference materials
- **tasks:** - Task creation, updates, completions
- **ideas:** - New ideas, concepts, innovations
- **fix:** - Bug fixes, corrections
- **feat:** - New features, capabilities
- **refactor:** - Code/content reorganization
- **chore:** - Maintenance, cleanup, triage

## Examples

**Good commit messages**:
```
docs: add meeting notes - Pump_123
tasks: add audit prep action (high priority)
ideas: capture "Intuition Layer" sketch
fix: correct due date on BEV task
feat: add new project folder for Generator Procurement
refactor: reorganize media files by year
chore: triage inbox - 8 items processed
```

**Bad commit messages**:
```
update
fixed stuff
changes
wip
```

## When to Commit

**Commit after**:
- Running `/triage` - Batch inbox processing
- Completing a task or project milestone
- Creating/updating important documentation
- Making significant organizational changes
- End of work session (daily commit)

**Don't commit**:
- Work in progress (unless using WIP branch)
- Incomplete triage operations
- Temporary/scratch files

## Git Workflow in Windsurf

### Using Built-in Git Support

Windsurf has native Git integration:

1. **View changes**: Source Control panel (left sidebar)
2. **Stage files**: Click + icon next to changed files
3. **Commit**: Enter message in text box, click ✓ commit
4. **Push**: Click ... menu → Push
5. **Pull**: Click ... menu → Pull

### Branch Management

**Default branch**: `main`

**When to branch**:
- Large refactoring operations
- Experimental features
- Multi-day projects

**Branch naming**:
```
feature/description
fix/issue-description
docs/topic
```

## Best Practices

1. **Commit frequently** - Small, focused commits
2. **Write clear messages** - Use conventional format
3. **Stage selectively** - Don't commit everything at once
4. **Pull before push** - Avoid conflicts
5. **Review changes** - Check diff before committing

## Integration with Workflows

**After `/triage`**:
```
chore: triage inbox - processed 5 notes, 2 media files
```

**After task completion**:
```
tasks: complete BEV fire safety review (high)
```

**After documentation**:
```
docs: add capital application guidelines
```

## MarthaVault-Specific Guidelines

**Separation of concerns**:
- ✅ MarthaVault: Task management, productivity, knowledge
- ❌ ProductionReports: Automation, equipment data (separate repo)

**Never commit**:
- Temporary files
- Cache or build artifacts
- Sensitive credentials
- Large binary files (use Google Drive, create pointer notes)

## Timezone

All commits use **Africa/Johannesburg (UTC+2)** timezone.
