---
Status:: Draft
Priority:: High
Assignee:: Greg
DueDate::
Tags:: #year/2025 #strategy #process #planning
---

# Strategic Review Process - Planning & Prioritization

## Purpose
Regular review session between Greg and Claude Code to ensure strategic alignment, consolidate all active actions, and maintain clarity on priorities from quarterly down to weekly focus areas.

## Frequency
**Recommended:** Weekly on Monday mornings (after admin tasks, before deep work)
**Duration:** 30-45 minutes
**Alternative:** Bi-weekly if weekly feels too frequent

## The Planning & Prioritization Workflow

### Why This Matters (Greg's Personal Note)
> "I have to go through the process of doing the planning and prioritization. Unfortunately, it is taking a bit longer than normal now. But as you are going through it, I've just realized that once I'm through it, I get a sense of comfort, and then I can continue to do the work. This has been holding me back."

**Key Insight:** The planning process itself creates psychological readiness and comfort to execute. Without this clarity, work feels blocked. The time investment in planning is actually enabling productivity, not delaying it.

## Review Structure

### Phase 1: Business Strategy Alignment (10 min)
**Review Documents:**
- `strategy/CompanyStrategy.md` - Long-term strategic framework
- `strategy/ActivePhase.md` - Q4 2025 strategic focus (current quarter)

**Questions to Answer:**
1. Are the 5 strategic focus areas still correct?
   - Fire Safety (2.0x)
   - BEV Program (1.5x)
   - Compliance (1.5x)
   - Team Capacity (1.2x)
   - Capital Planning (1.2x)
2. Do the ObjectiveWeight multipliers reflect current reality?
3. Any new strategic priorities emerging?
4. Any priorities that should be reduced/removed?

### Phase 2: Consolidate All Active Actions (15 min)
**Scan These Sources:**
- `tasks/master_task_list.md` - All tracked tasks
- `00_Inbox/` - Unprocessed items needing decisions
- Recent `Daily/*.md` notes - Emerging actions
- Email/WhatsApp follow-ups pending
- Meeting action items from last week

**Create Full View:**
- List ALL currently active initiatives
- Identify duplicates or related items that should be consolidated
- Flag items that have been sitting too long without progress
- Identify items that might be missing

**Output:** Consolidated action list with current status

### Phase 3: Prioritize Against Strategy (10 min)
**For Each Active Action:**
1. Which strategic focus area does it align with?
2. What's the urgency level? (Critical/High/Medium/Low)
3. What's the impact if delayed?
4. Can it be delegated?
5. Should it be this week's focus, next week, or later?

**Apply Priority Calculation:**
```
Final Priority = (Base Priority × Strategy Multiplier) + FocusBoost
```

### Phase 4: Set Weekly Focus (5-10 min)
**Update `strategy/FocusOfWeek.md`:**
- Choose 3-5 top priorities for the week
- Assign FocusBoost values
- Document what's being deferred and why
- Set success criteria for the week

**Output:** Clear weekly execution plan

## Psychological Benefit

### The "Comfort Checkpoint"
This process serves as a **mental state transition**:
- **Before:** Overwhelmed, unclear what to tackle first, work feels blocked
- **During:** Active thinking, decision-making, strategic alignment
- **After:** Clarity, comfort, readiness to execute

**This is not wasted time** - it's the enabling process that allows productive work to happen.

### Making It Sustainable
- **Don't skip it when busy** - that's when you need it most
- **Time-box it** - 30-45 min max, don't let it become all-morning
- **Accept imperfection** - "We might miss a few things, but we can add that later and re-prioritize"
- **Build the habit** - Weekly rhythm creates predictability and reduces decision fatigue

## Suggested Schedule

### Monday Morning Routine (Ideal Sequence)
1. **08:00-08:30:** Admin tasks (JDE, Firefly, Oracle approvals)
2. **08:30-09:15:** Strategic Review & Planning Session (this process)
3. **09:15-12:00:** Deep work on #1 priority for the week
4. **Afternoon:** Meetings, coordination, secondary priorities

### Alternative (If Monday Too Packed)
- **Friday afternoon (15:00-16:00):** Review week, plan next week
- **Monday morning (08:30-09:00):** Quick confirmation/adjustments

## Tools to Support This

### Graph Memory Integration
- Use `mcp__basic-memory__search_notes("active projects")` to surface all ongoing work
- Use `mcp__basic-memory__recent_activity(timeframe="1 week")` to see what changed
- Use `mcp__memory__read_graph()` to get full context of relationships

### Automation Opportunities
- **Weekly planning trigger**: Schedule recurring calendar event "Strategic Review Session" Monday 08:30
- **Claude Code support**: Use `/review-strategy` slash command (to be created)
- **Dashboard view**: Create filtered view in Obsidian showing all active priorities

## Questions for Next Review
- Are we tracking the right metrics?
- Are delegation opportunities being maximized?
- Are strategic focus areas delivering results?
- What's working well? What needs adjustment?

## Related Documents
- [[strategy/CompanyStrategy]]
- [[strategy/ActivePhase]]
- [[strategy/FocusOfWeek]]
- [[tasks/master_task_list]]

---

**First Review Session Scheduled:** Monday, October 13, 2025 @ 08:30
**Recurring:** Every Monday morning (or Friday afternoon planning alternative)
