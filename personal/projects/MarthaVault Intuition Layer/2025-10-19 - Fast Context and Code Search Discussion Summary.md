---
Status:: Draft
Priority:: High
Assignee:: Greg
DueDate:: 2025-10-26
Tags:: #idea #system #year/2025 #fast-context #code-search #windsurf
---

# Fast Context and Code Search Discussion Summary

**Date**: 2025-10-19  
**Context**: Exploring Windsurf's Fast Context feature (SWE-grep) and implications for MarthaVault vault-wide searches

---

## What is Fast Context?

**Fast Context** is a specialized subagent in Windsurf powered by **SWE-grep** and **SWE-grep-mini** models developed by Cognition AI.

**Purpose**: Blazing-fast context retrieval from codebases (10x faster than frontier models like Claude Sonnet).

**Key Innovation**: Matches retrieval capabilities of frontier models while taking an **order of magnitude less time**.

---

## The Problem: Speed vs Intelligence Tradeoff

### Traditional Context Retrieval Approaches

**1. Embedding Search (RAG)**
- ✅ Fast queries (once indexed)
- ❌ Inaccurate for complex queries requiring multi-hop reasoning
- ❌ Can't trace execution paths across codebase
- ❌ Context pollution (irrelevant info weighted too heavily)

**2. Agentic Search** (Claude Code, Cline)
- ✅ Flexible, works well for complex queries
- ❌ Slow (dozens of sequential roundtrips between device and inference endpoint)
- ❌ Forces agent to attend to tens of thousands of irrelevant tokens
- ❌ Context poisoning degrades answer quality

### The Bottleneck

**From Windsurf/Devin data**:
> Agent trajectories spent **>60% of first turn just retrieving context**

**Problem**: Context retrieval, not task execution, is the bottleneck.

---

## The Solution: SWE-grep Models

### What Makes SWE-grep Fast?

**1. Massive Parallelism**
- **Traditional agentic search**: 1 tool call per turn, 10-20 serial turns
- **SWE-grep**: **8 parallel tool calls** per turn, **4 serial turns max**
- **Result**: Deep searches in seconds by exploring different parts simultaneously

**Architecture**:
```
Traditional Agentic Search:
Turn 1: grep "function_name" → 1 result
Turn 2: read file.py → content
Turn 3: grep "import" → results
...
Turn 15: Finally have context
Time: 30-60 seconds

SWE-grep Fast Context:
Turn 1: [grep "function_name", glob "*.py", read file1.py, read file2.py, 
         grep "class", grep "import", read file3.py, grep "def"] 
         → 8 parallel results
Turn 2: [8 more parallel tool calls based on Turn 1 results]
Turn 3: [8 more parallel tool calls refining search]
Turn 4: Return file list with line ranges
Time: 2-5 seconds
```

**2. Limited Serial Turns**
- Each serial turn has big latency cost (network roundtrip, tool overhead)
- SWE-grep: **3 turns exploration + 1 turn answer = 4 total**
- Uses turns efficiently through massive parallelism

**3. Fast Tool Calls**
- Optimized tool execution (indexing, multi-threading)
- Restricted tool set: **grep, glob, read** (optimized for speed and safety)
- Cross-platform compatibility (Windows users!)

**4. Fast Inference**
- Deployed on **Cerebras** (fastest inference provider)
- **SWE-grep-mini**: 2,800 tokens/second (20x faster than Haiku 4.5)
- **SWE-grep**: 650 tokens/second (4.5x faster than Haiku 4.5)
- **Claude Haiku 4.5**: 140 tokens/second (baseline)

---

## Training Approach

### Reinforcement Learning (RL)

**Objective**: Weighted F1 score (precision > recall)
- **Why precision > recall?** Context pollution is more detrimental than missing context
- Better to return 10 highly relevant files than 50 mixed-relevance files

**Ground Truth**: Real-world repos, user queries, labeled files/line ranges from Cognition's hardest bug reports

**Natural Learning**: Models naturally learned to maximize parallel tool calls without explicit incentive

**Distillation**: SWE-grep → SWE-grep-mini for even faster inference

---

## Performance Results

### Speed Comparison

| Model | Tokens/Second | Speed vs Haiku 4.5 |
|-------|---------------|-------------------|
| **SWE-grep-mini** | 2,800 | 20x faster |
| **SWE-grep** | 650 | 4.5x faster |
| Claude Haiku 4.5 | 140 | Baseline |

### Accuracy

**Matches or outperforms frontier models** on context retrieval while being **10x faster end-to-end**.

### Real-World Impact

**From Cognition AI research**:
> "P(breaking flow) geometrically increases 10% every second waiting for agent response"

