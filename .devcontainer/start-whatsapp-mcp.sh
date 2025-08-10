#!/bin/bash
# WhatsApp MCP Server Startup Script
# Ensures the server is always running in background

set -e

echo "🚀 Starting WhatsApp MCP Server..."

# Change to MCP server directory
cd /workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge

# Check if server is already running
if pgrep -f "whatsapp-mcp" > /dev/null; then
    echo "✅ WhatsApp MCP server is already running"
    exit 0
fi

# Start the server in background with nohup
echo "📱 Launching WhatsApp MCP server in background..."
nohup python -m whatsapp_mcp.server > /tmp/whatsapp-mcp.log 2>&1 &

# Store the PID
echo $! > /tmp/whatsapp-mcp.pid

# Wait a moment for startup
sleep 3

# Verify it's running
if pgrep -f "whatsapp-mcp" > /dev/null; then
    echo "✅ WhatsApp MCP server started successfully (PID: $(cat /tmp/whatsapp-mcp.pid))"
    echo "📋 Log file: /tmp/whatsapp-mcp.log"
    echo "🔧 To stop: kill $(cat /tmp/whatsapp-mcp.pid)"
else
    echo "❌ Failed to start WhatsApp MCP server"
    echo "📋 Check log: cat /tmp/whatsapp-mcp.log"
    exit 1
fi