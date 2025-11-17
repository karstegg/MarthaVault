---
title: Memory Systems Phase 2 - Automated Indexing Project
type: note
permalink: projects/memory-systems-phase-2-automated-indexing-project
tags:
- personal
- MarthaVault
- memory-systems
- phase-2
- automation
- project
---

# Memory Systems Phase 2 - Automated Indexing Project

**Status:** Ready for Implementation
**Priority:** High (1.54 strategic score)
**Timeline:** 4 weeks (Nov 13 - Dec 11, 2025)
**Due Date:** 2025-12-11

## Problem Statement

**Nov 13 Discovery:** Three-tier memory system (Native + Graph + Basic Memory) had 8-day indexing gap. Memory queries returned stale Nov 5 data, missing Nov 10-13 critical activity:
- 8 OEM coordination meetings (CAS L9 DMRE deadline support)
- Production Support Meeting Framework establishment
- Emergency Preparedness Meeting (5 critical actions)
- BEV Fire Safety CO Sensor Decision (CRITICAL, 2.0x strategic priority)
- 4 new personnel (Jacques Breet, Jacques Farmer, Hendrik van Niekerk, Azena le Roux)

**Root Cause:** Passive indexing architecture with no automated file-change detection or scheduled resyncs.

## Solution: Phase 2 Automated Memory Indexing

### Goals
- **Primary:** Reduce indexing lag from 8 days to <5 minutes
- **Secondary:** Achieve >90% entity detection accuracy, >80% relation auto-creation
- **Operational:** Require <10% manual intervention for entity creation

### Implementation Plan

**Week 1 (Nov 13-20):** Core Hooks
- File-change watcher for Schedule/ and 00_Inbox/
- Entity detection logic (meetings, decisions, personnel)
- Retroactive validation on Nov 5-13 activity
- Production deployment with logging

**Week 2 (Nov 20-27):** Scheduled Sync
- Daily resync script (sync_vault_to_memory.py)
- Checksum-based change detection
- Relation validation and pruning
- 02:00 SAST scheduled execution

**Week 3 (Nov 27-Dec 4):** Smart Detection
- Business Process vs one-time event differentiation
- Decision entity auto-detection
- Relation auto-discovery from wikilinks/tags
- Accuracy testing on historical vault data

**Week 4 (Dec 4-11):** Memory Update Subagent
- Autonomous indexing agent for complex tasks
- Task tool integration for parsing
- Batch processing for bulk imports
- User approval workflow for ambiguous cases

### Technical Architecture

**Components:**
1. **File-change watcher:** Python watchdog library monitoring vault directories
2. **Entity detector:** Pattern matching for entity types (Business Process, Decision, Personnel, Task, Project)
3. **Relation builder:** Wikilink and tag parsing for automatic relation creation
4. **Daily resync:** Scheduled job at 02:00 SAST for validation and gap-filling
5. **Logging:** `.martha/indexing.log` for monitoring and troubleshooting

**Watched Directories:**
- `Schedule/` - Calendar events and meetings
- `00_Inbox/` - New captures requiring triage
- `projects/*/` - Project documentation updates
- `people/` - Personnel file changes
- `tasks/` - Task list modifications

### Nov 13 Manual Sync (Completed)

**Graph Memory:**
- +12 entities (52 → 64)
- +15 relations (60 → 75+)
- Now current through Nov 13

**Basic Memory:**
- +2 meeting notes (Production Support, Emergency Preparedness)
- Semantic search verified working

## Strategic Alignment

**Aligns with:**
- Team Capacity Building (Q4 2025 Active Phase) - 1.2x multiplier
- Personal/Professional Development
- MarthaVault Intuition Layer Phase 2 roadmap

**Priority Calculation:**
- Base: 0.70 (high value, medium urgency)
- Strategic Multiplier: 1 + 1.2 = 2.2
- Final: 0.70 × 2.2 = **1.54 (HIGH)**

**Rationale:** Automated memory indexing is foundational infrastructure enabling all MarthaVault workflows. Without it, context retrieval remains manual and error-prone.

## Success Metrics

**Technical:**
- Indexing lag < 5 minutes from file creation to memory availability
- Entity detection accuracy > 90%
- Relation auto-creation > 80% of obvious connections
- User intervention < 10% of files

**Operational:**
- Memory queries always return recent activity (last 48 hours minimum)
- Zero undetected indexing gaps > 24 hours
- Strategic context preserved (project-to-strategy relations auto-created)

## Key Files

**Project Documentation:**
- [[projects/Memory_Systems_Phase_2/2025-11-13 – Memory Systems Gap Resolution and Phase 2 Planning.md]] - Session summary and pickup guide

**Technical Specifications:**
- [[system/2025-11-13 – Memory Systems Phase 2 Auto-Indexing Requirements.md]] - Full implementation spec (4,800+ words)

**Task Tracking:**
- [[tasks/master_task_list.md]] lines 77-89 - Master task entry with timeline

## Next Session Pickup

**Start by reading:**
1. Technical spec in system/
2. Project summary in projects/Memory_Systems_Phase_2/

**Check memory status:**
- `mcp__memory__search_nodes("Personnel")` - Verify Graph Memory entity count
- `mcp__basic-memory__recent_activity(timeframe="7d")` - Confirm Basic Memory up-to-date

**Begin Week 1:**
- Choose file-watching library (watchdog recommended)
- Design entity detection patterns
- Set up logging infrastructure

**Key Question:** What entity detection patterns will reliably distinguish Business Processes from one-time events?

## References

**Related Phases:**
- Phase 1: Manual indexing with Graph + Basic Memory MCPs (COMPLETE)
- Phase 3: Behavioral intelligence with SQLite reflex cache (PLANNED)
- Phase 4: Advanced strategic integration and priority calculation (PLANNED)

**MCP Tools:**
- `mcp__memory__create_entities()` - Graph Memory entity creation
- `mcp__memory__create_relations()` - Graph Memory relation linking
- `mcp__basic-memory__write_note()` - Basic Memory document indexing

---

**Created:** 2025-11-13
**Owner:** Gregory Karsten
**Next Review:** When starting Phase 2 implementation
