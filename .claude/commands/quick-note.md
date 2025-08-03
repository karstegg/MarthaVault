# Quick Note Command

Creates a quick note/reminder that can either go to inbox or be made a task. Minimal processing with optional linking.

## Usage
```
/quick-note Battery invoices must be processed monthly
/quick-note Meeting with Sipho tomorrow - link to [[Gloria Mine]]
/quick-note Follow up on TLB quote #TLB #capital
```

## Implementation
1. Create note in `00_inbox/` with timestamp
2. Add basic front-matter with status and priority
3. Parse for links (people, projects, tags) and include them
4. If contains action words (must, need, follow up, etc.), offer to convert to task
5. Minimal processing - just capture and organize

## Arguments
- `$ARGUMENTS` - The note content with optional links and tags

## Output
- Quick note file in inbox with proper naming
- Optional task creation if action-oriented
- Link detection and inclusion
- Tag preservation