# Outlook Extractor - Real-World Workflows

Complete workflow examples for common Outlook automation tasks.

---

## Workflow 1: Daily Email Review

Extract and review all emails from today, then identify high-priority items.

```bash
# Step 1: Extract today's emails
python outlook_extractor.py emails --days 1 --limit 100

# Step 2: Review outlook_emails.json for:
# - Unread messages
# - Emails with attachments
# - Senders in your important list
```

**When to use**: Start of work day to catch critical emails

**Output**: `outlook_emails.json` with today's email metadata

---

## Workflow 2: Weekly Calendar Planning

View the coming week's meetings to prepare schedules and identify conflicts.

```bash
# Extract next 7 days of meetings
python outlook_extractor.py calendar --days 7 --limit 100
```

**When to use**: Sunday evening or Monday morning planning

**Output**: `outlook_calendar.json` with all meetings for the week

**Next step**: Review for:
- Early morning meetings (adjust start time?)
- Back-to-back meetings (add buffer time?)
- Conflicting attendee locations

---

## Workflow 3: Send Important Report with Attachment

Send a quarterly report to leadership with CC and high priority.

```bash
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --cc "gregory.karsten@company.com,melissa.muller@company.com" \
  --subject "Q4 2025 Operations Report" \
  --body "Please find attached the Q4 2025 operations report with detailed analysis and recommendations for Q1 2026." \
  --attachment "C:\Reports\Q4_2025_Operations_Report.pdf" \
  --priority "high"
```

**When to use**: Quarterly reporting deadlines

**Key points**:
- High priority ensures visibility
- CC keeps stakeholders informed
- Absolute file path required
- Professional body text

---

## Workflow 4: Schedule Team Meeting

Create a meeting with multiple attendees at a specific time.

```bash
python outlook_extractor.py create-meeting \
  --subject "Q4 Planning Session - Operations Team" \
  --start "2025-10-28 09:00" \
  --end "2025-10-28 10:30" \
  --location "SHERQ Conference Room" \
  --attendees "xavier.petersen@company.com,gregory.karsten@company.com,melissa.muller@company.com,marina.schoeman@company.com" \
  --body "Quarterly planning session to review Q3 results and plan Q4 initiatives. Please come prepared with departmental updates."
```

**When to use**: Before announcing team meetings

**Key points**:
- Use local SAST time (what you see in Outlook)
- Include specific location
- Add meeting notes for context
- Attendees get meeting invite

---

## Workflow 5: Cancel Meeting and Notify Team

Delete a meeting and send cancellation email to attendees.

```bash
# Step 1: Delete the meeting
python outlook_extractor.py delete-meeting \
  --subject "Q4 Planning Session - Operations Team" \
  --start "2025-10-28 09:00"

# Step 2: Send cancellation email
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com,gregory.karsten@company.com,melissa.muller@company.com,marina.schoeman@company.com" \
  --subject "CANCELLED: Q4 Planning Session - Rescheduled to October 30" \
  --body "The Q4 Planning Session scheduled for October 28 at 9:00 AM has been cancelled due to unforeseen circumstances. The meeting has been rescheduled to October 30 at 2:00 PM in the same location. Your calendar has been updated. Please confirm your attendance." \
  --priority "high"
```

**When to use**: Urgent meeting cancellations

**Key points**:
- Delete meeting first to prevent confusion
- Use high priority for cancellations
- Include new reschedule date/time if applicable
- Address all attendees

---

## Workflow 6: Extract and Archive Last Month's Emails

Get all emails from the past 30 days for archival or reporting.

```bash
# Extract past 30 days
python outlook_extractor.py emails --days 30 --limit 1000

# Results saved to outlook_emails.json
# Backup this file with timestamp for records
```

**When to use**: Month-end reporting or archival

**Output**: `outlook_emails.json` with all emails from past 30 days

---

## Workflow 7: Batch: Extract All Outlook Data

Get a complete snapshot of emails, calendar, and contacts.

```bash
python outlook_extractor.py all
```

**Output**: `outlook_all.json` containing:
- `emails`: 20 recent emails
- `calendar_events`: Next 7 days of meetings
- `contacts`: 50 contacts

**When to use**:
- System migration
- Backup creation
- Comprehensive reporting

---

## Workflow 8: Schedule Emergency Team Meeting

Quickly create an urgent meeting in the next hour.

```bash
python outlook_extractor.py create-meeting \
  --subject "URGENT: Emergency Operations Meeting" \
  --start "2025-10-20 15:00" \
  --end "2025-10-20 15:30" \
  --location "Microsoft Teams" \
  --attendees "xavier.petersen@company.com,gregory.karsten@company.com,melissa.muller@company.com" \
  --body "URGENT MEETING: Emergency operations discussion. All leadership must attend. Details to follow in Teams."
```

**When to use**: Crisis management

**Key points**:
- Use current time + 30-60 minutes
- Virtual meeting (Teams) for speed
- Clear URGENT in subject
- Notify all required attendees immediately

---

## Workflow 9: Send Performance Reviews to Team

Send performance review documents to multiple team members.

```bash
# Send to first team member
python outlook_extractor.py send-email \
  --to "xavier.petersen@company.com" \
  --subject "Your 2025 Q3 Performance Review" \
  --body "Please find attached your Q3 2025 performance review. Please review and schedule a discussion with your manager." \
  --attachment "C:\Reviews\Xavier_Petersen_Q3_2025_Review.pdf"

# Send to second team member
python outlook_extractor.py send-email \
  --to "gregory.karsten@company.com" \
  --subject "Your 2025 Q3 Performance Review" \
  --body "Please find attached your Q3 2025 performance review. Please review and schedule a discussion with your manager." \
  --attachment "C:\Reviews\Gregory_Karsten_Q3_2025_Review.pdf"

# Send to third team member
python outlook_extractor.py send-email \
  --to "melissa.muller@company.com" \
  --subject "Your 2025 Q3 Performance Review" \
  --body "Please find attached your Q3 2025 performance review. Please review and schedule a discussion with your manager." \
  --attachment "C:\Reviews\Melissa_Muller_Q3_2025_Review.pdf"
```

