#!/bin/bash
# WhatsApp MCP System Stop Script
# Stops both bridge and server components

set -e

echo "🛑 Stopping WhatsApp MCP System..."

# Stop using combined PID file first
if [ -f /tmp/whatsapp-mcp.pid ]; then
    echo "📋 Found combined PID file, stopping all processes..."
    while read -r PID; do
        if [ -n "$PID" ]; then
            if kill $PID 2>/dev/null; then
                echo "✅ Stopped process $PID"
            else
                echo "⚠️ Process $PID not found"
            fi
        fi
    done < /tmp/whatsapp-mcp.pid
    rm -f /tmp/whatsapp-mcp.pid
fi

# Stop bridge if running
if [ -f /tmp/whatsapp-bridge.pid ]; then
    BRIDGE_PID=$(cat /tmp/whatsapp-bridge.pid)
    if kill $BRIDGE_PID 2>/dev/null; then
        echo "🌉 Bridge stopped (PID: $BRIDGE_PID)"
    else
        echo "⚠️ Bridge process $BRIDGE_PID not found"
    fi
    rm -f /tmp/whatsapp-bridge.pid
fi

# Stop server if running
if [ -f /tmp/whatsapp-mcp-server.pid ]; then
    SERVER_PID=$(cat /tmp/whatsapp-mcp-server.pid)
    if kill $SERVER_PID 2>/dev/null; then
        echo "🖥️ Server stopped (PID: $SERVER_PID)"
    else
        echo "⚠️ Server process $SERVER_PID not found"
    fi
    rm -f /tmp/whatsapp-mcp-server.pid
fi

# Force kill any remaining processes
echo "🔍 Checking for remaining processes..."

if pgrep -f "bridge" > /dev/null; then
    echo "🔨 Force killing remaining bridge processes..."
    pkill -f "bridge"
fi

if pgrep -f "whatsapp.*mcp.*server" > /dev/null; then
    echo "🔨 Force killing remaining server processes..."
    pkill -f "whatsapp.*mcp.*server"
fi

# Clean up any remaining WhatsApp MCP processes
if pgrep -f "whatsapp.*mcp" > /dev/null; then
    echo "🔨 Force killing remaining WhatsApp MCP processes..."
    pkill -f "whatsapp.*mcp"
fi

echo "✅ WhatsApp MCP system cleanup complete"