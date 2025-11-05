---
'Status:': Draft
'Priority:': Med
'Assignee:': Greg
'DueDate:': null
'Tags:': null
permalink: archive/tasks-kanban-board-consolidated
---

# Tasks Kanban Board

## 📋 To Do
```tasks
status.type is TODO
not done
group by priority
sort by due
limit to 15 tasks
```

## 🔄 In Progress
```tasks
status.type is IN_PROGRESS
group by project
sort by due
```

## ✅ Done (This Week)
```tasks
status.type is DONE
done after last week
group by done
sort by done reverse
limit to 10 tasks
```

## ❌ Cancelled
```tasks
status.type is CANCELLED
done after last week
group by project
sort by done reverse
limit to 5 tasks
```

---

# Priority-Based View

## 🔴 Critical (Immediate Action)
```tasks
priority is critical
not done
sort by due
```

## 🟡 High Priority
```tasks
priority is high
not done
sort by due
limit to 10 tasks
```

## 🟢 Medium Priority
```tasks
priority is medium
not done
sort by due
limit to 8 tasks
```

## ⚪ Low Priority
```tasks
priority is low
not done
sort by due
limit to 5 tasks
```

---

# Project Boards

## 🔥 Safety & Compliance
```tasks
(tags include #WTW-audit) OR (tags include #fire-audit) OR (tags include #safety)
not done
group by priority
sort by due
```

## ⚡ BEV & Equipment
```tasks
(tags include #BEV) OR (tags include #equipment) OR (tags include #TMM)
not done
group by priority
sort by due
```

## 💰 Capital & Procurement
```tasks
(tags include #capital) OR (tags include #procurement) OR (tags include #contracts)
not done
group by priority
sort by due
```

## 👥 People & Management
```tasks
(tags include #GES) OR (tags include #recruitment) OR (tags include #performance)
not done
group by priority
sort by due
```