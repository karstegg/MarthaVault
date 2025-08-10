#!/bin/bash
# Check status of autonomous WhatsApp processing system

echo "🔍 AUTONOMOUS SYSTEM STATUS CHECK"
echo "================================="

# Check WhatsApp MCP server
echo "📱 WhatsApp MCP Server:"
if pgrep -f "whatsapp-mcp" > /dev/null; then
    PID=$(pgrep -f "whatsapp-mcp")
    echo "   ✅ Running (PID: $PID)"
    echo "   📊 Recent log entries:"
    tail -5 /tmp/whatsapp-mcp.log 2>/dev/null | sed 's/^/      /'
else
    echo "   ❌ Not running"
fi

echo ""

# Check autonomous listener
echo "🎧 Autonomous Webhook Listener:"
if pgrep -f "autonomous-webhook-listener" > /dev/null; then
    PID=$(pgrep -f "autonomous-webhook-listener")
    echo "   ✅ Running (PID: $PID)"
    echo "   📊 Recent log entries:"
    tail -5 /tmp/autonomous-listener.log 2>/dev/null | sed 's/^/      /'
else
    echo "   ❌ Not running"
fi

echo ""

# Check for recent processing requests
echo "🎯 Recent GitHub Issues:"
cd /workspaces/MarthaVault
python3 -c "
import requests
import os
import json
from datetime import datetime

token = os.getenv('GITHUB_TOKEN')
if not token:
    print('   ⚠️  GITHUB_TOKEN not found')
    exit()

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
url = 'https://api.github.com/repos/karstegg/MarthaVault/issues'
params = {'state': 'open', 'sort': 'created', 'direction': 'desc', 'per_page': 3}

try:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues[:3]:
            title = issue.get('title', 'No title')
            created = issue.get('created_at', '')
            if 'Autonomous Process WhatsApp Reports' in title:
                print(f'   🎯 {title}')
                print(f'      Created: {created}')
            else:
                print(f'   📄 {title[:60]}...')
    else:
        print(f'   ❌ GitHub API error: {response.status_code}')
except Exception as e:
    print(f'   ❌ Error: {e}')
"

echo ""

# Check extracted data files
echo "📁 Recent Extracted Data Files:"
find /workspaces/MarthaVault -name "extracted_data_*.txt" -mtime -1 2>/dev/null | head -5 | while read file; do
    if [ -n "$file" ]; then
        echo "   📄 $(basename $file) ($(stat -c%y "$file" | cut -d' ' -f1-2))"
    fi
done

if [ ! -f /workspaces/MarthaVault/extracted_data_*.txt ]; then
    echo "   📭 No recent extracted data files found"
fi

echo ""
echo "🚀 To trigger autonomous processing, create a GitHub Issue with title:"
echo "   'Autonomous Process WhatsApp Reports YYYY-MM-DD'"
echo ""
echo "📄 To view live logs:"
echo "   WhatsApp MCP: tail -f /tmp/whatsapp-mcp.log"
echo "   Listener: tail -f /tmp/autonomous-listener.log"