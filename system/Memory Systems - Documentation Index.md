# Memory Systems - Documentation Index

**Status**: Active
**Last Updated**: 2025-11-05
**Purpose**: Central navigation hub for all MarthaVault memory system documentation

---

## 📚 Document Library

### 1. Architecture & Integration
**[[Memory Systems Architecture - Claude Desktop Integration]]**
- **Purpose**: Visual architecture and integration guide
- **Audience**: Understanding the 3-layer orchestration model
- **Key Content**:
  - System architecture diagram (Native → Graph → Basic → Vault)
  - Role separation (Desktop vs CLI)
  - Decision matrix: Which layer for which query type
  - Integration points and configuration
  - Migration roadmap (Phase 1 → Phase 1.5 → Phase 2)
- **When to read**: First time setup, understanding how systems work together

---

### 2. Quick Reference Guide
**[[Dual Memory System - Quick Reference Guide]]**
- **Purpose**: Day-to-day operational reference
- **Audience**: Claude Desktop users and CLI automation
- **Key Content**:
  - 30-second health check procedure
  - Human memory analogy (explicit vs semantic)
  - Storage locations and formats
  - Progressive discovery pattern
  - Hybrid query patterns
  - Troubleshooting common issues
  - Best practices for Desktop vs CLI
- **When to read**: Daily use, troubleshooting, learning query patterns

---

### 3. Session Startup Protocol
**[[Memory Systems - Session Startup Protocol]]**
- **Purpose**: Automated health check and context loading
- **Audience**: Claude Code CLI sessions
- **Key Content**:
  - Simplified startup for Claude Desktop (10-second health check)
  - Full 3-phase protocol for CLI (health → context → intelligence)
  - Output format templates (healthy/degraded/broken states)
  - Automated repair workflows
  - Progressive discovery during session
- **When to read**: First session, long break, suspected issues, explicit health check request

---

### 4. Implementation & Validation Report
**[[Memory Systems Implementation & Validation Report]]**
- **Purpose**: Complete case study documenting discovery, fixes, and testing
- **Audience**: Technical reference, troubleshooting deep issues
- **Key Content**:
  - Part 1: Problem Discovery (3 root causes)
  - Part 2: Systematic Fixes (5 fixes applied)
  - Part 3: Comparative Testing (Test 1.2, 2.1 results)
  - Part 4: Key Learnings & Insights (6 major insights)
  - Part 5: Performance Benchmarks (4x speed, 25% accuracy)
  - Appendices: Entity inventory, relations schema, testing framework
- **When to read**: Deep troubleshooting, understanding system design decisions, reference for future enhancements

---

## 🚀 Quick Start Paths

### For Claude Desktop Users (Primary Interface)
1. Read: **Architecture & Integration** → Understand the 3-layer model
2. Skim: **Quick Reference Guide** → Sections on "When to use each system" and "Hybrid query patterns"
3. Bookmark: **Quick Reference Guide** → For daily troubleshooting
4. Optional: **Startup Protocol** → Only if health check needed

### For Claude Code CLI Users (Background Automation)
1. Read: **Architecture & Integration** → Understand role separation
2. Read: **Startup Protocol** → Full 3-phase health check
3. Read: **Quick Reference Guide** → Progressive discovery and troubleshooting
4. Reference: **Implementation Report** → Deep technical issues

### For Troubleshooting
1. Start: **Quick Reference Guide** → "Troubleshooting Guide" section
2. If degraded: **Startup Protocol** → Run automated health check
3. If broken: **Implementation Report** → Part 2 (Systematic Fixes)
4. If unclear: **Architecture & Integration** → Verify correct layer usage

---

## 🎯 Common Scenarios → Document Map

| Scenario | Primary Document | Secondary Reference |
|----------|------------------|---------------------|
| **First-time setup** | Architecture & Integration | Quick Reference Guide |
| **Daily queries** | Quick Reference Guide | Architecture (decision matrix) |
| **Session startup** | Startup Protocol | Quick Reference (health check) |
| **System not finding data** | Quick Reference (troubleshooting) | Implementation Report (fixes) |
| **Slow queries** | Architecture (decision matrix) | Implementation Report (benchmarks) |
| **Database path wrong** | Implementation Report (Error 1) | Startup Protocol (repair) |
| **Missing entities** | Implementation Report (Error 2) | Quick Reference (sync status) |
| **Understanding architecture** | Architecture & Integration | Implementation Report (insights) |
| **Learning query patterns** | Quick Reference (progressive discovery) | Architecture (hybrid patterns) |
| **Performance comparison** | Implementation Report (Part 5) | Quick Reference (decision tree) |

---

## 📊 System Status at a Glance

**Basic Memory**:
- **Database**: `~/.basic-memory/memory.db`
- **Indexed Files**: 613 (100% synced as of 2025-10-25)
- **Project Path**: `C:/Users/10064957/My Drive/GDVault/MarthaVault`
- **Health Check**: `mcp__basic-memory__sync_status(project="main")`

**Graph Memory**:
- **Database**: `.martha/memory.json` (JSONL, in-memory with periodic flush)
- **Entities**: 100+ (Personnel, Projects, Tasks, Strategy, Locations, Decisions)
- **Relations**: 88+ (reports_to, manages, assigned_to, aligns_with, etc.)
- **Health Check**: `mcp__memory__search_nodes("Gregory Karsten")` (expect 29+ relations)

**Vault Sync**:
- **Checkpoint**: `.vault-sync-checkpoint` (git commit SHA)
- **Health Check**: `cat .vault-sync-checkpoint && git rev-parse HEAD` (must match)
- **Full Sync**: `/sync-vault --full` (force re-index all files)

---

## 🔗 Related Documentation

**MarthaVault Core**:
- [[CLAUDE.md]] - Vault operating instructions
- [[system/policy.md]] - Always-on behavioral rules
- [[README.md]] - 6-phase roadmap (Phase 1 ✅, Phase 1.5 current, Phase 2 next)

**Phase 2 Planning** (Next Steps):
- Obsidian watcher plugin for real-time vault indexing
- Automated startup protocol (SessionStart hook)
- Post-commit Git hook for automatic `/sync-vault`

---

## 📝 Version History

- **2025-11-05**: Created documentation index
- **2025-10-29**: Added Claude Desktop integration sections
- **2025-10-25**: Completed Phase 1 implementation and validation
- **2025-10-21**: Initial memory systems setup

---

## 💡 Quick Tips

1. **Claude Desktop users**: Native Memory orchestrates for you - trust it, query naturally
2. **CLI users**: Run startup protocol every session for context loading
3. **Troubleshooting**: Start with Quick Reference, escalate to Implementation Report
4. **Learning**: Architecture for "why", Quick Reference for "how", Report for "what happened"
5. **Performance**: Graph for facts/relations (fast), Basic for semantic search (comprehensive)

---

#system #memory-systems #documentation #reference #year/2025
