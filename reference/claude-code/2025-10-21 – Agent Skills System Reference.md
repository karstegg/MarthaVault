---
'Status:': Reference
'Priority:': High
'Tags:': null
'Created:': 2025-10-21
permalink: reference/claude-code/2025-10-21-agent-skills-system-reference
---

# Agent Skills System Reference

## Overview

**Agent Skills** is a feature in Claude Code (released October 16, 2025) that enables Claude to automatically discover and invoke specialized capabilities based on user requests. Skills provide reusable, team-shareable expertise through a progressive disclosure system.

**Official Announcements:**
- Product announcement: https://www.anthropic.com/news/skills
- Engineering article: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Documentation: https://docs.claude.com/en/docs/claude-code/skills.md

---

## How Agent Skills Work

### Two-Stage Progressive Disclosure System

#### Stage 1: Metadata Loading (At Startup)
- Claude **pre-loads** `name` and `description` metadata from ALL installed skills
- Metadata is added to Claude's system prompt automatically
- Enables skill matching without consuming full context
- Scans three locations:
  - Personal skills: `~/.claude/skills/`
  - Project skills: `.claude/skills/`
  - Plugin skills: Installed via anthropics/skills marketplace

#### Stage 2: Dynamic Loading (During Conversation)
- User makes a request (e.g., "add to my outlook calendar")
- Claude **automatically matches** request to skill description
- Claude **triggers** the skill by loading full `SKILL.md` into context
- Claude **executes** the skill's scripts/commands with appropriate parameters
- **NO manual invocation needed** - fully automatic

### Key Principle
> "Claude loads them automatically when relevant." - Anthropic

**Skills are model-invoked**, not user-invoked. Claude autonomously decides when to use them based on request matching.

---

## Skill Locations & Purposes

| Location | Scope | Sharing | Use Case |
|----------|-------|---------|----------|
| **Personal Skills** `~/.claude/skills/` | All projects | Manual only | Individual workflows, experiments, personal productivity |
| **Project Skills** `.claude/skills/` | Single project | Automatic via git | Team conventions, project-specific expertise |
| **Plugin Skills** | All projects | Via marketplace | Organization-wide distribution |

