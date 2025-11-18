# Martha Agent - Claude CLI Inside Obsidian

**Embed Claude Code CLI directly inside your Obsidian vault.**

Version: 0.1.0
Status: ✅ Ready for Testing

---

## What Is This?

Martha Agent is an Obsidian plugin that runs the **actual Claude CLI** inside Obsidian, giving you a full terminal interface with:

- ✅ **Claude Code CLI** - The real thing, not a custom integration
- ✅ **Vault Context** - Terminal starts in your vault directory
- ✅ **All Features** - MCP servers, hooks, skills, everything works
- ✅ **Native Terminal** - Full xterm.js terminal with color support
- ✅ **Seamless UX** - Works like VS Code's integrated terminal

---

## Quick Start

### 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude setup-token
```

### 2. Build Plugin

```bash
cd ".obsidian/plugins/martha-agent"
npm install
npm run build
```

### 3. Enable in Obsidian

1. Settings → Community Plugins → Disable Safe Mode
2. Reload plugin list
3. Enable "Martha Agent"

### 4. Open Terminal

- Click **terminal icon** in ribbon (left sidebar)
- Or use Command Palette: **"Open Claude Terminal"**

You should see Claude CLI start automatically in your vault directory!

---

## Features

### Terminal Interface

Full xterm.js terminal with:
- Color support (ANSI 256-color)
- Clickable links
- Text selection & copy/paste
- Scrollback buffer (1000 lines)
- Automatic resizing

### Claude Code Integration

Since this runs the real Claude CLI:
- All slash commands work (`/task`, `/triage`, etc.)
- MCP servers load from `.mcp.json`
- Hooks and skills work as expected
- Memory systems active (Graph/Basic)
- Full file access to vault

### Convenience Commands

**Send current file to Claude:**
- Command: "Send current file to Claude"
- Sends: `Read and summarize <filename>`

**Ask Claude about selection:**
- Select text in editor
- Command: "Ask Claude about selection"
- Sends selected text to Claude

### Settings

- **Terminal Position**: Right sidebar or bottom panel
- **Font Size**: Adjustable (10-20px)
- **Auto-start**: Automatically run `claude` on terminal open

---

## Architecture

```
Obsidian Plugin
  ↓
xterm.js Terminal (UI)
  ↓
node-pty (PTY process)
  ↓
Shell (cmd.exe / bash)
  ↓
claude CLI
  ↓
• Claude API
• MCP Servers (Graph/Basic Memory)
• Hooks & Skills
• Vault files
```

**Key Insight:** By setting `cwd` to vault path, Claude automatically has context of all vault files.

---

## Why This Approach?

### vs. Windows Terminal

| Feature | Windows Terminal | Martha Agent |
|---------|-----------------|--------------|
| **Context** | Manual (you tell Claude where vault is) | Automatic (always in vault) |
| **Integration** | None (separate window) | Native (inside Obsidian) |
| **Workflow** | Switch windows, copy-paste | Seamless, in-app |
| **Commands** | Manual | Can trigger from UI |

### vs. Custom Agent SDK Integration

| Feature | Custom Integration | Martha Agent |
|---------|-------------------|--------------|
| **Complexity** | High (20-40 hours) | Low (5-10 hours) |
| **Maintenance** | You maintain custom code | Claude Code auto-updates |
| **Features** | Reimplement everything | Everything works out-of-box |
| **Reliability** | Custom code bugs | Battle-tested CLI |

---

## Usage Examples

### Basic Interaction

```
> claude

Claude Code v1.0
Working directory: /path/to/vault

You: what files are in 00_inbox?

Claude: I found 3 files in 00_inbox/:
- 2025-11-06 - Meeting notes.md
- 2025-11-05 - BEV update.md
...
```

### Using Slash Commands

```
You: /triage

Claude: Processing inbox files...
✓ Moved 2025-11-06 - Meeting notes.md to projects/BEV/
✓ Applied tags: #meeting #BEV #priority/high
...
```

### Context-Aware Queries

```
You: summarize recent BEV discussions

