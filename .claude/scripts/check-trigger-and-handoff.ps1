# Check for Task Handoff Trigger File
# Called by PreToolUse hook on Read operations
# If trigger file exists, output command to run /task-handoff

$triggerFile = "C:\Users\10064957\My Drive\GDVault\MarthaVault\.claude\.task-handoff-trigger"

if (Test-Path $triggerFile) {
    # Trigger exists - tell Claude to run /task-handoff
    Write-Output "PENDING TASK DETECTED - Running /task-handoff now..."
    Write-Output "/task-handoff"

    # Delete trigger file so we don't process it again
    Remove-Item $triggerFile -Force -ErrorAction SilentlyContinue
}
