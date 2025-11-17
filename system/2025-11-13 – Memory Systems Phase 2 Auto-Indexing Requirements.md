# Memory Systems Phase 2 Auto-Indexing Requirements

**Date:** 2025-11-13
**Context:** Gap analysis from Nov 5-13 memory system failure
**Status:** Requirements specification for Phase 2 implementation

---

## Executive Summary

The Nov 5-13 period exposed a critical gap: **passive memory indexing missed 8 days of vault activity**, including:
- 8 OEM coordination meetings (CAS L9 activation wave)
- 2 new business process frameworks (Production Support Meeting, Emergency Preparedness)
- 1 critical safety decision (BEV CO sensor requirement)
- 4 new personnel entries
- 3 major tasks with strategic alignment

**Root Cause:** Memory systems (Graph + Basic) require manual updates. No automated file-change detection or scheduled resyncs exist.

**Impact:** Memory queries from Nov 13 showed stale Nov 5 data, failing to surface recent critical activity.

---

## Current State (Phase 1 - Manual Indexing)

### What Works
✅ **Graph Memory**: 64 entities, 75+ relations (after manual sync Nov 13)
✅ **Basic Memory**: SQLite semantic search operational (after manual write_note calls)
✅ **Native Memory** (Claude Desktop): Conversational learning active

### What Failed
❌ **No real-time indexing**: Files created in Schedule/ and 00_Inbox/ not auto-indexed
❌ **No scheduled resyncs**: Memory snapshots become stale within 24-48 hours
❌ **No entity auto-detection**: Schedule entries don't auto-create Graph entities
❌ **Manual intervention required**: Every new meeting/decision/project needs explicit memory write

---

## Phase 2 Requirements

### 1. Post-File-Change Hook (CRITICAL)

**Trigger:** File creation or modification in watched directories
**Watched Directories:**
- `Schedule/` - Calendar events, meetings
- `00_Inbox/` - New captures requiring triage
- `projects/*/` - Project updates
- `people/` - Personnel file updates
- `tasks/` - Task list changes

**Actions:**
1. Detect file change event (create, modify, delete)
2. Parse file for extractable entities:
   - Meeting → Business Process or one-time event
   - Decision documented → Decision entity
   - New person mentioned → Personnel entity
   - Project milestone → Project entity update
3. Auto-create/update Graph Memory entities
4. Index content in Basic Memory SQLite database
5. Log indexing operations to `.martha/indexing.log`

**Technical Implementation:**
- File system watcher (Python `watchdog` library or Node.js `chokidar`)
- Event queue to batch updates (avoid overload on rapid changes)
- Parsing logic to extract YAML frontmatter, tags, links
- MCP tool invocations: `create_entities()`, `create_relations()`, `write_note()`

**Success Criteria:**
- File-to-memory lag < 5 minutes for new files
- 95%+ accuracy in entity type detection
- Zero duplicate entities created

---

### 2. Scheduled Memory Resync (MEDIUM PRIORITY)

**Frequency:** Daily at 02:00 SAST (off-hours)

**Process:**
1. Scan all watched directories for files modified in last 7 days
2. Compare file checksums against `.martha/indexed_files.json` registry
3. Re-index changed files
4. Prune deleted files from memory systems
5. Validate Graph Memory relations (detect broken links)

**Benefits:**
- Catch any files missed by file-change hook
- Periodic validation prevents drift
- Handles bulk imports or manual edits outside Claude Code

**Technical Implementation:**
- Cron job or systemd timer (Linux/WSL) or Windows Task Scheduler
- Python script: `sync_vault_to_memory.py`
- Uses same parsing/indexing logic as file-change hook

**Success Criteria:**
- Completes in < 10 minutes for typical vault size (500+ files)
- Detects and corrects any indexing gaps from previous 7 days

---

### 3. Smart Entity Detection (HIGH PRIORITY)

**Challenge:** Distinguish between one-time events and recurring processes

**Detection Logic:**

#### Business Process Entity
**Triggers:**
- Meeting title includes "Framework", "Program", "Monthly", "Weekly", "Recurring"
- File content describes structure, cadence, or recurring attendees
- Tags include `#framework`, `#recurring`, `#business-process`

**Example:** "Production Support Meeting Framework" → Business Process entity

#### One-Time Event
**Triggers:**
- Single date/time in frontmatter (not recurring)
- Meeting title includes vendor names, specific project names
- No mention of "weekly", "monthly", "framework"

**Example:** "Aard CAS L9 Activation" → One-time project task, not Business Process

#### Decision Entity
**Triggers:**
- File content includes "decided", "approved", "committed", "requirement"
- Keywords: "CRITICAL", "must", "will", "decision"
- Tags include `#decision`

**Example:** "BEV fire DDOPS must include CO sensors" → Decision entity

#### Personnel Entity
**Triggers:**
- New `[[Lastname, Firstname]]` wikilink in any file
- New file created in `people/` directory
- Mentioned in meeting attendees list

**Auto-actions:**
- Create Personnel entity if not exists
- Extract role, site, reporting structure from context
- Link to mentioned projects/meetings

---

### 4. Relation Auto-Discovery (MEDIUM PRIORITY)

**Parse wikilinks and tags to auto-create relations:**

| Pattern | Graph Relation |
|---------|----------------|
| `[[Person]]` in meeting file | Person `participates_in` Meeting |
| `Assignee:: [[Person]]` in task | Task `assigned_to` Person |
| `#site/Nchwaning3` in file | Entity `located_at` Nchwaning 3 |
| `#priority/critical` + `#BEV` | Task `aligns_with` BEV Fire Safety Programme |
| Meeting organized by X | X `owns_process` Meeting (if recurring) or `organized` Event |

**Success Criteria:**
- 80%+ of obvious relations auto-created
- Manual verification prompt for ambiguous cases
- No incorrect relations (precision > false positives)

---

### 5. Memory Update Subagent (ADVANCED - Phase 2.5)

**Purpose:** Autonomous agent that handles complex indexing tasks

**Capabilities:**
- Parse Schedule/ entries and infer project context
- Detect strategic alignment from tags and links
- Cross-reference new entities with existing Graph Memory
- Suggest new relations for user approval
- Batch-create entities from bulk imports

**Invocation:**
- Triggered by file-change hook for complex files (e.g., multi-entity meetings)
- Triggered by scheduled resync for batch processing
- Manual invocation: `/sync-memory --full` command

**Success Criteria:**
- Reduces manual entity creation by 80%
- Maintains 90%+ accuracy in entity/relation creation
- Completes full vault resync in < 15 minutes

---

## Implementation Roadmap

### Week 1 (Nov 13-20): Core Hooks
- [ ] Implement file-change watcher for Schedule/ and 00_Inbox/
- [ ] Build entity detection logic (meetings, decisions, personnel)
- [ ] Test on Nov 5-13 activity (retroactive validation)
- [ ] Deploy to production with logging

### Week 2 (Nov 20-27): Scheduled Sync
- [ ] Create daily resync script (`sync_vault_to_memory.py`)
- [ ] Implement checksum-based change detection
- [ ] Add relation validation and pruning
- [ ] Schedule daily 02:00 SAST run

### Week 3 (Nov 27-Dec 4): Smart Detection
- [ ] Refine Business Process vs one-time event logic
- [ ] Add Decision entity auto-detection
- [ ] Implement relation auto-discovery from wikilinks
- [ ] Test accuracy on historical vault data

### Week 4 (Dec 4-11): Memory Update Subagent
- [ ] Build autonomous indexing agent
- [ ] Integrate with Task tool for complex parsing
- [ ] Add batch processing for bulk imports
- [ ] User approval workflow for ambiguous cases

---

## Success Metrics

**Primary KPIs:**
- **Indexing Lag:** < 5 minutes from file creation to memory availability
- **Detection Accuracy:** > 90% correct entity type assignment
- **Relation Quality:** > 80% of obvious relations auto-created
- **User Intervention:** < 10% of files require manual entity creation

**Validation Tests:**
1. Create new meeting file → Verify entity appears in Graph Memory within 5 min
2. Run daily resync → Confirm no gaps in indexing for last 7 days
3. Query recent activity → Should return all Nov 13+ activity automatically
4. Strategic context retrieval → Auto-link tasks to Q4 priorities

---

## Lessons Learned (Nov 5-13 Gap)

### What We Discovered
1. **Passive indexing fails silently** - No alerts when memory becomes stale
2. **8-day lag is unacceptable** - Memory should be current within hours, not days
3. **Manual syncs don't scale** - 12 entities + 15 relations took 20+ minutes to add
4. **Strategic context is critical** - Missing CAS L9 OEM wave meant missing DMRE deadline context
5. **Both memory systems needed updates** - Graph alone or Basic alone isn't sufficient

### Design Principles for Phase 2
- **Fail loudly:** Alert if indexing falls > 24 hours behind
- **Validate continuously:** Daily resync catches what hooks miss
- **Precision over recall:** Better to prompt user than create wrong entities
- **Incremental improvement:** Start with high-confidence auto-creation, expand over time

---

## Next Actions

### Immediate (This Week)
- [x] Document Phase 2 requirements (this file)
- [ ] Prototype file-change hook for Schedule/ directory
- [ ] Test entity detection on Nov 10-13 meeting files
- [ ] Design `.martha/indexed_files.json` registry schema

### Short-Term (Next 2 Weeks)
- [ ] Implement production file-change hook
- [ ] Build daily resync script
- [ ] Deploy to MarthaVault with monitoring

### Medium-Term (December)
- [ ] Refine smart detection logic
- [ ] Build Memory Update Subagent
- [ ] Achieve 90%+ auto-indexing rate

---

**Document Owner:** Gregory Karsten
**Last Updated:** 2025-11-13
**Status:** Specification complete, implementation pending
**Priority:** HIGH (directly impacts memory system reliability)
