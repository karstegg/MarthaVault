---
Status:: Draft
Priority:: Med
Assignee:: Greg
DueDate:: 
Tags:: #year/2025 #note
---

# Tasks Dashboard

## Today's Focus
```tasks
due today
not done
group by priority
sort by priority
```

## This Week
```tasks
due after yesterday
due before next week
not done
group by due
sort by due
```

## High Priority Tasks
```tasks
priority is high
not done
group by project
sort by due
```

## Critical Tasks (Safety & Urgent)
```tasks
priority is critical
not done
group by tags
sort by due
```

## In Progress Tasks
```tasks
status.type is IN_PROGRESS
group by project
sort by due
```

## By Project
### BEV Project Tasks
```tasks
tags include #BEV
not done
sort by priority, due
```

### WTW Audit Tasks
```tasks
tags include #WTW-audit
not done
sort by priority, due
```

### Capital Projects
```tasks
tags include #capital
not done
sort by priority, due
```

## By Person
### Greg's Direct Tasks
```tasks
not done
tags include #greg
sort by priority, due
```

### Assigned to Others
```tasks
tags include #xavier OR tags include #sipho OR tags include #sikilela OR tags include #sello
not done
group by assignee
sort by due
```

## Calendar Integration
### Tasks Due This Week with Calendar Events
```tasks
due after yesterday
due before next week
not done
group by due
sort by due
```

## Overdue Tasks
```tasks
due before today
not done
sort by due
```

## Completed This Week
```tasks
done after last week
group by done
sort by done reverse
limit to 20 tasks
```