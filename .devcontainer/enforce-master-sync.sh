#!/bin/bash
# Master Branch Enforcement and Synchronization Script
# Ensures local, Codespace, and remote repository are always in sync on master

set -e

REPO_DIR="/workspaces/MarthaVault"
MAIN_BRANCH="master"

echo "🔄 Master Branch Synchronization Check"
echo "======================================"

# Function to ensure we're on master branch
ensure_master_branch() {
    local location=$1
    
    echo "🌿 Checking branch in $location..."
    
    CURRENT_BRANCH=$(git branch --show-current)
    
    if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]; then
        echo "⚠️  Currently on branch: $CURRENT_BRANCH"
        echo "🔄 Switching to $MAIN_BRANCH..."
        
        # Stash any uncommitted changes
        if ! git diff-index --quiet HEAD --; then
            echo "💾 Stashing uncommitted changes..."
            git stash push -m "Auto-stash before switching to master - $(date)"
        fi
        
        # Switch to master
        git checkout $MAIN_BRANCH
        
        # Pull latest changes
        git pull origin $MAIN_BRANCH
        
        # Ask about applying stashed changes
        if git stash list | grep -q "Auto-stash"; then
            echo "📋 Found stashed changes. Apply them? (y/N)"
            read -r APPLY_STASH
            if [[ $APPLY_STASH =~ ^[Yy]$ ]]; then
                git stash pop
                echo "✅ Stashed changes applied"
            else
                echo "📦 Changes remain in stash: git stash pop to apply later"
            fi
        fi
    else
        echo "✅ Already on $MAIN_BRANCH branch"
    fi
}

# Function to sync with remote
sync_with_remote() {
    echo ""
    echo "🔄 Synchronizing with remote repository..."
    
    # Fetch latest changes
    git fetch origin
    
    # Check if we're behind
    BEHIND=$(git rev-list HEAD..origin/$MAIN_BRANCH --count 2>/dev/null || echo "0")
    
    # Check if we have uncommitted changes
    UNCOMMITTED=$(git status --porcelain | wc -l)
    
    # Check if we're ahead
    AHEAD=$(git rev-list origin/$MAIN_BRANCH..HEAD --count 2>/dev/null || echo "0")
    
    echo "📊 Repository Status:"
    echo "   Ahead: $AHEAD commits"
    echo "   Behind: $BEHIND commits"
    echo "   Uncommitted changes: $UNCOMMITTED files"
    
    if [ "$BEHIND" -gt 0 ]; then
        if [ "$UNCOMMITTED" -gt 0 ]; then
            echo "💾 Stashing changes before pull..."
            git stash push -m "Auto-stash before pull - $(date)"
            STASHED=true
        fi
        
        echo "📥 Pulling $BEHIND new commits..."
        git pull origin $MAIN_BRANCH
        
        if [ "$STASHED" = true ]; then
            echo "📋 Reapplying stashed changes..."
            git stash pop
        fi
    fi
    
    if [ "$UNCOMMITTED" -gt 0 ]; then
        echo "📝 Found uncommitted changes:"
        git status --short
        echo ""
        echo "🤔 Commit and push these changes? (y/N)"
        read -r COMMIT_CHANGES
        
        if [[ $COMMIT_CHANGES =~ ^[Yy]$ ]]; then
            echo "📦 Adding all changes..."
            git add .
            
            echo "✍️ Enter commit message (or press Enter for auto-generated):"
            read -r COMMIT_MSG
            
            if [ -z "$COMMIT_MSG" ]; then
                COMMIT_MSG="chore: Auto-commit configuration and script updates

Updated configuration files and scripts for:
- WhatsApp MCP server automation
- Daily report processing workflows  
- Smart date detection system
- Master branch synchronization

🤖 Auto-committed via sync script on $(date)"
            fi
            
            git commit -m "$COMMIT_MSG"
            
            echo "🚀 Pushing to remote..."
            git push origin $MAIN_BRANCH
            
            echo "✅ Changes committed and pushed"
        else
            echo "📋 Changes left uncommitted"
        fi
    fi
    
    if [ "$AHEAD" -gt 0 ] && [ "$UNCOMMITTED" -eq 0 ]; then
        echo "🚀 Pushing $AHEAD local commits to remote..."
        git push origin $MAIN_BRANCH
    fi
}

# Function to create sync status file
create_sync_status() {
    local sync_file="/tmp/last-master-sync"
    
    cat > "$sync_file" << EOF
{
    "last_sync": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "branch": "$(git branch --show-current)",
    "commit": "$(git rev-parse HEAD)",
    "remote_commit": "$(git rev-parse origin/$MAIN_BRANCH 2>/dev/null || echo 'unknown')",
    "status": "synced"
}
EOF

    echo "📊 Sync status saved to $sync_file"
}

# Main execution
main() {
    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        echo "❌ Not in a git repository"
        exit 1
    fi
    
    # If running in Codespace, use that path
    if [ -d "$REPO_DIR" ]; then
        cd "$REPO_DIR"
        echo "📂 Working in Codespace: $REPO_DIR"
    else
        echo "📂 Working in current directory: $(pwd)"
    fi
    
    # Ensure we're on master
    ensure_master_branch "$(pwd)"
    
    # Sync with remote
    sync_with_remote
    
    # Create sync status
    create_sync_status
    
    echo ""
    echo "✅ Master branch synchronization complete!"
    echo "🌿 Branch: $(git branch --show-current)"
    echo "💾 Latest commit: $(git log -1 --oneline)"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi