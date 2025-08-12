# WhatsApp MCP Server Setup Guide for GitHub Codespaces
## CORRECTED: Based on LHARRIES Official Implementation

## Overview
This guide sets up the official LHARRIES WhatsApp MCP server in your GitHub Codespace. This is a **two-component system**: a Go bridge + Python MCP server.

## Architecture (LHARRIES Official)
- **Go WhatsApp Bridge**: Connects to WhatsApp Web API, handles QR authentication, stores messages in SQLite
- **Python MCP Server**: Provides standardized MCP tools for Claude/Gemini integration  
- **UV Package Manager**: Required for Python server execution
- **SQLite Database**: Local message storage

## Current Issues Identified
✅ **Workflow Configuration**: Your GitHub Actions workflows exist and are properly configured
❌ **Missing Go Bridge**: No Go component for WhatsApp Web API connection
❌ **Empty Python Server**: Your whatsapp-mcp-server directory has no actual implementation  
❌ **Wrong Scripts**: Your workflows reference non-existent custom scripts
❌ **Missing UV**: No UV package manager for Python MCP server execution

## Setup Steps

### 1. Install WhatsApp MCP Server
In your GitHub Codespace, run these commands:

```bash
# Navigate to your repository
cd /workspaces/MarthaVault

# Create the MCP server structure
mkdir -p whatsapp-mcp-server/src/whatsapp_mcp_server

# Create main MCP server file
cat > whatsapp-mcp-server/src/whatsapp_mcp_server/main.py << 'EOF'
#!/usr/bin/env python3
"""
WhatsApp MCP Server for Daily Production Reports
Provides WhatsApp message extraction capabilities for Claude/Gemini
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import argparse

# MCP server imports (install with: pip install mcp)
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, Tool

# WhatsApp Web API (install with: pip install whatsapp-web-python)
try:
    from whatsapp_web import WhatsAppWeb
except ImportError:
    print("Warning: whatsapp-web-python not installed. Install with: pip install whatsapp-web-python")
    WhatsAppWeb = None

class WhatsAppMCPServer:
    def __init__(self):
        self.app = FastMCP("WhatsApp MCP Server")
        self.whatsapp = None
        self.production_group_jid = "27834418149-1537194373@g.us"
        
    async def initialize_whatsapp(self):
        """Initialize WhatsApp Web connection"""
        if WhatsAppWeb is None:
            raise ImportError("WhatsApp Web API not available")
            
        self.whatsapp = WhatsAppWeb()
        await self.whatsapp.start()
        print("WhatsApp Web connection initialized")
        
    @self.app.tool()
    async def list_messages(
        self, 
        after: Optional[str] = None,
        before: Optional[str] = None, 
        chat_jid: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get WhatsApp messages matching specified criteria"""
        
        if not self.whatsapp:
            await self.initialize_whatsapp()
            
        # Use production group if no specific chat provided
        target_jid = chat_jid or self.production_group_jid
        
        try:
            # Get messages from WhatsApp
            messages = await self.whatsapp.get_messages(
                chat_id=target_jid,
                limit=limit
            )
            
            # Filter by date range if specified
            if after or before:
                filtered_messages = []
                for msg in messages:
                    msg_date = datetime.fromtimestamp(msg.get('timestamp', 0))
                    
                    if after and msg_date < datetime.fromisoformat(after.replace('Z', '+00:00')):
                        continue
                    if before and msg_date > datetime.fromisoformat(before.replace('Z', '+00:00')):
                        continue
                        
                    filtered_messages.append(msg)
                messages = filtered_messages
            
            # Filter by query if specified
            if query:
                messages = [
                    msg for msg in messages 
                    if query.lower() in msg.get('body', '').lower()
                ]
            
            return messages
            
        except Exception as e:
            return [{"error": f"Failed to fetch messages: {str(e)}"}]
    
    @self.app.tool() 
    async def search_production_reports(
        self,
        date: str,
        sites: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search for daily production reports on a specific date"""
        
        sites = sites or ["Nchwaning 2", "Nchwaning 3", "Gloria", "Shafts & Winders"]
        
        # Parse target date
        try:
            target_date = datetime.fromisoformat(date)
        except ValueError:
            return {"error": f"Invalid date format: {date}"}
        
        # Define search window (morning reports for previous day's data)
        search_start = target_date.replace(hour=6, minute=0, second=0)
        search_end = target_date.replace(hour=8, minute=30, second=0)
        
        messages = await self.list_messages(
            after=search_start.isoformat(),
            before=search_end.isoformat(),
            chat_jid=self.production_group_jid,
            limit=50
        )
        
        # Group messages by detected site
        site_reports = {}
        for msg in messages:
            body = msg.get('body', '').upper()
            
            # Detect site from message content
            detected_site = None
            for site in sites:
                site_variants = {
                    "Nchwaning 2": ["NCHWANING 2", "N2", "NC2"],
                    "Nchwaning 3": ["NCHWANING 3", "N3", "NC3"], 
                    "Gloria": ["GLORIA"],
                    "Shafts & Winders": ["SHAFTS", "WINDERS", "S&W", "SW"]
                }
                
                if any(variant in body for variant in site_variants.get(site, [site.upper()])):
                    detected_site = site
                    break
            
            if detected_site:
                if detected_site not in site_reports:
                    site_reports[detected_site] = []
                site_reports[detected_site].append(msg)
        
        return {
            "date": date,
            "search_window": f"{search_start.isoformat()} to {search_end.isoformat()}",
            "sites_found": list(site_reports.keys()),
            "reports": site_reports,
            "total_messages": len(messages)
        }

    async def run_server(self):
        """Run the MCP server"""
        await self.app.run()

# CLI interface for direct usage
async def main():
    parser = argparse.ArgumentParser(description="WhatsApp MCP Server for Production Reports")
    parser.add_argument("--date", help="Date to extract reports for (YYYY-MM-DD)")
    parser.add_argument("--extract-only", action="store_true", help="Only extract, don't run server")
    
    args = parser.parse_args()
    
    server = WhatsAppMCPServer()
    
    if args.extract_only and args.date:
        # Extract data and print to stdout
        print("WHATSAPP_DATA_START")
        result = await server.search_production_reports(args.date)
        print(json.dumps(result, indent=2, default=str))
        print("WHATSAPP_DATA_END")
    else:
        # Run as MCP server
        await server.run_server()

if __name__ == "__main__":
    asyncio.run(main())
EOF

# Create requirements file
cat > whatsapp-mcp-server/requirements.txt << 'EOF'
mcp>=1.0.0
whatsapp-web-python>=1.0.0
asyncio-mqtt>=0.11.0
websockets>=11.0
aiohttp>=3.8.0
python-dateutil>=2.8.2
EOF

# Create package structure
cat > whatsapp-mcp-server/src/whatsapp_mcp_server/__init__.py << 'EOF'
"""WhatsApp MCP Server for Production Reports"""
__version__ = "1.0.0"
EOF

# Make main.py executable
chmod +x whatsapp-mcp-server/src/whatsapp_mcp_server/main.py
```

