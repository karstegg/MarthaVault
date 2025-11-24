---
title: Outlook Extractor Skill - Usability Issues & Improvements
type: note
permalink: reference/claude-code/outlook-extractor-skill-usability-issues-improvements
---

# Outlook Extractor Skill - Usability Issues & Improvements

**Date**: 2025-11-23
**Status**: Diagnostic Report
**Priority**: High

---

## Problem Summary

The Outlook extractor skill has persistent usability issues for Claude Code:

1. **Slow execution** - Takes 30+ seconds to extract emails (Outlook COM API latency)
2. **Argument confusion** - Claude struggles with correct command syntax
3. **Documentation gaps** - Help text doesn't clearly show all parameter options
4. **Trial-and-error pattern** - Claude tries 3-4 different argument formats before finding the right one

---

## Root Causes Identified

### 1. **Slow Outlook COM API**
- **Issue**: Python pywin32 with Outlook COM API is inherently slow
- **Symptom**: First command took 30+ seconds to complete
- **Why it matters**: Claude can't know if command succeeded or failed until completion

### 2. **Argument Format Not Obvious from SKILL.md**
- **Issue**: SKILL.md shows command examples but doesn't match the actual argparse structure
- **Evidence**: 
  - SKILL.md line 37: `emails --days 7 --limit 50`
  - Script line 1019: `emails_parser.add_argument('--folder', ...)`
  - The `--folder` parameter is supported but not shown in SKILL.md examples
- **Impact**: Claude doesn't know `--folder "Sent Items"` exists without reading Python code

### 3. **Error Messages Are Unhelpful**
```
error: unrecognized arguments: --format=json
error: argument command: invalid choice: 'emails-sent'
```
- Claude tried `--format=json` (not supported)
- Claude tried `emails-sent` (should be just `emails`)
- No hints in error messages about available options

### 4. **No Quick Help for Commands**
- `python outlook_extractor.py emails --help` works but Claude doesn't know to try it
- SKILL.md should mention this

---

## Improvement Plan

### Priority 1: Update SKILL.md Documentation

**Current Gap**: Line 36-37 shows:
```
| `emails --days 7 --limit 50` | Extract recent emails from Inbox |
| `emails --days 7 --limit 50 --folder "Sent Items"` | Extract recent sent emails |
```

**Problem**: First example doesn't include `--folder`, making it unclear that `--folder` is a parameter.

**Fix**: Add a section titled **"Common Parameter Patterns"** showing all variations:

```markdown
## Common Email Extraction Patterns

### All emails from inbox (past 7 days)
python outlook_extractor.py emails --days 7 --limit 50

### Sent items only (past 5 days)  
python outlook_extractor.py emails --days 5 --limit 50 --folder "Sent Items"

### All parameters with defaults
python outlook_extractor.py emails \
  --days 30 \           # How far back to search
  --limit 20 \          # Max results to return
  --folder "Inbox"      # Which folder: Inbox or Sent Items
```

### Priority 2: Add Runtime Help Discovery

**Add to SKILL.md** (after "Quick Start" section):

```markdown
## Need Help with Command Parameters?

Run this to see all options for any command:
python outlook_extractor.py emails --help
python outlook_extractor.py calendar --help
python outlook_extractor.py send-email --help

This shows required parameters, optional flags, and defaults.
```

### Priority 3: Improve Error Messages in Script

**Current behavior**: Script gives raw argparse errors
**Better approach**: Wrap in try-catch to provide context

**Example improvement**:
```python
# Instead of raw argparse error, catch and suggest:
except SystemExit:
    print("\nValid commands: emails, calendar, contacts, send-email, delete-email, create-meeting, delete-meeting")
    print("Try: python outlook_extractor.py <command> --help")
    sys.exit(1)
```

### Priority 4: Create Quick Reference Card

**Add new file**: `.claude/skills/outlook-extractor/reference/quick-reference.md`

**Contents**:
```markdown
# Outlook Extractor – Quick Reference

## Most Common Commands

| What You Need | Command |
|--------------|---------|
| Recent emails (Inbox) | `emails --days 7 --limit 50` |
| Sent emails | `emails --days 5 --limit 50 --folder "Sent Items"` |
| This week's meetings | `calendar --days 7` |
| Find someone's email | `search-contact "Xavier"` |
| Send email | `send-email --to "x@y.com" --subject "Hi" --body "Message"` |
| Create meeting | `create-meeting --subject "Meeting" --start "2025-11-24 14:00"` |

## Common Mistakes

❌ `emails-sent` → ✅ `emails --folder "Sent Items"`
❌ `--format json` → ✅ Output is JSON by default
❌ `-days 5` → ✅ `--days 5` (double dash)
❌ Single quotes in command → ✅ Use double quotes on Windows

## Help Resources

- `python outlook_extractor.py --help` - See all commands
- `python outlook_extractor.py emails --help` - See emails command options
- `reference/commands.md` - Full parameter documentation
```

### Priority 5: Add Skill Metadata Hints

**Update SKILL.md metadata** (front matter):

```yaml
name: Outlook Extractor
description: Extract emails, calendar events, contacts, send emails, create/delete meetings via Outlook COM API integration
common_commands:
  - "emails --days 7 --limit 50"
  - "emails --days 5 --limit 50 --folder Sent Items"
  - "calendar --days 7"
  - "search-contact Xavier"
  - "send-email --to recipient@company.com --subject Title --body Message"
tips:
  - "Commands are slow (Outlook API latency) - use --days and --limit to reduce scope"
  - "Run 'python outlook_extractor.py <command> --help' for parameter details"
  - "All parameters use double dashes: --days (not -days)"
  - "Folder names must be exact: 'Inbox' or 'Sent Items' (case-sensitive)"
```

---

## Why Claude Struggles Specifically

1. **SKILL.md examples incomplete** → Claude doesn't see all possible parameters
2. **No context about slowness** → Claude doesn't know to run in background early
3. **argparse errors not helpful** → Claude tries random syntax guesses
4. **No quick reference** → Claude must read Python code to find answers
5. **Parameter variations not shown** → Claude doesn't know `--folder "Sent Items"` is valid

---

## Implementation Steps

1. **Today**: Update SKILL.md with complete parameter examples
2. **Today**: Add "Common Mistakes" section to reference docs
3. **This week**: Improve error messages in script (optional but helpful)
4. **This week**: Create quick-reference.md card

---

## Success Metrics

After improvements, Claude should:
- ✅ Get command syntax right on first try
- ✅ Know which parameters are optional vs required
- ✅ Understand why commands are slow (background execution)
- ✅ Not need to try multiple argument formats

