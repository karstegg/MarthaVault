```mermaid
flowchart TB
  You((You))
  subgraph Workspace
    Obsidian[[Obsidian Vault\nMarkdown + Front-matter + Links]]
    Watcher[Obsidian Watcher Plugin\n(onSave → parse + push deltas)]
  end
  %% …rest of the diagram…
```