---
task_id: 20251202-0830-001
from: claude-desktop
to: claude-cli
status: pending
created: 2025-12-02T08:30:00+02:00
permalink: reference/claude-code/task-handoff
---

## Task: Search Emails for DT0121 Status at N2

### Actions Required:
1. Execute: `/emails --search "DT0121" --days 7`
2. Execute: `/emails --search "Gae" --days 7 --filter "N2 OR Nchwaning"`
3. Execute: `/emails --search "SK OR Sikelela" --days 7 --filter "N2 OR Nchwaning"`

### Context:
- Greg needs status update on DT0121 equipment at Nchwaning 2
- Should be in emails from Gae or SK (Sikelela Nzuza)
- Equipment appears to be dump truck (DT prefix)

### Expected Outcome:
- Email(s) containing DT0121 status updates
- Sender, subject, date, and relevant content excerpts
- Current status/issue with the equipment

### Response Required:
- DT0121 status (breakdown, repair, availability)
- Who reported it (Gae or SK)
- Timeline/urgency indicators
- Any action items mentioned