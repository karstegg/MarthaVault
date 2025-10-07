---
Status:: Idea
Priority:: Medium
Assignee:: Greg
DueDate::
Tags:: #idea #year/2025 #gemini #cli #upgrade #mcp #memory
---

# Idea: Upgrade Gemini CLI with MCP Server Integration

**Date:** 2025-10-06

## Summary

This note captures the idea to upgrade the Gemini CLI's memory capabilities by integrating it with a dedicated "MCP" (Martha Control Program) server, mirroring the architecture used by the Claude agent.

## Current System

Currently, Gemini's memory consists of two systems:
1.  **Basic Memory:** Relies on direct file search tools (`search_file_content`, `glob`).
2.  **Graph Memory:** Relies on a Python script (`create_graph.py`) that periodically scans the vault and generates static JSON files (`entities.json`, `relationships.json`).

## Proposed Upgrade

The proposal is to replace both of these systems with a connection to a dedicated `mcp` server that would provide real-time Basic and Graph memory services through an API.

### Benefits

*   **Real-Time Updates:** The memory would always be up-to-date, eliminating the need to manually run the `create_graph.py` script.
*   **Efficiency:** A dedicated server would likely be much faster and more efficient at handling complex graph queries than parsing local JSON files on every request.
*   **Consistency:** Aligns the Gemini agent's architecture with the more advanced setup used by other agents in the ecosystem (like Claude).
*   **Advanced Capabilities:** Would allow for more sophisticated memory functions, such as those hinted at in `CLAUDE.md` (e.g., temporal filtering, semantic search).

## Action Plan

1.  **Investigate MCP Server:** Resume the investigation into the existing `mcp` server.
    *   Locate its source code, documentation, and any API definitions.
    *   Determine if it's currently running and how to connect to it.
2.  **Define Gemini API/Tool Requirements:** Specify the exact tool functions Gemini would need to interact with the server's Basic and Graph memory. This would likely involve creating tools that replicate the functionality of Claude's `search_nodes`, `build_context`, etc.
3.  **Implementation:**
    *   Develop the new tools for Gemini.
    *   Update `GEMINI.md` to reflect the new server-based architecture.
    *   Deprecate the `create_graph.py` script.
