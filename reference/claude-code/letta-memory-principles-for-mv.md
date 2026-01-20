---
'Status:': Reference
'Created:': 2025-12-22
'Tags:': null
permalink: reference/claude-code/letta-memory-principles-for-mv
---

# Letta Memory Agent: Principles & Application to MarthaVault

## What is Letta?

Letta (formerly MemGPT) is a platform for building **stateful AI agents** with advanced memory that can learn and self-improve over time. It originated from the MemGPT research paper which proposed treating LLMs as operating systems—with the agent actively managing its own memory like an OS manages RAM and disk.

### Core Philosophy

> "Agents don't just read from memory—they actively manage it."

Unlike traditional RAG (Retrieval-Augmented Generation) systems that passively fetch relevant context, Letta agents:
- **Decide** what to remember
- **Edit** their own memory in real-time
- **Forget** what's no longer relevant
- **Compress** information as it ages
- **Decompress** details when needed

This mirrors how human memory works: generalizing past events but recalling specific details when prompted.

## Letta's Memory Architecture

### The Four Memory Layers

```
┌────────────────────────────────────────────────────────┐
│                    CORE MEMORY                         │
│  Always in context • Agent edits directly              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │   persona    │ │    human     │ │   custom     │   │
│  │  (~2000 ch)  │ │  (~2000 ch)  │ │  (~2000 ch)  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  Agent identity    User preferences  Project context   │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│                  MESSAGE BUFFER                        │
│  Rolling window of recent conversation                 │
│  Fixed capacity • FIFO overflow to archival            │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│                 ARCHIVAL MEMORY                        │
│  Long-term storage • Semantic search                   │
│  Agent decides what to store • Vector DB backend       │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│                  RECALL MEMORY                         │
│  Raw conversation history • Full transcripts           │
│  Searchable by date and content                        │
└────────────────────────────────────────────────────────┘
```

### Memory Tools Available to Agent

The agent has explicit tools to manage memory:

| Tool | Purpose |
|------|---------|
| `memory_replace` | Targeted text substitution in a block |
| `memory_insert` | Add new lines to existing block |
| `memory_rethink` | Completely rewrite entire block |
| `archival_memory_insert` | Store information long-term |
| `archival_memory_search` | Retrieve from long-term storage |
| `conversation_search` | Search chat history |
| `conversation_search_date` | Search history by date range |

### Key Insight: Compression as Thinking

In Letta's design, **compression is part of the thinking process**. The agent continually:
1. Compresses history into generalizations
2. Stores distilled knowledge in archival memory
3. Decompresses (retrieves) specific details when needed

This prevents context window overflow while maintaining access to full history.

## Applying Letta Principles to MarthaVault

### Current MV Memory Architecture

```
┌────────────────────────────────────────────────────────┐
│                    CLAUDE.md                           │
│  Always in context • Static instructions               │
│  Rules, workflows, references                          │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│              GRAPH MEMORY (MCP)                        │
│  52 entities • 60+ relations                           │
│  Searched on demand • Entity-relationship store        │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│              BASIC MEMORY (MCP)                        │
│  30+ documents • Semantic search                       │
│  Searched on demand • Note-based                       │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│                 VAULT FILES                            │
│  Full documents • Git versioned                        │
│  Read on demand • Obsidian integration                 │
└────────────────────────────────────────────────────────┘
```

**Gap identified**: No always-in-context, self-editable working memory.

### Proposed Enhancement: MV Memory Blocks

Add a Letta-inspired layer between CLAUDE.md and retrieval systems:

```
┌────────────────────────────────────────────────────────┐
│                    CLAUDE.md                           │
│  Bootstrap + "Read memory blocks first"                │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│              .claude/memory/ (NEW)                     │
│  Always in context • Claude edits via Edit tool        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │  persona.md  │ │   human.md   │ │current_focus │   │
│  │  (~2000 ch)  │ │  (~2000 ch)  │ │  (~2000 ch)  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  ┌──────────────┐                                      │
│  │ learnings.md │  Claude's discovered patterns        │
│  │  (~2000 ch)  │                                      │
│  └──────────────┘                                      │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│        GRAPH + BASIC MEMORY (existing)                 │
│  Searched on demand • Rich context retrieval           │
└────────────────────────────────────────────────────────┘
```

### Memory Block Definitions

#### persona.md
What Claude knows about itself in MV context:
- Role and responsibilities
- Operating modes (autonomous, command, skills)
- Communication style preferences
- Self-editing rules

#### human.md
What Claude learns about Greg:
- Communication preferences
- Work patterns and habits
- Corrections and redirections
- Learned preferences (auto-updated)

