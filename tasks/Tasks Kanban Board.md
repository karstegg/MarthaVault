---
Status: Active
Priority: High
Assignee: Greg
Tags: #dashboard #tasks #kanban
LastUpdated: 2025-11-05
---

# Tasks Kanban Board

**Source**: [[tasks/master_task_list.md]] (72 open tasks)
**Last Updated**: 2025-11-05

---

## 🔴 CRITICAL & OVERDUE (Do First)

```tasks
not done
(priority is high OR priority is critical)
(due before today OR description includes CRITICAL OR description includes URGENT)
sort by due
limit 15
```

---

## 📋 TO DO

### 🔴 Critical Priority
```tasks
not done
priority is critical
due after yesterday
group by due
limit 10
```

### 🟡 High Priority
```tasks
not done
priority is high
due after yesterday
group by due
limit 10
```

### 🟢 Medium Priority
```tasks
not done
priority is medium
due after yesterday
group by project
limit 8
```

---

## 🔄 IN PROGRESS

```tasks
status.type is IN_PROGRESS
group by priority
sort by due
```

---

## ✅ RECENTLY COMPLETED (Last 7 Days)

```tasks
done after 1 week ago
sort by done
limit 15
```

---

## 📅 THIS WEEK (Due Before Sunday)

```tasks
not done
due before next week
sort by priority, due
```

---

## 🏢 BY SITE

### Nchwaning 3
```tasks
not done
description includes #site/Nchwaning3
sort by priority
limit 5
```

### Nchwaning 2
```tasks
not done
description includes #site/Nchwaning2
sort by priority
limit 5
```

### Gloria
```tasks
not done
description includes #site/Gloria
sort by priority
limit 5
```

---

## 🔥 BY PROJECT

### BEV Programme
```tasks
not done
description includes #BEV
sort by priority
limit 8
```

### Fire Safety
```tasks
not done
(description includes fire-safety OR description includes fire_safety)
sort by priority
limit 5
```

### Capital Projects
```tasks
not done
description includes #capital
sort by priority
limit 5
```

### Recruitment
```tasks
not done
description includes #recruitment
sort by priority
limit 5
```

---

## 👥 BY ASSIGNEE

### Assigned to Greg
```tasks
not done
description includes [[Karsten, Gregory]]
sort by priority, due
limit 10
```

### Delegated to Engineers
```tasks
not done
(description includes [[Sease, Sello]] OR description includes [[Dubazane, Sipho]] OR description includes [[Nzuza, Sikelela]])
sort by priority
limit 10
```

---

## 🔁 RECURRING TASKS

### Weekly (Mondays)
```tasks
not done
description includes #recurring
description includes Monday
```

### Monthly
```tasks
not done
description includes #recurring
description includes Monthly
```

---

## 📊 QUICK STATS

**Open Tasks**: 72
**Critical**: ~15
**High**: ~25
**Medium**: ~20
**Low**: ~12

**Top Priorities This Week**:
- BEV Fire Safety Programme (CRITICAL - Q4 2025 2.0x strategic weight)
- HD0054 Fire Investigation close-out actions
- Capital TMM FY25/26 Programme (Gloria DT orders placed early!)
- Recruitment (JPE & Electrical Foreman)
- WTW Audit outstanding actions

---

## 🎯 STRATEGIC CONTEXT (Q4 2025 Active Phase)

Tasks aligned with strategic objectives get priority multipliers:

- **Fire Safety & Risk Mitigation**: 2.0x (CRITICAL)
- **BEV Program Optimization**: 1.5x (HIGH)
- **Compliance & Audit Excellence**: 1.5x (HIGH)
- **Team Capacity Building**: 1.2x (MEDIUM)
- **Capital Planning & Delivery**: 1.2x (MEDIUM)

See: [[strategy/ActivePhase.md]] for full Q4 priorities

---

**Navigation**:
- [[tasks/master_task_list.md]] - Full task list
- [[Dashboard.md]] - Main dashboard
- [[tasks/archive/2025-Q3-completed.md]] - Completed tasks archive
