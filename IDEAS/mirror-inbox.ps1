# PowerShell script to mirror the 00_Inbox folder from the master branch to the MarthaVault-Claude37 branch.

# Ensure the script runs from the vault's root directory.
Push-Location $PSScriptRoot

Write-Host "Starting inbox mirroring process..."

# Define branch names
$sourceBranch = "master"
$targetBranch = "MarthaVault-Claude37"

# 1. Ensure we are on the source branch to get the correct inbox files
Write-Host "Ensuring we are on the '$sourceBranch' branch..."
git checkout $sourceBranch

# 2. Switch to the target branch to apply changes
Write-Host "Checking out '$targetBranch' branch..."
git checkout $targetBranch

# 3. Ensure the target branch is up-to-date with its remote counterpart
Write-Host "Pulling latest changes for '$targetBranch' branch..."
git pull origin $targetBranch

# 4. Copy files from the source branch's inbox to the current (target) branch's inbox.
# We use 'git checkout' to pull the files from the other branch without changing the HEAD.
Write-Host "Mirroring files from '$sourceBranch' inbox..."
git checkout $sourceBranch -- 00_Inbox/

# 5. Stage the newly mirrored files
Write-Host "Staging mirrored files from 00_Inbox..."
git add 00_Inbox/

# 6. Check if there are any staged changes to avoid empty commits
$changes = git diff --staged --quiet --exit-code
if (-Not $?) {
    # 7. Commit the staged files with a standardized message
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Automated Mirror: Sync inbox from master at $timestamp"
    Write-Host "Committing changes: $commitMessage"
    git commit -m $commitMessage

    # 8. Push the new commit to the remote target branch on GitHub
    Write-Host "Pushing changes to the '$targetBranch' branch on GitHub..."
    git push origin $targetBranch
} else {
    Write-Host "No new files detected in master's 00_Inbox. Nothing to mirror."
}

# 9. Switch back to the master branch for normal work
Write-Host "Returning to '$sourceBranch' branch..."
git checkout $sourceBranch

# Return to the original directory
Pop-Location

Write-Host "Inbox mirroring process complete."
