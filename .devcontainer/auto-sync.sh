#!/bin/bash
# Auto-sync script to keep Codespace in sync with latest repository changes

set -e

echo "🔄 Starting auto-sync process..."

# Function to sync repository
sync_repo() {
    echo "📥 Pulling latest changes from repository..."
    
    cd /workspaces/MarthaVault
    
    # Fetch latest changes
    git fetch origin
    
    # Check if there are new changes
    BEHIND=$(git rev-list HEAD..origin/master --count)
    
    if [ $BEHIND -gt 0 ]; then
        echo "📦 Found $BEHIND new commits, pulling changes..."
        git pull origin master
        
        # Check if WhatsApp MCP needs restart (if Python files changed)
        if git diff HEAD~$BEHIND --name-only | grep -E "\.(py|json|md)$" > /dev/null; then
            echo "🔄 Python/config files changed, restarting WhatsApp MCP..."
            /workspaces/MarthaVault/.devcontainer/restart-whatsapp-mcp.sh
        fi
        
        echo "✅ Repository synced successfully"
    else
        echo "✅ Repository is already up to date"
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

# Main sync loop
while true; do
    echo "🕐 $(date): Running auto-sync check..."
    
    sync_repo
    check_mcp_health
    
    # Wait 5 minutes before next sync
    echo "⏰ Next sync in 5 minutes..."
    sleep 300
done