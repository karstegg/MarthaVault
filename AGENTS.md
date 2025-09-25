# Repository Guidelines

## Project Structure & Module Organization
- MarthaVault is an Obsidian knowledge base tuned for agent triage; work-in-progress notes land in `00_Inbox/`.
- Deliverables belong in `projects/<Project>/`; personal dossiers stay under `people/`; leave automations outside the vault.
- Shared reference and glossary material sits in `reference/`; binaries or screenshots go in `media/`; dated agendas follow `Schedule/YYYY-MM-DD - Event Title.md`.
- Task mirrors live in `tasks/master_task_list.md`; confirm every checklist item appears there.
- Slash-command definitions reside in `.claude/commands/`, with agent briefs in `.claude/agents/`.

## Build, Test, and Development Commands
- `rg -n "Status::" 00_Inbox` - find notes missing normalized front matter before triage.
- `rg "prod_refs" -g "*.md" reference` - ensure production reporting mentions stay inside `reference/ProductionReports`.
- `git diff --stat` and `git diff path/to/file.md` - review bulk edits and confirm checkbox parity prior to commit.

## Coding Style & Naming Conventions
- Begin every note with: `Status:: Draft`, `Priority:: Low|Med|High`, `Assignee:: <Owner>`, `DueDate:: YYYY-MM-DD`, then `Tags:: #task #year/2025 <context>`.
- Name files `YYYY-MM-DD - Descriptive Title.md`; append `-2`, `-3`, etc. for collisions.
- Favor concise headings, lists built with `- [ ]`, and fenced code blocks for templates or command snippets.

## Testing Guidelines
- After running `/triage`, confirm the note moved, adopted the canonical filename, and retained metadata.
- Verify mirrored tasks by searching for the task sentence in both its source note and `tasks/master_task_list.md`.
- For reference edits, run `rg "<Title>" reference` or use Obsidian's graph to check backlinks.
- New slash-command behaviors need an executable example stored in `.claude/commands/*.md`.

## Commit & Pull Request Guidelines
- Use conventional prefixes (`feat:`, `fix:`, `clean:`) plus a short intent summary; keep related adjustments in one commit.
- PRs should list touched folders, highlight new tags or command files, link tasks/issues, and report manual validation (triage run, task mirror check).
- Include before/after snippets for structural moves so reviewers can confirm scope quickly.

## Agent Workflow Tips
- Default assumption: Greg owns execution unless the front matter names another assignee.
- Park experiments or scratch pads in `00_Inbox/` with a status note; scrub or file them during daily triage.
