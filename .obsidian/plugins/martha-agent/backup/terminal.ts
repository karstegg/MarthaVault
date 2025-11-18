import { ItemView, WorkspaceLeaf } from 'obsidian';
import MarthaAgentPlugin from './main';

export const TERMINAL_VIEW_TYPE = 'martha-terminal';

export class TerminalView extends ItemView {
  plugin: MarthaAgentPlugin;
  terminal: HTMLElement;
  output: HTMLElement;
  input: HTMLInputElement;
  vaultPath: string;
  agentClient: any; // Will be typed when SDK is imported

  constructor(leaf: WorkspaceLeaf, plugin: MarthaAgentPlugin) {
    super(leaf);
    this.plugin = plugin;
    this.vaultPath = (this.app.vault.adapter as any).basePath;
  }

  getViewType(): string {
    return TERMINAL_VIEW_TYPE;
  }

  getDisplayText(): string {
    return 'Claude Agent';
  }

  getIcon(): string {
    return 'bot';
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
    const prompt = inputContainer.createSpan({ cls: 'terminal-prompt', text: '💬 ' });
    this.input = inputContainer.createEl('input', { 
      cls: 'terminal-input',
      attr: { type: 'text', placeholder: 'Ask Claude anything...' }
    });

    // Handle input
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && this.input.value.trim()) {
        this.executePrompt(this.input.value);
        this.input.value = '';
      }
    });

    // Add styles
    this.addStyles();

    // Initialize Agent SDK
    await this.initializeAgent();

    // Welcome message
    this.appendOutput('Claude Agent Terminal - MarthaVault', 'info');
    this.appendOutput(`Vault: ${this.vaultPath}`, 'info');
    this.appendOutput('Agent SDK initializing...', 'info');
  }

  async initializeAgent() {
    try {
      console.log('[Martha Agent] Initializing Agent SDK...');
      
      // TODO: Actually import and initialize Agent SDK
      // const { AgentClient } = require('@anthropic-ai/claude-agent-sdk');
      // this.agentClient = new AgentClient({
      //   systemPrompt: `You are Martha, Greg's vault assistant for ${this.vaultPath}`,
      //   workingDirectory: this.vaultPath
      // });
      
      // For now, placeholder
      this.appendOutput('✓ Agent ready (SDK pending installation)', 'info');
      this.appendOutput('', 'info');
      
    } catch (error) {
      console.error('[Martha Agent] Failed to initialize:', error);
      this.appendOutput(`Error initializing Agent SDK: ${error.message}`, 'error');
      this.appendOutput('Install: npm install @anthropic-ai/claude-agent-sdk', 'info');
    }
  }

  async executePrompt(prompt: string) {
    console.log('[Martha Agent] Executing prompt:', prompt);
    this.appendOutput(`You: ${prompt}`, 'user');
    this.appendOutput('Claude: Thinking...', 'thinking');

    try {
      // TODO: Use actual Agent SDK
      // const response = await this.agentClient.query(prompt);
      // this.replaceLastOutput(response.text, 'assistant');
      
      // Placeholder - show what will happen
      this.replaceLastOutput(
        'Agent SDK not yet installed. This will use Claude Agent SDK to:\n' +
        '1. Process your prompt\n' +
        '2. Use MCP servers (Graph/Basic Memory)\n' +
        '3. Access vault files\n' +
        '4. Return intelligent responses\n\n' +
        `Your prompt was: "${prompt}"`,
        'assistant'
      );
      
    } catch (error) {
      console.error('[Martha Agent] Query error:', error);
      this.replaceLastOutput(`Error: ${error.message}`, 'error');
    }

    this.appendOutput('', 'info');
  }

  appendOutput(text: string, type: 'user' | 'assistant' | 'thinking' | 'error' | 'info' = 'info') {
    const line = this.output.createDiv({ cls: `terminal-line terminal-${type}` });
    line.textContent = text;
    this.output.scrollTop = this.output.scrollHeight;
  }

  replaceLastOutput(text: string, type: string) {
    const lines = this.output.querySelectorAll('.terminal-line');
    if (lines.length > 0) {
      const lastLine = lines[lines.length - 1] as HTMLElement;
      lastLine.textContent = text;
      lastLine.className = `terminal-line terminal-${type}`;
    }
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
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 14px;
        padding: 16px;
      }

      .terminal-output {
        flex: 1;
        overflow-y: auto;
        padding: 12px;
        background: var(--background-secondary);
        border-radius: 8px;
        margin-bottom: 12px;
      }

      .terminal-line {
        padding: 6px 0;
        line-height: 1.5;
        word-wrap: break-word;
        white-space: pre-wrap;
      }

      .terminal-user {
        color: var(--text-accent);
        font-weight: 500;
      }

      .terminal-assistant {
        color: var(--text-normal);
        padding-left: 12px;
        border-left: 3px solid var(--interactive-accent);
      }

      .terminal-thinking {
        color: var(--text-muted);
        font-style: italic;
      }

      .terminal-error {
        color: var(--text-error);
        background: var(--background-modifier-error);
        padding: 8px;
        border-radius: 4px;
      }

      .terminal-info {
        color: var(--text-muted);
        font-size: 12px;
      }

      .terminal-input-container {
        display: flex;
        align-items: center;
        background: var(--background-secondary);
        padding: 12px;
        border-radius: 8px;
        border: 2px solid transparent;
        transition: border-color 0.2s;
      }

      .terminal-input-container:focus-within {
        border-color: var(--interactive-accent);
      }

      .terminal-prompt {
        font-size: 18px;
        margin-right: 8px;
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
    // Cleanup if needed
  }
}
