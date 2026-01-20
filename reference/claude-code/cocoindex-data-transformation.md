---
'Status:': Reference
'Tags:': null
'Source:': https://github.com/cocoindex-io/cocoindex
permalink: reference/claude-code/cocoindex-data-transformation
---

# CocoIndex - Data Transformation Framework for AI

## Overview

Ultra performant data transformation framework with Rust core engine. Designed for AI pipelines: vector indexing, knowledge graphs, RAG systems.

## Key Features

- **Speed:** Rust core, ~100 lines Python to define pipelines
- **Incremental:** Only recomputes changed data
- **Data Lineage:** Track data provenance
- **Plug-and-Play:** Swap sources/targets via config

## How It Works

Dataflow model - declare transformations, not mutations:

```python
pipeline = (
    source("local_files", path="./docs")
    .transform("split_text", chunk_size=512)
    .transform("embed", model="openai")
    .target("qdrant", collection="docs")
)
```

## Supported Integrations

**Sources:** Local files, S3, Azure Blob, Google Drive, Custom

**Targets:** PostgreSQL, Qdrant, LanceDB, Knowledge graphs

**Transformations:** Text embedding, chunking, LLM extraction, image captioning, PDF parsing

## Use Cases

- RAG pipelines (files → chunks → embeddings → vector DB)
- Knowledge graph construction
- Semantic search indexing
- Document processing

## Requirements

- Python 3.8+
- PostgreSQL (for incremental state)
- `pip install -U cocoindex`

## Potential Application

Could improve MarthaVault sync to memory systems:
- Incremental file processing
- Automatic updates on change
- Lineage tracking

## Links

- GitHub: https://github.com/cocoindex-io/cocoindex
- License: Apache 2.0

---

Archived via ClaudeBox triage 2025-12-20.