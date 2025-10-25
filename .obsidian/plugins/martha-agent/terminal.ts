import { ItemView, WorkspaceLeaf } from 'obsidian';
import { spawn, ChildProcess } from 'child_process';
import MarthaAgentPlugin from './main';

export const TERMINAL_VIEW_TYPE = 'martha-terminal';

export class TerminalView extends ItemView {
  plugin: MarthaAgentPlugin;
  terminal: HTMLElement;
  output: HTMLElement;
  input: HTMLInputElement;
  claudeProcess: ChildProcess | null = null;
  vaultPath: string;

  constructor(leaf: WorkspaceLeaf, plugin: MarthaAgentPlugin) {
    super(leaf);
    this.plugin = plugin;
    this.vaultPath = (this.app.vault.adapter as any).basePath;
  }

  getViewType(): string {
    return TERMINAL_VIEW_TYPE;
  }

  getDisplayText(): string {
    return 'Claude CLI';
  }

  getIcon(): string {
    return 'terminal';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass('martha-terminal-container');

    // Create terminal UI
    this.terminal = container.createDiv({ cls: 'martha-terminal' });
    
    // Output area
    this.output = this.terminal.createDiv({ cls: 'terminal-output' });
    
    // Input area
    const inputContainer = this.terminal.createDiv({ cls: 'terminal-input-container' });
    const prompt = inputContainer.createSpan({ cls: 'terminal-prompt', text: '$ ' });
    this.input = inputContainer.createEl('input', { 
      cls: 'terminal-input',
      attr: { type: 'text', placeholder: 'claude "your prompt here"' }
    });

    // Handle input
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        this.executeCommand(this.input.value);
        this.input.value = '';
      }
    });

    // Add styles
    this.addStyles();

    // Welcome message
    this.appendOutput('Claude CLI Terminal - MarthaVault', 'info');
    this.appendOutput(`Vault: ${this.vaultPath}`, 'info');
    this.appendOutput('Type commands like: claude "analyze this file"', 'info');
    this.appendOutput('', 'info');
  }

  executeCommand(command: string) {
    if (!command.trim()) return;

    this.appendOutput(`$ ${command}`, 'command');

    // Parse command to get full path for claude
    let actualCommand = command;
    if (command.startsWith('claude ')) {
      const claudePath = 'C:\\Users\\10064957\\.npm-global\\bin\\claude.cmd';
      actualCommand = command.replace('claude', claudePath);
    }

    // Set environment variables
    const env = {
      ...process.env,
      CLAUDE_CODE_OAUTH_TOKEN: this.plugin.settings.oauthToken,
      PWD: this.vaultPath
    };

    // Execute command
    const proc = spawn(actualCommand, {
      shell: true,
      cwd: this.vaultPath,
      env: env
    });

    // Capture stdout
    proc.stdout.on('data', (data: Buffer) => {
      this.appendOutput(data.toString(), 'stdout');
    });

    // Capture stderr
    proc.stderr.on('data', (data: Buffer) => {
      this.appendOutput(data.toString(), 'stderr');
    });

    // Handle exit
    proc.on('close', (code: number) => {
      if (code !== 0) {
        this.appendOutput(`Process exited with code ${code}`, 'error');
      }
      this.appendOutput('', 'info');
    });

    proc.on('error', (err: Error) => {
      this.appendOutput(`Error: ${err.message}`, 'error');
    });
  }

  appendOutput(text: string, type: 'command' | 'stdout' | 'stderr' | 'error' | 'info' = 'stdout') {
    const line = this.output.createDiv({ cls: `terminal-line terminal-${type}` });
    line.textContent = text;
    
    // Auto-scroll
    this.output.scrollTop = this.output.scrollHeight;
  }

  addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .martha-terminal-container {
        height: 100%;
        display: flex;
        flex-direction: column;
      }

      .martha-terminal {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: var(--background-primary);
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 12px;
        padding: 10px;
      }

      .terminal-output {
        flex: 1;
        overflow-y: auto;
        padding: 5px;
        background: var(--background-secondary);
        border-radius: 4px;
        margin-bottom: 10px;
      }

      .terminal-line {
        padding: 2px 0;
        word-wrap: break-word;
      }

      .terminal-command {
        color: var(--text-accent);
        font-weight: bold;
      }

      .terminal-stdout {
        color: var(--text-normal);
      }

      .terminal-stderr {
        color: var(--text-warning);
      }

      .terminal-error {
        color: var(--text-error);
      }

      .terminal-info {
        color: var(--text-muted);
      }

      .terminal-input-container {
        display: flex;
        align-items: center;
        background: var(--background-secondary);
        padding: 8px;
        border-radius: 4px;
      }

      .terminal-prompt {
        color: var(--text-accent);
        margin-right: 8px;
        font-weight: bold;
      }

      .terminal-input {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: var(--text-normal);
        font-family: inherit;
        font-size: inherit;
      }

      .terminal-input::placeholder {
        color: var(--text-faint);
      }
    `;
    document.head.appendChild(style);
  }

  async onClose() {
    if (this.claudeProcess) {
      this.claudeProcess.kill();
    }
  }
}
