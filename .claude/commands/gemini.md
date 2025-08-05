# /gemini - Communicate with Gemini

Send a message to Gemini via GEMINI_CHAT.md file.

## Usage
```
/gemini [message]
```

## Examples
```
/gemini Status update on July reports?
/gemini Process July 5th reports next - high priority
/gemini Great work on PR #7 fixes!
```

## Implementation
```markdown
---
### Claude-Desktop to Gemini
**Timestamp:** {{current_timestamp}}
**Subject:** {{auto_generated_subject}}

{{user_message}}

**—Claude-Desktop**

---
```

## Process
1. Append message to GEMINI_CHAT.md with proper formatting
2. Include timestamp and subject line
3. Use standard communication protocol
4. Gemini monitors this file for new messages