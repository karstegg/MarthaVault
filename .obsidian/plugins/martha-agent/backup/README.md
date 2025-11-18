# Martha Agent - Obsidian Plugin Prototype

**Status:** Prototype v0.1.0

## Quick Start

```bash
cd "C:/Users/10064957/My Drive/GDVault/MarthaVault/.obsidian/plugins/martha-agent"
npm install
npm run build
```

Then enable in Obsidian Settings → Community Plugins.

## What's Built

✅ Plugin structure (TypeScript)  
✅ Commands: Process file, Process inbox  
✅ File watching (00_Inbox/)  
✅ Settings framework  
⏳ Agent SDK (requires npm install)  
⏳ MCP connections  
⏳ Skills integration

## Next Steps

1. Install Agent SDK: `npm install @anthropic-ai/claude-agent-sdk`
2. Add API key in settings
3. Wire up agent client in `initializeAgent()`
4. Connect MCP servers
5. Test with inbox processing

## Commands

- Process current file with Martha
- Process inbox folder

## Architecture

```
Obsidian → Agent SDK → Claude API
                     → MCPs (Graph/Basic Memory)
                     → Skills
```

Ready for development.
