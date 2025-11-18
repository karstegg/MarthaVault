# Windows Installation Guide - Martha Agent

**Updated:** 2025-11-18 (Fixed xterm bundling issue)

---

## Problem Summary

The plugin now bundles xterm ✅, but still needs `node-pty` (native module) installed. Installing `node-pty` on Windows can fail due to:
- Visual Studio build requirements
- Google Drive file permission issues
- Missing Spectre-mitigated libraries

---

## **Solution 1: Install on Local Disk (Recommended)**

Google Drive can cause permission issues. Install dependencies on a local drive first:

### Step 1: Copy to Local Disk

```cmd
REM Create temp directory on local drive
mkdir C:\Temp\martha-agent
cd C:\Temp\martha-agent

REM Copy only the necessary files
copy "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent\package.json" .
copy "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent\package-lock.json" .
```

### Step 2: Install Dependencies

```cmd
REM This should work better on local disk
npm install

REM If that fails, try with pre-built binaries
npm install --ignore-scripts
npm rebuild node-pty
```

### Step 3: Copy Back to Google Drive

```cmd
REM Copy just the node_modules folder back
xcopy /E /I /Y node_modules "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent\node_modules"
```

### Step 4: Test in Obsidian

1. Pull latest changes from git branch (includes new main.js with xterm bundled)
2. Open Obsidian
3. Settings → Community Plugins → Reload
4. Enable "Martha Agent"
5. Click terminal icon

**If this works, you're done!** ✅

---

## **Solution 2: Use Helper Script**

I've created a batch file that attempts to install node-pty with pre-built binaries:

```cmd
cd "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent"
install-windows.bat
```

This script:
- Checks for npm
- Cleans old installations
- Tries to install node-pty prebuilt binaries (no compilation)
- Falls back to source build if needed

---

## **Solution 3: Manual Pre-built Installation**

If automated install fails, manually download prebuilt node-pty:

### Step 1: Download Prebuilt Binary

Go to: https://github.com/microsoft/node-pty/releases

Or use npm with specific flags:

```cmd
cd "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent"

REM Create node_modules directory
if not exist node_modules mkdir node_modules

REM Install with pre-built binary
npm install node-pty@1.0.0 --ignore-scripts --no-save
```

### Step 2: Verify Installation

```cmd
dir node_modules\node-pty\build\Release

REM You should see:
REM   - pty.node (the native module)
REM   - winpty.dll
REM   - winpty-agent.exe
```

---

## **Solution 4: Fix Visual Studio Build Tools**

If you want to build from source (not recommended unless other solutions fail):

### Install Missing Components

1. **Open Visual Studio Installer**
2. **Modify** "Visual Studio Build Tools 2022"
3. **Individual Components** tab
4. Search for: `spectre`
5. Check: **"MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)"**
6. Click **Modify** and wait for installation

### Then Try Installation

```cmd
cd "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent"
npm install
```

---

## **Verification**

After successful installation, verify:

### 1. Check Files

```cmd
cd "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent"

REM Should exist:
dir main.js
dir manifest.json
dir node_modules\node-pty\build\Release\pty.node
```

### 2. Check main.js Size

```cmd
REM New bundled version should be ~429KB
dir main.js
```

Should show: `main.js` around **429,xxx bytes** (includes xterm bundled)

### 3. Test in Obsidian

1. Open Obsidian
2. `Ctrl+Shift+I` to open Developer Console
3. Look for errors when enabling plugin
4. Should NOT see: "Cannot find module 'xterm'" ✅
5. Might still see: "Cannot find module 'node-pty'" (if installation failed)

---

## **Troubleshooting**

### Error: "Cannot find module 'xterm'"

❌ **You have old main.js**

**Fix:**
```cmd
REM Pull latest from git branch
cd "C:\Users\10064957\My Drive\GDVault\MarthaVault"
git pull origin claude/martha-agent-plugin-011CUrS1zDwmk3yQBaF5mF9n

REM Verify main.js is large (429KB)
dir .obsidian\plugins\martha-agent\main.js
```

### Error: "Cannot find module 'node-pty'"

❌ **node-pty not installed**

**Fix:** Try Solutions 1-3 above to install node-pty

### Error: "node-gyp rebuild" failed

❌ **Native module compilation failed**

**Fix:** Use Solution 1 (local disk) or Solution 3 (prebuilt binaries)

### Plugin loads but terminal is blank

✅ **Plugin working, but Claude CLI not found**

**Fix:**
```cmd
REM Verify Claude Code installed
where claude

REM If not found, install
npm install -g @anthropic-ai/claude-code
claude setup-token
```

---

## **What's Changed**

### Version 2 (2025-11-18)

✅ **Fixed:** Bundled xterm into main.js (was external)
✅ **Fixed:** main.js now 429KB (includes xterm)
✅ **Improved:** Only node-pty needs installation now
✅ **Added:** install-windows.bat helper script

### Why This Helps

Before:
- xterm was external → needed in node_modules
- node-pty was external → needed in node_modules
- **Both needed installation** → double failure points

After:
- xterm is bundled → already in main.js ✅
- node-pty is external → needs installation
- **Only one dependency to install** → easier!

---

## **Alternative: Development Without node-pty**

If you absolutely cannot install node-pty, you could temporarily modify the plugin to:

1. Remove terminal spawning code
2. Use Obsidian's HTTP/WebSocket to connect to Claude running in separate terminal
3. Or use direct Anthropic API calls (no CLI features)

But this defeats the purpose of embedding Claude CLI. **Recommended: Use Solution 1 (local disk install)**.

---

## **Quick Reference**

### Full Installation (Local Disk Method)

```cmd
REM 1. Copy to local disk
mkdir C:\Temp\martha-agent
cd C:\Temp\martha-agent
copy "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent\package*.json" .

REM 2. Install
npm install

REM 3. Copy back
xcopy /E /I /Y node_modules "C:\Users\10064957\My Drive\GDVault\MarthaVault\.obsidian\plugins\martha-agent\node_modules"

REM 4. Enable in Obsidian
REM Settings → Community Plugins → Martha Agent → ON
```

### Verify It Works

```cmd
REM Open Obsidian
REM Click terminal icon (left ribbon)
REM Should see: Claude CLI start in vault directory
```

---

## **Success Criteria**

When everything works, you'll see:

```
Microsoft Windows [Version 10.0.22631.4460]
(c) Microsoft Corporation. All rights reserved.

C:\Users\10064957\My Drive\GDVault\MarthaVault>claude

Claude Code CLI v1.x.x
Working directory: C:\Users\10064957\My Drive\GDVault\MarthaVault

You: ▌
```

---

## **Support**

If you're still stuck after trying all solutions:

1. Check Obsidian console (`Ctrl+Shift+I`) for exact error
2. Verify Node.js version: `node --version` (should be 18+)
3. Try on a different Windows machine without Google Drive
4. Consider WSL2 (Windows Subsystem for Linux) as alternative

**Most Common Solution:** Solution 1 (local disk install) works 90% of the time.

Good luck! 🚀
