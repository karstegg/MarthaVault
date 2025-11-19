---
Status: Active
Priority: High
Assignee: Claude
DueDate: null
Tags: null
permalink: system/2025-11-19-session-learnings-outlook-sent-items-capital-project-tracking
---

# Session Learnings: Outlook Sent Items & Capital Project Tracking

**Date:** 2025-11-19
**Context:** Bearing Temperature Monitoring capital project estimate extraction

---

## 1. Skills Enhancement

### Outlook-Extractor: Sent Items Support Added

**Problem:** User requested email extraction from Sent Items, but skill only supported Inbox.

**Solution Implemented:**
- Added `--folder` parameter to emails command
- Choices: "Inbox" (default) or "Sent Items"
- Updated `get_emails()` method to handle folder selection
- Folder mapping: Inbox=6 (olFolderInbox), Sent Items=5 (olFolderSentMail)
- Time field handling: `SentOn` for Sent Items, `ReceivedTime` for Inbox
- Added `To` field for Sent Items output

**Usage:**
```bash
# Extract sent emails
python outlook_extractor.py emails --folder "Sent Items" --days 7 --limit 100

# Extract inbox emails (default)
python outlook_extractor.py emails --days 7 --limit 100
```

**Files Modified:**
- `C:\Users\10064957\.claude\skills\outlook-extractor\scripts\outlook_extractor.py`
- `C:\Users\10064957\.claude\skills\outlook-extractor\SKILL.md`

**Lesson:** When user requests skill modifications for missing functionality, implement them immediately to improve future sessions.

---

## 2. Capital Project Tracking Workflow

### Context: User sent capital estimate email, needed it extracted for documentation

**Workflow Pattern Identified:**
1. User prepares estimate based on input from engineers
2. Updates estimate based on additional information (SK added more belts)
3. Sends estimate to Management Accountant (Ilze Malouly) for unplanned capital register
4. Waits for GM feedback on capital allocation approval
5. Once approved, submits formal unplanned capital application

**Key Learning:** Capital estimates often change during preparation phase as site engineers provide updated counts/scopes.

### Information to Capture When Tracking Capital Projects

**Essential Fields:**
- Total estimate amount (R value)
- Breakdown by site/location
- Date sent and recipients
- Attachment filename
- Context explaining any updates/changes from original estimate
- Current status (waiting for X to do Y)
- Next step in approval chain

**Example from Today:**
- Total: R9.55M
- Breakdown: N2 (R5.3M), N3 (R3.3M), Gloria (R950k)
- Context: SK added N2 Graben conveyors (226 plumber blocks, corrected from 192)
- Status: Waiting for Ilze → GM feedback → Capital application decision

---

## 3. Email Search Strategy Improvements

### Pattern: User says "I sent an email between 3-5pm today"

**Optimal Search Approach:**
1. **Use Sent Items folder** with date filter
2. Search by keywords from subject/recipients if known
3. Extract full email body + attachments for context
4. Parse key numbers/data from email body

**Script Pattern for Email Content Extraction:**
```python
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')
sent_items = namespace.GetDefaultFolder(5)  # Sent Items
items = sent_items.Items
items.Sort('[SentOn]', False)

for item in items:
    if 'keyword' in item.Subject and 'time_check' in str(item.SentOn):
        # Extract body, attachments, recipients
        print(item.Body)
        for i in range(item.Attachments.Count):
            att = item.Attachments.Item(i+1)
            print(att.FileName)
```

---

## 4. Priority Classification Guidance

### Learning: User Corrected Priority Assessment

**Initial Assessment:** Belt Temperature Monitoring = High Priority
**User Correction:** Medium Priority

**Reasoning:**
- Project is waiting on external approvals (Ilze → GM)
- No immediate action required from Greg
- Regulatory requirement (DMPR) but not time-critical
- Budget allocation decision pending

**Lesson:** Don't assume regulatory requirements = High priority. Consider:
- User's current action items (can they do anything now?)
- Dependencies on external approvals
- Time sensitivity vs. importance
- User's explicit priority statements override inference

**Updated Priority Assessment Framework:**
- **Critical (🔴):** Immediate action required, blocking other work, safety-critical
- **High (🟡):** User has active tasks, near-term deadlines, dependencies on user's action
- **Medium (🟢):** Waiting on others, regulatory but not time-bound, standard operations
- **Low (⚪):** Nice to have, long-term planning, background research

---

## 5. Memory System Usage Patterns

### Effective Memory Query Strategy

**Today's Pattern:**
1. Initial search: Limited results (pre-sync)
2. User triggered `/sync-vault` manually
3. Re-search: Full context available post-sync

**Lesson:** When vault changes are made during session:
- Proactively suggest `/sync-vault` after significant file changes
- Re-query memory systems after sync completes
- Don't assume first search is comprehensive if recent edits occurred

