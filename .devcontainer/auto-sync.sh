#!/bin/bash
# Auto-sync script to keep Codespace in sync with latest repository changes

set -e

echo "🔄 Starting auto-sync process..."

# Function to sync repository with master branch enforcement
sync_repo() {
    echo "📥 Syncing repository with master branch enforcement..."
    
    cd /workspaces/MarthaVault
    
    # Use the master enforcement script for comprehensive sync
    if [ -f ".devcontainer/enforce-master-sync.sh" ]; then
        # Run master enforcement (non-interactive mode)
        export GIT_AUTO_SYNC=true  # Flag for automated mode
        bash .devcontainer/enforce-master-sync.sh
        SYNC_EXIT_CODE=$?
        
        if [ $SYNC_EXIT_CODE -eq 0 ]; then
            echo "✅ Master branch sync completed successfully"
            
            # Check if services need restart based on changes
            if git diff HEAD~1 --name-only 2>/dev/null | grep -E "\.(py|json|sh)$" > /dev/null; then
                echo "🔄 Service files changed, may need restart..."
                # Services will be checked by individual health functions
            fi
        else
            echo "⚠️ Master sync completed with warnings"
        fi
    else
        # Fallback to simple sync
        echo "⚠️ Master sync script not found, using fallback..."
        git fetch origin
        git pull origin master
    fi
}

# Function to check MCP server health
check_mcp_health() {
    if pgrep -f "whatsapp-mcp" > /dev/null; then
        echo "💚 WhatsApp MCP server is running"
    else
        echo "🔴 WhatsApp MCP server is down, restarting..."
        /workspaces/MarthaVault/.devcontainer/start-whatsapp-mcp.sh
    fi
}

# Function to check daily processing scheduler
check_scheduler() {
    if pgrep -f "schedule-daily-processing" > /dev/null; then
        echo "📅 Daily processing scheduler is running"
    else
        echo "🔄 Starting daily processing scheduler..."
        nohup python3 /workspaces/MarthaVault/.devcontainer/schedule-daily-processing.py > /tmp/scheduler.log 2>&1 &
        echo "✅ Daily processing scheduler started"
    fi
}

# Main sync loop
while true; do
    echo "🕐 $(date): Running auto-sync check..."
    
    sync_repo
    check_mcp_health
    check_scheduler
    
    # Wait 5 minutes before next sync
    echo "⏰ Next sync in 5 minutes..."
    sleep 300
done