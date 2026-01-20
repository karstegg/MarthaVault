# /triage-whatsapp

Interactive review of ClaudeBox messages - items Greg found interesting while browsing YouTube, X, and the web.

## Purpose
Greg sends links to ClaudeBox when he sees something potentially useful for our systems. During triage, we:
1. Review each item in detail together
2. Analyze what it's about and potential applications
3. Decide collaboratively whether to save it and how to categorize it

## Source
- **ClaudeBox Group**: `120363406450230552@g.us`

## Checkpoint File
`reference/claude-code/whatsapp-triage-checkpoint.json`

## Workflow

### Step 1: Read Checkpoint
Read `reference/claude-code/whatsapp-triage-checkpoint.json` to get last processed timestamp.
If file doesn't exist, use 7 days ago as default.

### Step 2: Fetch Messages
From ClaudeBox group:
```
mcp__whatsapp__list_messages(
  chat_jid="120363406450230552@g.us",
  after="<checkpoint_timestamp>",
  limit=50
)
```

### Step 3: Review Each Message Interactively

For each message, process **one at a time** with user collaboration:

**A. Fetch and Analyze Content**

**If URL/Link:**
1. Use `WebFetch` to retrieve the content
2. Analyze and summarize:
   - What is this about? (brief overview)
   - Key concepts/technologies mentioned
   - Potential applications for our systems (BEV, automation, mining operations, etc.)
   - Relevance to current projects or strategic priorities
3. Present summary to user with the URL

**If Image/Media:**
1. Download: `mcp__whatsapp__download_media(message_id, chat_jid)`
2. Copy to vault temp location
3. Use Read tool to view and analyze the image
4. Describe what it contains and potential relevance

**B. Collaborative Decision**

Present the analysis and ask user:
```
📋 Item Review:
[Summary of what it is]

Potential applications:
- [List relevant use cases for our context]

Options:
1. Save as idea (create note in ideas/)
2. Create task (if actionable)
3. Archive reference (if useful for future lookup)
4. Skip (not relevant)

What would you like to do with this?
```

**C. Execute User's Choice**

Based on user response:

**If "Save as idea":**
- Ask for brief title/description
- Create `ideas/YYYY-MM-DD – ClaudeBox – [User's Title].md`
- Include: Full summary, URL, analysis, potential applications
- Ask user for additional tags beyond defaults
- Tag: `#idea #to-explore #year/2025` + custom tags

**If "Create task":**
- Ask for task description and priority
- Create `ideas/YYYY-MM-DD – ClaudeBox – [Title].md`
- Add to `tasks/master_task_list.md` with priority
- Tag: `#task #from-whatsapp #year/2025 #priority/[level]`

**If "Archive reference":**
- Create `reference/YYYY-MM-DD – ClaudeBox – [Title].md`
- Include full content summary
- Tag: `#reference #year/2025` + domain-specific tags

**If "Skip":**
- No file created
- Move to next message
- Still update checkpoint to mark as reviewed

### Step 4: Update Checkpoint
After each reviewed message, update checkpoint file:
```json
{
  "last_run": "ISO timestamp",
  "sources": {
    "claudebox": {
      "jid": "120363406450230552@g.us",
      "last_message_id": "last reviewed message ID",
      "last_timestamp": "timestamp of last reviewed message"
    }
  }
}
```

This allows resuming if session is interrupted - already reviewed messages won't be shown again.

### Step 5: Session Summary
At end of triage session, provide summary:
- Total messages reviewed: X
- Saved as ideas: X (list paths)
- Created tasks: X (list descriptions)
- Archived references: X (list paths)
- Skipped: X
- Next checkpoint: [timestamp]

## File Naming Conventions

**Ideas:** `ideas/YYYY-MM-DD – ClaudeBox – [User-Provided Title].md`

**Tasks:** `ideas/YYYY-MM-DD – ClaudeBox – [Task Description].md` (also mirrored in master_task_list.md)

**References:** `reference/YYYY-MM-DD – ClaudeBox – [Title].md`

Examples:
- `ideas/2025-12-20 – ClaudeBox – Agent Harness Patterns for Martha.md`
- `ideas/2025-12-20 – ClaudeBox – Audio AI for Voice Note Processing.md`
- `reference/2025-12-20 – ClaudeBox – Context Engineering Best Practices.md`

## Frontmatter Templates

**For Ideas:**
```yaml
---
Status:: To Review
Source:: WhatsApp ClaudeBox
CapturedDate:: YYYY-MM-DD
URL:: [original URL]
PotentialApplications:: [list from analysis]
Tags:: #idea #to-explore #year/2025 [+ user-specified tags]
---
```

**For Tasks:**
```yaml
---
Status:: Todo
Source:: WhatsApp ClaudeBox
CapturedDate:: YYYY-MM-DD
Priority:: [user-specified]
URL:: [original URL if applicable]
Tags:: #task #from-whatsapp #year/2025 #priority/[level]
---
```

**For References:**
```yaml
---
Status:: Reference
Source:: WhatsApp ClaudeBox
CapturedDate:: YYYY-MM-DD
URL:: [original URL]
Domain:: [technology/topic area]
Tags:: #reference #year/2025 [+ domain tags]
---
```

## Important Notes

### Interactive Process
- **One message at a time** - Don't batch process
- **Wait for user decision** before creating files
- **User provides title** - Don't auto-generate without approval
- **Collaborative tagging** - Ask if user wants additional tags beyond defaults

### Content Analysis
- **Use WebFetch** for all URLs to get full context
- **Read images** with Read tool to understand visual content
- **Analyze for relevance** to: BEV systems, mining operations, automation, AI/ML applications, current projects
- **Connect to strategy** - mention if it aligns with active strategic priorities

### Quality Over Speed
- Focus on understanding each item deeply
- Don't rush through the list
- User may want to discuss implications or ask questions
- Allow for back-and-forth dialogue on each item
