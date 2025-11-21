import { ItemView, WorkspaceLeaf, Notice } from 'obsidian';
import MarthaAgentPlugin from './main';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import * as os from 'os';
import * as path from 'path';

// Load node-pty dynamically with absolute path to work around Obsidian's module resolution
// Import types for TypeScript
import type * as ptyTypes from 'node-pty';

const loadNodePty = (pluginDir: string): typeof ptyTypes => {
  try {
    // Try loading from plugin's node_modules with absolute path
    const ptyPath = path.join(pluginDir, 'node_modules', 'node-pty');
    console.log('[Martha] Attempting to load node-pty from:', ptyPath);
    return require(ptyPath);
  } catch (e) {
    console.error('[Martha] Failed to load node-pty:', e);
    // Fallback to normal require (will probably fail but worth trying)
    return require('node-pty');
  }
};

export const TERMINAL_VIEW_TYPE = 'martha-terminal';

export class TerminalView extends ItemView {
  plugin: MarthaAgentPlugin;
  terminal: Terminal;
  fitAddon: FitAddon;
  ptyProcess: ptyTypes.IPty | null = null;
  pty: typeof ptyTypes | null = null;
  vaultPath: string;
  pluginDir: string;
  resizeObserver: ResizeObserver | null = null;

  constructor(leaf: WorkspaceLeaf, plugin: MarthaAgentPlugin) {
    super(leaf);
    this.plugin = plugin;
    this.vaultPath = (this.app.vault.adapter as any).basePath;
    // Calculate plugin directory from vault path
    this.pluginDir = path.join(this.vaultPath, '.obsidian', 'plugins', 'martha-agent');
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
        if (this.ptyProcess) {
          this.ptyProcess.resize(this.terminal.cols, this.terminal.rows);
        }
      }
    });
    this.resizeObserver.observe(terminalDiv);

    // Load xterm CSS
    this.loadXtermStyles();

    // Load node-pty module with correct plugin directory
    this.pty = loadNodePty(this.pluginDir);
    if (!this.pty) {
      this.terminal.writeln('\x1b[1;31mError: Failed to load node-pty module.\x1b[0m');
      this.terminal.writeln('Please check that node_modules/node-pty is installed.');
      return;
    }

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

      // Determine shell
      const shell = os.platform() === 'win32' ? 'cmd.exe' : process.env.SHELL || '/bin/bash';
      const isWindows = os.platform() === 'win32';

      // Spawn PTY process
      this.ptyProcess = this.pty!.spawn(shell, [], {
        name: 'xterm-256color',
        cols: this.terminal.cols,
        rows: this.terminal.rows,
        cwd: this.vaultPath,
        env: {
          ...process.env,
          TERM: 'xterm-256color',
          COLORTERM: 'truecolor'
        }
      });

      console.log('[Martha] PTY process spawned with PID:', this.ptyProcess.pid);

      // Handle PTY data -> Terminal
      this.ptyProcess.onData((data: string) => {
        this.terminal.write(data);
      });

      // Handle PTY exit
      this.ptyProcess.onExit(({ exitCode, signal }: { exitCode: number; signal?: number }) => {
        console.log('[Martha] PTY process exited:', { exitCode, signal });
        this.terminal.writeln('');
        this.terminal.writeln('\x1b[1;33mClaude CLI session ended.\x1b[0m');
        this.ptyProcess = null;
      });

      // Handle Terminal input -> PTY
      this.terminal.onData((data: string) => {
        if (this.ptyProcess) {
          this.ptyProcess.write(data);
        }
      });

      // Wait a moment for shell to initialize
      await new Promise(resolve => setTimeout(resolve, 500));

      // Start Claude CLI
      console.log('[Martha] Starting Claude CLI...');
      if (isWindows) {
        this.ptyProcess.write('claude\r');
      } else {
        this.ptyProcess.write('claude\n');
      }

      new Notice('✓ Claude CLI started in vault directory');

    } catch (error) {
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
    if (this.ptyProcess) {
      const isWindows = os.platform() === 'win32';
      this.ptyProcess.write(text + (isWindows ? '\r' : '\n'));
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

    // Kill PTY process
    if (this.ptyProcess) {
      try {
        this.ptyProcess.kill();
      } catch (e) {
        console.error('[Martha] Error killing PTY process:', e);
      }
      this.ptyProcess = null;
    }

    // Dispose terminal
    if (this.terminal) {
      this.terminal.dispose();
    }
  }
}