**Current Setup (Greg's Environment):**
- All skills currently in: `~/.claude/skills/` (Personal)
- Available across all projects
- Not version controlled with MarthaVault project

---

## Currently Installed Skills

### 1. extract-epiroc-bev-report
**Location:** `~/.claude/skills/extract-epiroc-bev-report/`
**Purpose:** Extract key sections from Epiroc BRMO BEV weekly PDF reports into structured markdown
**Triggers:** "Extract the Epiroc report", "Process BEV weekly report", "Get the Epiroc data"
**Output:** Markdown file with General Summary, BEV Daily Exceptions, Planned Work, Battery Status, Critical Issues
**Script:** `scripts/extract_epiroc_bev_report.py`

**Typical Use:**
```bash
# Claude should automatically invoke when you say:
"Extract the Epiroc report for week 16"

# Manual invocation (debugging):
python ~/.claude/skills/extract-epiroc-bev-report/scripts/extract_epiroc_bev_report.py --week=16
```

### 2. extract-pptx-heal
**Location:** `~/.claude/skills/extract-pptx-heal/`
**Purpose:** Extract HEAL matrix content (Highlights, Emerging Issues, Lowlights, Priorities, Actions) from PowerPoint slides
**Triggers:** "Extract HEAL from PowerPoint", "Get HEAL content", "Process Gloria HEAL presentation"
**Sites Supported:** Gloria, Shafts & Winders, N3
**Output:** Formatted text file with bullet-pointed HEAL sections
**Script:** `scripts/extract_pptx_heal.py`

**Typical Use:**
```bash
# Claude should automatically invoke when you say:
"Extract the HEAL content from the Gloria presentation for week 16"

# Manual invocation:
python ~/.claude/skills/extract-pptx-heal/scripts/extract_pptx_heal.py gloria 16
```

### 3. outlook-extractor
**Location:** `~/.claude/skills/outlook-extractor/`
**Purpose:** Extract emails, calendar events, contacts, send emails, create/delete meetings via Outlook COM API
**Triggers:** "Extract my emails", "Create a meeting", "Send an email", "Delete this meeting", "Show my calendar"
**Commands:** emails, calendar, contacts, send-email, create-meeting, delete-meeting
**Script:** `scripts/outlook_extractor.py`
**Timezone:** SAST (UTC+2) - always use local time when specifying meeting times

**Typical Use:**
```bash
# Claude should automatically invoke when you say:
"Add a meeting to my calendar for tomorrow at 2pm"

# Manual invocation:
python ~/.claude/skills/outlook-extractor/scripts/outlook_extractor.py create-meeting \
  --subject "VFL - Black Rock" \
  --start "2025-10-21 08:00" \
  --location "Black Rock"
```

---

## Skill Structure Requirements

### Minimum Required File
**`SKILL.md`** with YAML frontmatter:
```yaml
---
name: "Skill Name"
description: "Clear description of what the skill does and when to use it"
---
```

### Optional but Recommended
- **`scripts/`** - Python scripts or executables
- **`reference/`** - Detailed documentation (commands.md, workflows.md, troubleshooting.md)
- **`forms.md`** - Additional forms/templates
- **Other supporting files** - Loaded contextually when needed

### Best Practices
1. **Clear descriptions** - Include both WHAT the skill does and WHEN Claude should use it
2. **Focused scope** - One skill = one capability (don't bundle multiple functions)
3. **Example triggers** - Show in SKILL.md what phrases should trigger the skill
4. **Testing** - Ask questions matching skill description to verify automatic activation

---

## How to Use Skills

### Automatic Invocation (Preferred)
Simply make requests that match skill descriptions:
- ❌ "Use the outlook skill to create a meeting" (too explicit)
- ✅ "Add a meeting to my calendar for Friday at 10am" (natural language)

### Manual Invocation (Debugging Only)
For testing or when automatic invocation fails:
1. Use the `Skill` tool with skill name: `/extract-epiroc-bev-report`
2. This loads the full SKILL.md for inspection
3. Then use the scripts manually if needed

**Note:** Manual invocation is NOT the intended workflow - it's for debugging only.

---

## Troubleshooting

### Skill Not Triggering Automatically?

**Check 1: Is the skill installed?**
```bash
ls ~/.claude/skills/
ls .claude/skills/
```

**Check 2: Is SKILL.md properly formatted?**
- Must have YAML frontmatter with `name` and `description`
- Description should clearly state WHEN to use the skill

**Check 3: Does request match description?**
- Use phrases that align with skill's described purpose
- Example: "create meeting" matches "create/delete meetings via Outlook"

**Check 4: Test with manual invocation**
- Use Skill tool to verify skill exists and loads correctly
- If manual works but automatic doesn't, description may need improvement

### Script Execution Fails?

**Check 1: Prerequisites installed?**
- Python version correct?
- Required libraries installed? (pywin32, python-pptx, etc.)

**Check 2: File paths correct?**
- Scripts use absolute paths from skill directory
- Check script location: `scripts/script_name.py`

**Check 3: Permissions?**
- Windows: Outlook must be running for outlook-extractor
- File system: Read/write permissions on target directories

---

## Version Control Considerations

### Current Setup (Personal Skills)
- Skills in `~/.claude/skills/` are NOT version controlled
- Each team member would need manual installation
- Changes not tracked in git

### Recommended for MarthaVault Project
Consider moving project-specific skills to `.claude/skills/`:

**Candidates for Project Skills:**
- `extract-epiroc-bev-report` - Specific to mining operations
- `extract-pptx-heal` - Specific to HEAL reporting workflow

**Keep Personal:**
- `outlook-extractor` - Generic tool used across all projects

**Benefits of Project Skills:**
- Automatic sharing with team via git
- Version controlled alongside project
- Team members get skills on `git clone` or `git pull`

**To Convert:**
```bash
# Copy skill to project
cp -r ~/.claude/skills/extract-epiroc-bev-report .claude/skills/

# Add to git (if desired)
git add .claude/skills/extract-epiroc-bev-report
git commit -m "feat: add Epiroc BEV report extraction skill"

# Optional: Remove from personal (keep both if preferred)
# rm -rf ~/.claude/skills/extract-epiroc-bev-report
```

---

## Learning From October 21, 2025 Session

### What Happened
- User requested: "add all events 21st and 4/11 [to outlook calendar]"
- Claude initially tried manual file operations instead of using skill
- Only after user prompted did Claude use `outlook-extractor` skill
- Skills WERE pre-loaded correctly - Claude failed to recognize the match

### What SHOULD Have Happened
1. ✅ User request: "add to my outlook calendar"
2. ✅ Claude recognizes: matches `outlook-extractor` description "create/delete meetings"
3. ✅ Claude automatically triggers skill
4. ✅ Claude executes: `create-meeting` command with proper parameters
5. ✅ No manual intervention needed

### Root Cause
- Skills system working correctly (metadata pre-loaded)
- Claude failed to match natural language request to skill description
- This is a **model behavior issue**, not a setup problem

### Action Items
- ✅ Skills are correctly installed and pre-loaded
- ✅ Claude needs to improve automatic skill recognition
- ✅ Documentation created for future reference
- ⏳ Consider moving project-specific skills to `.claude/skills/` for team sharing

---

## References

### Official Documentation
- [Claude Code Skills Guide](https://docs.claude.com/en/docs/claude-code/skills.md)
- [Skills vs Slash Commands](https://docs.claude.com/en/docs/claude-code/slash-commands.md)
- [Plugins Documentation](https://docs.claude.com/en/docs/claude-code/plugins.md)

### Anthropic Blog Posts
- [Agent Skills Announcement](https://www.anthropic.com/news/skills) - October 16, 2025
- [Engineering Deep Dive](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### Internal Documentation
- Project CLAUDE.md: `C:\Users\10064957\My Drive\GDVault\MarthaVault\CLAUDE.md`
- User CLAUDE.md: `C:\Users\10064957\.claude\CLAUDE.md`
- Skill directories:
  - Personal: `C:\Users\10064957\.claude\skills\`
  - Project: `C:\Users\10064957\My Drive\GDVault\MarthaVault\.claude\skills\` (not yet created)

---

## Quick Reference Commands

### List Available Skills
```bash
ls ~/.claude/skills/
ls .claude/skills/
```

### Test Skill Manually
```bash
# Load skill documentation
# Use Skill tool in Claude Code: /skill-name

# Execute script directly
python ~/.claude/skills/skill-name/scripts/script_name.py [args]
```

### Create New Skill
```bash
# Create skill directory
mkdir ~/.claude/skills/my-new-skill

# Create SKILL.md with frontmatter
cat > ~/.claude/skills/my-new-skill/SKILL.md << EOF
---
name: "My New Skill"
description: "Description of what the skill does and when to use it"
---

# My New Skill

## When to Use This Skill
[Explain when Claude should use this skill]

## Usage
[Provide examples]
EOF

# Add scripts if needed
mkdir ~/.claude/skills/my-new-skill/scripts
```

---

**Last Updated:** 2025-10-21
**Author:** Gregory Karsten (with Claude Code assistance)
**Status:** Living document - update as skills evolve