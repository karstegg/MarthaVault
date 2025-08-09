# Codespace WhatsApp Data Extractor
# Run this in Codespace to extract and send WhatsApp data to GitHub Actions

import sqlite3
import json
import requests
import os
from datetime import datetime, timedelta

def extract_whatsapp_data(target_date):
    """Extract WhatsApp messages for target date"""
    db_path = "/workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query for production group messages from target date
    query = """
    SELECT timestamp, sender, content, message_id
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
    return response.status_code == 204

if __name__ == "__main__":
    # Extract yesterday's data (typical use case)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Extracting WhatsApp data for {yesterday}")
    data = extract_whatsapp_data(yesterday)
    
    print(f"Found {len(data['messages'])} messages")
    
    if data['messages']:
        success = trigger_github_actions(data)
        if success:
            print("✅ Triggered GitHub Actions successfully")
        else:
            print("❌ Failed to trigger GitHub Actions")
    else:
        print("No messages found for date")
