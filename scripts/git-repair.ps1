#!/usr/bin/env pwsh
# MarthaVault Git Repair - Fix sync issues

$vaultPath = "C:\Users\10064957\My Drive\GDVault\MarthaVault"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "MarthaVault Git Repair Started" -ForegroundColor Green
Write-Host "Time: $timestamp"
Write-Host "================================================"
Write-Host ""

# Navigate to vault
Set-Location $vaultPath

# Step 1: Remove nul file from Git
Write-Host "[1/6] Removing 'nul' from Git..."
git rm --cached nul 2>$null | Out-Null
Remove-Item -Path "nul" -Force -ErrorAction SilentlyContinue

# Step 2: Configure Git line endings
Write-Host "[2/6] Configuring Git line endings..."
git config core.autocrlf false
git config core.safecrlf false

# Step 3: Reset index
Write-Host "[3/6] Resetting Git index..."
git reset HEAD

# Step 4: Add only tracked files (exclude nul)
Write-Host "[4/6] Adding vault changes..."
git add -A
git status --short

# Step 5: Commit
Write-Host "[5/6] Committing changes..."
git commit -m "vault sync: update IDEAS files + fix git config (nul, line endings)" 2>&1 | Select-Object -First 5

# Step 6: Pull and push
Write-Host "[6/6] Syncing with remote..."
Write-Host ""
Write-Host "Pulling latest from remote..."
git pull origin master --no-edit

Write-Host "Pushing to remote..."
git push origin master

Write-Host ""
Write-Host "✅ Sync Complete!"
Write-Host ""
Write-Host "Latest commits:"
git log --oneline -3

$endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host ""
Write-Host "Completed at $endTime"
