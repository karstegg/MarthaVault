---
'Status:': Draft
'Priority:': Medium
'Tags:': null
'Source:': https://gist.github.com/alexknowshtml/747f396413fc186fc7502242acbef3be
permalink: ideas/2025-12-22-memory-catcher-agent-for-session-insights
---

# Memory-Catcher Agent for Session Insights

A specialized agent that extracts structured, strategic memories from Claude Code session transcripts.

## What It Does

Analyzes session interactions to capture decisions, insights, patterns, corrections, and learnable information for cross-session recall.

## 10 Memory Types

| Type | What It Captures |
|------|------------------|
| **Decision** | Choices + reasoning |
| **Insight** | Cross-session discoveries |
| **Confidence** | Completeness assessments |
| **Pattern Seed** | Early observations |
| **Commitment** | Promises to follow up |
| **Learning** | Technical discoveries |
| **Correction** | User redirections |
| **Cross-Agent** | Info for other agents |
| **Workflow Note** | Non-standard handling |
| **Gap** | Missing info/capabilities |

## 12 Entity Types Tracked

Persons, Projects, Files, Businesses, Events, Tasks, Reminders, Workstreams, Spaces, Orbits, Commands, Agents

## Quality Guidelines

- 3-10 strategic memories per session
- Confidence scoring (90-100 for explicit, skip below 50)
- Focus on "why" behind choices

## "Surprise Triggers" (High Priority)

- Failures recovered from
- User corrections
- Unexpected enthusiasm
- "Actually, let's do X instead..."

## Comparison to claude-mem

| Aspect | Memory-Catcher | claude-mem |
|--------|----------------|------------|
| Type | Agent prompt | Plugin with hooks |
| Trigger | Manual/scheduled | Automatic |
| Focus | Strategic insights | Comprehensive capture |
| Output | JSON | SQLite + Chroma |

**Complementary:** claude-mem captures everything, Memory-Catcher extracts strategic insights.

## Potential Use Cases

1. Post-session review agent
2. Weekly synthesis of learnings
3. Combine with claude-mem for layered memory

## Notes

Discovered via ClaudeBox triage 2025-12-22.
Consider implementing after claude-mem is tested.

## claude-mem Links

**Main Resources:**
- GitHub: https://github.com/thedotmack/claude-mem
- Web UI: http://localhost:37777 (after install)

**Additional:**
- Author: Alex Newman (@thedotmack)
- License: AGPL-3.0
- Stars: 3.7K+
- Current Version: v6.4.9

**Documentation within repo:**
- CLAUDE.md - How the plugin works
- README.md - Installation & configuration
- CHANGELOG.md - Version history