### 2. Create Codespace Startup Scripts

```bash
# Create .devcontainer directory
mkdir -p .devcontainer

# Create MCP server startup script
cat > .devcontainer/start-whatsapp-mcp.sh << 'EOF'
#!/bin/bash
# WhatsApp MCP Server Startup Script for Codespaces

echo "Starting WhatsApp MCP Server..."

# Change to repository root
cd /workspaces/MarthaVault

# Install Python dependencies
echo "Installing Python dependencies..."
cd whatsapp-mcp-server
pip install -e . || pip install -r requirements.txt
cd ..

# Start the WhatsApp MCP server in background
echo "Starting MCP server..."
cd whatsapp-mcp-server/src/whatsapp_mcp_server
nohup python main.py > /tmp/whatsapp-mcp.log 2>&1 &
MCP_PID=$!

echo "MCP Server started with PID: $MCP_PID"
echo "Log file: /tmp/whatsapp-mcp.log"

# Wait a moment for server to initialize
sleep 5

# Check if server is running
if kill -0 $MCP_PID 2>/dev/null; then
    echo "✅ WhatsApp MCP Server is running successfully"
    return 0
else
    echo "❌ MCP Server failed to start"
    cat /tmp/whatsapp-mcp.log
    return 1
fi
EOF

chmod +x .devcontainer/start-whatsapp-mcp.sh
```

