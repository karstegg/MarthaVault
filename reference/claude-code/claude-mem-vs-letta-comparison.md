---
'Status:': Reference
'Created:': 2025-12-22
'Tags:': null
permalink: reference/claude-code/claude-mem-vs-letta-comparison
---

# Comprehensive Comparison: claude-mem vs Letta

## Overview

Two approaches to persistent memory for AI agents:
- **claude-mem**: Plugin for Claude Code CLI - passive capture + intelligent retrieval
- **Letta**: Platform for stateful agents - active self-editing memory

## Architecture Philosophy

| Aspect | claude-mem | Letta |
|--------|------------|-------|
| **Core Concept** | Passive capture + intelligent retrieval | Active self-editing memory |
| **Agent Role** | Observer (captures what Claude does) | Manager (agent controls memory) |
| **Design Origin** | Plugin for Claude Code CLI | MemGPT research paper (LLM as OS) |
| **Memory Model** | Capture → Compress → Retrieve | Edit → Archive → Recall |

## Memory Hierarchy

### claude-mem (3 layers)

```
┌─────────────────────────────────────┐
│ Layer 1: Injected Context           │
│ - ~50 recent observations           │
│ - Session summaries                 │
│ - Passively injected at start       │
└─────────────────────────────────────┘
         ↓ (retrieval on demand)
┌─────────────────────────────────────┐
│ Layer 2: SQLite + FTS5              │
│ - Full-text search                  │
│ - Sessions, prompts, tool results   │
└─────────────────────────────────────┘
         ↓ (semantic search)
┌─────────────────────────────────────┐
│ Layer 3: Chroma Vector DB           │
│ - Embeddings for semantic matching  │
│ - Hybrid keyword + vector search    │
└─────────────────────────────────────┘
```

### Letta (4 layers)

```
┌─────────────────────────────────────┐
│ Core Memory (always in context)     │
│ - Persona, human, custom blocks     │
│ - ~2000 chars per block             │
│ - AGENT EDITS DIRECTLY              │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Message Buffer (rolling window)     │
│ - Recent conversation               │
│ - Fixed capacity, FIFO overflow     │
└─────────────────────────────────────┘
         ↓ (overflow → archive)
┌─────────────────────────────────────┐
│ Archival Memory (vector DB)         │
│ - Agent-managed storage             │
│ - Semantic search                   │
│ - Agent decides what to store       │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Recall Memory (raw history)         │
│ - Full conversation logs            │
│ - Searchable by date/content        │
└─────────────────────────────────────┘
```

## Self-Editing Capability

| Aspect | claude-mem | Letta |
|--------|------------|-------|
| **Who edits memory?** | Background worker (AI extraction) | Agent itself (in-loop) |
| **When?** | Post-session, async | During conversation, real-time |
| **Edit tools** | None (passive) | `memory_replace`, `memory_insert`, `memory_rethink` |
| **Agent awareness** | Unaware of capture | Fully aware, decides what to remember |

### Letta's Self-Editing Tools

- `memory_replace` — targeted text substitution in a block
- `memory_insert` — add new lines to block
- `memory_rethink` — completely rewrite block
- `archival_memory_insert` — store in long-term
- `archival_memory_search` — retrieve from long-term
- `conversation_search` — search chat history

### claude-mem Approach

No agent editing. Worker process extracts "observations" asynchronously using Claude Agent SDK.

## Data Capture

| Aspect | claude-mem | Letta |
|--------|------------|-------|
| **What's captured** | Everything (sessions, prompts, tool executions) | What agent decides to store |
| **Observation types** | decision, bugfix, feature, refactor, discovery, change | User defines block structure |
| **Extraction method** | Claude Agent SDK (async worker) | Agent tools (in-loop) |
| **Privacy control** | `<private>` tags | Agent discretion |

## Storage & Retrieval

| Aspect | claude-mem | Letta |
|--------|------------|-------|
| **Primary storage** | SQLite + Chroma (local) | PostgreSQL + Chroma (server) |
| **Search types** | FTS5 + semantic | Semantic + date-based |
| **Deployment** | Local plugin | Server + client architecture |
| **Web UI** | localhost:37777 | Letta Cloud or self-hosted |

## Integration & Hooks

### claude-mem (5 lifecycle hooks)

1. `SessionStart` — inject recent observations
2. `UserPromptSubmit` — save prompts
3. `PostToolUse` — capture tool executions
4. `Stop` — checkpoint
5. `SessionEnd` — generate summary

### Letta

- No hooks needed — agent manages memory natively
- Tools are first-class citizens in agent's capabilities
- Server handles persistence automatically

## Context Management

| Aspect | claude-mem | Letta |
|--------|------------|-------|
| **Always in context** | ~50 observations (configurable) | Core memory blocks |
| **Context optimization** | "Endless Mode" (experimental) | Native compression/decompression |
| **Scaling** | O(N) in endless mode | Native hierarchical management |

## Use Cases

### claude-mem excels at

- Comprehensive session history across all projects
- "What did I do last week?" queries
- Cross-project pattern discovery
- Zero-config capture (just install and go)

### Letta excels at

- Personalized agents that learn preferences
- Long-running agents with evolving context
- Agents that need to actively forget/update
- Multi-agent systems with shared memory

## Key Differentiators

| Feature | claude-mem | Letta |
|--------|------------|-------|
| **Memory agency** | Passive capture | Active management |
| **Real-time learning** | Async extraction | In-loop editing |
| **Works with Claude Code** | Native plugin | Separate platform |
| **Self-improvement** | Capture only | Agent decides what matters |
| **Setup complexity** | Low (npm install) | Higher (server deployment) |
| **Transparency** | View captured data | Agent explains memory decisions |

## MarthaVault Context

| Consideration | claude-mem | Letta |
|---------------|------------|-------|
| **Compatibility** | Works with CCLI today | Requires migration |
| **Preserves vault** | Additive layer | Different paradigm |
| **Graph/Basic Memory** | Complements existing | Replaces with Letta memory |
| **Rollback** | DB backup | Different system |
| **Skills/commands** | Preserved | Would need reimplementation |

## Summary

**claude-mem** = **Comprehensive historian** — captures everything, searches intelligently, but doesn't actively learn during conversations.

**Letta** = **Self-aware agent** — actively manages its own memory, decides what to remember, forgets what's irrelevant, but requires platform migration.

**Proposed MV Memory Blocks** = **Best of both** — Letta-style self-editing via Edit tool on `.claude/memory/*.md` files, while preserving CCLI, vault, and optionally adding claude-mem as archive layer.

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

## Letta Links

**Main Resources:**
- GitHub: https://github.com/letta-ai/letta
- Documentation: https://docs.letta.com
- Memory Guide: https://docs.letta.com/guides/agents/memory/

**Additional Reading:**
- [Adding memory to LLMs with Letta](https://tersesystems.com/blog/2025/02/14/adding-memory-to-llms-with-letta/)
- [Graphlit vs Letta Comparison](https://www.graphlit.com/vs/letta)
- [MemGPT Research Background](https://docs.letta.com/concepts/letta/)

## Related Files

- `IDEAS/2025-12-22 – Memory-Catcher Agent for Session Insights.md` - Memory-Catcher vs claude-mem comparison
- `.claude/plans/federated-kindling-anchor.md` - MV Memory Blocks implementation plan
- `reference/claude-code/memory-systems.md` - Current MV memory architecture