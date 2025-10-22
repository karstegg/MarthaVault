# Rule: Strategic Priority Calculation

## Strategic Context Integration

MarthaVault uses a strategic priority system that multiplies base priority by strategic alignment weights.

## Strategy Layer Documents

**Location**: `strategy/` folder

1. **CompanyStrategy.md** - 5 strategic pillars, long-term goals
2. **ActivePhase.md** - Q4 2025 priorities with ObjectiveWeight multipliers
3. **FocusOfWeek.md** - Weekly tactical priorities with FocusBoost values

## Priority Calculation Formula

```
Base Priority = 0.30×Deadline + 0.25×ActiveProject
              + 0.15×KeyPeople + 0.10×Standard
              + 0.10×Recency + 0.05×Historical
              - 0.05×ArchivedPenalty

Strategy Multiplier:
- Direct objective link: 1 + ObjectiveWeight (from ActivePhase.md)
- One hop via project: 1 + 0.5×ObjectiveWeight
- Focus-of-week: add FocusBoost (from FocusOfWeek.md)

Final Priority = (Base × Multiplier) + FocusBoost (capped at 2.5)
```

## Q4 2025 Strategic Weights

From `strategy/ActivePhase.md`:

- **Fire Safety & Risk Mitigation**: **2.0x** (CRITICAL)
- **BEV Program Optimization**: **1.5x** (HIGH)
- **Compliance & Audit Excellence**: **1.5x** (HIGH)
- **Team Capacity Building**: **1.2x** (MEDIUM)
- **Capital Planning & Delivery**: **1.2x** (MEDIUM)

## Usage

When prioritizing tasks:

1. **Check Graph Memory** for Project→Strategy relations
2. **Apply correct multiplier** based on strategic alignment
3. **Consider FocusOfWeek** for additional boost
4. **Calculate final priority** using formula

## Example

**Task**: "Review BEV fire safety procedures with Kishore"

**Analysis**:
- Project: BEV Fire Safety Program
- Strategic alignment: Fire Safety & Risk Mitigation (2.0x)
- Base priority: High (0.8)
- Final priority: 0.8 × 2.0 = 1.6 (CRITICAL)

**Result**: This task gets elevated to CRITICAL priority due to strategic alignment.

## When to Apply

- Task prioritization and scheduling
- Project planning and resource allocation
- Decision-making when multiple options exist
- Weekly planning and focus setting

## Integration with Memory Systems

**Graph Memory**: Use `mcp3_search_nodes()` to find Project→Strategy relations

**Basic Memory**: Search `strategy/` documents for current weights and priorities

**Always cite strategic alignment** when explaining priority decisions.
