#!/bin/bash
# WhatsApp MCP Server Stop Script

set -e

echo "🛑 Stopping WhatsApp MCP Server..."

if [ -f /tmp/whatsapp-mcp.pid ]; then
    PID=$(cat /tmp/whatsapp-mcp.pid)
    if kill $PID 2>/dev/null; then
        echo "✅ WhatsApp MCP server stopped (PID: $PID)"
        rm -f /tmp/whatsapp-mcp.pid
    else
        echo "⚠️  Process $PID not found, cleaning up PID file"
        rm -f /tmp/whatsapp-mcp.pid
    fi
else
    echo "⚠️  No PID file found"
fi

# Force kill any remaining processes
if pgrep -f "whatsapp-mcp" > /dev/null; then
    echo "🔨 Force killing remaining WhatsApp MCP processes..."
    pkill -f "whatsapp-mcp"
fi

echo "✅ WhatsApp MCP server cleanup complete"