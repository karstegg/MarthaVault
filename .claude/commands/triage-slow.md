# /triage-slow
Interactive triage processing - handle inbox items one-by-one with discussion and confirmation.

---

## Overview
Process every item in **00_inbox/** individually with user discussion and confirmation before taking action. This provides full control over each processing decision while maintaining systematic organization.

## Process Flow

### 1. **Scan & Inventory**
1. List all items in `00_inbox/` with basic info
2. Show total count and file types
3. Provide overview of what will be processed

### 2. **Individual Item Processing**
For each item in sequence:

#### **A. Item Analysis & Display**
- **Show Progress**: "Processing item X of Y"
- **File Info**: Name, size, type, last modified
- **Content Preview**: 
  - Text files: First 10-20 lines
  - Images: Display image with description
  - PDFs: Page count and title if available
  - Other files: File type and basic metadata

#### **B. Intelligent Suggestions**
Based on content analysis, suggest:
- **File Type Classification**: Meeting, task, idea, decision, reference, etc.
- **Destination Folder**: `projects/`, `people/`, `reference/`, etc.
- **Filename Format**: Proper `YYYY-MM-DD – Title.md` naming
- **Task Extraction**: Any checkboxes or action items found
- **Priority Assessment**: Urgent, High, Medium, Low based on content
- **Related Items**: Connections to existing projects or people

#### **C. User Interaction**
Present options for each item:
- **✅ Accept**: Proceed with suggested processing
- **📝 Modify**: Change destination, naming, or processing approach
- **⏭️ Skip**: Leave in inbox for later processing  
- **🗑️ Delete**: Remove file (ask for confirmation)
- **🔄 Custom**: Specify completely custom processing
- **ℹ️ More Info**: Show additional file details or content

#### **D. Execute Action**
Based on user choice:
- Move and rename files appropriately
- Create or update front-matter with Status, Priority, Assignee, DueDate
- Extract and sync tasks to `tasks/master_task_list.md`  
- Create person notes in `people/` if needed
- Create project folders if they don't exist
- Add proper tagging and linking

### 3. **Safety & Error Handling**
- **Never overwrite** existing files (add numeric suffix)
- **Always confirm** before deleting anything
- **Validate destinations** before moving files
- **Handle binary files** appropriately (images, PDFs, etc.)
- **Preserve original timestamps** when possible

### 4. **Media File Handling**
Special processing for media files following existing triage rules:

#### **Images/Videos/Audio** (`*.jpg *.png *.gif *.webp *.m4a *.wav *.mp3 *.mp4 *.mov *.avi *.mkv`)
- Rename: `YYYY-MM-DD_HHMM_<slug>.<ext>`
- Move to: `media/<type>/<YYYY>/`
- Create companion note with:
  - Front-matter with MediaType tag
  - Embedded media link: `![[media/<type>/<YYYY>/<file>]]`
  - Auto-generated summary
  - Proper tagging and linking
- **Audio files**: Offer transcription option

### 5. **Completion Summary**
After processing all items, provide:
- **Items Processed**: Count and types
- **Files Moved**: Source → Destination mapping
- **Tasks Created**: New entries in master task list  
- **Projects Created**: New project folders established
- **People Added**: New person notes created
- **Errors/Skipped**: Items that couldn't be processed
- **Inbox Status**: Final state (empty, remaining items)

## Interactive Commands During Processing

### **Universal Commands** (available anytime):
- `help` - Show available options for current item
- `info` - Display additional file information  
- `preview` - Show more content preview
- `list` - Show remaining items in queue
- `quit` - Exit triage (safely, with summary)

### **Processing Options** (for each item):
- `accept` or `a` - Accept suggested processing
- `modify` or `m` - Modify suggested action
- `skip` or `s` - Skip this item  
- `delete` or `d` - Delete this item (with confirmation)
- `custom` or `c` - Custom processing instructions

### **Modification Sub-Commands**:
- `folder <path>` - Change destination folder
- `name <title>` - Change filename/title
- `priority <level>` - Set priority (urgent/high/medium/low)  
- `assignee <person>` - Set assignee
- `date <YYYY-MM-DD>` - Set due date
- `tags <tag1> <tag2>` - Add specific tags

## Example Processing Flow

```
📁 Inbox Triage - Interactive Mode
Found 8 items to process

[1/8] Processing: "Meeting notes from John.txt"
📄 Text file, 2.1KB, modified 2025-08-10

Preview:
---
Meeting with John about project X...
- Need to follow up on budget
- Schedule review meeting for next week
---

💡 Suggestions:
- Type: Meeting note  
- Destination: projects/Project_X/
- Filename: 2025-08-10 – Meeting with John about Project X.md
- Tasks: 2 action items detected
- Priority: Medium
- Create: [[John Smith]] person note

Options: [A]ccept, [M]odify, [S]kip, [D]elete, [C]ustom, [I]nfo
Your choice: A

✅ Processed: Meeting note → projects/Project_X/2025-08-10 – Meeting with John about Project X.md
✅ Added 2 tasks to master task list
✅ Created person note: people/John Smith.md

[2/8] Processing: "Screenshot_20250810.png"
...
```

## Usage
`/triage-slow` - Start interactive triage of all inbox items

## Notes
- This command is designed for careful, considered processing
- Take your time with each item - there's no rush
- The system will remember your preferences and improve suggestions
- You can always exit and resume later
- All changes are tracked and can be reviewed in the completion summary

#triage #inbox #interactive #organization #workflow #year/2025