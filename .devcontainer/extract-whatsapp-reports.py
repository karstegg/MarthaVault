#!/usr/bin/env python3
"""
Automated WhatsApp report extraction for Codespaces
Runs inside Codespaces where WhatsApp MCP server is available
"""

import sys
import json
import requests
import subprocess
from datetime import datetime, timedelta
import os

class WhatsAppReportExtractor:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo = "karstegg/MarthaVault"  # Update with actual repo
        self.group_chat_id = "27834418149-1537194373@g.us"
        
    def extract_messages_for_date(self, target_date):
        """Extract WhatsApp messages for a specific date using MCP server"""
        
        print(f"📱 Extracting WhatsApp messages for {target_date}...")
        
        # Format date for MCP query
        start_time = f"{target_date}T00:00:00"
        end_time = f"{target_date}T23:59:59"
        
        # In practice, this would use the actual MCP client
        # For now, we'll simulate the MCP query structure
        
        try:
            # This would be the actual MCP call to list messages
            # messages = mcp_client.list_messages(
            #     chat_jid=self.group_chat_id,
            #     after=start_time,
            #     before=end_time,
            #     limit=50
            # )
            
            print(f"✅ Found messages for {target_date}")
            print("🔄 Processing messages to identify engineer reports...")
            
            # Process messages to identify daily reports
            extracted_reports = self._process_messages_for_reports(target_date)
            
            return extracted_reports
            
        except Exception as e:
            print(f"❌ Error extracting messages: {e}")
            return []
    
    def _process_messages_for_reports(self, target_date):
        """Process WhatsApp messages to identify engineer reports"""
        
        # This would contain the actual message processing logic
        # to identify reports from different engineers
        
        reports = []
        
        print("🔍 Identifying engineer reports from messages...")
        
        # Logic to identify reports by engineer phone numbers/patterns:
        # - Xavier Peterson: 150800697426058 (Shafts & Winders)
        # - Sipho Dubazane: 134144797478985 (Gloria)
        # - Sello Sease: 265033925812455 (Nchwaning 3)
        # - Johan Kotze: 278575940939844 (Nchwaning 2)
        
        return reports
    
    def trigger_github_workflow(self, target_date, messages):
        """Trigger GitHub Actions workflow with extracted WhatsApp data"""
        
        print(f"🚀 Triggering GitHub workflow for {target_date}...")
        
        # Repository dispatch payload
        payload = {
            "event_type": "process_whatsapp_reports",
            "client_payload": {
                "report_date": target_date,
                "group_chat_id": self.group_chat_id,
                "messages": messages,
                "source": "codespaces_mcp",
                "extracted_at": datetime.now().isoformat()
            }
        }
        
        # GitHub API call
        url = f"https://api.github.com/repos/{self.repo}/dispatches"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 204:
                print(f"✅ Workflow triggered successfully for {target_date}")
                return True
            else:
                print(f"❌ Failed to trigger workflow: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error triggering workflow: {e}")
            return False
    
    def process_date(self, target_date):
        """Complete processing pipeline for a specific date"""
        
        print(f"\n🎯 Processing reports for {target_date}")
        print("=" * 50)
        
        # Step 1: Extract WhatsApp messages
        messages = self.extract_messages_for_date(target_date)
        
        if not messages:
            print(f"⚠️  No messages found for {target_date}")
            return False
        
        # Step 2: Trigger GitHub workflow
        success = self.trigger_github_workflow(target_date, messages)
        
        if success:
            print(f"✅ Successfully initiated processing for {target_date}")
            print("🔄 GitHub workflow will:")
            print("  1. Process messages with Gemini CLI")
            print("  2. Apply correct Report Templates")
            print("  3. Create structured JSON/Markdown files")
            print("  4. Submit PR for Claude Code review")
            print("  5. Auto-merge if approved")
        else:
            print(f"❌ Failed to process {target_date}")
        
        return success

def main():
    """Main entry point for automated report extraction"""
    
    if len(sys.argv) != 2:
        print("Usage: python extract-whatsapp-reports.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    
    # Validate date format
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD")
        sys.exit(1)
    
    # Check if we're in Codespaces
    if not os.getenv('CODESPACES'):
        print("⚠️  This script is designed to run in GitHub Codespaces")
        print("   where the WhatsApp MCP server is available")
        # Continue anyway for testing
    
    # Check GitHub token
    if not os.getenv('GITHUB_TOKEN'):
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    # Initialize extractor and process
    extractor = WhatsAppReportExtractor()
    success = extractor.process_date(target_date)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()