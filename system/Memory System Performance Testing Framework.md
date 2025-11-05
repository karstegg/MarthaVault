---
title: Memory System Performance Testing Framework
type: note
permalink: system/memory-system-performance-testing-framework
tags:
- system
- testing
- memory-systems
- performance
- evaluation
---

# Memory System Performance Testing Framework

**Created**: 2025-11-04
**Purpose**: Evaluate dual memory system (Graph + Basic Memory) vs direct vault search
**Status**: Test design phase

---

## Test Categories

### 1. Speed & Performance Tests

#### Test 1.1: Simple Entity Lookup
**Question**: "Who is Sipho Dubazane?"

**Methods to compare**:
- **Graph Memory**: `search_nodes("Sipho Dubazane")` - single API call
- **Basic Memory**: `search_notes("Sipho Dubazane", project="main")` - single API call
- **Direct Search**: `Grep("Sipho Dubazane", output_mode="files_with_matches")` → `Read(people/Dubazane, Sipho.md)`

**Metrics**:
- Time to result
- Number of tool calls required
- Context completeness (role, site, projects, relationships)

---

#### Test 1.2: Relationship Traversal
**Question**: "Who reports to Gregory Karsten?"

**Methods**:
- **Graph Memory**: `search_nodes("Gregory Karsten")` → see relations in single response
- **Basic Memory**: `build_context("memory://people/gregory-karsten", depth=1)` → traverses links
- **Direct Search**: `Grep("reports to.*Gregory", output_mode="content")` → multiple file reads

**Metrics**:
- Number of API calls
- Accuracy of results
- Completeness (did we find all 4 direct reports?)

---

#### Test 1.3: Cross-Domain Query
**Question**: "What BEV tasks are assigned to people at Nchwaning 3?"

**Methods**:
- **Graph Memory**: `search_nodes("Nchwaning 3")` → find people → find tasks via relations
- **Basic Memory**: `search_notes("BEV Nchwaning 3 assigned", project="main")`
- **Direct Search**: Multiple greps across people/, tasks/, projects/BEV/

**Metrics**:
- Total tool calls
- Time to complete answer
- Accuracy (missed tasks or false positives)

---

### 2. Context Quality Tests

#### Test 2.1: Strategic Alignment Discovery
**Question**: "Which tasks align with Fire Safety & Compliance strategy?"

**Expected**: Should find tasks + WHY they're strategic priorities (via Project→Strategy relations)

**Methods**:
- **Graph Memory**: `search_nodes("Safety & Compliance Excellence")` → follow aligns_with relations → tasks
- **Basic Memory**: `search_notes("fire safety compliance strategic priority", project="main")`
- **Direct Search**: Grep for #fire-safety tags → read strategy files → manual correlation

**Quality metrics**:
- Does it show strategic alignment automatically?
- Does it calculate priority multiplier (2.0x for Fire Safety)?
- Is the reasoning transparent?

---

#### Test 2.2: Task Context Web
**Question**: "Give me full context for the 'Renew NCH3 Certiq contract' task"

**Expected**: Task details + assignee (Philip Moller) + site (N3) + project (BEV) + why it matters (blocks S2 optimization)

**Methods**:
- **Graph Memory**: `search_nodes("Certiq")` → single result with all relations embedded
- **Basic Memory**: `build_context("memory://tasks/master-task-list", depth=2)` → traverses links
- **Direct Search**: Read master_task_list.md → grep for Philip Moller → grep for N3 → grep for BEV

**Quality metrics**:
- How many hops to get complete picture?
- Is context automatically assembled or manual?
- Relevance of returned context

---

### 3. Accuracy & Reliability Tests

#### Test 3.1: Temporal Filtering
**Question**: "What tasks were added in the last week?"

**Methods**:
- **Graph Memory**: ❌ No temporal filtering (limitation)
- **Basic Memory**: `recent_activity(timeframe="1 week", project="main")`
- **Direct Search**: `git log --since="1 week ago" -- tasks/` → parse changes

**Metrics**:
- Can the system answer this type of question?
- Accuracy of date filtering
- False positives/negatives

---

#### Test 3.2: Ambiguous Entity Resolution
**Question**: "What tasks does Simon have?"

**Challenge**: "Simon" = "Simon Sease" = "Sello Sease" = "Sello Simon Sease" (all same person)

**Methods**:
- **Graph Memory**: `search_nodes("Simon")` - finds all entity name variants
- **Basic Memory**: `search_notes("Simon assigned task", project="main")` - full-text search
- **Direct Search**: Grep "Simon" - might miss "Sease, Sello" format

**Metrics**:
- Does it find all 11 tasks despite name variations?
- Precision (no false matches on other Simons)