**Best Practice:**
```
1. Make file changes
2. Run /sync-vault
3. Wait for sync completion
4. Query memory systems with updated data
```

---

## 6. Documentation Patterns for Capital Projects

### Template Structure Validated

**What Works Well:**
```markdown
## Final Estimate & Status

**Estimate sent:** [Date/Time] to [[Person]] (with team cc'd)
**Updated estimate breakdown:**
- **Site 1:** R[Amount]
- **Site 2:** R[Amount]
- **Total:** R[Total]

**Estimate file:** `filename.xlsx`

**Context:** [Why estimate changed, who added what]

**Recipients:** [Full list]

**Current status:** [What we're waiting for]
**Next step:** [What happens after current blocker resolves]
```

**Why This Works:**
- Clear financial breakdown
- Context explains changes (critical for future reference)
- Status tracking shows where project is blocked
- Next step provides forward-looking action

---

## 7. Skill Modification Protocol

### Today's Process (Successful)

**Steps Taken:**
1. User requested feature: "Edit outlook-extractor to enable searches in sent items"
2. Read existing implementation
3. Identify required changes (argparse, method signature, folder mapping)
4. Implement changes systematically
5. Test immediately with real use case
6. Update documentation (SKILL.md)
7. Create learning document (this file)

**Key Success Factors:**
- Clear user requirement
- Immediate testing with actual data
- Documentation updated same session
- Learning captured for future reference

---

## 8. Conversational Context Management

### Pattern: User Provided Screenshot

**User Behavior:** Instead of describing email, shared screenshot
**Expected Response:** Parse visual info, extract what you can, then request missing details

**Lesson:** When user shares screenshot but you need more detail:
1. Acknowledge what you can see
2. Request specific additional info you need
3. Offer alternative: "Can you paste the numbers?" or "Let me try to find it programmatically"

**Today:** User showed email screenshot, Claude asked for numbers, user redirected to programmatic extraction (better outcome).

---

## 9. Memory Entity Updates

### New Information Captured Today

**Ilze Malouly:**
- Role: Management Accountant (not SHERQ as previously documented)
- Responsibilities: Capital budgeting, unplanned capital register management, GM capital allocation interface
- Context: She's the gateway for unplanned capital applications

**Bearing Temperature Monitoring Project:**
- Full entity created with estimate breakdown
- Status tracking established
- Context about N2 Graben conveyor additions documented

**Lesson:** Always update person entities when role/responsibility becomes clearer through context.

---

## 10. Instructions to Add to CLAUDE.md

### Proposed Addition: Sent Items Email Extraction

Add to "Outlook Extractor Script Path" section:

```markdown
### Extracting Sent Emails

When user references emails they sent, use `--folder "Sent Items"` parameter:

```bash
cd "C:\Users\10064957\.claude\skills\outlook-extractor\scripts"
python outlook_extractor.py emails --folder "Sent Items" --days 7 --limit 100
```

**Use cases:**
- "I sent an email about X" → search Sent Items
- "Check my estimate email" → search Sent Items
- "What did I tell [Person] about [Topic]" → search Sent Items

**Output differences:**
- `From`: Always "Me (Gregory Karsten)"
- `To`: Recipients list (comma-separated)
- `SentOn`: Timestamp (instead of ReceivedTime)
```

### Proposed Addition: Capital Project Tracking

Add new section after "Contact Management":

```markdown
### Capital Project Estimate Tracking

When user mentions sending or preparing a capital estimate:

**Required information to capture:**
1. Total estimate amount (R value)
2. Site/location breakdown
3. Date sent and recipients
4. Attachment filename (Excel file typically)
5. Context explaining any changes from initial estimate
6. Current approval status and next step

**Workflow stages:**
1. Engineer preparation (gather input from site engineers)
2. Updates based on additional information
3. Send to Management Accountant (Ilze Malouly)
4. Await GM feedback on capital allocation
5. Submit formal unplanned capital application (if approved)

**Document in:** `projects/Capital/[Project Name]/[Date] – [Project Name].md`
```

---

## Action Items

- [x] Update outlook-extractor SKILL.md with --folder parameter documentation
- [x] Create this learning document
- [ ] Add Sent Items extraction usage to CLAUDE.md (Outlook section)
- [ ] Add Capital Project Tracking section to CLAUDE.md
- [ ] Update priority classification framework in system/policy.md with user's guidance
- [ ] Review and consolidate all capital project documentation patterns

---

## Future Session Improvements

1. **Proactive Sent Items Search:** When user mentions "I sent..." automatically search Sent Items
2. **Capital Estimate Template:** Create reusable template for capital project documentation
3. **Priority Inference:** Always defer to user's explicit priority statements over inference
4. **Memory Sync Awareness:** Suggest `/sync-vault` after significant file changes before memory queries

---

**Tags for Reference:** #outlook-extractor #sent-items #capital-projects #priority-classification #skill-modifications #learnings