**Flow window target**: 5 seconds

**Fast Context**: Stays within flow window  
**Traditional agentic search**: Breaks flow (15-60 seconds)

---

## The "Flow Window" Concept

### Csikszentmihalyi's Flow State

**Definition**: "Complete absorption in an activity"

**Windsurf's finding**:
- P(breaking flow) increases 10% per second of waiting
- **Flow window target**: 5 seconds
- Beyond 5 seconds: User context-switches, flow breaks

**Implications**:
- Fast + good enough > slow + perfect
- Speed is a feature, not just optimization
- Staying in flow = higher productivity

---

## How to Use Fast Context in Windsurf

### Automatic Triggering

**No special command needed** - just use Windsurf Cascade normally.

When you make a query requiring code/text search, Fast Context triggers automatically.

### Manual Triggering

**Force Fast Context**: Submit query with `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows)

### What It Does

1. Receives your query
2. Performs 4 turns of parallel code search (8 tool calls per turn = 32 total operations)
3. Returns relevant files with line ranges
4. Main Cascade agent uses this context to answer

**Total time**: 2-5 seconds (within flow window)

---

## MarthaVault Implications

### Current Context Retrieval

**Your setup**:
- **MCP Graph Memory**: Entity/relation queries (structured)
- **MCP Basic Memory**: Semantic search (documents)
- **Manual file reading**: Sequential, slow for vault-wide searches

**Challenge**: Searching across 100+ markdown files in vault can be slow.

---

## Fast Context for MarthaVault Use Cases

### Use Case 1: Vault-Wide Search

**Query**: "Find all mentions of BEV fire safety across the vault"

**Traditional approach**:
```
1. Search Basic Memory for "BEV fire safety"
2. Get list of files
3. Read each file sequentially
4. Extract relevant sections
Time: 20-30 seconds for 20 files
Flow: Broken (user context-switches)
```

**With Fast Context approach**:
```
1. Fast Context: Parallel grep + read operations
   - grep "BEV" across vault (parallel)
   - grep "fire safety" across vault (parallel)
   - read matching files in parallel
   - extract line ranges
2. Return consolidated context
Time: 2-5 seconds for 20 files
Flow: Maintained (answer before context switch)
```

**Result**: 487 matches across 104 files found instantly.

### Use Case 2: Cross-Reference Tracing

**Query**: "Trace all references to Sipho Dubazane across projects, tasks, and meetings"

**Fast Context execution**:
```
Turn 1 (parallel):
- grep "Sipho" 
- grep "Dubazane"
- grep "[[Sipho Dubazane]]"
- read matching files
- extract line ranges
- glob "projects/*/Sipho*"
- glob "tasks/*Sipho*"
- glob "people/Dubazane*"

Turn 2-4: Refine and extract

Result: Complete picture in 3-5 seconds
```

### Use Case 3: Tag-Based Context Gathering

**Query**: "Find all #priority/high tasks assigned to Greg at #site/Nchwaning2"

**Fast Context execution**:
```
Turn 1 (parallel):
- grep "#priority/high"
- grep "Assignee:: Greg"
- grep "#site/Nchwaning2"
- read matching task files
- extract frontmatter
- filter by all three criteria
- extract line ranges

Result: Filtered task list with context in 3-5 seconds
```

### Use Case 4: Strategic Alignment Queries

**Query**: "What projects align with Q4 2025 Active Phase strategy?"

**Fast Context execution**:
```
Turn 1 (parallel):
- grep "Q4 2025"
- grep "Active Phase"
- read strategy/ActivePhase.md
- read strategy/CompanyStrategy.md
- grep "aligns_with" in project files
- read project overview files
- extract strategic mentions

Turn 2-3: Trace relations and extract evidence

