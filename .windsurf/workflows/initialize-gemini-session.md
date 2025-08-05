---
description: Initializes a new Gemini session with complete context and validation requirements.
---

### **Workflow: Initialize Gemini Session**

**This workflow provides Gemini with complete context when starting a new session in Windsurf/Cascade IDE.**

### **Workflow Definition**
```yaml
name: Initialize Gemini Session
description: Loads complete context for Gemini daily production report processing
author: Claude-Desktop
version: 1.0.0

steps:
  - name: Load Primary Context
    run: |
      echo "🚀 INITIALIZING GEMINI SESSION"
      echo "================================="
      echo ""
      echo "📋 Loading primary context from .claude/commands/gemini.md..."
      echo ""
      # Read primary context file
      Get-Content ".claude/commands/gemini.md" | Write-Host
      echo ""
      echo "✅ Primary context loaded successfully"

  - name: Load Repository Guidelines  
    run: |
      echo ""
      echo "📖 Loading repository guidelines from CLAUDE.md..."
      echo ""
      # Show key sections from CLAUDE.md
      $claudeContent = Get-Content "CLAUDE.md" -Raw
      if ($claudeContent -match '(?s)## 🔄 \*\*Active Session Context\*\*(.*?)(?=##|\z)') {
        echo "Current Session Context:"
        echo $matches[1]
      }
      echo ""
      echo "✅ Repository guidelines referenced"

  - name: Check Communication Status
    run: |
      echo ""
      echo "💬 Checking communication status..."
      echo ""
      # Check for pending messages
      if (Test-Path "GEMINI_CHAT.md") {
        $lastLines = Get-Content "GEMINI_CHAT.md" | Select-Object -Last 10
        $hasNewMessages = $lastLines -match "Claude-Desktop to Gemini"
        if ($hasNewMessages) {
          echo "📨 PENDING MESSAGES detected in GEMINI_CHAT.md"
          echo "   Please check for new instructions from Claude-Desktop"
        } else {
          echo "✅ No pending messages - ready for new tasks"
        }
      } else {
        echo "⚠️  GEMINI_CHAT.md not found - creating communication file"
        New-Item -Path "GEMINI_CHAT.md" -ItemType File -Force
      }

  - name: Verify Data Sources
    run: |
      echo ""
      echo "📊 Verifying data sources..."
      echo ""
      # Check primary data source
      if (Test-Path "00_Inbox/Raw Whatsap Data for Daily Reports.md") {
        $sourceSize = (Get-Item "00_Inbox/Raw Whatsap Data for Daily Reports.md").Length
        echo "✅ WhatsApp source data available ($([math]::Round($sourceSize/1KB, 1)) KB)"
      } else {
        echo "⚠️  Primary WhatsApp source data not found"
      }
      
      # Check equipment reference
      if (Test-Path "daily_production/equipment_codes.md") {
        echo "✅ Equipment codes reference available"
      } else {
        echo "⚠️  Equipment codes reference not found"
      }
      
      # Check fleet database
      if (Test-Path "reference/equipment/brmo_fleet_database.json") {
        echo "✅ Fleet database available"
      } else {
        echo "⚠️  Fleet database not found"
      }

  - name: Verify Output Structure
    run: |
      echo ""
      echo "📁 Verifying output structure..."
      echo ""
      # Check daily production folder
      if (Test-Path "daily_production") {
        echo "✅ Daily production folder exists"
        if (Test-Path "daily_production/data") {
          $dataFolders = Get-ChildItem "daily_production/data" -Directory | Measure-Object
          echo "✅ Data folder structure exists ($($dataFolders.Count) month folders)"
        } else {
          echo "⚠️  Data subfolder structure needs creation"
        }
      } else {
        echo "❌ Daily production folder missing - critical error"
      }

  - name: Load Processing Instructions
    run: |
      echo ""
      echo "⚙️  Loading processing instructions..."
      echo ""
      # Show /pdr command is available
      if (Test-Path ".claude/commands/pdr.md") {
        echo "✅ Primary processing command (/pdr) available"
      } else {
        echo "❌ Critical: /pdr command definition missing"
      }
      
      # Check specialized agents
      $agents = @("pdr-nchwaning2", "pdr-nchwaning3", "pdr-gloria", "pdr-shafts-winders")
      foreach ($agent in $agents) {
        if (Test-Path ".claude/agents/$agent.md") {
          echo "✅ Specialized agent available: $agent"
        } else {
          echo "⚠️  Agent missing: $agent"
        }
      }

  - name: Display Critical Reminders
    run: |
      echo ""
      echo "🚨 CRITICAL REMINDERS"
      echo "===================="
      echo ""
      echo "📊 DATA VALIDATION REQUIREMENTS:"
      echo "   • NEVER INVENT DATA - extract only from source"
      echo "   • EVERY report must include source_validation section"
      echo "   • Quote specific line numbers and exact text"
      echo "   • If data missing from source, use null - do NOT fabricate"
      echo ""
      echo "📁 FOLDER STRUCTURE:"
      echo "   • Use hierarchical: daily_production/data/YYYY-MM/DD/"
      echo "   • NOT flat structure like: daily_production/data/YYYY-MM-DD/"
      echo ""
      echo "💬 COMMUNICATION:"
      echo "   • Monitor GEMINI_CHAT.md for messages from Claude-Desktop"
      echo "   • Use proper message format with timestamps"
      echo "   • Tag @claude-code in GitHub PRs for review"
      echo ""
      echo "⚠️  LESSON FROM PR #7:"
      echo "   • Previous error: Invented 15,670t when source showed 5,545t"
      echo "   • Prevention: All numbers must trace to source lines"

  - name: Session Ready Confirmation
    run: |
      echo ""
      echo "🎯 SESSION INITIALIZATION COMPLETE"
      echo "=================================="
      echo ""
      echo "✅ Context loaded from .claude/commands/gemini.md"
      echo "✅ Repository guidelines from CLAUDE.md referenced"
      echo "✅ Communication channels verified"
      echo "✅ Data sources checked"
      echo "✅ Output structure confirmed" 
      echo "✅ Processing instructions loaded"
      echo "✅ Critical validation requirements understood"
      echo ""
      echo "🚀 GEMINI IS READY TO PROCESS DAILY PRODUCTION REPORTS"
      echo ""
      echo "📋 Available Commands:"
      echo "   • /pdr - Process daily production reports (with source validation)"
      echo "   • /task - Create tasks and track progress"
      echo "   • /triage - Organize files in inbox"
      echo ""
      echo "📞 Next Steps:"
      echo "   1. Check GEMINI_CHAT.md for any pending messages"
      echo "   2. Await processing instructions from Claude-Desktop"
      echo "   3. Remember: Data accuracy > Technical compliance"
      echo ""
      echo "=================================="
      echo "Session initialized at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
```

### **Usage Instructions**

**When starting a new Gemini session in Windsurf:**

1. **Run this workflow first**: Execute `initialize-gemini-session` 
2. **Review output**: Check all verification steps pass
3. **Address any warnings**: Fix missing files or structure issues
4. **Confirm readiness**: Ensure critical reminders are understood
5. **Begin processing**: Gemini is now fully contextualized

### **Key Context Loaded:**

- **🏭 Operational Context**: Assmang Black Rock mining operations
- **📊 Data Requirements**: Mandatory source validation with line numbers  
- **📁 File Structure**: Hierarchical folder organization
- **⚙️ Processing Flow**: Step-by-step report processing workflow
- **💬 Communication**: GEMINI_CHAT.md monitoring and GitHub workflows
- **🎯 Quality Standards**: Data accuracy and technical compliance

### **Critical Validation Rules Emphasized:**

1. **Never invent data** - extract only from WhatsApp source
2. **Source validation mandatory** - every report needs line numbers/quotes
3. **Folder structure** - use YYYY-MM/DD/ hierarchy not flat structure
4. **Communication protocol** - monitor GEMINI_CHAT.md for instructions

**This workflow ensures Gemini starts each session with complete context and understanding of the data validation requirements implemented after the PR #7 failure.**