Claude: Based on files in projects/BEV/ and recent memory:
- Fire safety is Q4 critical priority (2.0x weight)
- Contract extension approved through Oct 2025
- Charger procurement task due this week
...
```

### File Operations

```
You: create a task for following up with Sipho about GES recruitment

Claude: I'll create a task file...
Created: tasks/2025-11-06 - Follow up Sipho GES.md
Added to master_task_list.md
```

---

## Technical Details

### Dependencies

- **xterm** (5.3.0): Terminal emulator
- **xterm-addon-fit**: Auto-resize terminal
- **xterm-addon-web-links**: Clickable links
- **node-pty** (1.0.0): PTY process spawning

### Platform Support

- ✅ **Windows**: Uses cmd.exe + claude.cmd
- ✅ **macOS**: Uses bash/zsh + claude
- ✅ **Linux**: Uses bash + claude

### Claude Executable Detection

Plugin searches for `claude` in:

**Windows:**
- `%APPDATA%\npm\claude.cmd`
- `%USERPROFILE%\AppData\Roaming\npm\claude.cmd`
- System PATH

**macOS/Linux:**
- `/usr/local/bin/claude`
- `~/.npm-global/bin/claude`
- `~/.local/bin/claude`
- System PATH

---

## Troubleshooting

### "Claude CLI not found"

**Solution:**
```bash
npm install -g @anthropic-ai/claude-code
# Verify installation
which claude  # macOS/Linux
where claude  # Windows
```

### "Authentication failed"

**Solution:**
```bash
claude setup-token
# Follow prompts to get OAuth token
```

### Terminal doesn't open

**Solution:**
1. Check console (Ctrl+Shift+I in Obsidian)
2. Look for `[Martha]` log messages
3. Verify plugin is enabled
4. Try rebuilding: `npm run build`

### Claude starts but vault path wrong

**Solution:**
Plugin uses `this.app.vault.adapter.basePath` - this should auto-detect vault path. If incorrect, check Obsidian installation.

### Terminal is blank/frozen

**Solution:**
1. Close terminal view
2. Reopen using ribbon icon
3. If persists, reload Obsidian (Ctrl+R)

---

## Development

### File Structure

```
martha-agent/
├── main.ts          # Plugin entry point
├── terminal.ts      # Terminal view (xterm + pty)
├── settings.ts      # Settings UI
├── package.json     # Dependencies
├── tsconfig.json    # TypeScript config
├── esbuild.config.mjs # Build config
└── manifest.json    # Plugin metadata
```

### Build Commands

```bash
# Development (watch mode)
npm run dev

# Production build
npm run build
```

### Debugging

Enable developer console in Obsidian:
- `Ctrl+Shift+I` (Windows/Linux)
- `Cmd+Option+I` (macOS)

Look for `[Martha]` prefix in console logs.

---

## Future Enhancements

### Planned Features

- [ ] Multiple terminal tabs
- [ ] Custom themes
- [ ] Terminal history persistence
- [ ] Keyboard shortcuts
- [ ] Context menu integration (right-click → Send to Claude)
- [ ] Auto-triage on file creation (vault event hooks)

### Potential Additions

- Terminal session save/restore
- Custom commands palette
- Integration with Obsidian Daily Notes
- Proactive briefings (morning routine)

---

## Credits

**Author:** Greg Karsten
**License:** MIT
**Technologies:**
- [Obsidian](https://obsidian.md) - Knowledge base platform
- [Claude Code](https://www.anthropic.com/claude/code) - AI coding assistant
- [xterm.js](https://xtermjs.org) - Terminal emulator
- [node-pty](https://github.com/microsoft/node-pty) - PTY process wrapper

---

## Support

**Issues:** Report bugs or feature requests in plugin settings or vault documentation

**Prerequisites:**
- Node.js 18+
- Claude Code CLI installed globally
- Valid Claude Code subscription

**Compatibility:**
- Obsidian 1.4.0+
- Desktop only (uses Node.js APIs)

---

**Ready to use Claude Code inside your vault? Open the terminal and start chatting! 🚀**
