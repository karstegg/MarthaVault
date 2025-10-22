# Windsurf Context Loading System

**Created**: 2025-10-15  
**Purpose**: Replicate Claude Code CLI's automatic context loading in Windsurf

---

## Overview

Windsurf now has a comprehensive context loading system that provides the same onboarding experience as Claude Code CLI, with automatic context loading for every new session.

## System Architecture

### Layer 1: Rules (Always Active) ✅
**Location**: `.windsurf/rules/`

These files are **automatically loaded** in every Windsurf session:

1. **`martha-vault-identity.md`**
   - Your identity as Greg's back-office AI assistant
   - Operating modes (Autonomous vs Command)
   - File creation guidelines
   - Response style

2. **`whatsapp-messaging-protocol.md`**
   - @Claude direct instruction handling
   - WhatsApp message drafting protocol (ALWAYS ask permission)
   - Greg's messaging style guide
   - Communication patterns by audience

3. **`memory-systems-usage.md`**
   - Dual memory system (Graph + Basic)
   - When to use which system
   - Tool usage examples
   - Entity types and relationships

4. **`file-organization-standards.md`**
   - Folder structure and naming conventions
   - Front matter standards
   - Tagging conventions
   - Task management rules
   - Media organization
   - Triage process

### Layer 2: Memories (Persistent) ✅
**System**: Cascade memory database

Automatically retrieved based on relevance:
- Critical configurations
- Technical debt items
- Context from previous sessions
- Project-specific knowledge

### Layer 3: MCP Servers (Shared Knowledge) ✅
**Configuration**: `.mcp.json`

Shared with Claude Code CLI:

1. **Graph Memory** (`memory`)
   - Storage: `C:\Users\10064957\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-memory\dist\memory.json`
   - Content: 348 entities (Personnel, Projects, Locations, Tasks, Ideas, etc.)
   - Size: 92KB
   - **⚠️ WARNING**: Temporary location - migrate to `.martha/memory.json` (see urgent task in 00_Inbox)

2. **Basic Memory** (`basic-memory`)
   - Storage: `C:\Users\10064957\.basic-memory\` (config) + `C:\Users\10064957\basic-memory\` (files)
   - Content: Markdown files organized by folder (people/, projects/, tasks/, etc.)
   - Database: 2.1MB SQLite

3. **WhatsApp** (`whatsapp`)
   - Server: `C:/whatsapp-mcp/whatsapp-mcp-server`
   - Purpose: Send/receive WhatsApp messages

### Layer 4: Workflows (Manual Execution)
**Location**: `.windsurf/workflows/`

Available slash commands:

1. **`/initialize-windsurf-session`** - Run at session start for full context
2. **`/triage`** - Process all items in 00_Inbox/
3. **`/task [description]`** - Add task to master list
4. **`/quick-note [content]`** - Create quick note in inbox
5. **`/initialize-gemini-session`** - For Gemini-specific production report processing
6. **`/check-for-new-messages-in-gemini-chat`** - Check GEMINI_CHAT.md
7. **`/send-claude-message`** - Send message to Claude via GEMINI_CHAT.md
8. **`/submit-pr-for-review`** - Create PR for Claude Cloud review

## Usage Guide

### Starting a New Session

**Automatic** (no action needed):
1. ✅ Rules load automatically
2. ✅ Memories retrieved based on context
3. ✅ MCP servers connect (verify in UI)

**Manual** (recommended for comprehensive onboarding):
```
/initialize-windsurf-session
```

This workflow:
- Verifies MCP server connections
- Checks pending items in 00_Inbox/
- Reviews master task list
- Scans for @Claude instructions
- Displays critical reminders
- Confirms session readiness

### Daily Workflow

1. **Start session** → Run `/initialize-windsurf-session` (optional but recommended)
2. **Check inbox** → Run `/triage` if items present
3. **Review tasks** → Check `tasks/master_task_list.md`
4. **Process requests** → Handle user requests with full context
5. **Add tasks** → Use `/task [description]` as needed
6. **Draft messages** → Always ask permission before sending WhatsApp

### Memory System Usage

**Quick Entity Lookup** (Graph Memory):
```
Search for "Gregory Karsten" to get personnel info
Search for "BEV Fire Safety" to get project details
```

**Semantic Search** (Basic Memory):
```
Search notes for "capital application procedures"
Build context around "BEV project" with depth 2
```

**Best Practice**: Use both systems in parallel for comprehensive context.

## Comparison with Claude Code CLI

| Feature | Claude Code CLI | Windsurf |
|---------|----------------|----------|
| **Auto-load CLAUDE.md** | ✅ Yes | ✅ Yes (via rules) |
| **Slash commands** | ✅ `.claude/commands/` | ✅ `.windsurf/workflows/` |
| **Agents** | ✅ `.claude/agents/` | ❌ Not directly portable |
| **Graph Memory** | ✅ Shared storage | ✅ Shared storage |
| **Basic Memory** | ✅ Shared storage | ✅ Shared storage |
| **Persistent context** | ✅ Session-based | ✅ Memory-based |
| **Initialization** | ✅ Automatic | ✅ Manual via workflow |

## Critical Reminders

### File Creation
- ❌ NEVER create files unless absolutely necessary
- ✅ ALWAYS prefer editing existing files
- ❌ NEVER proactively create documentation

### WhatsApp Protocol
- ✅ ALWAYS draft messages first
- ✅ ALWAYS ask permission before sending
- ❌ NEVER send without user approval

### Memory Updates
- ✅ Update Graph Memory when new entities/relationships emerge
- ✅ Basic Memory syncs automatically via file watcher
- ✅ Keep master task list synchronized

### Separation of Concerns
- ✅ MarthaVault = Task management, productivity, knowledge
- ✅ ProductionReports = Automation, equipment data, GitHub Actions
- ❌ NEVER mix production automation into MarthaVault

## Troubleshooting

### MCP Servers Not Connected
1. Check `.mcp.json` configuration
2. Restart Windsurf
3. Verify npm package installed: `npx @modelcontextprotocol/server-memory --help`
4. Check Basic Memory config: `C:\Users\10064957\.basic-memory\config.json`

### Rules Not Loading
- Rules load automatically - no action needed
- Check `.windsurf/rules/` directory exists
- Verify markdown files are properly formatted

### Workflows Not Appearing
- Workflows require manual execution via slash commands
- Check `.windsurf/workflows/` directory
- Verify YAML frontmatter has `description` field

### Memory Not Persisting
- **Graph Memory**: Check storage location (see urgent task in 00_Inbox about migration)
- **Basic Memory**: Verify `C:\Users\10064957\.basic-memory\memory.db` exists
- **Cascade Memories**: Automatically managed by Windsurf

## Next Steps

1. ✅ **Urgent**: Migrate Graph Memory to permanent storage (see 00_Inbox reminder)
2. ✅ Test MCP server connections in new session
3. ✅ Run `/initialize-windsurf-session` to verify full context loading
4. ✅ Port additional workflows as needed from `.claude/commands/`

---

**Status**: ✅ Complete - Windsurf context loading system fully operational

**Last Updated**: 2025-10-15  
**Maintained By**: Greg + AI Assistants
