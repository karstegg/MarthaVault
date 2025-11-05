#!/bin/bash
# MarthaVault GitHub Sync Status Check
# Usage: ./check-sync-status.sh
# Returns: 0 (in sync), 1 (behind), 2 (ahead/conflict)

VAULT_PATH="C:/Users/10064957/My Drive/GDVault/MarthaVault"
REPO="karstegg/MarthaVault"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=========================================="
echo "MarthaVault GitHub Sync Status"
echo "Checked: $TIMESTAMP"
echo "=========================================="

cd "$VAULT_PATH" || exit 2

# Get current commit hashes
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo ""
echo "Branch: $BRANCH"
echo "Local Commit:  $LOCAL"
echo "Remote Commit: $REMOTE"

# Check status
if [ "$LOCAL" = "$REMOTE" ]; then
    echo ""
    echo "Status: ✅ IN SYNC"
    echo "Your vault is synchronized with GitHub."
    
    # Check for uncommitted changes
    if git diff --quiet && git diff --cached --quiet; then
        echo "Working tree: ✅ CLEAN (no uncommitted changes)"
        exit 0
    else
        echo "Working tree: ⚠️ DIRTY (uncommitted changes present)"
        git status --short
        exit 1
    fi
else
    # Count commits
    BEHIND=$(git rev-list --count origin/master..HEAD)
    AHEAD=$(git rev-list --count HEAD..origin/master)
    
    if [ $AHEAD -gt 0 ] && [ $BEHIND -eq 0 ]; then
        echo ""
        echo "Status: 🔴 OUT OF SYNC - LOCAL BEHIND"
        echo "Remote is $AHEAD commits ahead."
        echo "Run: git pull origin master"
        exit 1
    elif [ $BEHIND -gt 0 ] && [ $AHEAD -eq 0 ]; then
        echo ""
        echo "Status: 🟡 OUT OF SYNC - LOCAL AHEAD"
        echo "Local is $BEHIND commits ahead."
        echo "Run: git push origin master"
        exit 1
    else
        echo ""
        echo "Status: 🔴 MERGE CONFLICT DETECTED"
        echo "Local: $BEHIND commits ahead, $AHEAD commits behind"
        echo "Manual intervention required."
        exit 2
    fi
fi

# Additional info
echo ""
echo "Recent commits:"
git log --oneline -3
echo ""
echo "Last push:"
git log -1 --format="%ai by %an"
