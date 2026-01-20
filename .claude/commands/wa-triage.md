# /wa-triage

Alias for `/triage-whatsapp`. See that command for full documentation.

**Interactive review workflow for ClaudeBox messages:**

Greg sends links to ClaudeBox when browsing YouTube, X, and the web. This command reviews them together:

1. Fetch unreviewed messages from ClaudeBox group
2. For each message:
   - Analyze content using WebFetch
   - Summarize what it is and potential applications
   - Discuss relevance to our systems (BEV, mining, automation)
   - User decides: Save as idea / Create task / Archive reference / Skip
3. Update checkpoint after each review

**Key difference:** Interactive and collaborative, not automated batch processing.

Run `/triage-whatsapp` for the full workflow.
