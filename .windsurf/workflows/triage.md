---
description: Scan and process all items in 00_Inbox/ according to type
---

# /triage

Scan every item in **00_Inbox/** and process according to type.

## Processing Rules

### Text / Markdown Files (`*.md`, `*.txt`)

1. **Analyze intent** → meeting, task, idea, etc.

2. **Scan for dates & create calendar events**:
   - Detect dates in content
   - Create calendar events in `Schedule/YYYY-MM-DD - Event Title.md`
   - Use format:
     ```yaml
     ---
     title: Event Title
     allDay: true
     date: YYYY-MM-DD
     completed: null
     ---
     ```

3. **Move** file to correct folder (`projects/`, `people/`, `IDEAS/`, etc.)

4. **Rename** to `YYYY-MM-DD - Title.md` if needed

5. **Add/update front-matter**:
   ```yaml
   ---
   Status:: #status/active
   Priority:: Med
   Assignee:: Greg
   DueDate:: YYYY-MM-DD
   Tags:: #task #project_name #year/2025
   ---
   ```

6. **Mirror checkboxes** to `tasks/master_task_list.md`

7. **Link calendar events** → ensure events reference source note via `**Source**: [[note title]]`

### Media Files (`*.jpg`, `*.png`, `*.gif`, `*.webp`, `*.m4a`, `*.wav`, `*.mp3`, `*.mp4`, `*.mov`, `*.avi`, `*.mkv`)

#### Relocate & Rename
- Detect type → *image*, *audio*, *video*
- Rename to `YYYY-MM-DD_HHMM_<slug>.<ext>`
- Move to: `media/<type>/<YYYY>/`

#### Create Companion Note
- Target: matching note in `00_Inbox/` OR new file `YYYY-MM-DD_HHMM_<slug>.md`
- Insert front-matter:
  ```yaml
  ---
  Status:: #status/new
  MediaType:: #image | #audio | #video
  Assignee::
  DueDate::
  Tags:: #media #year/2025
  ---
  ```
- Embed link: `![[media/<type>/<YYYY>/<file>]]`
- **Summary section**: Auto-generate one-sentence description
- **Tagging**:
  - Primary: `#image` / `#audio` / `#video`
  - Infer project/person tags: `[[Pump 123]]`, `[[Jane Smith]]`
  - Add `#year/YYYY`
- **Audio only**: Transcribe with local Whisper CLI, append under `## Transcript`
- **Action items**: If summary implies action, create `- [ ]` line and sync to master task list

#### Cleanup
- Delete original file in `00_Inbox/` only after successful move

## Output Format

For each processed item:
```
[✓] <old path> → <new path or note> (#tags…)
[📅] Created calendar event: <event title> (<date>)
```

Summary at end:
```
Moved 3 notes, 1 image, 1 audio. Created 2 calendar events. Inbox empty.
```

## Safety Rules

- **Never overwrite** existing files—append numeric suffix if needed
- **Ask** before deleting any note or media if something fails to move
- Verify all moves completed successfully before cleanup