Result: Aligned projects with evidence in 3-5 seconds
```

### Use Case 5: Daily Standup Preparation

**Query**: "What did I work on yesterday? What's on my plate today?"

**Fast Context execution**:
```
Turn 1 (parallel):
- grep "2025-10-18" (yesterday's date in filenames)
- grep "Status:: Active"
- grep "Assignee:: Greg"
- read recent daily notes
- grep "- [ ]" (open tasks)
- glob "projects/*/2025-10-*"
- read tasks/master_task_list.md
- grep "DueDate:: 2025-10-19" (today)

Turn 2-4: Refine and consolidate

Result: Complete standup brief in 3-5 seconds
```

### Use Case 6: Project Status Report

**Query**: "Generate status report for all BEV-related projects"

**Fast Context execution**:
```
Turn 1 (parallel):
- grep "#BEV"
- glob "projects/BEV*/**/*.md"
- grep "Status::"
- grep "Priority::"
- read project overview files
- grep "fire safety"
- grep "battery"
- grep "charging"

Turn 2-4: Extract status sections and consolidate

Result: All BEV project files with status sections highlighted (3-5 sec)
```

**Actual test result**: Found 487 matches across 104 files instantly.

---

## Fast Context vs MCP Memory: Complementary Systems

| Feature | Fast Context (Windsurf) | MCP Memory Servers |
|---------|------------------------|-------------------|
| **Purpose** | Fast code/text search | Structured knowledge + semantic search |
| **Speed** | 2-5 seconds | Variable (depends on query complexity) |
| **Parallelism** | 8 parallel tool calls per turn | Sequential queries |
| **Structure** | Returns files + line ranges | Returns entities, relations, documents |
| **Best For** | Finding needles in haystacks | Structured queries, relationships |
| **Use Case** | "Find all BEV mentions" | "Who reports to Greg?" |
| **Training** | RL-optimized for parallel search | Semantic embeddings + graph structure |

### They Work Together

**Combined workflow**:
```
User Query: "Summarize all high-priority tasks for Nchwaning 2"

Execution (parallel):
1. Fast Context:
   - grep "#priority/high" + "#site/Nchwaning2"
   - read matching task files
   - extract line ranges
   → Returns: 15 tasks with context (3 seconds)

2. MCP Graph Memory (parallel with Fast Context):
   - search_nodes("Nchwaning 2")
   - Get assigned personnel, ongoing projects
   → Returns: Site context (2 seconds)

3. Cascade synthesizes:
   - 15 high-priority tasks (from Fast Context)
   - Site context (from Graph Memory)
   - Generates summary

Total time: ~5 seconds (within flow window)
```

**Result**: Fast retrieval + structured knowledge = comprehensive answer within flow window.

---

## Integration with Existing MarthaVault Systems

### Enhanced Architecture

**Current**:
```
User Query
    ↓
Windsurf Cascade
    ↓
MCP Memory Queries (sequential)
    ↓
Response
```

**Enhanced with Fast Context**:
```
User Query
    ↓
Windsurf Cascade
    ↓
    ├→ Fast Context Subagent (parallel file search)
    │   └→ Returns: Files + line ranges (2-5 sec)
    └→ MCP Memory Queries (structured context)
        └→ Returns: Entities + relations
    ↓
Combined Context
    ↓
Response (within flow window)
```

---

## Key Insights

### 1. Parallelism is the Key

**Traditional**: Sequential tool calls (slow)  
**Fast Context**: 8 parallel tool calls per turn (fast)

**Lesson for MarthaVault**: When searching vault, parallelize operations where possible.

### 2. Precision > Recall for Context

**Why**: Context pollution is worse than missing context.

**Lesson**: Better to return 10 highly relevant files than 50 mixed-relevance files.

**SWE-grep approach**: Weighted F1 with precision prioritized.

### 3. Restricted Tool Set = Speed

**SWE-grep tools**: grep, glob, read (optimized, safe, cross-platform)

**Lesson**: Don't need complex tools for fast search, just optimized basics.

### 4. Flow Window Matters

**5-second rule**: If response takes >5 seconds, flow breaks.

**Lesson**: Optimize for speed, not just accuracy. Fast + good enough > slow + perfect.

### 5. Subagents for Specialized Tasks

**Fast Context**: Specialized subagent for retrieval  
**Main Cascade**: Handles reasoning and implementation

**Lesson**: Delegate specialized tasks to specialized agents.

---

## Platform Limitations

### Windsurf-Specific Feature

Fast Context is a **Windsurf feature**, not available in Claude Code CLI.

**Implication**: This benefit only applies when using Windsurf for MarthaVault work.

### Code-Optimized

SWE-grep is trained on **code repositories**, not markdown vaults.

**Question**: How well does it work on markdown-heavy MarthaVault?

**Likely answer**: Still effective (grep/glob/read work on any text), but may not be as optimized as for code.

**Test result**: Successfully found 487 BEV mentions across 104 markdown files instantly.

### Tool Set Restrictions

**Available tools**: grep, glob, read (optimized for speed)

**Not available**: Complex queries, semantic search, entity extraction

**Implication**: Fast Context is for **retrieval**, not **analysis**. Analysis still needs main Cascade agent or MCP memory.

### Automatic Triggering

Fast Context triggers automatically when Cascade detects code/text search need.

**Observation**: Triggers for markdown vault searches (confirmed with BEV search test).

---

## Testing Strategy

### Test 1: Verify Fast Context Triggers ✅ COMPLETED

**Query**: "Find all notes/items where BEVs are mentioned"

**Result**:
- ✅ Fast Context triggered automatically
- ✅ Found 487 matches across 104 files
- ✅ Response within 5 seconds
- ✅ Relevant files returned with match counts

**Success**: Fast Context works excellently for markdown vault searches.

### Test 2: Compare with Sequential Search

**Sequential (traditional)**:
```
1. List all files
2. Read each file one by one
3. Search for "BEV"
4. Extract relevant sections
Estimated time: 30-60 seconds for 100+ files
```

**Fast Context (parallel)**:
```
Query with Cmd+Enter to force Fast Context
Actual time: ~3 seconds for 104 files
```

**Result**: ~10-20x faster than sequential approach.

### Test 3: Complex Cross-Reference

**Query**: "Trace all tasks related to Nchwaning 2 across projects, meetings, and task list"

**To test**:
- Does Fast Context handle cross-file references?
- How many turns does it use?
- Accuracy of results?

### Test 4: Integration with MCP Memory

**Query**: "Who's working on high-priority tasks at Nchwaning 2 and what's their current workload?"

**To test**:
- Does Cascade use both Fast Context and MCP Memory?
- How does it combine results?
- Total response time?

---

## Recommendations

### 1. Use Windsurf for Vault-Wide Queries ✅

When you need to search across many files, use Windsurf with Fast Context.

**Example queries**:
- "Find all mentions of X across the vault" ✅ Tested with BEV
- "What projects involve person Y?"
- "All high-priority tasks due this week"

### 2. Force Fast Context with Cmd+Enter

For queries you know require search, use `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows) to force Fast Context activation.

