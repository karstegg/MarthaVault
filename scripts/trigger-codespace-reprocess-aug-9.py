#!/usr/bin/env python3
"""
Trigger Codespace-based reprocessing of August 9th reports
Uses the autonomous system with live WhatsApp MCP data
"""

import requests
import json
from datetime import datetime
import os

def trigger_codespace_processing():
    """Trigger the Codespace extraction and GitHub workflow for August 9th"""
    
    target_date = "2025-08-09"
    
    print("🚀 AUTONOMOUS REPROCESSING: August 9th via Codespace WhatsApp MCP")
    print("=" * 60)
    print()
    print("🔄 This will:")
    print("  1. Extract LIVE WhatsApp messages for Aug 9th from Codespace MCP")
    print("  2. Apply corrected Report Templates (not generic schemas)")
    print("  3. Create feature branch and PR")
    print("  4. Claude Code reviews and auto-merges")
    print("  5. OVERWRITE existing incorrect Aug 9th files")
    print()
    
    # Repository dispatch payload - this triggers the Codespace-based extraction
    github_token = os.getenv('GITHUB_TOKEN')
    repo = "karstegg/MarthaVault"
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment")
        print("💡 This script is designed to run from Codespaces or with GitHub token")
        print()
        print("🔧 Manual alternative:")
        print("   1. Open Codespaces")
        print("   2. Run: python /workspaces/MarthaVault/.devcontainer/extract-whatsapp-reports.py 2025-08-09")
        return False
    
    payload = {
        "event_type": "process_whatsapp_reports",
        "client_payload": {
            "report_date": target_date,
            "group_chat_id": "27834418149-1537194373@g.us",
            "source": "codespace_mcp_reprocess",
            "reason": "Template compliance - previous files used incorrect templates",
            "overwrite": True,
            "priority": "high"
        }
    }
    
    url = f"https://api.github.com/repos/{repo}/dispatches"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        print("📡 Triggering repository dispatch for Codespace processing...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 204:
            print("✅ Autonomous processing triggered successfully!")
            print()
            print("⏳ Workflow process:")
            print("  🔄 Codespace WhatsApp MCP extracts real messages")
            print("  🧠 Gemini processes with corrected templates")
            print("  🌿 Creates feature branch with timestamp")
            print("  📝 Opens PR with operational review standards")
            print("  👁️ Claude Code reviews for data accuracy")
            print("  ✅ Auto-merges if compliant")
            print()
            print("🔍 Monitor progress:")
            print(f"   GitHub Actions: https://github.com/{repo}/actions")
            print(f"   Expected PR: https://github.com/{repo}/pulls")
            print()
            print("🕐 Estimated completion: 3-5 minutes")
            return True
            
        else:
            print(f"❌ Failed to trigger workflow: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error triggering workflow: {e}")
        return False

def main():
    print("🎯 TESTING AUTONOMOUS WHATSAPP REPORT SYSTEM")
    print("Target: August 9th reports (currently incorrect)")
    print()
    
    success = trigger_codespace_processing()
    
    if success:
        print()
        print("🎉 SUCCESS: Autonomous reprocessing initiated!")
        print()
        print("📋 What happens next:")
        print("  1. Codespace extracts live WhatsApp data for Aug 9th")
        print("  2. System applies proper site-specific templates")
        print("  3. Gloria gets Standard Mine Site template (silo sections)")
        print("  4. S&W gets Infrastructure template (dam levels, no BEV)")
        print("  5. N3 gets Standard template with BEV analysis")
        print("  6. Claude Code verifies operational accuracy")
        print("  7. Files automatically overwrite incorrect versions")
        print()
        print("⚡ The autonomous system is now working!")
    else:
        print()
        print("⚠️ Autonomous trigger failed - likely need to run from Codespaces")
        print("🔧 Try running this from the Codespace environment instead")

if __name__ == "__main__":
    main()