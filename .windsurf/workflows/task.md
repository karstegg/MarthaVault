---
description: Add a new task to the master task list
---

# /task

Add a new task to `tasks/master_task_list.md`.

## Usage

```
/task [task description]
```

## Process

1. **Append task** to `tasks/master_task_list.md`:
   ```markdown
   - [ ] [task description]
   ```

2. **Add tags**:
   - `#task`
   - `#year/2025`
   - Any relevant project/context tags

3. **Create file if missing**: If `tasks/master_task_list.md` doesn't exist, create it with proper front matter:
   ```yaml
   ---
   Status:: #status/active
   Priority:: Med
   Assignee:: Greg
   Tags:: #task #master_list #year/2025
   ---
   
   # Master Task List
   
   - [ ] [task description]
   ```

4. **Confirm** in chat: `Task added → line X`

## Example

**Input**: `/task Review BEV fire safety procedures with Kishore`

**Output**:
```markdown
- [ ] Review BEV fire safety procedures with Kishore #task #BEV #year/2025
```

**Confirmation**: `Task added → line 47`
