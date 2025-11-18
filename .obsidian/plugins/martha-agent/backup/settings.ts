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

    new Setting(containerEl)
      .setName('OAuth Token')
      .setDesc('Long-lived Claude Code OAuth token (from claude setup-token)')
      .addText(text => text
        .setPlaceholder('sk-ant-oat01-...')
        .setValue(this.plugin.settings.oauthToken)
        .onChange(async (value) => {
          this.plugin.settings.oauthToken = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Auto-process inbox')
      .setDesc('Automatically process files when added to 00_Inbox/')
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.autoProcess)
        .onChange(async (value) => {
          this.plugin.settings.autoProcess = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Graph Memory Path')
      .setDesc('Path to Graph Memory MCP storage')
      .addText(text => text
        .setValue(this.plugin.settings.mcpGraphMemory)
        .onChange(async (value) => {
          this.plugin.settings.mcpGraphMemory = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Basic Memory Path')
      .setDesc('Path to Basic Memory MCP storage')
      .addText(text => text
        .setValue(this.plugin.settings.mcpBasicMemory)
        .onChange(async (value) => {
          this.plugin.settings.mcpBasicMemory = value;
          await this.plugin.saveSettings();
        }));
  }
}