---

#### Test 3.3: Negative Query (Find Gaps)
**Question**: "Which sites have NO critical tasks assigned?"

**Methods**:
- **Graph Memory**: Query all sites → check relations → identify gaps
- **Basic Memory**: Search each site → count tasks → manual comparison
- **Direct Search**: Multiple greps per site → manual aggregation

**Metrics**:
- Can the system identify absences/gaps?
- Requires manual logic or automatic?

---

### 4. Complex Reasoning Tests

#### Test 4.1: Multi-Constraint Search
**Question**: "Critical priority BEV tasks due before November 5 assigned to Epiroc personnel"

**Constraints**: 
- Priority = critical
- Tags include #BEV
- Due date < 2025-11-05
- Assignee works for Epiroc

**Methods**:
- **Graph Memory**: Multiple searches + manual filtering
- **Basic Memory**: `search_notes("critical BEV Epiroc", project="main")` + manual date filter
- **Direct Search**: Grep with regex → multiple file reads → manual filtering

**Metrics**:
- How many manual steps required?
- Accuracy of final result set
- Did we find: DT171 A-frame (due Oct 28) and Certiq renewal (due Nov 1)?

---

#### Test 4.2: Impact Analysis
**Question**: "If Philip Moller goes on leave, what's impacted?"

**Expected**: 
- 5 tasks blocked
- BEV program affected
- S2 optimization blocked (Certiq contract)
- Equipment downtime extended (DT171)

**Methods**:
- **Graph Memory**: `open_nodes(["Philip Moller"])` → see all assigned_to relations → task details
- **Basic Memory**: `search_notes("Philip Moller assigned", project="main")` → parse results
- **Direct Search**: Grep "Philip Moller" → read each file → extract impacts

**Quality metrics**:
- Completeness (found all 5 tasks?)
- Automatic impact inference or manual?
- Shows cascading effects?

---

## Success Criteria

### Speed Metrics
- **Fast**: < 3 tool calls to answer
- **Medium**: 3-7 tool calls
- **Slow**: > 7 tool calls

### Quality Metrics
- **Excellent**: Complete context, relationships visible, strategic alignment shown
- **Good**: Core info present, some relationships, missing strategic context
- **Poor**: Basic facts only, no relationships, no context

### Accuracy Metrics
- **Perfect**: 100% precision, 100% recall
- **Good**: >90% precision, >90% recall
- **Needs improvement**: <90% precision or recall

---

## Testing Protocol

### For Each Test:
1. **Record start time**
2. **Execute using each method** (Graph, Basic, Direct)
3. **Count tool calls**
4. **Record end time**
5. **Evaluate result quality** (completeness, accuracy, relevance)
6. **Document findings** in results table

### Results Template:
```markdown
## Test X.X: [Name]

| Method | Tool Calls | Time (est) | Quality | Accuracy | Notes |
|--------|-----------|------------|---------|----------|-------|
| Graph Memory | X | Xs | Excellent/Good/Poor | X% | ... |
| Basic Memory | X | Xs | Excellent/Good/Poor | X% | ... |
| Direct Search | X | Xs | Excellent/Good/Poor | X% | ... |

**Winner**: [Method]
**Reason**: [Why]
```

---

## Expected Outcomes

### Where Graph Memory Should Win:
- Relationship queries ("who reports to X")
- Entity lookups (fast, single call)
- Strategic alignment discovery
- Impact analysis (traverse relations)

### Where Basic Memory Should Win:
- Temporal queries (recent activity)
- Natural language semantic search
- Full-text content search
- Deep context building (depth parameter)

### Where Direct Search Might Win:
- Regex pattern matching
- File-level operations
- Grep-specific use cases (e.g., "find all files containing...")

### Where Dual System Wins:
- Complex queries requiring BOTH entity relations AND semantic search
- "Which critical BEV tasks assigned to N3 engineers align with Fire Safety strategy?"
  - Graph: Find N3 engineers → their tasks → strategic alignment
  - Basic: Semantic search for BEV + fire safety context
  - Combined: Complete picture with reasoning

---

## Next Steps

1. **Run pilot tests** (Tests 1.1, 1.2, 2.1) to validate framework
2. **Refine metrics** based on pilot results
3. **Execute full test suite** (12 tests)
4. **Analyze results** and create performance report
5. **Identify optimization opportunities** for dual memory system
6. **Document best practices** for when to use which system

---

## Related Documents
- [[system/policy.md]] - Priority calculation formula using strategic alignment
- [[README.md]] - Memory systems architecture (Phase 1 complete)
- [[strategy/ActivePhase.md]] - Strategic priorities with ObjectiveWeight multipliers
