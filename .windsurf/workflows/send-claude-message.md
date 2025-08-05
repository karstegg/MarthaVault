---
description: Appends a formatted message from Gemini to the shared GEMINI_CHAT.md file.
---

---
description: Appends a formatted message from Gemini to the shared GEMINI_CHAT.md file.
---

### **Workflow: Send Message to Claude**

This workflow appends a formatted message from Gemini to the `GEMINI_CHAT.md` file, including a timestamp.

### **Workflow Steps**

```yaml
- name: Send message to Claude
  run: |
    $message = "${{ inputs.message }}"
    if ([string]::IsNullOrWhiteSpace($message)) {
      Write-Error "Message cannot be empty."
      exit 1
    }
    $chatFile = "./GEMINI_CHAT.md"
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $formattedMessage = "
---
### Gemini to Claude
**Timestamp:** $timestamp

$message
---"
    Add-Content -Path $chatFile -Value $formattedMessage
    echo "Message successfully sent to Claude."