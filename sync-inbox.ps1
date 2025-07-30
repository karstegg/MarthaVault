# PowerShell script to automatically sync the 00_Inbox folder to the inbox-sync branch on GitHub.

# Ensure the script runs from the vault's root directory.
Push-Location $PSScriptRoot

Write-Host "Starting inbox sync process..."

# 1. Fetch the latest state from the remote repository
Write-Host "Fetching latest from origin..."
git fetch origin

# 2. Switch to the dedicated sync branch
Write-Host "Checking out 'inbox-sync' branch..."
git checkout inbox-sync

# 3. Ensure the local sync branch is up-to-date with the remote
Write-Host "Pulling latest changes for 'inbox-sync' branch..."
git pull origin inbox-sync

# 4. Stage any new or modified files specifically from the 00_Inbox directory
Write-Host "Staging files from 00_Inbox..."
git add 00_Inbox/

# 5. Check if there are any staged changes to avoid empty commits
$changes = git diff --staged --quiet --exit-code
if (-Not $?) {
    # 6. Commit the staged files with a standardized message
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Automated Sync: Update inbox at $timestamp"
    Write-Host "Committing changes: $commitMessage"
    git commit -m $commitMessage

    # 7. Push the new commit to the remote inbox-sync branch on GitHub
    Write-Host "Pushing changes to GitHub..."
    git push origin inbox-sync
} else {
    Write-Host "No changes detected in 00_Inbox. Nothing to sync."
}

# 8. Switch back to the master branch for normal work
Write-Host "Returning to 'master' branch..."
git checkout master

# Return to the original directory
Pop-Location

Write-Host "Inbox sync process complete."
