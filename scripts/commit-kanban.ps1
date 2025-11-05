#!/usr/bin/env pwsh
# Commit and push Kanban board fixes + reference guide

$vaultPath = "C:\Users\10064957\My Drive\GDVault\MarthaVault"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "Committing Kanban updates..." -ForegroundColor Green
Write-Host "Time: $timestamp"
Write-Host ""

Set-Location $vaultPath

Write-Host "Adding files..."
git add -A

Write-Host "Committing..."
git commit -m "feat: kanban board setup + reference guide

- Fixed Tasks Kanban Board with proper Obsidian Kanban format
- Added YAML frontmatter: kanban-plugin: basic
- Created 5 columns: CRITICAL, HIGH, IN PROGRESS, COMPLETED, BACKLOG
- Saved comprehensive Kanban setup guide to reference folder
- All cards now draggable and functional"

Write-Host ""
Write-Host "Pushing to remote..."
git push origin master

Write-Host ""
Write-Host "✅ Complete!"
Write-Host ""
Write-Host "Latest commits:"
git log --oneline -3
