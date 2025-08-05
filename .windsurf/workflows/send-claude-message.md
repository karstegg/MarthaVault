---
description: Appends a formatted message from Gemini to the shared GEMINI_CHAT.md file.
---

---
description: Appends a formatted message from Gemini to the shared GEMINI_CHAT.md file using a fully autonomous, multi-step temporary file workaround.
---

**ZERO-TOLERANCE AUTONOMY PROTOCOL IN EFFECT: ALL COMPLEXITY MUST BE OFFLOADED TO TEMP FILES CREATED WITH THE BUILT-IN `write_to_file` TOOL.**

### **Workflow: Send Message to Claude (Fully Autonomous)**

This workflow sends a message to `claude-desktop` by appending it to [GEMINI_CHAT.md](cci:7://file:///c:/Users/10064957/My%20Drive/GDVault/MarthaVault/GEMINI_CHAT.md:0:0-0:0). It uses a two-file temporary workaround to achieve full autonomy.

### **Workflow Definition**
```yaml
name: Send Message to Claude
description: Appends a formatted message from Gemini to the shared GEMINI_CHAT.md file.
author: Gemini
version: 2.0.0

inputs:
  - name: message
    type: string
    description: "The message content to send to Claude."
    required: true

steps:
  - name: Write message content to temp file
    uses: write_to_file
    with:
      path: ./temp_message_content.txt
      content: ${{ inputs.message }}

  - name: Create temporary script to send message
    uses: write_to_file
    with:
      path: ./temp_send_message.ps1
      content: |
        if (-not (Test-Path "./temp_message_content.txt")) {
            Write-Error "Message content file not found."
            exit 1
        }
        $message = Get-Content -Path "./temp_message_content.txt" -Raw
        $chatFile = "./GEMINI_CHAT.md"
        $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $formattedMessage = "`n---`n### Gemini to Claude`n**Timestamp:** $timestamp`n`n$message`n---"
        Add-Content -Path $chatFile -Value $formattedMessage
        echo "Message successfully sent to Claude."

  - name: Wait for file system
    run: Start-Sleep -Seconds 2

  - name: Execute temporary script
    run: powershell.exe -ExecutionPolicy Bypass -File ./temp_send_message.ps1

  - name: Clean up temporary script file
    run: Remove-Item -Path "./temp_send_message.ps1"

  - name: Clean up temporary content file
    run: Remove-Item -Path "./temp_message_content.txt"