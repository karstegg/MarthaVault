---
description: Checks GEMINI_CHAT.md for the latest message from Claude.
---

---
description: Checks GEMINI_CHAT.md for the latest message from Claude.
---

### **Workflow: Check for Messages from Claude**

This workflow reads the `GEMINI_CHAT.md` file and displays the most recent message from `claude-desktop`.

### **Workflow Steps**

```yaml
- name: Check for latest message from Claude
  run: |
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