#### current_focus.md
Active working context:
- Current projects and priorities
- This week's focus areas
- Pending decisions
- Active strategic objectives

#### learnings.md
Claude's discovered insights:
- Workflow patterns that work
- Edge cases and solutions
- System quirks and workarounds
- Things to avoid

### Self-Editing Implementation

Unlike Letta which has dedicated memory tools, MV uses Claude Code's native **Edit tool**:

```markdown
## CLAUDE.md Instructions (new section)

At session start, read these memory blocks:
- `.claude/memory/persona.md`
- `.claude/memory/human.md`
- `.claude/memory/current_focus.md`
- `.claude/memory/learnings.md`

You have EDIT permission. Update blocks when:
- User expresses preference → update human.md
- Focus shifts → update current_focus.md
- Workflow succeeds → update learnings.md
- You discover something → update learnings.md
```

### Trigger Patterns for Self-Editing

**Update human.md when:**
- "I prefer..." / "I like..." / "Don't..."
- User corrects your approach
- Pattern observed in user behavior

**Update current_focus.md when:**
- New project becomes active
- Priorities shift
- Major context change
- Week/quarter boundary

**Update learnings.md when:**
- Workflow completes successfully
- Edge case handled
- Error resolved
- Pattern discovered

### Commands for Explicit Learning

| Command | Purpose |
|---------|---------|
| `/init` | Scan vault, populate initial blocks |
| `/remember [fact]` | Explicit "remember this" trigger |
| `/reflect` | End-of-session consolidation |
| `/memory-status` | Show all blocks with char counts |
| `/memory-rollback` | Restore previous version via Git |

### Async Consolidation (Letta Pattern)

Spawn background agent at session end:

```
Task(
  subagent_type="general-purpose",
  run_in_background=true,
  prompt="Review conversation. Update memory blocks:
          - human.md: New preferences learned?
          - learnings.md: Workflow insights?
          - current_focus.md: Focus shifted?
          Keep under 2000 chars. Be selective."
)
```

## Comparison: Letta vs MV Memory Blocks

| Aspect | Letta Native | MV Implementation |
|--------|--------------|-------------------|
| **Storage** | PostgreSQL | Markdown files |
| **Versioning** | Internal | Git history |
| **Edit mechanism** | Dedicated tools | Edit tool |
| **Block types** | persona, human, custom | persona, human, focus, learnings |
| **Char limits** | ~2000 per block | ~2000 per block |
| **Retrieval layer** | Archival + Recall | Graph + Basic Memory |
| **Rollback** | Version history | Git restore |
| **Deployment** | Server required | Native to CCLI |

## Benefits of This Approach

1. **Always-in-context**: Memory blocks loaded every session
2. **Self-editing**: Claude updates without explicit commands
3. **Git versioned**: Full history, easy rollback
4. **Zero migration**: Works with existing vault
5. **Preserves tools**: Skills, commands, MCP all intact
6. **Transparent**: Human-readable markdown files
7. **Complementary**: Works alongside claude-mem if installed

## Implementation Priority

1. **Phase 1**: Create memory blocks with initial content
2. **Phase 2**: Add self-editing instructions to CLAUDE.md
3. **Phase 3**: Create learning commands (/init, /remember, /reflect)
4. **Phase 4**: Test async consolidation sub-agent
5. **Phase 5**: Evaluate claude-mem as archive layer (2025-12-28)

## Key Letta Insights Applied

| Letta Principle | MV Application |
|-----------------|----------------|
| "Memory as OS resource" | Memory blocks as working RAM |
| "Agent controls memory" | Claude edits blocks directly |
| "Compression as thinking" | Learnings.md distills patterns |
| "Hierarchical layers" | Blocks → Graph/Basic → Vault files |
| "Transparent management" | Human-readable, Git-versioned |

## Related Documents

- `reference/claude-code/claude-mem-vs-letta-comparison.md` - Full comparison
- `.claude/plans/federated-kindling-anchor.md` - Implementation plan
- `reference/claude-code/memory-systems.md` - Current MV architecture
- `IDEAS/2025-12-22 – Memory-Catcher Agent for Session Insights.md` - Memory-Catcher concept

## Sources

- [Letta Documentation](https://docs.letta.com)
- [Letta Memory Guide](https://docs.letta.com/guides/agents/memory/)
- [MemGPT Research Background](https://docs.letta.com/concepts/letta/)
- [Adding memory to LLMs with Letta](https://tersesystems.com/blog/2025/02/14/adding-memory-to-llms-with-letta/)
- [Layers of Memory, Layers of Compression](https://timkellogg.me/blog/2025/06/15/compression)