---
'Status:': Active
'Priority:': High
'Assignee:': Greg
'DueDate:': null
'Tags:': null
permalink: dashboard
---

# MarthaVault Comprehensive Dashboard

**Last Updated**: September 11, 2025  
**Refresh Rate**: Daily  
**Next Review**: September 13, 2025

---

## 🎯 Today's Focus

### ⚠️ Critical Actions Required
```tasks
priority is critical
not done
sort by due
```

### 📅 Due Today
```tasks
due today
not done
group by priority
sort by priority
```

### 🔴 Overdue Items
```tasks
due before today
not done
sort by due
```

---

## 📊 Quick Stats Dashboard

### Current Status Overview
```chart
type: doughnut
labels: [To Do, In Progress, Blocked, Overdue]
series:
  - title: Task Status Distribution
    data: [12, 5, 1, 2]
width: 350
height: 250
```

### Priority Breakdown
```chart
type: bar
labels: [Critical, High, Medium, Low]
series:
  - title: Active Tasks by Priority
    data: [3, 8, 12, 4]
width: 400
height: 200
```

### Weekly Timeline
```chart
type: line
labels: [Overdue, Today, Tomorrow, This Week, Next Week, This Month]
series:
  - title: Task Distribution
    data: [2, 3, 4, 8, 6, 5]
tension: 0.3
width: 500
height: 180
```

---

## 🚨 Priority Matrix

### 🔴 Critical & Urgent (Do First)
```tasks
priority is critical
not done
sort by due
group by project
```

### 🟡 High Priority (Schedule)
```tasks
priority is high
not done
due before next week
sort by due
limit to 8 tasks
```

### 🟢 Medium & Low Priority (Delegate/Do Later)
```tasks
(priority is medium) OR (priority is low)
not done
sort by priority, due
limit to 10 tasks
```

---

## 📋 Kanban View

### 📌 To Do
```tasks
status.type is TODO
not done
group by priority
sort by due
limit to 12 tasks
```

### 🔄 In Progress
```tasks
status.type is IN_PROGRESS
group by project
sort by due
```

### ⏸️ Blocked/Waiting
```tasks
status.type is BLOCKED
not done
group by project
sort by due
```

### ✅ Completed This Week
```tasks
status.type is DONE
done after last week
group by done
sort by done reverse
limit to 8 tasks
```

---

## 🏗️ Project Views

### ⚡ BEV & Equipment Operations
```tasks
(tags include #BEV) OR (tags include #equipment) OR (tags include #TMM)
not done
group by priority
sort by due
```

### 🔥 Safety & Compliance
```tasks
(tags include #WTW-audit) OR (tags include #fire-audit) OR (tags include #safety) OR (tags include #DMRE)
not done
group by priority
sort by due
```

### 💰 Capital & Procurement
```tasks
(tags include #capital) OR (tags include #procurement) OR (tags include #contracts)
not done
group by priority
sort by due
```

### 👥 People & Management
```tasks
(tags include #GES) OR (tags include #recruitment) OR (tags include #performance)
not done
group by priority
sort by due
```

### 🏭 Production Operations
```tasks
(tags include #production) OR (tags include #daily-report) OR (tags include #weekly-report)
not done
group by priority
sort by due
```

---

## 📅 Calendar Integration

### This Week's Schedule
```tasks
due after yesterday
due before next week
not done
group by due
sort by due
```

### Next Week's Pipeline
```tasks
due after this week
due before next month
not done
group by priority
sort by due
limit to 15 tasks
```

### Monthly View
```tasks
due before next month
not done
group by project
sort by due
limit to 20 tasks
```

---

## 👥 Assignment Overview

### Greg's Direct Tasks
```tasks
not done
tags include #greg
sort by priority, due
limit to 15 tasks
```

### Delegated Tasks
```tasks
(tags include #xavier) OR (tags include #sipho) OR (tags include #sikilela) OR (tags include #sello) OR (tags include #johan) OR (tags include #rudy)
not done
group by assignee
sort by due
```

