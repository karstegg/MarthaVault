# Breadcrumb Navigation Rules
<!-- How to efficiently traverse the vault for context -->

## Navigation Principles

### 1. Start Narrow, Expand as Needed
```
Query: "HD62 issues"
Level 0: HD62 file only (50 tokens)
Level 1: + Simon Sease + N3 context (200 tokens)  
Level 2: + Related equipment + recent failures (500 tokens)
Level 3: + Historical patterns + solutions (1000 tokens)
```

### 2. Follow Natural Relationships
```
Person → Projects → Tasks → Equipment
Site → Equipment → Issues → Assigned Person
Project → Dependencies → Blockers → Critical Path
```

### 3. Time-Based Filtering
- Hot: Last 7 days - Load immediately
- Warm: Last 30 days - Load if relevant
- Cold: > 30 days - Load only if explicitly needed

## Smart Context Loading Examples

### Query: "What should Greg focus on today?"
```breadcrumb
1. context_map.md → Hot Zones section
2. master_task_list.md → Critical priority only
3. Schedule/ → Today's date file
4. people/Gregory Karsten.md → Active assignments
STOP - Sufficient context (usually < 500 tokens)
```

### Query: "Fire safety status"
```breadcrumb
1. Search: #fire-safety #MSTA
2. Load: Active fire safety tasks
3. Expand: BEV project (has fire safety deps)
4. Check: Recent audit findings
5. IF compliance question → Load DMR docs
```

### Query: "Why is HD62 failing?"
```breadcrumb
1. equipment_graph.md → HD62 node
2. Search: "HD62" in last 30 days
3. Load: Simon Sease recent reports
4. Pattern check: Other hydraulic failures
5. IF pattern found → Load historical solutions
```

## Efficiency Rules

### Always Skip
- Completed tasks (unless analyzing history)
- Archive folder (unless explicitly requested)
- Personal folder (unless Greg asks)
- Media files (load descriptions only)

### Always Include
- Current assignee for any equipment/task
- Critical priority items in domain
- Today/tomorrow calendar items
- Active project status

### Load on Demand
- Historical patterns (if troubleshooting)
- Compliance docs (if regulatory question)
- Meeting notes (if decision history needed)
- Org structure (if delegation question)

## Token Budget Guide
- Quick answer: 200-500 tokens
- Detailed analysis: 1000-2000 tokens  
- Comprehensive report: 3000-5000 tokens
- Full investigation: 5000+ tokens

Remember: **Better to be precise than complete**
