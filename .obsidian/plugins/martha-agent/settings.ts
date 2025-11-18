import { App, PluginSettingTab, Setting } from 'obsidian';
import MarthaAgentPlugin from './main';

export class MarthaSettingTab extends PluginSettingTab {
  plugin: MarthaAgentPlugin;

  constructor(app: App, plugin: MarthaAgentPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl('h2', { text: 'Martha Agent Settings' });

    containerEl.createEl('p', {
      text: 'This plugin embeds Claude CLI directly inside Obsidian. Make sure Claude Code is installed globally.',
      cls: 'setting-item-description'
    });

    new Setting(containerEl)
      .setName('Terminal position')
      .setDesc('Where to open the Claude terminal panel')
      .addDropdown(dropdown => dropdown
        .addOption('right', 'Right sidebar')
        .addOption('bottom', 'Bottom panel')
        .setValue(this.plugin.settings.terminalPosition)
        .onChange(async (value: 'right' | 'bottom') => {
          this.plugin.settings.terminalPosition = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Font size')
      .setDesc('Terminal font size (requires reopening terminal)')
      .addSlider(slider => slider
        .setLimits(10, 20, 1)
        .setValue(this.plugin.settings.fontSize)
        .setDynamicTooltip()
        .onChange(async (value) => {
          this.plugin.settings.fontSize = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Auto-start Claude')
      .setDesc('Automatically run "claude" command when opening terminal')
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.autoStartClaude)
        .onChange(async (value) => {
          this.plugin.settings.autoStartClaude = value;
          await this.plugin.saveSettings();
        }));

    // Installation instructions
    containerEl.createEl('h3', { text: 'Setup Instructions' });

    const instructions = containerEl.createEl('div', { cls: 'martha-setup-instructions' });

    instructions.createEl('p', { text: '1. Install Claude Code globally:' });
    instructions.createEl('pre', { text: 'npm install -g @anthropic-ai/claude-code' });

    instructions.createEl('p', { text: '2. Set up authentication:' });
    instructions.createEl('pre', { text: 'claude setup-token' });

    instructions.createEl('p', { text: '3. Open terminal in Obsidian:' });
    instructions.createEl('p', { text: 'Use the ribbon icon (terminal) or Command Palette → "Open Claude Terminal"' });

    instructions.createEl('p', { text: '4. The terminal will start in your vault directory with full Claude Code features.' });

    // Add styles
    const style = containerEl.createEl('style');
    style.textContent = `
      .martha-setup-instructions {
        background: var(--background-secondary);
        padding: 16px;
        border-radius: 8px;
        margin-top: 12px;
      }

      .martha-setup-instructions p {
        margin: 8px 0;
      }

      .martha-setup-instructions pre {
        background: var(--background-primary);
        padding: 8px 12px;
        border-radius: 4px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 13px;
        color: var(--text-accent);
        margin: 4px 0 12px 0;
      }
    `;
  }
}
