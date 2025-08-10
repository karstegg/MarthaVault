# Test the fixed workflow with August 8th, 2025 data
# This will overwrite the existing incorrect files with proper template formatting

import sqlite3
import json
import requests
import os

def extract_whatsapp_data(target_date):
    """Extract WhatsApp messages for target date"""
    db_path = "/workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query for production group messages from target date
    query = """
    SELECT timestamp, sender, content, id
    FROM messages 
    WHERE chat_jid = '27834418149-1537194373@g.us'
    AND date(timestamp) = ?
    ORDER BY timestamp ASC
    """
    
    cursor.execute(query, (target_date,))
    messages = cursor.fetchall()
    
    conn.close()
    
    # Structure data for GitHub Actions
    return {
        "report_date": target_date,
        "group_chat_id": "27834418149-1537194373@g.us",
        "messages": [
            {
                "timestamp": msg[0],
                "sender": msg[1], 
                "content": msg[2],
                "message_id": msg[3]
            }
            for msg in messages
        ]
    }

def trigger_github_actions(whatsapp_data):
    """Send data to GitHub Actions via repository dispatch"""
    
    url = "https://api.github.com/repos/karstegg/MarthaVault/dispatches"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "event_type": "process_whatsapp_reports",
        "client_payload": whatsapp_data
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Response status: {response.status_code}")
    if response.status_code != 204:
        print(f"Response body: {response.text}")
    
    return response.status_code == 204

if __name__ == "__main__":
    # Reprocess August 8th with corrected templates
    target_date = "2025-08-08"
    
    print(f"🔄 REPROCESSING: Extracting WhatsApp data for {target_date}")
    print("📋 This will OVERWRITE existing files with correct templates")
    print("✅ Expected: Proper site-specific templates (Shafts & Winders vs Standard Mine)")
    print("✅ Expected: Correct JSON schemas and Markdown formatting")
    print()
    
    data = extract_whatsapp_data(target_date)
    
    print(f"Found {len(data['messages'])} messages")
    
    if data['messages']:
        print("Sample message preview:")
        for i, msg in enumerate(data['messages'][:2]):
            print(f"  {i+1}. {msg['sender']}: {msg['content'][:80]}...")
        
        print(f"\n🚀 Triggering GitHub Actions workflow...")
        success = trigger_github_actions(data)
        if success:
            print("✅ Triggered GitHub Actions successfully")
            print("📊 Monitor: https://github.com/karstegg/MarthaVault/actions")
            print("🔍 Files will be updated in: daily_production/data/2025-08/08/")
        else:
            print("❌ Failed to trigger GitHub Actions")
    else:
        print("No messages found for date")