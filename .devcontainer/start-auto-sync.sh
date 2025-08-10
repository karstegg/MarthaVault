#!/bin/bash
# Start auto-sync in background

set -e

echo "🚀 Starting auto-sync daemon..."

# Kill existing auto-sync if running
pkill -f "auto-sync.sh" 2>/dev/null || true

# Start auto-sync in background
nohup bash /workspaces/MarthaVault/.devcontainer/auto-sync.sh > /tmp/auto-sync.log 2>&1 &

# Store PID
echo $! > /tmp/auto-sync.pid

echo "✅ Auto-sync daemon started (PID: $(cat /tmp/auto-sync.pid))"
echo "📋 Log file: /tmp/auto-sync.log" 
echo "🔧 To stop: kill $(cat /tmp/auto-sync.pid)"