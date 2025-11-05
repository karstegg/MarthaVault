---
'Status:': Draft
'Priority:': Med
'Assignee:': Greg
'DueDate:': null
'Tags:': null
permalink: tasks/filtered-task-list
---

# Live Filtered Task List (Excluding Personal & Completed)

## Final Working Query (No #task filter)
```tasks
not done
description does not include #personal
sort by priority, due
group by priority
```

## Additional Useful Queries

### Critical & High Priority Tasks Due Soon
```tasks
not done
description does not include #personal
description does not include #WTW-audit 
(description includes #priority/critical) OR (description includes #priority/high)
due before 2025-09-30
sort by due
```

### Overdue Tasks
```tasks
not done
description does not include #personal
due before today
sort by due
```

### BEV Project Tasks
```tasks
not done
description does not include #personal
description includes #BEV
sort by priority, due
```

### DMR/DMRE Compliance Tasks
```tasks
not done
description does not include #personal
(description includes #DMR) OR (description includes #DMRE)
sort by priority, due
```

### Tasks Assigned to Others
```tasks
not done
description does not include #personal
(description includes Xavier) OR (description includes Lourens) OR (description includes Willie) OR (description includes Gerard) OR (description includes Marina)
sort by priority, due
group by function task.text.match(/Xavier|Lourens|Willie|Gerard|Marina/)?.[0] || "Other"
```