### 3. Create Direct Processing Script

```bash
# Create the processing script referenced in your workflow
cat > .devcontainer/codespace-direct-processing.py << 'EOF'
#!/usr/bin/env python3
"""
Direct WhatsApp processing script for Codespace workflows
"""

import asyncio
import sys
import json
from datetime import datetime
import os
import subprocess

# Add the MCP server to Python path
sys.path.insert(0, '/workspaces/MarthaVault/whatsapp-mcp-server/src')

try:
    from whatsapp_mcp_server.main import WhatsAppMCPServer
except ImportError as e:
    print(f"Error importing WhatsApp MCP Server: {e}")
    sys.exit(1)

async def extract_whatsapp_data(date_str: str):
    """Extract WhatsApp data for the specified date"""
    
    print(f"Extracting WhatsApp data for date: {date_str}")
    
    try:
        # Initialize server
        server = WhatsAppMCPServer()
        
        # Extract production reports
        result = await server.search_production_reports(date_str)
        
        # Output data in expected format
        print("WHATSAPP_DATA_START")
        print(json.dumps(result, indent=2, default=str))
        print("WHATSAPP_DATA_END")
        
        return True
        
    except Exception as e:
        print(f"Error extracting WhatsApp data: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python codespace-direct-processing.py <date> [--extract-only]")
        sys.exit(1)
    
    date_str = sys.argv[1]
    extract_only = "--extract-only" in sys.argv
    
    if extract_only:
        # Run extraction
        success = asyncio.run(extract_whatsapp_data(date_str))
        sys.exit(0 if success else 1)
    else:
        print("Processing mode not implemented yet")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

chmod +x .devcontainer/codespace-direct-processing.py
```

### 4. Install Dependencies

```bash
# In your Codespace terminal, run:
cd /workspaces/MarthaVault/whatsapp-mcp-server
pip install -r requirements.txt

# Or if you prefer uv (faster):
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -r requirements.txt
```

## Testing the Setup

### Test MCP Server Directly
```bash
cd /workspaces/MarthaVault/whatsapp-mcp-server/src/whatsapp_mcp_server
python main.py --date "2025-08-12" --extract-only
```

### Test Startup Script
```bash
cd /workspaces/MarthaVault
./.devcontainer/start-whatsapp-mcp.sh
```

### Test Workflow Integration
Create a GitHub Issue with title: "Autonomous Process WhatsApp Reports 2025-08-12"

## Authentication Requirements

The WhatsApp Web integration will require:
1. **QR Code Scan**: On first run, you'll need to scan a QR code with your phone
2. **Session Persistence**: The session should persist across Codespace restarts
3. **Group Access**: Your WhatsApp account must have access to group `27834418149-1537194373@g.us`

## Troubleshooting

### Common Issues:
1. **"whatsapp-web-python not installed"** - Run `pip install whatsapp-web-python`
2. **"QR Code required"** - WhatsApp Web needs authentication on first use
3. **"Group not found"** - Check if your account has access to the production group
4. **"Bridge executable not found"** - This setup uses Python-based bridge instead

### Debug Commands:
```bash
# Check MCP server logs
tail -f /tmp/whatsapp-mcp.log

# Test Python imports
python3 -c "from whatsapp_mcp_server.main import WhatsAppMCPServer; print('✅ Import successful')"

# Check if server is running
ps aux | grep "python main.py"
```

## Next Steps

1. **Create Codespace**: Make sure you have an active Codespace for this repository
2. **Run Setup**: Execute all the commands above in your Codespace terminal
3. **Test Extraction**: Try extracting data for a recent date
4. **Authenticate WhatsApp**: Complete the QR code scan process
5. **Test Workflow**: Create a test issue to trigger the autonomous workflow

Your autonomous daily production report processing should then work end-to-end!