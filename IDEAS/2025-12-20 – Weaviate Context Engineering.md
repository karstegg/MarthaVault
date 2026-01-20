---
'Status:': Draft
'Priority:': High
'Tags:': null
'Source:': https://weaviate.io/blog/context-engineering
permalink: ideas/2025-12-20-weaviate-context-engineering
---

# Weaviate: Context Engineering Guide

## What is Context Engineering?

The discipline of designing systems that deliver the right information to LLMs at optimal times. Treats the finite context window as a scarce resource requiring strategic allocation.

## Six Foundational Pillars

1. **Agents** - Decision-making systems that orchestrate information flow and tool selection
2. **Query Augmentation** - Refining user inputs to match different downstream tasks
3. **Retrieval** - Optimizing how external knowledge is fetched (chunking strategies)
4. **Prompting Techniques** - Guiding model behavior (Chain-of-Thought, etc.)
5. **Memory** - Storing info in layers (short-term context, long-term external storage)
6. **Tools** - Enabling agents to interact with external systems

## Failure Modes to Avoid

- Context poisoning
- Distraction
- Confusion
- Clash

## Tools Mentioned

- **Elysia**: Open-source agentic RAG framework with built-in tools
- **Model Context Protocol (MCP)**: Standardization for tool integration
- **Weaviate**: Vector database for knowledge retrieval

## Application to MarthaVault

- Memory layering aligns with Graph Memory + Basic Memory architecture
- Could improve vault sync and context building
- Retrieval optimization for production data analysis

## Notes

Discovered via ClaudeBox triage 2025-12-20.