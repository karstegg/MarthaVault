#!/usr/bin/env python3
"""
Claude Cloud Orchestration Trigger
Creates GitHub Issues that trigger the autonomous processing pipeline
"""

import requests
import json
import os
from datetime import datetime, timedelta

class ClaudeOrchestrationTrigger:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo = "karstegg/MarthaVault"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_processing_issue(self, target_date, priority="medium", notes=""):
        """Create a GitHub Issue that triggers autonomous processing"""
        
        print(f"🤖 Creating Claude Orchestration Issue for {target_date}")
        
        # Determine priority emoji and urgency
        priority_config = {
            "urgent": {"emoji": "🔴", "label": "priority-urgent"},
            "high": {"emoji": "🟡", "label": "priority-high"}, 
            "medium": {"emoji": "🟢", "label": "priority-medium"},
            "low": {"emoji": "⚪", "label": "priority-low"}
        }
        
        config = priority_config.get(priority, priority_config["medium"])
        
        # Create structured issue title (contains date for parsing)
        title = f"🤖 Autonomous Process WhatsApp Reports: {target_date}"
        
        # Create detailed issue body
        body = f"""## {config['emoji']} Autonomous WhatsApp Report Processing Request

**Report Date**: `{target_date}`
**Priority**: {priority.upper()}
**Requested By**: Claude Cloud Orchestration System
**Request Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

### Processing Instructions
This issue triggers the **autonomous processing pipeline**:

1. **🔄 GitHub Actions** detects this issue and orchestrates processing
2. **📱 Codespace Execution** extracts live WhatsApp MCP data
3. **🧠 Gemini Processing** applies correct Report Templates
4. **💾 File Creation** generates structured JSON/Markdown reports
5. **🚀 Git Operations** commits directly to master branch
6. **👁️ Claude Review** automatically reviews and approves results

### Expected Output Files
📂 `daily_production/data/{target_date[:7].replace('-', '-')}/{target_date[-2:]}/`
- `{target_date}_gloria.json` & `.md` (Sipho Dubazane - Gloria)
- `{target_date}_nchwaning3.json` & `.md` (Sello Sease - Nchwaning 3) 
- `{target_date}_shafts-winders.json` & `.md` (Xavier Peterson - S&W)

### Site-Specific Requirements
- **Gloria**: Standard Mine Site template with silo levels
- **Nchwaning 3**: Standard template with BEV analysis (7 DTs + 6 FLs)
- **Shafts & Winders**: Infrastructure template (dams, power, no BEV)

### Quality Standards
- **Data Source**: Live WhatsApp MCP extraction
- **Templates**: Exact Report Templates folder compliance
- **Validation**: Source data validation sections required
- **Review**: Autonomous Claude Cloud approval

### Additional Notes
{notes if notes else 'Standard daily production report processing'}

---
**🎯 ACTION REQUIRED**: None - fully autonomous processing
**⏱️ ESTIMATED TIME**: 5-8 minutes end-to-end
**📊 SUCCESS CRITERIA**: Files created, Claude approved, issue auto-closed

/label: autonomous-processing,daily-production,{config['label']}
**This issue will auto-close when processing completes successfully.**"""

        # Create the issue
        url = f"https://api.github.com/repos/{self.repo}/issues"
        
        payload = {
            "title": title,
            "body": body,
            "labels": [
                "autonomous-processing", 
                "daily-production", 
                config['label'],
                "claude-orchestrated"
            ]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ Orchestration Issue Created Successfully!")
                print(f"   Issue #{issue['number']}: {issue['title']}")
                print(f"   URL: {issue['html_url']}")
                print()
                print("🔄 Autonomous processing pipeline will now execute:")
                print("   1. GitHub Actions detects issue → orchestrates")
                print("   2. Codespace executes → live WhatsApp MCP data")
                print("   3. Reports generated → committed to master")
                print("   4. Claude reviews → auto-approves → issue closes")
                print()
                print("⏱️ Expected completion: 5-8 minutes")
                return issue
            else:
                print(f"❌ Failed to create issue: HTTP {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"💥 Error creating orchestration issue: {e}")
            return None
    
    def batch_process_dates(self, start_date, end_date, priority="medium"):
        """Create orchestration issues for a date range"""
        
        print(f"📅 BATCH ORCHESTRATION: {start_date} to {end_date}")
        print("=" * 50)
        
        from datetime import datetime, timedelta
        
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        issues_created = []
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            
            # Add delay between requests to avoid rate limiting
            if issues_created:
                print("⏳ Waiting 30 seconds between requests...")
                import time
                time.sleep(30)
            
            issue = self.create_processing_issue(
                date_str, 
                priority=priority,
                notes=f"Part of batch processing: {start_date} to {end_date}"
            )
            
            if issue:
                issues_created.append(issue)
            
            current += timedelta(days=1)
        
        print(f"\n🎉 BATCH ORCHESTRATION COMPLETE")
        print(f"📊 Created {len(issues_created)} orchestration issues")
        print("🔄 Autonomous processing pipelines will execute in sequence")
        
        return issues_created

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("🤖 Claude Cloud Orchestration Trigger")
        print("=====================================")
        print()
        print("Usage:")
        print("  Single date:     python3 claude-orchestration-trigger.py 2025-08-09")
        print("  Date range:      python3 claude-orchestration-trigger.py 2025-08-09 2025-08-15")
        print("  With priority:   python3 claude-orchestration-trigger.py 2025-08-09 high")
        print() 
        print("Priority levels: low, medium, high, urgent")
        print()
        return 1
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable required")
        print("💡 This token is used to create GitHub Issues that trigger processing")
        return 1
    
    trigger = ClaudeOrchestrationTrigger()
    
    # Parse arguments
    if len(sys.argv) == 2:
        # Single date
        target_date = sys.argv[1]
        trigger.create_processing_issue(target_date)
        
    elif len(sys.argv) == 3:
        arg2 = sys.argv[2]
        if arg2 in ["low", "medium", "high", "urgent"]:
            # Single date with priority
            target_date = sys.argv[1]
            priority = arg2
            trigger.create_processing_issue(target_date, priority=priority)
        else:
            # Date range
            start_date = sys.argv[1]
            end_date = sys.argv[2]
            trigger.batch_process_dates(start_date, end_date)
            
    elif len(sys.argv) == 4:
        # Date range with priority
        start_date = sys.argv[1]
        end_date = sys.argv[2] 
        priority = sys.argv[3]
        trigger.batch_process_dates(start_date, end_date, priority=priority)
    
    return 0

if __name__ == "__main__":
    exit(main())