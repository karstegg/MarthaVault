# /triage
Scan every item in **00_inbox/** and process according to type.

---

## 1 ║ Text / Markdown files (`*.md`, `*.txt`)
1. **Analyse intent** → meeting, task, idea, etc.  
2. **Move** file to the correct folder (`projects/…`, `people/…`, etc.).  
3. **Rename** `YYYY-MM-DD – Title.md` if needed.  
4. **Add / update front-matter** (Status, Priority, Assignee, DueDate).  
5. **Mirror check-boxes** to `tasks/master_task_list.md`.

---

## 2 ║ Media files (`*.jpg *.png *.gif *.webp *.m4a *.wav *.mp3 *.mp4 *.mov *.avi *.mkv`)
### 2.1 Relocate & rename
- Detect type → *image*, *audio*, *video*.  
- Rename `YYYY-MM-DD_HHMM_<slug>.<ext>`  
  (derive `<slug>` from filename or nearby note text if any).  
- Move to:

media/<type>/<YYYY>/

markdown
Copy
Edit

### 2.2 Create (or append to) a companion note
- Target: matching note in `00_inbox/` **or** new file  
  `YYYY-MM-DD_HHMM_<slug>.md`.
- Insert / ensure this front-matter:

Status:: #status/new
MediaType:: #image / #audio / #video
Assignee::
DueDate::

markdown
Copy
Edit

- Embed link:  
  `![[media/<type>/<YYYY>/<file>]]`

- **Summary section** (auto-generate one-sentence description).

- **Tagging**  
  - Primary: `#image` / `#audio` / `#video`.  
  - Infer project / person tags and wiki-links (`[[Pump 123]]`, `[[Jane Smith]]`).  
  - Add `#year/YYYY`.

- **Audio only** → transcribe with local Whisper CLI and append under **## Transcript**.

- **Action items**: if summary text implies an action (fix, review, send), create `- [ ] …` line and sync it to the master task list.

### 2.3 Cleanup
- Delete original file in `00_inbox/` only after successful move.

---

## 3 ║ Echo report
For each processed item output:

[✓] <old path> → <new path or note> (#tags…)

css
Copy
Edit

At the end, report a summary count:

Moved 3 notes, 1 image, 1 audio. Inbox empty.

yaml
Copy
Edit

---

## 4 ║ Safety
- **Never overwrite** existing files—append numeric suffix if needed.  
- **Ask** before deleting any note or media if something fails to move.