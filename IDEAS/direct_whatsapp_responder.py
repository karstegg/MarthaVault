#!/usr/bin/env python3
"""
Direct WhatsApp MCP Responder - bypasses Claude Code layer
Monitors SQLite database and sends WhatsApp responses directly via MCP
"""
import sqlite3
import time
import subprocess
import json
import sys
import os

# Configuration
DB_PATH = "/workspaces/MarthaVault/whatsapp-mcp/whatsapp-bridge/store/messages.db"
SELF_JID = "27833911315@s.whatsapp.net"
SELF_NUMBER = "27833911315"
CHECK_INTERVAL = 2  # seconds
PROCESSED_FILE = "/tmp/processed_messages.txt"

def load_processed_messages():
    """Load set of already processed message timestamps"""
    try:
        with open(PROCESSED_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_processed_message(timestamp):
    """Save processed message timestamp"""
    with open(PROCESSED_FILE, 'a') as f:
        f.write(f"{timestamp}\n")

def send_whatsapp_message(recipient, message):
    """Send WhatsApp message directly via MCP using uv"""
    try:
        # Create MCP message using uv run (direct MCP call)
        cmd = [
            "uv", "--directory", "/workspaces/MarthaVault/whatsapp-mcp/whatsapp-mcp-server",
            "run", "python", "-c",
            f'''
import json
import sys
sys.path.append("/workspaces/MarthaVault/whatsapp-mcp/whatsapp-mcp-server")
from main import WhatsAppMCP

# Initialize MCP
mcp = WhatsAppMCP()

# Send message
result = mcp.send_message("{recipient}", "{message}")
print(json.dumps(result))
'''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            response = json.loads(result.stdout.strip())
            print(f"✅ Message sent: {message[:50]}...")
            return True
        else:
            print(f"❌ MCP Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Send error: {e}")
        return False

def process_command(message_content, timestamp):
    """Process command and generate response"""
    content = message_content.strip()
    
    # Parse command structure
    if not content or '/' not in content:
        return None
        
    parts = content.split('/', 1)
    if len(parts) != 2:
        return None
        
    command = parts[0].upper() + '/'
    content_part = parts[1].strip()
    
    # Generate responses based on command
    responses = {
        'T/': f'📋 Task created: \'{content_part[:35]}{"..." if len(content_part) > 35 else ""}\'',
        'N/': f'📝 Note saved: \'{content_part[:35]}{"..." if len(content_part) > 35 else ""}\'',
        'D/': f'📅 Added to daily: \'{content_part[:35]}{"..." if len(content_part) > 35 else ""}\'',
        'C/': f'💬 Comment saved: \'{content_part[:35]}{"..." if len(content_part) > 35 else ""}\'',
        'R/': f'⏰ Reminder set: \'{content_part[:35]}{"..." if len(content_part) > 35 else ""}\''
    }
    
    response = responses.get(command)
    if response:
        print(f"🎯 Processing {command}: {content_part[:30]}...")
        return response
    
    return None

def check_new_messages():
    """Check for new self-messages and process them"""
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get processed messages
        processed = load_processed_messages()
        
        # Query for recent self-messages
        query = """
        SELECT timestamp, content
        FROM messages 
        WHERE chat_jid = ? AND sender = ?
        AND timestamp > datetime('now', '-5 minutes')
        ORDER BY timestamp ASC
        """
        
        cursor.execute(query, (SELF_JID, SELF_NUMBER))
        messages = cursor.fetchall()
        
        for timestamp, content in messages:
            if timestamp in processed:
                continue
                
            print(f"📱 New message: {content}")
            
            # Process command
            response = process_command(content, timestamp)
            
            if response:
                # Send WhatsApp response
                success = send_whatsapp_message(SELF_NUMBER, response)
                
                if success:
                    # Mark as processed
                    save_processed_message(timestamp)
                    print(f"✅ Responded to: {content}")
                else:
                    print(f"❌ Failed to respond to: {content}")
            else:
                # Mark non-command messages as processed to avoid reprocessing
                save_processed_message(timestamp)
                print(f"ℹ️ Non-command message ignored: {content}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

def main():
    print("🚀 Direct WhatsApp MCP Responder starting...")
    print(f"📁 Database: {DB_PATH}")
    print(f"📱 Self JID: {SELF_JID}")
    print(f"⏱️ Check interval: {CHECK_INTERVAL}s")
    print("=" * 50)
    
    while True:
        try:
            check_new_messages()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down responder...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()