### Team Capacity View
```tasks
not done
group by assignee
sort by priority, due
limit to 25 tasks
```

---

## 📈 Performance Metrics

### Completion Rate (This Week)
```tasks
done after last week
group by done
sort by done reverse
limit to 15 tasks
```

### Productivity Trends
```chart
type: line
labels: [Week 1, Week 2, Week 3, Week 4]
series:
  - title: Tasks Completed
    data: [12, 15, 18, 14]
  - title: Tasks Created
    data: [10, 12, 16, 18]
tension: 0.4
width: 450
height: 200
```

### Project Completion Status
```chart
type: doughnut
labels: [BEV Project, Safety Audits, Capital Projects, HR Tasks, Operations]
series:
  - title: Project Progress
    data: [75, 60, 85, 40, 90]
width: 300
height: 250
```

---

## 🔍 Filter Views

### Site-Specific Tasks

#### Nchwaning 2
```tasks
tags include #site/Nchwaning2
not done
sort by priority, due
limit to 8 tasks
```

#### Nchwaning 3
```tasks
tags include #site/Nchwaning3
not done
sort by priority, due
limit to 8 tasks
```

#### Gloria Mine
```tasks
tags include #site/Gloria
not done
sort by priority, due
limit to 8 tasks
```

#### Shafts & Winders
```tasks
tags include #site/S&W
not done
sort by priority, due
limit to 8 tasks
```

---

## 🛠️ System Operations

### Recurring Tasks
```tasks
tags include #recurring
not done
sort by due
```

### Personal Development
```tasks
tags include #personal
not done
sort by priority, due
limit to 5 tasks
```

### Ideas & Innovation
```tasks
tags include #idea
sort by priority
limit to 8 tasks
```

---

## 📋 Quick Actions

### 🎯 Quick Wins (< 30 min)
- Check email approvals
- Schedule meetings
- Review and approve documents
- Send status updates

### 📞 Calls to Make
- Lourens (SA Cranes approval)
- Cornette (Capital applications)
- Equipment vendors
- Site managers

### 📧 Emails to Send
- Weekly reports
- Meeting confirmations
- Status updates
- Document reviews

### 📄 Documents to Review
- Capital applications
- Safety reports
- Equipment proposals
- Contract updates

---

## 🔄 Dashboard Maintenance

### Auto-Update Queries
All task queries refresh automatically when:
- Task status changes
- Due dates are modified
- Priority levels are updated
- Tags are added/removed

### Manual Updates Required
- Chart data (weekly refresh)
- Quick actions list (daily review)
- Team assignments (as needed)
- Project status (weekly review)

### Dashboard Health Check
- [ ] All queries rendering correctly
- [ ] Charts displaying accurate data
- [ ] No broken links or references
- [ ] Performance optimization check

---

## 📚 Related Documents

- [[tasks/master_task_list.md]] - Master task repository
- [[Schedule/]] - Calendar events and meetings
- [[projects/]] - Project-specific task breakdowns
- [[people/]] - Team directory and assignments
- [[operations/]] - Operational task tracking

---

## 🎛️ Dashboard Controls

### View Toggles
- **Compact View**: Show only essential information
- **Detailed View**: Include descriptions and notes
- **Chart View**: Focus on visual analytics
- **List View**: Traditional task listing

### Filter Options
- **Time Range**: Today, This Week, This Month, All
- **Priority**: Critical, High, Medium, Low, All
- **Status**: To Do, In Progress, Blocked, All
- **Project**: BEV, Safety, Capital, Operations, All
- **Assignee**: Greg, Team Members, All

### Export Options
- **PDF Report**: Weekly task summary
- **CSV Export**: Task data for analysis
- **Chart Images**: For presentations
- **Print View**: Optimized for paper

---

*Dashboard Version: 2.0*  
*Created: September 11, 2025*  
*Consolidated from: Task Management Dashboard, Tasks Dashboard, Tasks Kanban Board*

#dashboard #task-management #kanban #analytics #productivity #team-coordination #project-management #year/2025