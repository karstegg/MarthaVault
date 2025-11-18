# Martha Agent - Installation Guide

**Quick installation guide for embedding Claude CLI inside Obsidian.**

---

## Prerequisites

- ✅ **Node.js 18+** installed
- ✅ **Claude Code subscription** (Pro/Max tier)
- ✅ **Obsidian Desktop** (1.4.0+)

---

## Step 1: Install Claude Code Globally

```bash
npm install -g @anthropic-ai/claude-code
```

Verify installation:

```bash
# Windows
where claude

# macOS/Linux
which claude
```

You should see the path to the claude executable.

---

## Step 2: Set Up Authentication

```bash
claude setup-token
```

This will:
1. Open browser for OAuth login
2. Generate long-lived token
3. Store token globally

Test it works:

```bash
cd /path/to/your/vault
claude
```

You should see Claude CLI start successfully.

---

## Step 3: Build Plugin

Navigate to plugin directory:

```bash
# Windows
cd "C:\Users\YOUR_USERNAME\path\to\vault\.obsidian\plugins\martha-agent"

# macOS/Linux
cd "/path/to/vault/.obsidian/plugins/martha-agent"
```

Install dependencies:

```bash
npm install
```

Build the plugin:

```bash
npm run build
```

You should see:
```
✓ Typescript check passed
✓ Build succeeded
main.js created
```

---

## Step 4: Enable in Obsidian

1. **Open Obsidian Settings** (gear icon)
2. **Community Plugins** → Click **"Turn on community plugins"** (if needed)
3. **Reload plugin list** (refresh icon)
4. Find **"Martha Agent"** in the list
5. **Toggle ON** the switch

You should see: "Martha Agent plugin loaded successfully" in console.

---

## Step 5: Open Terminal

**Method 1: Ribbon Icon**
- Look for **terminal icon** in left sidebar
- Click to open Claude terminal

**Method 2: Command Palette**
- Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (macOS)
- Type: "Open Claude Terminal"
- Press Enter

**Method 3: Settings**
- Settings → Martha Agent
- Adjust terminal position/font size
- Instructions are shown

---

## Step 6: Test It Works

You should see:

```
Microsoft Windows [Version ...]
(c) Microsoft Corporation. All rights reserved.

C:\path\to\vault> claude

Claude Code v1.x
Working directory: C:\path\to\vault

You: ▌
```

Type a test prompt:

```
You: what files are in this directory?

Claude: I can see your vault files...
[Claude lists files]
```

**Success!** Claude is running inside Obsidian with full vault context.

---

## Configuration

### Settings → Martha Agent

**Terminal Position:**
- Right sidebar (default)
- Bottom panel

**Font Size:**
- 10-20px (default: 14px)

**Auto-start Claude:**
- ON: Automatically runs `claude` when opening terminal
- OFF: Opens shell only (you type `claude` manually)

---

## Troubleshooting

### "Claude CLI not found"

**Symptom:** Terminal shows error message about missing Claude.

**Fix:**
1. Verify Claude is installed: `npm list -g @anthropic-ai/claude-code`
2. If not installed: `npm install -g @anthropic-ai/claude-code`
3. Add npm global bin to PATH:
   - Windows: `%APPDATA%\npm`
   - macOS/Linux: `~/.npm-global/bin`

---

### "Build fails" / "npm install errors"

**Symptom:** `npm install` or `npm run build` fails.

**Fix:**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Or force clean
npm cache clean --force
npm install
```

---

### "Plugin doesn't appear in Obsidian"

**Symptom:** Can't find "Martha Agent" in plugin list.

**Fix:**
1. Verify files exist: `.obsidian/plugins/martha-agent/manifest.json`
2. Check `manifest.json` is valid JSON
3. Ensure `main.js` exists (run `npm run build`)
4. Reload Obsidian: `Ctrl+R` or restart app

---

### "Terminal is blank"

**Symptom:** Terminal opens but nothing appears.

**Fix:**
1. Open Obsidian Developer Console: `Ctrl+Shift+I`
2. Look for errors with `[Martha]` prefix
3. Check if `node-pty` installed: `npm list node-pty`
4. Verify Node.js version: `node --version` (must be 18+)

---

### "Authentication failed" in terminal

**Symptom:** Claude says "Authentication error" or "Invalid token".

**Fix:**
```bash
# Re-authenticate
claude setup-token

# Or logout and login again
claude logout
claude login
```

---

### "Working directory is wrong"

**Symptom:** Claude shows wrong directory (not vault path).

**Fix:**
1. Check console for: `[Martha] Vault path: ...`
2. Path should match your vault location
3. If wrong, this is an Obsidian API issue - report in plugin settings

---

## Uninstall

### Remove Plugin

1. Obsidian Settings → Community Plugins
2. Find "Martha Agent"
3. Click X to disable
4. Delete folder: `.obsidian/plugins/martha-agent/`

### Keep Claude Code

Claude CLI remains installed globally for use in terminal.

### Uninstall Claude Code

```bash
npm uninstall -g @anthropic-ai/claude-code
```

---

## Development Mode

### Watch Mode (Auto-rebuild)

```bash
cd .obsidian/plugins/martha-agent
npm run dev
```

- Changes to `.ts` files auto-rebuild
- Reload Obsidian to see changes: `Ctrl+R`

### Debug Logging

Check Obsidian Developer Console (`Ctrl+Shift+I`):

```
[Martha] Loading plugin...
[Martha] Vault path: C:\path\to\vault
[Martha] Spawning Claude CLI process...
[Martha] PTY process spawned with PID: 12345
[Martha] Starting Claude CLI...
```

### Type Checking

```bash
# Check types without building
npx tsc --noEmit
```

---

## Next Steps

Once installed and working:

1. **Test slash commands**: `/triage`, `/task`, etc.
2. **Check MCP servers**: Memory systems should load from `.mcp.json`
3. **Try convenience commands**: "Send current file to Claude"
4. **Customize settings**: Adjust terminal position/font

**Enjoy Claude Code embedded in your vault! 🎉**
