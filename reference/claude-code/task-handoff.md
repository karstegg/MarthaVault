---
task_id: 20251126-0644-001
from: claude-desktop
to: claude-cli
status: pending
created: 2025-11-26 06:44:00+02:00
permalink: reference/claude-code/task-handoff
---

## Task: Check Recent Emails (Last 24 Hours)

### Actions Required:
1. Execute: `/emails --received --days 1`
2. Execute: `/emails --sent --days 1`

### Expected Outcome:
- List of received emails from last 24 hours (sender, subject, timestamp)
- List of sent emails from last 24 hours (recipient, subject, timestamp)
- Summary of any actionable items or follow-ups needed

### Response Required:
- Email counts (received/sent)
- Key highlights or urgent items
- Any emails requiring immediate attention