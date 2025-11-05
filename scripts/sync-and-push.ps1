#!/usr/bin/env pwsh
# MarthaVault Git Sync - Push Pending Changes

$vaultPath = "C:\Users\10064957\My Drive\GDVault\MarthaVault"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "MarthaVault Git Sync Started at $timestamp"
Write-Host "================================================"
Write-Host ""

# Change to vault directory
Set-Location $vaultPath

# Check current status
Write-Host "Current Status:"
git status --short | Select-Object -First 10

Write-Host ""
Write-Host "Adding changes..."
git add -A

Write-Host "Committing..."
git commit -m "vault sync: update IDEAS files and Martha architecture diagrams"

Write-Host ""
Write-Host "Pushing to remote..."
git push origin master

Write-Host ""
Write-Host "Sync Complete!"
Write-Host "Latest commits:"
git log --oneline -3

$endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host ""
Write-Host "Completed at $endTime"
