#!/bin/bash
# Autonomous System Startup Script for Codespace
# Starts WhatsApp MCP server and autonomous webhook listener

echo "🚀 Starting Autonomous WhatsApp Processing System..."

# Ensure we're in the right directory
cd /workspaces/MarthaVault

# Check if WhatsApp MCP server is running
echo "🔍 Checking WhatsApp MCP server status..."

# Start WhatsApp MCP server if not running
if ! pgrep -f "whatsapp-mcp" > /dev/null; then
    echo "📱 Starting WhatsApp MCP server..."
    cd /whatsapp-mcp/whatsapp-mcp-server
    nohup uv run main.py > /tmp/whatsapp-mcp.log 2>&1 &
    echo $! > /tmp/whatsapp-mcp.pid
    echo "✅ WhatsApp MCP server started (PID: $(cat /tmp/whatsapp-mcp.pid))"
    cd /workspaces/MarthaVault
else
    echo "✅ WhatsApp MCP server already running"
fi

# Wait for MCP server to be ready
echo "⏳ Waiting for MCP server to be ready..."
sleep 5

# Start autonomous webhook listener
echo "🎧 Starting autonomous webhook listener..."
cd /workspaces/MarthaVault

# Run listener in background
nohup python3 .devcontainer/autonomous-webhook-listener.py > /tmp/autonomous-listener.log 2>&1 &
echo $! > /tmp/autonomous-listener.pid

echo "✅ Autonomous webhook listener started (PID: $(cat /tmp/autonomous-listener.pid))"

echo ""
echo "🎯 AUTONOMOUS SYSTEM READY"
echo "📡 Listening for GitHub Issues with 'Autonomous Process WhatsApp Reports'"
echo "📱 WhatsApp MCP server: http://localhost:3000"
echo "📄 Logs:"
echo "   MCP server: tail -f /tmp/whatsapp-mcp.log"
echo "   Listener: tail -f /tmp/autonomous-listener.log"
echo ""
echo "🔥 The system will now autonomously:"
echo "   1. Monitor GitHub Issues for processing requests"
echo "   2. Extract WhatsApp data when triggered"
echo "   3. Commit data to repository"
echo "   4. Trigger GitHub Actions for Gemini processing"
echo ""