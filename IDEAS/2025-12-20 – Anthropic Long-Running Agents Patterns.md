---
'Status:': Draft
'Priority:': High
'Tags:': null
'Source:': https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
permalink: ideas/2025-12-20-anthropic-long-running-agents-patterns
---

# Anthropic: Effective Harnesses for Long-Running Agents

Official Anthropic guidance on making agents work across multiple sessions.

## The Problem

Agents lose context between sessions. Each new conversation starts fresh with no memory of what came before.

## Solution: Dual-Agent Architecture

| Agent | When | Purpose |
|-------|------|---------|
| **Initializer** | First session only | Set up environment, create tracking files |
| **Coding Agent** | All subsequent sessions | Incremental progress, one feature at a time |

## Key Files to Create

### 1. `init.sh` - Environment setup
```bash
# Run dev server, install deps, verify environment
```

### 2. `claude-progress.txt` - Session log
```
Session 1: Set up project structure
Session 2: Implemented auth flow
Session 3: Added user profile page
```

### 3. Feature List (JSON format)
```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": ["Navigate to main interface", "Click 'New Chat' button"],
  "passes": false
}
```
Agents only modify `passes` field - prevents feature drift.

## Session Startup Checklist

1. `pwd` - Confirm working directory
2. Read git logs + progress files
3. Select highest-priority incomplete feature
4. Run `init.sh` for basic end-to-end tests
5. Work on **ONE feature only**

## Key Rules

- One feature per session (prevents sprawl)
- Test before marking complete
- Never edit/remove tests
- Git commit after each feature
- Leave code in clean, mergeable state

## Application to MarthaVault

| Anthropic Pattern | Our Equivalent |
|-------------------|----------------|
| `claude-progress.txt` | `tasks/master_task_list.md` |
| Feature JSON | Structure todos with `passes: true/false` |
| `init.sh` | Create session startup script |
| Git commits per feature | Already doing this |
| Dual-agent | Split planning vs execution |

## Implementation Ideas

- [ ] Create `claude-init.sh` for MarthaVault session startup
- [ ] Add `passes` field to task list items
- [ ] Create `claude-progress.txt` for session-to-session continuity
- [ ] Structure feature lists as JSON instead of markdown
- [ ] Add verification tests before marking tasks complete

## Notes

Discovered via ClaudeBox triage 2025-12-20.