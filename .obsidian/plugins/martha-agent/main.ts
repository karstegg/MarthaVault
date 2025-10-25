import { Plugin, TFile, Notice } from 'obsidian';

// Plugin settings interface
interface MarthaSettings {
  apiKey: string;
  autoProcess: boolean;
  mcpGraphMemory: string;
  mcpBasicMemory: string;
}

const DEFAULT_SETTINGS: MarthaSettings = {
  apiKey: '',
  autoProcess: false,
  mcpGraphMemory: 'C:/Users/10064957/.martha/memory.json',
  mcpBasicMemory: 'C:/Users/10064957/.basic-memory/'
};

export default class MarthaAgentPlugin extends Plugin {
  settings: MarthaSettings;
  agentClient: any; // Will be ClaudeAgentClient from SDK

  async onload() {
    console.log('Loading Martha Agent plugin');

    // Load settings
    await this.loadSettings();

    // Add ribbon icon
    this.addRibbonIcon('bot', 'Martha Agent', () => {
      new Notice('Martha Agent is running');
    });

    // Add command to process current file
    this.addCommand({
      id: 'process-current-file',
      name: 'Process current file with Martha',
      callback: () => this.processCurrentFile()
    });

    // Add command to process inbox
    this.addCommand({
      id: 'process-inbox',
      name: 'Process inbox folder',
      callback: () => this.processInbox()
    });

    // Watch vault changes if auto-process enabled
    if (this.settings.autoProcess) {
      this.registerEvent(
        this.app.vault.on('modify', (file) => this.onFileModified(file))
      );
    }

    // Initialize Agent SDK (placeholder - needs actual SDK installation)
    await this.initializeAgent();
  }

  async initializeAgent() {
    if (!this.settings.apiKey) {
      new Notice('⚠️ Martha Agent: API key not configured');
      return;
    }

    // TODO: Initialize actual Agent SDK
    // This requires: npm install @anthropic-ai/claude-agent-sdk
    console.log('Martha Agent: Ready to initialize SDK');
    new Notice('Martha Agent initialized');
  }

  async processCurrentFile() {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) {
      new Notice('No active file');
      return;
    }

    new Notice(`Processing: ${activeFile.name}`);
    
    // TODO: Send to Agent SDK for processing
    const content = await this.app.vault.read(activeFile);
    console.log('File content loaded:', content.substring(0, 100));
    
    // Placeholder for agent processing
    new Notice('✓ File processed');
  }

  async processInbox() {
    const inboxFolder = '00_Inbox';
    const files = this.app.vault.getMarkdownFiles()
      .filter(f => f.path.startsWith(inboxFolder));

    new Notice(`Processing ${files.length} inbox files...`);
    
    for (const file of files) {
      console.log('Processing:', file.path);
      // TODO: Agent SDK processing logic
    }

    new Notice('✓ Inbox processed');
  }

  async onFileModified(file: TFile) {
    // Only auto-process files in 00_Inbox
    if (!file.path.startsWith('00_Inbox/')) return;
    
    console.log('Auto-processing modified file:', file.path);
    // TODO: Queue for agent processing
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
