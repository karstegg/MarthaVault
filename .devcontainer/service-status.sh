#!/bin/bash
# Check status of all MarthaVault services

echo "📊 MarthaVault Services Status"
echo "================================"

# WhatsApp MCP Bridge
echo "📱 WhatsApp MCP Bridge:"
if pgrep -f "bridge" > /dev/null; then
    PID=$(pgrep -f "bridge")
    echo "   ✅ Running (PID: $PID)"
    if [ -f /tmp/whatsapp-bridge.log ]; then
        echo "   📋 Log: tail -f /tmp/whatsapp-bridge.log"
    fi
else
    echo "   🔴 Not running"
fi

# WhatsApp MCP Server
echo "📱 WhatsApp MCP Server:"
if pgrep -f "whatsapp.*mcp.*server" > /dev/null; then
    PID=$(pgrep -f "whatsapp.*mcp.*server")
    echo "   ✅ Running (PID: $PID)"
    if [ -f /tmp/whatsapp-mcp-server.log ]; then
        echo "   📋 Log: tail -f /tmp/whatsapp-mcp-server.log"
    fi
else
    echo "   🔴 Not running"
fi

# Auto-sync Daemon
echo
echo "🔄 Auto-sync Daemon:"
if pgrep -f "auto-sync.sh" > /dev/null; then
    PID=$(pgrep -f "auto-sync.sh")
    echo "   ✅ Running (PID: $PID)"
    if [ -f /tmp/auto-sync.log ]; then
        echo "   📋 Log: tail -f /tmp/auto-sync.log"
    fi
else
    echo "   🔴 Not running"
fi

# Repository status
echo
echo "📦 Repository Status:"
cd /workspaces/MarthaVault 2>/dev/null || { echo "   ❌ Not in MarthaVault directory"; exit 1; }

BRANCH=$(git branch --show-current)
BEHIND=$(git rev-list HEAD..origin/master --count 2>/dev/null || echo "unknown")
LAST_COMMIT=$(git log -1 --oneline 2>/dev/null || echo "unknown")

echo "   🌿 Branch: $BRANCH"
echo "   📈 Behind origin: $BEHIND commits"
echo "   💾 Last commit: $LAST_COMMIT"

# Disk usage
echo
echo "💿 Storage Usage:"
USAGE=$(df -h /workspaces | tail -1 | awk '{print $5}')
echo "   📊 Disk usage: $USAGE"

echo
echo "🔧 Management Commands:"
echo "   Start MCP: bash .devcontainer/start-whatsapp-mcp.sh"
echo "   Stop MCP:  bash .devcontainer/stop-whatsapp-mcp.sh" 
echo "   Restart:   bash .devcontainer/restart-whatsapp-mcp.sh"
echo "   Auto-sync: bash .devcontainer/start-auto-sync.sh"