# Memory Systems Architecture

**Status**: Phase 1 Complete (October 2025)
**Reference**: See [[README.md]] for full 6-phase roadmap

---

## Dual Memory System

MarthaVault uses **two complementary memory systems**:

| System | Tool Prefix | Best For |
|--------|-------------|----------|
| **Graph Memory** | `mcp__memory__*` | Entity lookups, relationships, exact queries |
| **Basic Memory** | `mcp__basic-memory__*` | Semantic search, document content, temporal filtering |

**Best Practice**: Use BOTH systems in parallel for comprehensive context.

---

## Quick Decision Matrix

| Use Case | Graph Memory | Basic Memory |
|----------|--------------|--------------|
| Quick lookups | ✅ Entity name/type | ❌ Slower |
| Relationships | ✅ Traverse relations | ✅ Build context with depth |
| Natural language search | ❌ Exact keywords only | ✅ Semantic search |
| Temporal filtering | ❌ Not supported | ✅ After/before dates |
| Strategic alignment | ✅ Project→Strategy relations | ✅ Search strategy docs |

---

## Graph Memory

### Tools
- `search_nodes(query)` - Find entities by name/type/observation
- `open_nodes([names])` - Get full entity details
- `read_graph()` - Full graph dump
- `create_entities([...])` - Add new entities
- `create_relations([...])` - Add relationships

### Entity Types
- **Personnel**: Gregory Karsten, Sipho Dubazane, Xavier Peterson, etc.
- **Project**: BEV Fire Safety Program, Rock Winder Clutch Repair, etc.
- **Location**: Nchwaning 2, Nchwaning 3, Gloria Mine
- **Strategy**: Safety & Compliance Excellence, Q4 2025 Active Phase
- **Decision**: BEV BaaS Contract Extension, Generator Procurement
- **Business Process**: VFL Program, Monthly Engineering Meeting

### Relation Types
- `reports_to`, `dotted_line_reports_to`, `manages`
- `assigned_to`, `located_at`, `stationed_at`
- `participates_in`, `made_decision`, `impacts`
- `aligns_with`, `owns_strategy`

### Limitations
- No natural language queries (exact names/keywords only)
- No temporal filtering
- Requires exact entity names

---

## Basic Memory

### Tools
- `search_notes(query, project="main")` - Semantic search
- `build_context(uri, depth=2, project="main")` - Deep context retrieval
- `recent_activity(timeframe="1 week", project="main")` - Recent changes
- `read_note(uri, project="main")` - Read specific note
- `write_note(...)` - Create/update note

### Temporal Filtering (varies by tool)
- `search_notes()`: Use `after_date="YYYY-MM-DD"` (NOT `timeframe`)
- `build_context()`: Use `timeframe="7d"` or `"2 weeks"`
- `recent_activity()`: Use `timeframe="1 week"`

### Depth Parameter (build_context only)
- `depth=1`: Direct connections only
- `depth=2`: Friends-of-friends (2 hops)
- `depth=3`: Extended network (use sparingly)

### Ground Truth Documents
- `tasks/master_task_list.md` - All tasks
- `people/*.md` - Personnel details
- `projects/*/` - Project documentation
- `strategy/*.md` - Strategic framework
- `system/*.md` - Policies and skills

---

## Automatic Context Retrieval

Proactively enhance context when these triggers are detected:

### People Triggers
Names like Greg, Sipho, Xavier, Sello → Query both systems for role + projects

### Project Triggers
BEV, fire safety, capital, equipment → Get strategic alignment + status

### Site Triggers
Nchwaning 2, N2, N3, Gloria, S&W → Get site entity + assigned personnel

### Recent Activity Triggers
"What's new", "recent updates", "lately" → `recent_activity()` + strategic context

---

## Strategic Context Integration

### Strategy Documents
- `strategy/CompanyStrategy.md` - 5 strategic pillars
- `strategy/ActivePhase.md` - Q4 2025 priorities with weights
- `strategy/FocusOfWeek.md` - Weekly tactical priorities

### Q4 2025 Priority Weights
| Priority | Weight |
|----------|--------|
| Fire Safety & Risk Mitigation | **2.0x** (CRITICAL) |
| BEV Program Optimization | **1.5x** (HIGH) |
| Compliance & Audit Excellence | **1.5x** (HIGH) |
| Team Capacity Building | **1.2x** (MEDIUM) |
| Capital Planning & Delivery | **1.2x** (MEDIUM) |

### Priority Formula
See `system/policy.md` for full calculation:
```
Final Priority = (Base × Strategy Multiplier) + FocusBoost (capped at 2.5)
```

---

## When NOT to Use Memory

Skip memory queries for:
- Simple file operations (read/write specific files)
- Pure command execution (slash commands)
- General questions unrelated to vault content
- User explicitly says to skip searching

---

## Example Workflows

### Person Context
**Q**: "What should I discuss with Sipho?"
1. Graph: `search_nodes("Sipho Dubazane")` → Role, reporting
2. Basic: `build_context("memory://people/sipho-dubazane", depth=1)` → Projects

### Project Status
**Q**: "How's the BEV project?"
1. Basic: `search_notes("BEV project status")` → Contract, safety
2. Graph: `search_nodes("BEV")` → Entities
3. Graph: Follow `aligns_with` → Strategic weight (2.0x)

### Recent Activity
**Q**: "Any updates from last week?"
1. Basic: `recent_activity(timeframe="1 week")`
2. Graph: `search_nodes("Q4 2025 Active Phase")` → Current focus

---

## Future Phases

- **Phase 2**: Obsidian Watcher Plugin (real-time indexing)
- **Phase 3**: Behavioral Intelligence (reflex cache, pattern learning)
- **Phase 4**: Advanced Strategic Integration (automated priority calculation)
- **Phase 5**: Production Deployment (monitoring, metrics)

See [[README.md]] for complete roadmap.