**When to use**: Performance review cycles

**Key points**:
- One email per recipient for privacy
- Use person-specific review file
- Professional subject line
- Clear instructions in body

---

## Workflow 10: Meeting Room Reservation

Create a recurring series of placeholder meetings to reserve a room.

```bash
# Reserve room for Q4 weekly meetings
python outlook_extractor.py create-meeting \
  --subject "[RESERVED] SHERQ Conference Room - Weekly Operations" \
  --start "2025-10-28 13:00" \
  --end "2025-10-28 15:00" \
  --location "SHERQ Conference Room" \
  --body "Room reserved for weekly operations meetings. Contact Xavier Petersen if conflicts arise."
```

**Note**: For recurring meetings, you'll need to create multiple instances:

```bash
# Week 2
python outlook_extractor.py create-meeting \
  --subject "[RESERVED] SHERQ Conference Room - Weekly Operations" \
  --start "2025-11-04 13:00" \
  --end "2025-11-04 15:00" \
  --location "SHERQ Conference Room"

# Week 3
python outlook_extractor.py create-meeting \
  --subject "[RESERVED] SHERQ Conference Room - Weekly Operations" \
  --start "2025-11-11 13:00" \
  --end "2025-11-11 15:00" \
  --location "SHERQ Conference Room"
```

**When to use**: Recurring room bookings

**Key points**:
- Use [RESERVED] prefix for visibility
- Include contact for conflicts
- Repeat for each week/month needed

---

## Workflow 11: Email Status Report Before Shutdown

At end of day, email stakeholders on progress and send to archive.

```bash
# Extract today's emails for reference
python outlook_extractor.py emails --days 1 --limit 100

# Send status update
python outlook_extractor.py send-email \
  --to "gregory.karsten@company.com" \
  --cc "xavier.petersen@company.com" \
  --subject "EOD Status Report - October 20, 2025" \
  --body "End of day status:

Completed:
- Q4 planning initial draft
- Operations report review
- Budget forecast updated

In Progress:
- Team performance reviews (80% complete)
- Infrastructure audit

Blocked:
- Waiting for finance department approval on capital project

Next Actions:
- Schedule performance review meetings
- Complete infrastructure audit
- Review finance response

See attached email summary for detail." \
  --priority "normal"
```

**When to use**: Daily status reporting

**Key points**:
- Reference extracted emails for context
- Structured format (Completed/In Progress/Blocked)
- CC relevant stakeholders
- Clear next actions

---

## Workflow 12: Delegate Task with Calendar Entry

Create meeting for delegation and send detailed task email.

```bash
# Create delegation meeting
python outlook_extractor.py create-meeting \
  --subject "Task Delegation: Q4 Budget Consolidation" \
  --start "2025-10-24 10:00" \
  --end "2025-10-24 10:30" \
  --location "Microsoft Teams" \
  --attendees "melissa.muller@company.com" \
  --body "Task delegation meeting. Will discuss Q4 budget consolidation responsibilities and timeline."

# Send task email with details
python outlook_extractor.py send-email \
  --to "melissa.muller@company.com" \
  --subject "Task Delegation: Q4 Budget Consolidation" \
  --body "Melissa,

I'm delegating the Q4 budget consolidation task to you. Details:

TASK: Consolidate Q4 departmental budgets into company-wide report

DEADLINE: November 15, 2025

REQUIREMENTS:
- Collect budget actuals from all departments
- Calculate variance from budget
- Prepare summary presentation
- Flag any variances >10%

RESOURCES:
- Budget template: C:\Templates\Budget_Consolidation_Template.xlsx
- Department contacts: C:\Contacts\Department_Heads.csv

DELIVERABLE:
- Final report and presentation

We'll meet Friday at 10 AM to discuss. Let me know if you have questions.

Thanks,
Xavier" \
  --priority "high"
```

**When to use**: Task assignments and delegation

**Key points**:
- Schedule meeting for discussion
- Send detailed email with requirements
- Include resources and templates
- Set clear deadline

---

## Tips for Workflow Success

### Timing
- Schedule meetings 30+ minutes in advance
- Send emails at least 1 hour before urgent meetings
- Review calendar before end of workday

### Communication
- Always include location for physical meetings
- Use Teams link for remote meetings
- Be specific in meeting descriptions

### Follow-up
- Extract emails after sending to verify
- Review calendar after creating meetings
- Test delete workflow on test meetings first

### Error Handling
- Always verify email addresses before sending
- Double-check file paths for attachments
- Confirm SAST times match Outlook display
- Test on non-critical items first

---

## Common Workflow Combinations

### Daily Productivity Startup
```bash
# 1. Review yesterday's emails
python outlook_extractor.py emails --days 1 --limit 100

# 2. Check today's meetings
python outlook_extractor.py calendar --days 1 --limit 50
```

### Weekly Planning
```bash
# 1. Review week's meetings
python outlook_extractor.py calendar --days 7 --limit 100

# 2. Prepare status updates
python outlook_extractor.py emails --days 7 --limit 100
```

### Month-End
```bash
# 1. Archive all data
python outlook_extractor.py all

# 2. Send summary report
python outlook_extractor.py send-email ...
```

---

For detailed command parameters, see `reference/commands.md`
For troubleshooting, see `reference/troubleshooting.md`
