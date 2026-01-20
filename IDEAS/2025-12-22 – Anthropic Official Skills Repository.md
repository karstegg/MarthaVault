---
'Status:': Draft
'Priority:': High
'Tags:': null
'Source:': https://github.com/anthropics/skills
permalink: ideas/2025-12-22-anthropic-official-skills-repository
---

# Anthropic Official Skills Repository

Official collection of Claude Code skills from Anthropic.

## Stats

- 24.9K stars, 2.3K forks
- 83.9% Python, 9.4% JavaScript

## Repository Structure

```
anthropics/skills/
├── skills/
│   ├── Creative & Design/
│   ├── Development & Technical/
│   ├── Enterprise & Communication/
│   └── Document Skills/
├── spec/                    # Agent Skills specification
└── template/               # Skill template
```

## Skill Categories

- **Creative & Design** - Art, music, design
- **Development & Technical** - Testing web apps, MCP server generation
- **Enterprise & Communication** - Branding workflows
- **Document Skills** - PDF, DOCX, PPTX, XLSX creation/editing

## Skill Structure

```markdown
---
name: my-skill-name
description: What this skill does
---

# My Skill Name

[Instructions for Claude]

## Examples
## Guidelines
```

## Installation

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

## Usage Example

"Use the PDF skill to extract the form fields from path/to/some-file.pdf"

## What to Explore

- [ ] Review document-skills for PDF/DOCX/PPTX handling
- [ ] Check MCP server generation skill
- [ ] Look at template for creating custom skills
- [ ] Compare to our existing skills structure

## Links

- GitHub: https://github.com/anthropics/skills
- Skills API Quickstart: https://docs.claude.com/en/api/skills-guide

## Notes

Discovered via ClaudeBox triage 2025-12-22.
Official Anthropic examples - high quality reference for skill development.