import { Plugin, Notice, WorkspaceLeaf } from 'obsidian';
import { MarthaSettingTab } from './settings';
import { TerminalView, TERMINAL_VIEW_TYPE } from './terminal';

// Plugin settings interface
interface MarthaSettings {
  terminalPosition: 'right' | 'bottom';
  fontSize: number;
  autoStartClaude: boolean;
}

const DEFAULT_SETTINGS: MarthaSettings = {
  terminalPosition: 'right',
  fontSize: 14,
  autoStartClaude: true
};

export default class MarthaAgentPlugin extends Plugin {
  settings: MarthaSettings;

  async onload() {
    console.log('Loading Martha Agent plugin');

    // Load settings
    await this.loadSettings();

    // Register terminal view
    this.registerView(
      TERMINAL_VIEW_TYPE,
      (leaf) => new TerminalView(leaf, this)
    );

    // Add ribbon icon
    this.addRibbonIcon('terminal', 'Open Claude Terminal', () => {
      this.activateTerminal();
    });

    // Add command to open terminal
    this.addCommand({
      id: 'open-terminal',
      name: 'Open Claude Terminal',
      callback: () => this.activateTerminal()
    });

    // Add command to send current file path to Claude
    this.addCommand({
      id: 'send-file-to-claude',
      name: 'Send current file to Claude',
      callback: () => this.sendCurrentFileToClaude()
    });

    // Add command to send selected text to Claude
    this.addCommand({
      id: 'send-selection-to-claude',
      name: 'Ask Claude about selection',
      editorCallback: (editor) => {
        const selection = editor.getSelection();
        if (selection) {
          this.sendTextToClaude(`Explain this:\n\n${selection}`);
        } else {
          new Notice('No text selected');
        }
      }
    });

    // Add settings tab
    this.addSettingTab(new MarthaSettingTab(this.app, this));

    console.log('Martha Agent plugin loaded successfully');
  }

  async sendCurrentFileToClaude() {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) {
      new Notice('No active file');
      return;
    }

    // Activate terminal and send command
    await this.activateTerminal();
    this.sendTextToClaude(`Read and summarize ${activeFile.path}`);
  }

  async sendTextToClaude(text: string) {
    // Find or create terminal view
    const leaves = this.app.workspace.getLeavesOfType(TERMINAL_VIEW_TYPE);

    if (leaves.length === 0) {
      // Terminal not open, activate it first
      await this.activateTerminal();
      // Wait for terminal to initialize
      setTimeout(() => {
        const newLeaves = this.app.workspace.getLeavesOfType(TERMINAL_VIEW_TYPE);
        if (newLeaves.length > 0) {
          const view = newLeaves[0].view as TerminalView;
          view.sendToTerminal(text);
        }
      }, 1000);
    } else {
      const view = leaves[0].view as TerminalView;
      view.sendToTerminal(text);
    }
  }

  async activateTerminal() {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(TERMINAL_VIEW_TYPE);

    if (leaves.length > 0) {
      // Terminal already exists, just reveal it
      leaf = leaves[0];
    } else {
      // Create new terminal
      if (this.settings.terminalPosition === 'right') {
        leaf = workspace.getRightLeaf(false);
      } else {
        leaf = workspace.getLeaf('split', 'horizontal');
      }

      if (leaf) {
        await leaf.setViewState({ type: TERMINAL_VIEW_TYPE, active: true });
      }
    }

    if (leaf) {
      workspace.revealLeaf(leaf);
    }
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  onunload() {
    console.log('Unloading Martha Agent plugin');
  }
}
