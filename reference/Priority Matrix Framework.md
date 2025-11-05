---
Status: Active
Priority: High
Tags: null
LastUpdated: 2025-11-05
permalink: reference/priority-matrix-framework
---

# Priority Matrix Framework (Urgency × Importance)

**Author**: MarthaVault System  
**Model**: Eisenhower Matrix / 2D Priority Model  
**Application**: MarthaVault task prioritization  
**Created**: 2025-11-05

---

## Problem This Solves

Traditional single-axis priority (Critical → High → Medium → Low) conflates two different dimensions:

- **Urgency**: Time-sensitive (deadline near?)
- **Importance**: Strategic value (does it matter to goals?)

**Result**: Important-but-not-urgent tasks get neglected. WTW audit (March 2026) shouldn't clutter "Do Now" board, but it shouldn't be ignored either.

**Solution**: Two-dimensional matrix that separates these concerns.

---

## The Four Quadrants

### 🔴 QUADRANT 1: Do Now (High Urgency + High Importance)

**Characteristics**:
- Deadline is imminent (< 2 weeks)
- Strategic or critical impact
- Often crisis management
- Cannot be delegated

**Examples in MarthaVault**:
- DMR Brake Test Compliance (due Nov 5)
- Fire Suppression Pre-Start Checks (due Nov 7)
- HD0054 Fire Investigation (due Nov 6)
- Critical safety incidents

**Management**:
- Execute immediately
- Drop lower-priority work
- Escalate if blocked
- Daily review

**Tag**: `#urgent #important`

---

### 🟡 QUADRANT 2: Schedule & Plan (Low Urgency + High Importance)

**Characteristics**:
- Deadline is distant (> 2 weeks away)
- Strategic or high-value work
- Requires planning and resources
- Should be scheduled proactively

**Examples in MarthaVault**:
- WTW Audit (March 2026, but prep starts now)
- Capital TMM planning (December delivery, plan Nov-Dec)
- BEV program (Q4/Q1 rollout, plan Sep-Oct)
- Team recruitment (future hire, recruit now)
- Long-term compliance projects

**Management**:
- Add to strategic roadmap
- Schedule specific work phases
- Allocate resources now
- Weekly/monthly review

**Tag**: `#important #lowurgency`

**Why WTW fits here**:
- Audit not until March 2026 (4+ months)
- But high importance for compliance
- Should start prep work now
- Prevents last-minute crisis

---

### 🟢 QUADRANT 3: Delegate (High Urgency + Low Importance)

**Characteristics**:
- Deadline is soon (< 2 weeks)
- Low strategic value
- Operational/tactical
- Can be delegated or automated

**Examples in MarthaVault**:
- Routine inspections (due Nov 12)
- Meeting preparation (due Nov 19)
- Recurring reports
- Status updates
- Scheduling

**Management**:
- Assign to appropriate person
- Automate if possible
- Quick turnaround (48 hours)
- Weekly review

**Tag**: `#urgent #lowimportance`

---

### ⚪ QUADRANT 4: Backlog/Eliminate (Low Urgency + Low Importance)

**Characteristics**:
- Deadline is far (> 2 weeks away)
- Low strategic value
- Optional or nice-to-have
- Often can be eliminated

**Examples in MarthaVault**:
- Optional training (December)
- Nice-to-have improvements
- Low-priority meetings
- Non-critical documentation

**Management**:
- Do only if time permits
- Consider eliminating
- Review quarterly
- Keep out of main workflow

**Tag**: `#lowurgency #lowimportance`

---

## Assessing Urgency

### High Urgency Indicators

✅ **Regulatory deadline approaching**
- Due date < 2 weeks
- Legal/compliance requirement
- External stakeholder waiting

✅ **Safety/critical issue**
- Fire, safety, or security concern
- Equipment failure affecting operations
- Risk of injury or loss

✅ **Blocker for other work**
- Multiple people waiting on this
- Blocks downstream tasks
- Critical path dependency

✅ **Immediate customer need**
- Client/stakeholder request
- Service interruption
- SLA/contractual deadline

### Low Urgency Indicators

❌ **Deadline is distant**
- Due date > 2 weeks away
- Multi-month planning horizon
- No immediate time pressure

❌ **Flexible deadline**
- Can be moved if needed
- Soft deadline vs. hard deadline
- Opportunity-driven vs. mandate

❌ **Sequential task**
- Depends on other work first
- Planning phase (not execution)
- Future-oriented

---

## Assessing Importance

### High Importance Indicators

✅ **Strategic alignment**
- Supports Q4 2025 objectives
- Links to company goals
- Strategic weight 1.5x or higher

✅ **Business impact**
- Financial consequence
- Customer retention
- Competitive advantage
- Risk mitigation

✅ **Core responsibility**
- Core to your role
- Central to team mission
- Directly impacts KPIs

✅ **Cascading effects**
- Affects multiple teams
- Shapes future work
- Sets precedent

### Low Importance Indicators

❌ **Operational only**
- Keeps things running but doesn't improve
- Routine maintenance
- Status quo work

❌ **Local/isolated**
- Affects only one task
- Doesn't cascade
- Doesn't shape strategy

❌ **Nice-to-have**
- Improvement, not necessity
- Enhancement, not fix
- Can be deferred indefinitely

---

