---
description: Checks GEMINI_CHAT.md for the latest message from Claude.
---

---
description: Checks GEMINI_CHAT.md for the latest message from Claude directly and reliably.
---

**RELIABILITY FIX V3.0: This version uses a single, self-contained command to avoid file-system race conditions present in the cloud-synced environment. You may need to add the command to the Windsurf allow-list once for it to run autonomously.**

### **Workflow: Check for Messages from Claude (Reliable Version)**

This workflow reads the [GEMINI_CHAT.md](cci:7://file:///c:/Users/10064957/My%20Drive/GDVault/MarthaVault/GEMINI_CHAT.md:0:0-0:0) file and displays the most recent message from `claude-desktop`.

### **Workflow Definition**
```yaml
name: Check for Messages from Claude
description: Checks GEMINI_CHAT.md for the latest message from Claude.
author: Gemini
version: 3.0.0

steps:
  - name: Check for messages directly
    run: |
      $chatFile = "./GEMINI_CHAT.md";
      if (-not (Test-Path $chatFile)) {
        echo "Chat file not found. No messages to check.";
        exit 0;
      }
      $content = Get-Content $chatFile -Raw;
      $blocks = $content -split '---';
      $latestMessage = "";
      for ($i = $blocks.Length - 1; $i -ge 0; $i--) {
        $block = $blocks[$i];
        if ($block -like '*### Claude-Desktop to Gemini*') {
          $latestMessage = "---$($block.Trim())---";
          break;
        }
      }
      if ($latestMessage) {
        echo "Latest message from Claude:";
        echo $latestMessage;
      } else {
        echo "No new messages from Claude found.";
      }