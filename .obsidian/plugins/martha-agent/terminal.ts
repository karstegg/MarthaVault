import { ItemView, WorkspaceLeaf, Notice } from 'obsidian';
import MarthaAgentPlugin from './main';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import * as os from 'os';
import * as path from 'path';
import { ChildProcess } from 'child_process';

// Use child_process instead of node-pty (works in Electron renderer)
const { spawn } = require('child_process');

export const TERMINAL_VIEW_TYPE = 'martha-terminal';

export class TerminalView extends ItemView {
  plugin: MarthaAgentPlugin;
  terminal: Terminal;
  fitAddon: FitAddon;
  childProcess: ChildProcess | null = null;
  vaultPath: string;
  resizeObserver: ResizeObserver | null = null;

  constructor(leaf: WorkspaceLeaf, plugin: MarthaAgentPlugin) {
    super(leaf);
    this.plugin = plugin;
    this.vaultPath = (this.app.vault.adapter as any).basePath;
  }

  getViewType(): string {
    return TERMINAL_VIEW_TYPE;
  }

  getDisplayText(): string {
    return 'Claude Terminal';
  }

  getIcon(): string {
    return 'terminal';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass('martha-terminal-container');

    // Create terminal container div
    const terminalDiv = container.createDiv({ cls: 'xterm-container' });

    // Initialize xterm.js
    this.terminal = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Consolas, "Courier New", monospace',
      theme: {
        background: 'var(--background-primary)',
        foreground: 'var(--text-normal)',
        cursor: 'var(--text-accent)',
        cursorAccent: 'var(--background-primary)',
        selectionBackground: 'var(--text-selection)',
        black: '#000000',
        red: '#e06c75',
        green: '#98c379',
        yellow: '#d19a66',
        blue: '#61afef',
        magenta: '#c678dd',
        cyan: '#56b6c2',
        white: '#abb2bf',
        brightBlack: '#5c6370',
        brightRed: '#e06c75',
        brightGreen: '#98c379',
        brightYellow: '#d19a66',
        brightBlue: '#61afef',
        brightMagenta: '#c678dd',
        brightCyan: '#56b6c2',
        brightWhite: '#ffffff'
      },
      allowProposedApi: true,
      scrollback: 1000,
      convertEol: true
    });

    // Add addons
    this.fitAddon = new FitAddon();
    this.terminal.loadAddon(this.fitAddon);
    this.terminal.loadAddon(new WebLinksAddon());

    // Open terminal in DOM
    this.terminal.open(terminalDiv);
    this.fitAddon.fit();

    // Add resize observer
    this.resizeObserver = new ResizeObserver(() => {
      if (this.fitAddon) {
        this.fitAddon.fit();
      }
    });
    this.resizeObserver.observe(terminalDiv);

    // Load xterm CSS
    this.loadXtermStyles();

    // Spawn Claude CLI process
    await this.spawnClaudeProcess();
  }

  async spawnClaudeProcess() {
    try {
      console.log('[Martha] Spawning Claude CLI process...');
      console.log('[Martha] Vault path:', this.vaultPath);

      // Find claude executable
      const claudePath = await this.findClaudeExecutable();
      if (!claudePath) {
        this.terminal.writeln('\x1b[1;31mError: Claude CLI not found.\x1b[0m');
        this.terminal.writeln('Please install Claude Code: npm install -g @anthropic-ai/claude-code');
        this.terminal.writeln('Or ensure "claude" is in your PATH.');
        return;
      }

      console.log('[Martha] Using Claude executable:', claudePath);

      const isWindows = os.platform() === 'win32';

      // Spawn Claude CLI process directly using child_process
      // Set environment variables to simulate terminal
      this.childProcess = spawn(claudePath, [], {
        cwd: this.vaultPath,
        env: {
          ...process.env,
          TERM: 'xterm-256color',
          COLORTERM: 'truecolor',
          FORCE_COLOR: '1',
          // Set terminal dimensions
          COLUMNS: String(this.terminal.cols),
          LINES: String(this.terminal.rows),
          // Try to force interactive mode
          CLICOLOR_FORCE: '1',
          // Unbuffered output
          PYTHONUNBUFFERED: '1'
        },
        shell: isWindows,
        windowsHide: true,
        // Set stdio to inherit for better interaction
        stdio: ['pipe', 'pipe', 'pipe']
      });

      if (!this.childProcess) {
        throw new Error('Failed to spawn process');
      }

      console.log('[Martha] Claude process spawned with PID:', this.childProcess.pid);

      // Handle stdout -> Terminal
      if (this.childProcess.stdout) {
        this.childProcess.stdout.on('data', (data: Buffer) => {
          this.terminal.write(data.toString());
        });
      }

      // Handle stderr -> Terminal
      if (this.childProcess.stderr) {
        this.childProcess.stderr.on('data', (data: Buffer) => {
          const text = data.toString();
          // Write stderr in default color (Claude CLI uses stderr for normal output too)
          this.terminal.write(text);
        });
      }

      // Handle process exit
      this.childProcess.on('exit', (code: number | null, signal: string | null) => {
        console.log('[Martha] Claude process exited:', { code, signal });
        this.terminal.writeln('');
        this.terminal.writeln('\x1b[1;33mClaude CLI session ended.\x1b[0m');
        if (code !== 0 && code !== null) {
          this.terminal.writeln(`\x1b[1;31mExit code: ${code}\x1b[0m`);
        }
        this.childProcess = null;
      });

      // Handle Terminal input -> stdin
      this.terminal.onData((data: string) => {
        if (this.childProcess && this.childProcess.stdin) {
          this.childProcess.stdin.write(data);
        }
      });

      new Notice('✓ Claude CLI started in vault directory');

    } catch (error: any) {
      console.error('[Martha] Failed to spawn Claude process:', error);
      this.terminal.writeln('\x1b[1;31mError starting Claude CLI:\x1b[0m');
      this.terminal.writeln(error.message);
      this.terminal.writeln('');
      this.terminal.writeln('Troubleshooting:');
      this.terminal.writeln('1. Install Claude Code: npm install -g @anthropic-ai/claude-code');
      this.terminal.writeln('2. Run: claude setup-token');
      this.terminal.writeln('3. Ensure Node.js is installed');
      new Notice('⚠️ Failed to start Claude CLI - see terminal for details');
    }
  }

  async findClaudeExecutable(): Promise<string | null> {
    const isWindows = os.platform() === 'win32';

    // Possible locations
    const possiblePaths = isWindows ? [
      path.join(process.env.APPDATA || '', 'npm', 'claude.cmd'),
      path.join(process.env.USERPROFILE || '', 'AppData', 'Roaming', 'npm', 'claude.cmd'),
      'claude.cmd',
      'claude'
    ] : [
      '/usr/local/bin/claude',
      path.join(process.env.HOME || '', '.npm-global', 'bin', 'claude'),
      path.join(process.env.HOME || '', '.local', 'bin', 'claude'),
      'claude'
    ];

    // Try each path
    for (const cmdPath of possiblePaths) {
      try {
        const { execSync } = require('child_process');
        const testCmd = isWindows
          ? `where ${cmdPath} 2>nul`
          : `which ${cmdPath} 2>/dev/null`;

        const result = execSync(testCmd, { encoding: 'utf8' }).trim();
        if (result) {
          return cmdPath;
        }
      } catch (e) {
        // Try next path
        continue;
      }
    }

    // If all else fails, just try 'claude' and hope it's in PATH
    return 'claude';
  }

  sendToTerminal(text: string) {
    if (this.childProcess && this.childProcess.stdin) {
      const isWindows = os.platform() === 'win32';
      this.childProcess.stdin.write(text + (isWindows ? '\r\n' : '\n'));
    }
  }

  loadXtermStyles() {
    // Check if styles already loaded
    if (document.getElementById('martha-xterm-styles')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'martha-xterm-styles';
    style.textContent = `
      /* xterm.js base styles */
      @import url('https://unpkg.com/xterm@5.3.0/css/xterm.css');

      .martha-terminal-container {
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        background: var(--background-primary);
        padding: 0;
      }

      .xterm-container {
        flex: 1;
        width: 100%;
        height: 100%;
        padding: 12px;
        overflow: hidden;
      }

      .xterm {
        height: 100%;
        width: 100%;
      }

      .xterm .xterm-viewport {
        background-color: transparent !important;
      }

      .xterm .xterm-screen {
        background-color: transparent !important;
      }

      /* Scrollbar styling */
      .xterm .xterm-viewport::-webkit-scrollbar {
        width: 10px;
      }

      .xterm .xterm-viewport::-webkit-scrollbar-track {
        background: var(--background-secondary);
      }

      .xterm .xterm-viewport::-webkit-scrollbar-thumb {
        background: var(--background-modifier-border);
        border-radius: 5px;
      }

      .xterm .xterm-viewport::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
      }

      /* Selection color */
      .xterm .xterm-selection div {
        background-color: var(--text-selection) !important;
      }

      /* Link styling */
      .xterm a {
        color: var(--text-accent);
        text-decoration: underline;
      }

      .xterm a:hover {
        color: var(--text-accent-hover);
      }
    `;
    document.head.appendChild(style);
  }

  async onClose() {
    console.log('[Martha] Closing terminal view...');

    // Cleanup resize observer
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }

    // Kill child process
    if (this.childProcess) {
      try {
        this.childProcess.kill();
      } catch (e) {
        console.error('[Martha] Error killing child process:', e);
      }
      this.childProcess = null;
    }

    // Dispose terminal
    if (this.terminal) {
      this.terminal.dispose();
    }
  }
}