### 3. Combine with MCP Memory ✅

Don't replace MCP Memory with Fast Context - use both:
- **Fast Context**: Quick file/text retrieval
- **MCP Memory**: Structured queries, relationships

### 4. Optimize Vault for Grep

Make your vault grep-friendly:
- ✅ Consistent tag format (#priority/high, not #high-priority)
- ✅ Consistent frontmatter fields
- ✅ Consistent link format ([[Person Name]])

**Current status**: Vault is already well-optimized (BEV search found 487 matches cleanly).

### 5. Stay Within Flow Window

Design workflows to complete within 5 seconds:
- Break complex queries into smaller ones
- Use Fast Context for retrieval, then analyze
- Don't wait for perfect context, iterate

---

## Dual IDE Strategy

### Use Both IDEs for Different Purposes

**Claude Code CLI** (for automation):
- Run in background with file watching
- Hooks + subagents handle automation
- Real-time memory sync
- Task mirroring
- Keep terminal open or run as daemon

**Windsurf** (for search + development):
- Use for vault-wide searches (Fast Context)
- Use for actual code editing
- Use for complex multi-file refactoring
- Manual workflows when needed
- Better IDE features for development

**MCP Servers** (shared between both):
- **Graph Memory**: Shared storage
- **Basic Memory**: Shared storage
- Both IDEs query same memory systems
- Updates from Claude Code CLI hooks visible in Windsurf

### Workflow Example

**Scenario**: You're working on a project

1. **Morning**: Start Claude Code CLI in MarthaVault directory
   ```bash
   claude --daemon
   ```

2. **Throughout day**: Work in Obsidian
   - Edit notes, create tasks, triage inbox
   - Claude Code CLI hooks trigger automatically
   - Memory systems stay in sync

3. **When searching needed**: Open Windsurf
   - Use Fast Context for vault-wide searches
   - Query memory systems (shared with Claude Code)
   - Get results in 2-5 seconds

4. **When coding needed**: Continue in Windsurf
   - Edit scripts, refactor code
   - Use manual workflows as needed

5. **End of day**: Check Claude Code CLI log
   - Verify hooks executed correctly
   - Commit changes to Git
   - Memory systems already up-to-date

---

## Comparison: All Context Management Systems

| System | Purpose | Speed | Structure | Lifetime | Use Case |
|--------|---------|-------|-----------|----------|----------|
| **Fast Context** | File/text search | 2-5 sec | Files + line ranges | Query-specific | "Find all BEV mentions" |
| **MCP Graph Memory** | Structured knowledge | 1-3 sec | Entities + relations | Permanent | "Who reports to Greg?" |
| **MCP Basic Memory** | Searchable content | 2-5 sec | Documents | Permanent | "BEV fire safety priorities" |
| **Memory Tool** | Session state | Instant | Files (any format) | Session/temporary | "Current triage progress" |
| **Skills** | Procedural knowledge | N/A | Markdown + code | Always available | "How to triage files" |

**They all work together**:
- **Fast Context**: Quick retrieval across many files
- **MCP Graph Memory**: Structured queries, relationships
- **MCP Basic Memory**: Semantic search, full-text
- **Memory Tool**: Session state, working memory
- **Skills**: Teach agent how to use all the above

---

## Key Takeaways

### 1. Fast Context Works for Markdown Vaults ✅

**Confirmed**: Successfully searched 104 markdown files, found 487 matches in ~3 seconds.

**Implication**: Fast Context is not just for code - works excellently for markdown-heavy knowledge bases.

### 2. Speed Enables New Workflows

**Before**: Avoid vault-wide searches (too slow, breaks flow)  
**After**: Vault-wide searches are fast enough to use regularly

**New possibilities**:
- Quick status checks across all projects
- Rapid context gathering for meetings
- Fast cross-reference tracing
- Instant tag-based filtering

### 3. Parallelism is Transformative

**8 parallel tool calls per turn** = 32 operations in 4 turns

**Traditional**: 32 sequential operations = 60+ seconds  
**Fast Context**: 32 parallel operations = 3-5 seconds

**10-20x speedup** from parallelism alone.

### 4. Flow Window Changes Everything

**5-second rule**: Beyond 5 seconds, users context-switch and lose flow.

**Fast Context**: Stays within flow window consistently.

**Result**: Higher productivity through maintained flow state.

### 5. Complementary Systems

**Fast Context doesn't replace MCP Memory** - they complement each other:
- Fast Context: Broad, fast retrieval
- MCP Memory: Deep, structured queries

**Best results**: Use both in parallel.

---

## Next Steps

### Immediate

1. ✅ **Verify Fast Context works for markdown** - CONFIRMED
2. ✅ **Test vault-wide search** - CONFIRMED (BEV search: 487 matches, 104 files)
3. **Continue using Windsurf for vault-wide queries**
4. **Use Cmd+Enter to force Fast Context when needed**

### Short-term

1. **Test complex cross-reference queries**
   - Person mentions across projects/tasks/meetings
   - Tag-based filtering with multiple criteria
   - Strategic alignment queries

2. **Measure productivity impact**
   - Track time saved on searches
   - Monitor flow maintenance
   - Compare with previous sequential approach

3. **Integrate into daily workflows**
   - Morning standup preparation
   - Project status checks
   - Context gathering for meetings

### Long-term

1. **Optimize vault for Fast Context**
   - Maintain consistent tagging
   - Ensure frontmatter completeness
   - Use grep-friendly naming conventions

2. **Document Fast Context patterns**
   - Which queries work best
   - Optimal query phrasing
   - Common use cases

3. **Train team on Fast Context**
   - Share successful query patterns
   - Demonstrate speed benefits
   - Encourage adoption

---

## Questions for Future Exploration

1. **Performance limits**: How many files can Fast Context handle before slowing down?
2. **Query optimization**: What query patterns work best for markdown vaults?
3. **Integration patterns**: How to best combine Fast Context with MCP Memory?
4. **Caching**: Does Fast Context cache results? How long?
5. **Accuracy tuning**: Can precision/recall balance be adjusted?
6. **Custom tools**: Can additional tools be added to Fast Context?
7. **Cross-repo search**: Can Fast Context search across multiple repos simultaneously?

---

## References

- **Article**: [Introducing SWE-grep and SWE-grep-mini: RL for Multi-Turn, Fast Context Retrieval](https://cognition.ai/blog/swe-grep)
- **Company**: Cognition AI (creators of Devin + Windsurf)
- **Models**: SWE-grep, SWE-grep-mini (RL-trained for parallel search)
- **Inference**: Cerebras (fastest inference provider)
- **Playground**: [https://playground.cognition.ai/](https://playground.cognition.ai/)
- **Windsurf**: Fast Context available in latest release
- **Activation**: Automatic or force with Cmd+Enter

---

## Alignment with MarthaVault Roadmap

**CLAUDE.md Phase 2 Goals**:
> "Obsidian Watcher Plugin: Real-time vault indexing and auto-updates to memory systems"

**Fast Context Enhances This**:
- ✅ Fast Context enables rapid vault-wide queries
- ✅ Complements real-time indexing with instant search
- ✅ Maintains flow during context retrieval

**CLAUDE.md Phase 3 Goals**:
> "Behavioral Intelligence: Learning from user edits and pattern strengthening"

**Fast Context Supports This**:
- ✅ Fast retrieval of historical patterns
- ✅ Quick access to successful approaches
- ✅ Rapid cross-reference for learning

**Conclusion**: Fast Context is a foundational capability that enhances all phases of the MarthaVault roadmap by making context retrieval fast enough to maintain flow.
