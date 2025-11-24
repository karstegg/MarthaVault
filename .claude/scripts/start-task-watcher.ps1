# Start Task Handoff Watcher in Background
# Called by SessionStart hook to launch the file watcher

$scriptPath = "$PSScriptRoot\watch-task-handoff.ps1"
$vaultPath = "C:\Users\10064957\My Drive\GDVault\MarthaVault"
$lockFile = "$vaultPath\.claude\.watcher-running"

# Check if watcher is already running
if (Test-Path $lockFile) {
    $existingPid = Get-Content $lockFile -ErrorAction SilentlyContinue
    if ($existingPid -and (Get-Process -Id $existingPid -ErrorAction SilentlyContinue)) {
        Write-Output "Watcher already running (PID: $existingPid)"
        exit 0
    }
}

# Start watcher in background (hidden window)
try {
    $process = Start-Process -WindowStyle Hidden -FilePath "powershell" -ArgumentList "-ExecutionPolicy", "Bypass", "-File", "`"$scriptPath`"" -PassThru
    Write-Output "✓ Task handoff watcher started in background (PID: $($process.Id))"
} catch {
    Write-Output "❌ Failed to start watcher: $_"
    exit 1
}