## MarthaVault Implementation

### Tagging System

Add these tags to `master_task_list.md`:

```markdown
- [ ] Task name #priority/high #urgent #important 📅 2025-11-05
```

**Components**:
- `#priority/X` - Single-axis (for compatibility)
- `#urgent` or `#lowurgency` - Urgency dimension
- `#important` or `#lowimportance` - Importance dimension

### Board Views

| Board | Best For |
|-------|----------|
| [[Tasks Kanban Board]] | Overall workflow |
| [[Priority Matrix Board]] | Strategic prioritization |
| [[Tasks by Person]] | Delegation |
| [[Tasks by Theme]] | Strategic alignment |
| [[Tasks by Site]] | Operational execution |

### Workflow

1. **New task arrives**
2. **Quick assessment**: Urgency + Importance
3. **Place in matrix**: Do Now → Schedule → Delegate → Backlog
4. **Add tags**: `#urgent #important` etc.
5. **Set due date**: Use strategic deadline (not just hard deadline)
6. **Assign**: To person or roadmap
7. **Review**: Daily (Do Now), Weekly (Schedule), Monthly (Backlog)

---

## Decision Rules

### When in doubt, ask:

**Is it urgent?** (< 2 weeks)
→ Yes: Red or Green quadrant
→ No: Yellow or Gray quadrant

**Is it important?** (Strategic weight)
→ Yes: Red or Yellow quadrant
→ No: Green or Gray quadrant

### Conflict Resolution

**Q: What if something is urgent but not important?**
A: Quadrant 3 (Green) - Delegate or automate it

**Q: What if something is important but I keep delaying it?**
A: Quadrant 2 (Yellow) - It's not getting done because it's not urgent. Schedule it with hard dates.

**Q: What if I'm not sure if something is important?**
A: Consult strategy/ActivePhase.md or escalate to manager

---

## Real World Examples

### Example 1: WTW Audit

```
Task: WTW Audit Outstanding Actions
Due: 2026-03-15 (audit date)
Urgency: LOW (4+ months away)
Importance: HIGH (compliance 1.5x weight)

Quadrant: 🟡 SCHEDULE & PLAN

Action: 
- Schedule Q1 2026 prep work
- Plan resources now (Nov 2025)
- Don't clutter Do Now board
- Add to roadmap with phases
- Review monthly

Tags: #important #lowurgency #compliance
```

### Example 2: DMR Brake Test

```
Task: DMR Brake Test Compliance Response
Due: 2025-11-05 (today!)
Urgency: HIGH (< 2 weeks)
Importance: HIGH (compliance 1.5x weight)

Quadrant: 🔴 DO NOW

Action:
- Execute immediately
- Clear calendar if needed
- Daily check-in
- Escalate if blocked
- Complete this week

Tags: #urgent #important #critical
```

### Example 3: Monthly Engineering Meeting

```
Task: Monthly Engineering Meeting Prep
Due: 2025-11-19 (< 2 weeks)
Urgency: HIGH (deadline soon)
Importance: LOW (operational only)

Quadrant: 🟢 DELEGATE

Action:
- Assign to junior engineer
- Provide template/requirements
- Quick turnaround (48 hours)
- Doesn't need VP attention

Tags: #urgent #lowimportance
```

### Example 4: Optional Training

```
Task: Claude Code Advanced Training
Due: 2025-12-15 (> 2 weeks)
Urgency: LOW (distant)
Importance: LOW (optional)

Quadrant: ⚪ BACKLOG

Action:
- Do only if time permits
- Consider eliminating
- Nice-to-have enhancement
- Monthly review

Tags: #lowurgency #lowimportance
```

---

## Benefits of 2D Priority System

✅ **Prevents crisis management**
- Important-but-not-urgent work gets planned
- Reduces last-minute emergencies

✅ **Protects strategic work**
- Long-term initiatives don't get lost
- Roadmap stays on track

✅ **Empowers delegation**
- Clear rubric for what to delegate
- Fast decisions on task routing

✅ **Reduces cognitive load**
- Clear matrix vs. ambiguous ranking
- Less re-prioritizing

✅ **Aligns with strategy**
- Links to Q4 2025 strategic weights
- Supports ActivePhase objectives

---

## Quick Reference Card

```
                    URGENT
                      ↑
    🔴 DO NOW          │      🟢 DELEGATE
  (Execute now)        │     (Quick win)
                       │
IMPORTANT ←────────────┼────────────→ UNIMPORTANT
                       │
   🟡 SCHEDULE         │     ⚪ BACKLOG
   (Plan now)          │    (Skip/defer)
                       ↓
                   NOT URGENT

Quadrant Assessment:
- High Urgency = Due < 2 weeks
- Low Urgency = Due > 2 weeks
- High Importance = Strategic weight or critical business impact
- Low Importance = Operational or optional
```

---

## Related Files

- [[tasks/Priority Matrix Board.md]] - Kanban implementation
- [[strategy/ActivePhase.md]] - Strategic weights and Q4 2025 priorities
- [[tasks/master_task_list.md]] - Master task list with 2D tags
- [[Tasks by Theme]] - Tasks grouped by strategic initiative

---

**Framework Status**: ✅ Active in MarthaVault  
**Last Updated**: 2025-11-05  
**Next Review**: 2025-12-01