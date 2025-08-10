#!/bin/bash
# WhatsApp MCP Server Restart Script

set -e

echo "🔄 Restarting WhatsApp MCP Server..."

# Stop the server
/workspaces/MarthaVault/.devcontainer/stop-whatsapp-mcp.sh

# Wait a moment
sleep 2

# Start the server
/workspaces/MarthaVault/.devcontainer/start-whatsapp-mcp.sh

echo "✅ WhatsApp MCP server restarted successfully"