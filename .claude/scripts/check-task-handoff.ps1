# Check for Pending Tasks on SessionStart
# Called by SessionStart hook to check if there are pending tasks

$vaultPath = "C:\Users\10064957\My Drive\GDVault\MarthaVault"
$filePath = "$vaultPath\reference\claude-code\task-handoff.md"

# Check if file exists
if (-not (Test-Path $filePath)) {
    # File doesn't exist yet - that's okay
    exit 0
}

try {
    # Read file content
    $content = Get-Content $filePath -Raw -ErrorAction Stop

    # Check if status is pending
    if ($content -match "status:\s*pending") {
        # Output message that Claude will see
        Write-Output "⚠️  Pending task detected in task-handoff.md - run /task-handoff to process"
    }
} catch {
    # Silent fail - don't block session start
    exit 0
}
