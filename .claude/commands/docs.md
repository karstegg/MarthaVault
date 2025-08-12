# Claude Code Documentation Command

When the user runs `/docs [topic]`, provide Claude Code documentation on the requested topic.

## Available Topics
- overview: General overview of Claude Code
- quickstart: Getting started guide
- memory: Memory management and CLAUDE.md
- common-workflows: Extended thinking, pasting images, --resume
- ide-integrations: IDE and editor integrations
- mcp: Model Context Protocol
- github-actions: GitHub Actions integration
- sdk: Software Development Kit
- troubleshooting: Common issues and solutions
- third-party-integrations: External tool integrations
- amazon-bedrock: AWS Bedrock integration
- google-vertex-ai: Google Vertex AI integration
- corporate-proxy: Corporate proxy configuration
- llm-gateway: LLM Gateway setup
- devcontainer: Dev container support
- iam: Authentication and permissions
- security: Security considerations
- monitoring-usage: OpenTelemetry monitoring
- costs: Usage and cost management
- cli-reference: Command line reference
- interactive-mode: Keyboard shortcuts and interaction
- slash-commands: Available slash commands
- settings: Settings files and environment variables
- hooks: Event hooks configuration
- terminal-config: Terminal configuration
- sub-agents: Specialized sub-agent usage
- statusline: Status line configuration

## Usage
- `/docs` - Show this help
- `/docs [topic]` - Show documentation for specific topic
- `/docs list` - List all available topics

## Implementation
Read the appropriate markdown file from `.claude-code-docs/docs/[topic].md` and display the content to the user.