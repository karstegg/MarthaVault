---
Status:: Draft
Priority:: Critical
Assignee:: Greg
DueDate:: 2025-10-13
Tags:: #year/2025 #idea #architecture #critical #intuition-layer
---

# CRITICAL: Persistent Memory Architecture Decision

**Date:** October 6, 2025
**Priority:** 🔴 CRITICAL - Blocks Phase 2+
**Status:** Architecture decision required before proceeding

---

## 🚨 **Problem Discovered**

### **The Issue**
Current Graph Memory implementation (`@modelcontextprotocol/server-memory`) is **volatile (RAM-only)**:
- All entities and relations lost on MCP server restart
- No persistence across sessions
- **Fundamentally incompatible** with Intuition Layer vision (Phases 2-6)

### **Impact on Roadmap**
Phase 3+ requirements **cannot be implemented** with volatile memory:
- ❌ Behavioral intelligence (confidence scoring)
- ❌ Pattern learning over time
- ❌ User edit pattern analysis
- ❌ Success rate tracking
- ❌ Pattern strengthening/decay
- ❌ "Learning your way of working"

**This is a foundational architecture flaw that must be fixed before Phase 2.**

---

## 📊 **Current Architecture (Broken for Learning)**

```
Markdown Files (Git)
    ↓ Source of Truth
Graph Memory (RAM) ← ❌ VOLATILE - Lost on restart
Basic Memory (SQLite) ← ✅ Persistent
    ↓
Claude Code Queries
```

**Why this breaks learning:**
- Confidence scores stored in volatile memory = lost
- Pattern history wiped on restart = no learning
- User preferences forgotten = no intuition
- Behavioral cache meaningless = starts from scratch every time

---

## 🎯 **Required Architecture (Phase 2+)**

### **Three-Layer Persistence Model**

```
┌─────────────────────────────────────────┐
│ LAYER 1: SOURCE OF TRUTH                │
│ - Markdown files (Git version control)  │
│ - Human-readable, editable              │
│ - Synced via /sync-vault                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 2: KNOWLEDGE INDEX (Persistent)   │
│ - Entities & Relations (SQLite)         │
│ - Semantic search (SQLite + embeddings) │
│ - Full content index                    │
│ - Rebuilt from Layer 1                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ LAYER 3: BEHAVIORAL INTELLIGENCE         │
│ - Reflex cache (Intent → Action)        │
│ - Confidence scores (0.0-1.0)           │
│ - Pattern frequencies                   │
│ - Success metrics                       │
│ - User preference learning              │
└─────────────────────────────────────────┘
```

---

## 🔧 **Solution Options**

### **Option 1: Custom Martha Memory Server (RECOMMENDED)**

**Replace** `@modelcontextprotocol/server-memory` with custom persistent implementation:

**Pros:**
- ✅ Full control over persistence
- ✅ Single unified memory system
- ✅ Optimized for MarthaVault use case
- ✅ Foundation for Phases 2-6
- ✅ Can implement learning algorithms
- ✅ Performance tuning possible

**Cons:**
- ⚠️ Development effort (2-3 weeks)
- ⚠️ Need to implement MCP protocol
- ⚠️ Ongoing maintenance responsibility

**Implementation:**
```python
# martha-memory-server/
├── main.py              # MCP server entry point
├── knowledge_graph.py   # Entities & relations (SQLite)
├── semantic_search.py   # Content indexing
├── behavioral_cache.py  # Learning & patterns (Phase 3)
└── config.py            # Database paths, settings
```

**Database Structure:**
```sql
-- knowledge.db
entities (id, name, type, observations, created_at, updated_at)
relations (id, from_id, to_id, relation_type, context, created_at)
documents (id, path, content, embedding, last_synced)

-- behavioral.db (Phase 3)
reflexes (id, intent_pattern, entity_pattern, site_pattern, action, confidence, success_count, failure_count)
preferences (id, preference_type, key, value, strength, last_updated)
patterns (id, pattern_type, pattern_data, frequency, last_seen)
```

**Migration Path:**
1. Week 1: Implement persistent Graph Memory replacement
2. Week 2: Migrate to custom server, test parity
3. Week 3: Add behavioral intelligence foundation
4. Week 4+: Implement learning algorithms

