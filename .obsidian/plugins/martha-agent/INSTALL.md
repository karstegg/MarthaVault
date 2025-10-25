# Martha Agent - Installation Guide

## Prerequisites

1. **Node.js 18+** installed
2. **Claude Code subscription** (Pro/Max)
3. **OAuth token generated**

## Step 1: Generate OAuth Token

```bash
npm install -g @anthropic-ai/claude-code
claude setup-token
```

Copy the token that starts with `sk-ant-oat01-...`

## Step 2: Build Plugin

```bash
cd "C:/Users/10064957/My Drive/GDVault/MarthaVault/.obsidian/plugins/martha-agent"
npm install
npm run build
```

## Step 3: Enable in Obsidian

1. Open Obsidian Settings
2. Community Plugins → Disable Safe Mode
3. Reload plugins list
4. Find "Martha Agent"
5. Toggle ON

## Step 4: Configure

1. Settings → Martha Agent
2. Paste OAuth token
3. Verify MCP paths:
   - Graph: `C:/Users/10064957/.martha/memory.json`
   - Basic: `C:/Users/10064957/.basic-memory/`
4. Toggle auto-process if desired

## Step 5: Test

Run command: `Process current file with Martha`

Check console for: "Martha Agent initialized with OAuth"

## Troubleshooting

**"OAuth token not configured"**
→ Add token in settings

**"npm not found"**
→ Install Node.js

**Build fails**
→ `rm -rf node_modules && npm install`

**Agent not responding**
→ Check console (Ctrl+Shift+I)

## Next Steps

Once working, implement actual Agent SDK integration:
1. Wire up agent client
2. Connect MCP servers
3. Add Skills support
4. Test file processing
