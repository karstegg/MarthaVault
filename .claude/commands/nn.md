# /new-note $ARGUMENTS
You are given the raw text in $ARGUMENTS.
1. Parse front-matter hints:
     - `project:` → determines folder
     - `title:`   → note title
2. Create the note as `projects/<project>/<YYYY-MM-DD>_<slug>.md`
   (or 00_inbox/ if no project).
3. Add YAML header: title, date, project (if any).
4. Tag according to the Tagging policy in claude.md.
5. Echo the created file path in chat.