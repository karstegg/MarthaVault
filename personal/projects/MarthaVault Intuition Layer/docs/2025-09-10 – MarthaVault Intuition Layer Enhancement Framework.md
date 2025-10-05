---
"Status:": Draft
"Priority:": Low
"Assignee:": Greg
"Date:": 2025-09-10
"Tags:":
---

# MarthaVault Intuition Layer Enhancement Framework - September 10, 2025

## PRD-style Summary (concise, implementation-ready)
## 1) Background: current system (Vault-centric OS)

- **Workspace doctrine:** Obsidian vault is the working surface and long-term store. Strict front-matter, one primary tag (#task | #meeting | #idea | #decision), file naming `YYYY-MM-DD – Title.md`, consistent [[links]] to people/sites/equipment.
    
- **Task spine:** Checkbox tasks mirror into `tasks/master_task_list.md`. Daily notes + Schedule (UTC+2) provide planning surface.
    
- **Change control:** Human edits allowed directly; AI-generated edits must be PR-style or at least logged and source-grounded (no fabrication).
      
- **Claude usage today:** Claude CLI handles interactive work (voice via WhisperFlow/Windows voice). Claude app memory is conversation-side only; it does not index the vault.
    

## 2) Problem framing

- **Context window ≠ working memory:** We need durable, queryable memory across months/years without changing model weights.
    
- **Speed + traceability:** Fast “do the right thing” behavior must remain source-grounded and auditable.
    
- **Low-friction ops:** Prefer Obsidian-native workflows; avoid daemon bloat if possible (Obsidian plugin watcher first).
    

## 3) Target outcomes

- **Super-familiar assistant:** Feels “intuitive” in Greg’s domain; fires proven moves quickly, slows down when novelty/ambiguity appears.
    
- **Just-in-time retrieval:** Only the minimum relevant snippets enter the model context; everything else stays in the vault.
    
- **Continuously improving behavior:** Over time, fewer edits needed; responses converge on Greg’s style and standards.
    

## 4) Architecture (high level)

- **Surface:** Obsidian (authoring, daily use).
    
- **Dispatcher:** Claude CLI (planner/executor; writes outputs back to vault with correct front-matter and links).
    
- **Sidecars (“librarians”):**
    
    - **Memory service (MCP):** text chunk store + embeddings + exact file/line anchors; exposes `upsert_document`, `search_snippets`.
        
    - **Graph service (MCP):** property graph of notes/people/sites/tasks; exposes `upsert_nodes_and_edges`, `neighborhood(entity,time)`.
        
- **Watcher (indexer):** Preferred as **Obsidian plugin** that reacts to file events; alternative is CLI-based watcher. Publishes deltas to memory/graph.
    

## 5) Obsidian watcher (in-app plugin) – spec

- **Triggers:** on create/modify/rename/delete of `.md`; debounce saves; ignore `.obsidian/` and temp files.
    
- **Parse:** use Obsidian metadata cache (front-matter, tags, links/backlinks) + read body text.
    
- **Ingest calls:**
    
    - Memory: `upsert_document({path, mtime, text})` (server handles chunking/embeddings; returns chunk IDs).
        
    - Graph: `upsert_nodes_and_edges({noteId=path, props:{title,date,primaryTag,…}, edges:[links_to, at_site, mentions_person, originates_from]})`.
        
- **State:** tiny local map `{path: contentHash, mtime}` to avoid redundant pushes; replay on plugin start if missed events.
    
- **Settings UI:** endpoints, shared local token, include/exclude folders, debounce ms.
    

## 6) Retrieval flow (answering a query)

- **Plan:** CLI extracts entities + time window from the user request.
    
- **Graph first:** `neighborhood(entities, time, k)` returns a small ranked set of candidate note IDs.
    
- **Memory next:** `search_snippets({noteIds, query, limit})` returns quotable passages with file/line anchors.
    
- **Compose:** CLI builds a tight “retrieval pack” → prompt → generate grounded answer.
    
- **Write-back:** CLI saves outputs into the vault (correct folder/name/front-matter, backlinks to sources).
    

## 7) Intuition layer (behavioral stack)

- **Reflex cache:** Compact Q→A traces for recurring moves (trigger pattern, key signals, snippets used, output template). If a strong match, execute immediately with soft confirmation where prudent.
    
- **Skills library:** Small, named prompt modules encoding “how Greg does it” (e.g., Inbox→Triage, Meeting→Actions, DailyNote in SAST, BEV incident summary). Parameters: site/person/equipment/date.
    
- **Policy memory (always-on):** Short rules that shape every output (front-matter discipline, one primary tag, cite source lines, UTC+2, style/tone).
    
- **Gatekeeper:** If inputs match a known reflex + within guardrails → fast path. Otherwise fall back to deliberate retrieval + reasoning with citations.
    
- **Daily “sleep” pass:** When closing the daily note, distill accepted results into improved skill examples and/or cache entries; decay or drop noisy/unused ones.
    

## 8) Data & interfaces (concrete)

- **Front-matter minimum:** `Status::`, `Priority::`, `Assignee::`, `DueDate::`, `Tags::` (+ `#year/2025` + exactly one primary tag).
    
- **Graph edges (canonical):** `links_to`, `originates_from`, `at_site/#site/*`, `mentions_person`, `supersedes`, `belongs_to_project`, `has_task`.
    
- **Memory indexing:** store `{chunkId, path, lineStart, lineEnd, hash, embedding, timestamp}`; queries must return anchors for citation.
    
- **Security:** localhost endpoints; shared token; no vault secrets sent to model; outputs always include source pointers.
    

## 9) MVP scope (deliver in vault with Claude Code)

- **Obsidian watcher plugin (minimal):** listens, parses, sends `upsert_*` to memory/graph; settings pane; hash cache; debounce.
    
- **Two skills:**
    
    - Inbox→Triage note normalizer.
        
    - Daily note composer (UTC+2, due/blocked summary with links back to origin).
        
- **Reflex cache v0:** simple nearest-neighbor over prior accepted tasks; fires only on high-confidence matches, else no-op.
    
- **Policy prompt v0:** 10–15 lines injected on every call to enforce standards and tone.
    
- **CLI write-back:** create/update notes with correct naming, front-matter, backlinks; log one-line confirmations.
    

## 10) Phase 2 (after MVP)

- Add skill cards for Meetings→Actions, BEV risk summaries, Site stand-ups, Weekly roll-ups.
    
- Expand reflex cache with acceptance/edited/reject outcomes; lightweight confidence learning.
    
- Add “conflict detector” when sources disagree; auto surface links and ask.
    
- Optional headless watcher (Codespace/CLI) for indexing while Obsidian is closed.
    

## 11) Success metrics

- **Speed:** median time-to-answer for common workflows (triage, daily note) under X seconds.
    
- **Edit rate:** % of assistant outputs accepted with ≤1 minor edit rises week-over-week.
    
- **Grounding:** 100% of factual answers include at least one valid source anchor.
    
- **Adoption:** # of times reflex path fires vs deliberate path; should increase with safe acceptance.
    

## 12) Open questions / decisions

- Exact schemas for `upsert_*` payloads (JSON field names, error codes, versioning).
    
- Confidence thresholds for reflex firing and soft confirmations.
    
- How many “concept centers” to seed initially (BEV, Winders, DMRE, Inspections, CAPEX, Fire Risk, Sites).
    
- Where to persist skill cards and cache (vault `system/` folder vs local DB).
    

---

If you want, I can turn this into two files in the vault now: `docs/intuition_layer_prd.md` and `docs/api_contracts.md` with the `upsert_*` payload shapes so you can wire Claude Code against them.