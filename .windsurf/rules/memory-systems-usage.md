# Rule: Memory Systems Usage

## Dual Memory System Architecture

MarthaVault uses **two complementary memory systems** for intelligent context retrieval:

1. **Graph Memory** (`mcp3_*`) - Entity-relationship knowledge graph
2. **Basic Memory** (`mcp__basic-memory__*`) - Semantic document search

**Current Indexed Content**:
- **Graph Memory**: 348 entities including Personnel, Projects, Locations, Tasks, Ideas, Business Processes, Decisions, Strategy
- **Basic Memory**: Documents in "main" project (people/, projects/, tasks/, strategy/, system/)

## Memory System Decision Matrix

Use the right memory system for the task:

| Use Case | Graph Memory | Basic Memory |
|----------|--------------|--------------|
| **Quick lookups** | ✅ Entity name/type queries | ❌ Slower for simple lookups |
| **Relationships** | ✅ Traverse relations (depth) | ✅ Build context with depth parameter |
| **Natural language search** | ❌ No NL queries, exact keywords only | ✅ Semantic search |
| **Temporal filtering** | ❌ Not supported | ✅ After/before dates |
| **Strategic alignment** | ✅ Project→Strategy relations | ✅ Search strategy documents |
| **Task context** | ✅ Task links to Project/Person/Site | ✅ Task details in master_task_list.md |

**Best Practice**: Use **BOTH** systems in parallel for comprehensive context.

## Graph Memory Tools & Usage

**Tools**: `mcp3_search_nodes()`, `mcp3_open_nodes()`, `mcp3_read_graph()`, `mcp3_create_entities()`, `mcp3_create_relations()`

**When to Use**:
- "Who reports to Gregory?" → `mcp3_search_nodes("Gregory Karsten")`
- "Which projects at Nchwaning 3?" → `mcp3_search_nodes("Nchwaning 3")`
- "What's Sipho's role?" → `mcp3_open_nodes(["Sipho Dubazane"])`

**Entity Types**:
- **Personnel**: Gregory Karsten, Sipho Dubazane, Sikelela Nzuza, Xavier Peterson, etc.
- **Project**: BEV Fire Safety Program, Rock Winder Clutch Repair, Drill Rig Capital Application, etc.
- **Location**: Nchwaning 2, Nchwaning 3, Gloria Mine
- **Strategy**: Safety & Compliance Excellence, Q4 2025 Active Phase, etc.
- **Decision**: BEV BaaS Contract Extension Decision, Generator Procurement Decision, etc.
- **Business Process**: VFL Program, Monthly Engineering Meeting, Standards Meeting, etc.
- **Task**: High-level task entities (master_task_list.md is in Basic Memory)
- **Idea**: Martha AI Concept, Intuition Layer Development, etc.

**Relation Types**:
- `reports_to`, `dotted_line_reports_to`, `manages`
- `assigned_to`, `located_at`, `stationed_at`
- `participates_in`, `made_decision`, `impacts`
- `aligns_with`, `owns_strategy`

**Limitations**:
- No natural language queries (use exact names/types/keywords)
- No temporal filtering
- Requires exact entity names

## Basic Memory Tools & Usage

**Tools**: `mcp__basic-memory__search_notes()`, `mcp__basic-memory__build_context()`, `mcp__basic-memory__read_note()`, `mcp__basic-memory__write_note()`

**When to Use**:
- "What are the BEV fire safety priorities?" → `search_notes("BEV fire safety priorities", project="main")`
- "Recent decisions about capital?" → `search_notes("capital decision", project="main")`
- "Context for BEV project?" → `build_context("memory://projects/bev", depth=2, project="main")`

**Key Features**:
- Semantic search with relevance scoring
- Relationship traversal with `depth` parameter (1-3 hops)
- Temporal filtering (varies by tool)
- Document types: notes, relations, entities

**Temporal Filtering by Tool**:
- `search_notes()`: Use `after_date="YYYY-MM-DD"` (NOT `timeframe`)
- `build_context()`: Use `timeframe="7d"` or natural language like `"2 weeks"`

**Depth Parameter** (for `build_context()` only):
- `depth=1`: Direct connections only
- `depth=2`: Friends-of-friends (2 hops)
- `depth=3`: Extended network (use sparingly)

**Ground Truth Documents**:
- `tasks/master_task_list.md` - All tasks (searchable, not all in Graph)
- `people/*.md` - Personnel details
- `projects/*/` - Project documentation
- `reference/` - Standards, equipment, terminology
- `strategy/` - Strategic planning documents

## When to Update Memory Systems

**Graph Memory**: Update when:
- New personnel join or roles change
- New projects are initiated
- Important decisions are made
- Strategic direction changes
- New relationships form between entities

**Basic Memory**: Updates automatically via file sync
- Monitors markdown files in configured directories
- Syncs changes in real-time
- No manual intervention needed
