---
Status:: Draft
Priority:: High
Tags:: #year/2025 #idea #context-engineering #agents #google
Source:: https://github.com/google/adk-python
---

# Google ADK - Context Engineering Framework

Google's Agent Development Kit treats context as a first-class system with its own architecture.

## Core Concept

> "Context is a compiled view over a richer stateful system" - not a mutable string buffer

## The Problem with "Append Everything"

| Issue | Impact |
|-------|--------|
| Cost explosion | Entire history sent every turn |
| Latency degradation | Larger contexts = longer processing |
| "Lost in the middle" | Models struggle with buried instructions |

## Four-Layer Context Architecture

| Layer | Purpose |
|-------|---------|
| **Working Context** | Compiled view sent to LLM (this turn only) |
| **Session** | Interaction history |
| **Memory** | Persistent knowledge |
| **Artifacts** | Large files referenced by handle |

## How It Works

```
Sources (sessions, memory, artifacts)
    ↓ compiler pipeline (flows, processors)
Working context (what LLM sees)
```

## Available In

- Python (primary)
- TypeScript (v0.2.0)
- Go (v0.3.0)

## Relevance to MarthaVault

Maps to our current architecture:
- Working Context → Current prompt + CLAUDE.md
- Session → claude-mem captures this
- Memory → Graph Memory + Basic Memory
- Artifacts → Vault files

Could inform improvements to how we structure context injection.

## Links

- Docs: https://google.github.io/adk-docs/
- GitHub: https://github.com/google/adk-python
- Context Docs: https://google.github.io/adk-docs/context/
- Blog: https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/

## Notes

Discovered via ClaudeBox triage 2025-12-22.
