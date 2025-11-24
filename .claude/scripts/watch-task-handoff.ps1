# Task Handoff File Watcher
# Monitors reference/claude-code/task-handoff.md for changes
# Automatically triggers /task-handoff when status: pending detected

$vaultPath = "C:\Users\10064957\My Drive\GDVault\MarthaVault"
$filePath = "$vaultPath\reference\claude-code\task-handoff.md"
$lockFile = "$vaultPath\.claude\.watcher-running"

# Check if file exists
if (-not (Test-Path $filePath)) {
    Write-Host "Error: task-handoff.md not found at $filePath"
    exit 1
}

# Prevent multiple watchers
if (Test-Path $lockFile) {
    $existingPid = Get-Content $lockFile -ErrorAction SilentlyContinue
    if ($existingPid -and (Get-Process -Id $existingPid -ErrorAction SilentlyContinue)) {
        Write-Host "Watcher already running (PID: $existingPid)"
        exit 0
    }
    # Stale lock file, remove it
    Remove-Item $lockFile -ErrorAction SilentlyContinue
}

# Create lock file with current process ID
$PID | Out-File $lockFile
Write-Host "Task handoff watcher started (PID: $PID)"
Write-Host "  Watching: $filePath"
Write-Host "  Press Ctrl+C to stop"

try {
    # Create FileSystemWatcher
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = Split-Path $filePath
    $watcher.Filter = Split-Path $filePath -Leaf
    $watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite
    $watcher.EnableRaisingEvents = $true

    # Define action to execute when file changes
    $action = {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] File changed detected"

        try {
            # Read file content
            $content = Get-Content "C:\Users\10064957\My Drive\GDVault\MarthaVault\reference\claude-code\task-handoff.md" -Raw -ErrorAction Stop

            # Check if status is pending
            if ($content -match "status:\s*pending") {
                Write-Host "  Pending task detected - creating trigger file"

                # Write marker file that hooks can detect
                $triggerFile = "C:\Users\10064957\My Drive\GDVault\MarthaVault\.claude\.task-handoff-trigger"
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                $timestamp | Out-File $triggerFile -Force

                Write-Host "  Trigger file created - Claude CLI hook will process on next Read operation"
            }
            else {
                Write-Host "  No pending task (status not 'pending')"
            }
        }
        catch {
            Write-Host "  Error reading file: $_"
        }
    }

    # Register event handler
    $eventJob = Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action $action

    Write-Host ""
    Write-Host "Watcher active - monitoring for changes..."
    Write-Host ""

    # Keep script running
    while ($true) {
        Start-Sleep -Seconds 10

        # Check if we should still be running
        if (-not (Test-Path $lockFile)) {
            Write-Host "Lock file removed - stopping watcher"
            break
        }
    }

}
catch {
    Write-Host "Error: $_"
}
finally {
    # Cleanup
    if ($eventJob) {
        Unregister-Event -SourceIdentifier $eventJob.Name -ErrorAction SilentlyContinue
        Remove-Job -Name $eventJob.Name -Force -ErrorAction SilentlyContinue
    }

    if ($watcher) {
        $watcher.EnableRaisingEvents = $false
        $watcher.Dispose()
    }

    Remove-Item $lockFile -ErrorAction SilentlyContinue
    Write-Host "Watcher stopped"
}
