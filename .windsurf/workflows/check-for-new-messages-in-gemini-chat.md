---
description: Checks GEMINI_CHAT.md for the latest message from Claude.
---

---
description: Checks GEMINI_CHAT.md for the latest message from Claude using a fully autonomous temporary script workaround.
---

**ZERO-TOLERANCE AUTONOMY PROTOCOL IN EFFECT: ALL COMPLEXITY MUST BE OFFLOADED TO TEMP FILES CREATED WITH THE BUILT-IN `write_to_file` TOOL.**

### **Workflow: Check for Messages from Claude (Fully Autonomous)**

This workflow reads the [GEMINI_CHAT.md](cci:7://file:///c:/Users/10064957/My%20Drive/GDVault/MarthaVault/GEMINI_CHAT.md:0:0-0:0) file and displays the most recent message from `claude-desktop`.

### **Workflow Definition**
```yaml
name: Check for Messages from Claude
description: Checks GEMINI_CHAT.md for the latest message from Claude.
author: Gemini
version: 2.0.0

steps:
  - name: Create temporary script to check for messages
    uses: write_to_file
    with:
      path: ./temp_check_messages.ps1
      content: |
        $chatFile = "./GEMINI_CHAT.md"
        if (-not (Test-Path $chatFile)) {
          echo "Chat file not found. No messages to check."
          exit 0
        }
        $content = Get-Content $chatFile -Raw
        $blocks = $content -split '---'
        for ($i = $blocks.Length - 1; $i -ge 0; $i--) {
          $block = $blocks[$i]
          if ($block -like '*### Claude-Desktop to Gemini*') {
            echo "Latest message from Claude:"
            echo "---$($block.Trim())---"
            exit 0
          }
        }
        echo "No new messages from Claude found."

  - name: Wait for file system
    run: Start-Sleep -Seconds 2

  - name: Execute temporary script
    run: powershell.exe -ExecutionPolicy Bypass -File ./temp_check_messages.ps1

  - name: Clean up temporary script
    run: Remove-Item -Path "./temp_check_messages.ps1"