---

### **Option 2: Keep Volatile Graph, Add Learning Database**

Keep `@modelcontextprotocol/server-memory` for quick lookups, add separate learning database.

**Pros:**
- ✅ Faster initial implementation
- ✅ Uses official Anthropic server
- ✅ Less code to maintain

**Cons:**
- ❌ Entities duplicated (RAM + SQLite)
- ❌ Sync complexity (two sources of truth)
- ❌ More failure modes
- ❌ No control over Graph Memory behavior
- ❌ Learning disconnected from knowledge graph

**Not recommended** due to complexity and fragility.

---

### **Option 3: Extend Basic Memory**

Enhance existing Basic Memory MCP server to handle both knowledge graph AND behavioral intelligence.

**Pros:**
- ✅ Single MCP server
- ✅ Already persistent
- ✅ Already in use

**Cons:**
- ❌ Mixing concerns (knowledge + learning)
- ❌ May not support graph queries well
- ❌ Unknown codebase quality
- ❌ Third-party dependency

**Evaluation needed** - check Basic Memory source code first.

---

## 📅 **Decision Timeline**

### **This Week (Oct 6-11):**
- [ ] Review Basic Memory source code capabilities
- [ ] Prototype SQLite schema for persistent Graph Memory
- [ ] Estimate development effort for Option 1
- [ ] **DECISION**: Choose architecture approach by Friday Oct 10

### **Next Week (Oct 13-18):**
- [ ] If Option 1: Start Martha Memory Server development
- [ ] If Option 3: Extend Basic Memory server
- [ ] Update README.md with revised roadmap

### **Blockers:**
- Phase 2 (Obsidian Plugin) should NOT proceed until memory persistence is resolved
- Phase 3 (Behavioral Intelligence) is impossible without this fix

---

## 💡 **Key Insights**

### **Why Volatile Memory Seemed OK Initially:**
- Git is the source of truth → rebuild is fast
- Entities/relations can be re-extracted from markdown
- **But:** Learning patterns CANNOT be re-extracted from markdown
- **Learning requires** accumulation over time, which requires persistence

### **The Fundamental Requirement:**
> "The Intuition Layer must remember patterns, preferences, and confidence scores across sessions, weeks, and months. This is impossible with volatile memory."

### **What Makes Martha Different:**
- Not just a knowledge base (that can be volatile)
- **A learning system** (must be persistent)
- Behavioral adaptation requires historical data
- Confidence scoring requires success/failure tracking over time

---

## 🎯 **Recommendation**

**Implement Option 1: Custom Martha Memory Server**

**Rationale:**
1. Full control over persistence and learning algorithms
2. Purpose-built for MarthaVault's unique needs
3. Foundation for all future phases
4. Investment pays off long-term
5. Clean separation of concerns

**Timeline:**
- Week 1 (Oct 7-13): Design & schema
- Week 2-3 (Oct 14-25): Development & testing
- Week 4 (Oct 26-31): Migration & validation
- Phase 2 starts: November 2025

**Alternative:**
If development time is prohibitive, evaluate Option 3 (extend Basic Memory) as a pragmatic compromise.

---

## 🔗 **Related Documents**
- [[README.md]] - Intuition Layer roadmap (needs update)
- [[IDEAS/Martha Design n Evolution/2025-09-24 – Intuition Layer Design]] - Original vision
- [[strategy/ActivePhase.md]] - Q4 2025 priorities (may need adjustment)

---

## 📝 **Action Items**

- [ ] **Greg**: Review this analysis and choose architecture direction
- [ ] **Greg**: Set deadline for decision (recommend Friday Oct 10)
- [ ] **Claude**: Research Basic Memory source code capabilities
- [ ] **Claude**: Draft SQLite schema for Martha Memory Server
- [ ] **Greg + Claude**: Weekly review session (Monday Oct 13) to finalize approach

---

**Status:** Awaiting decision
**Next Review:** Friday, October 10, 2025
**Blocking:** Phase 2, 3, 4, 5, 6 of Intuition Layer roadmap
