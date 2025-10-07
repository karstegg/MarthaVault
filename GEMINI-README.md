# Gemini CLI Integration for MarthaVault

**Date:** 2025-10-06

This document outlines the process of configuring the Gemini CLI to act as an intelligent agent within the MarthaVault, serving as a viable alternative to the existing Claude agent.

## Objective

The primary goal was to replicate the core functionalities of the Claude agent, particularly its advanced memory systems, using the tools available to the Gemini CLI. This involved establishing a new set of instructions (`GEMINI.md`) and implementing both "Basic" and "Graph" memory capabilities.

---

## Phase 1: Initial Setup & Basic Memory

### `GEMINI.md` Instruction File

The first step was to create `GEMINI.md`, a dedicated instruction file for the Gemini agent. This file was adapted from `CLAUDE.md` and defines Gemini's identity, operating modes, and core instructions.

### Basic Memory System

A "Basic Memory" system was established, as documented in `GEMINI.md`. This system relies on Gemini's built-in tools to perform keyword and regex-based searches across the vault.

- **Tools Used:** `search_file_content`, `glob`, `read_file`
- **Capability:** Allows Gemini to answer questions based on the literal content found within notes, as demonstrated when answering questions about the "HD0054 fire incident".

---

## Phase 2: Graph Memory Implementation (File-Based)

To replicate Claude's ability to understand relationships between notes, we implemented a file-based Graph Memory system.

### Approach

After discussing the possibility of connecting to an existing "mcp server", the decision was made to first build a graph from scratch by scanning the vault's contents. This approach provides a self-contained, functional graph without external dependencies.

### The `create_graph.py` Script

A Python script was created at `scripts/create_graph.py` to serve as the engine for the Graph Memory.

- **Functionality:**
    1.  Recursively scans the entire vault directory for markdown files (`.md`).
    2.  Ignores hidden directories (e.g., `.git`, `.obsidian`).
    3.  Parses each file to extract entities from file names and `[[wiki-links]]`.
    4.  Establishes `links_to` relationships between the entities.
    5.  Outputs the results into two structured JSON files in the `.gemini/` directory:
        - `entities.json`: A flat list of all unique entities found.
        - `relationships.json`: A list of all source-target relationships.

- **Execution & Results:**
    - After fixing an initial syntax error related to character escaping, the script was run successfully.
    - The initial scan found **734 entities** and **1188 relationships**, creating the first version of the graph.

### Demonstrated Capability

This new Graph Memory was successfully tested by answering the question: **"Who does SK report to?"**

1.  Gemini identified "SK" as "Sikelela Nzuza" from `entities.json`.
2.  By querying `relationships.json`, it found that the `2025-07-29 – Assmang Black Rock Org Chart.md` note was linked to "Sikelela Nzuza".
3.  By reading the content of the org chart note, Gemini determined that **Sikelela Nzuza reports to Gregory Karsten**.

---

## Future Work: MCP Server Integration

While the file-based graph is functional, it is not real-time and requires manual re-scans to stay updated.

An idea for a future upgrade has been captured in the note:
- **[[IDEAS/2025-10-06 - Gemini CLI Future Upgrade - MCP Server Integration.md]]**

This proposes replacing the file-based system with a connection to a dedicated `mcp` server, which would provide more robust, real-time memory capabilities and align Gemini's architecture with other agents in the ecosystem.

## Current Status

As of now, the Gemini CLI is functionally aligned with the core memory capabilities of the Claude agent. It possesses both a basic text-based memory and a functional, relationship-aware graph memory, making it a powerful and effective agent for working within the MarthaVault.
