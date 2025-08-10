#!/bin/bash
# WhatsApp MCP Server Startup Script
# Works with existing WhatsApp MCP installation in Codespaces

set -e

echo "🚀 Starting WhatsApp MCP Server..."

# Find existing WhatsApp MCP installation
SERVER_PATH=""
POSSIBLE_PATHS=(
    "/workspaces/MarthaVault/whatsapp-mcp-server"
    "/workspaces/whatsapp-mcp-server" 
    "/workspaces/whatsapp-mcp"
)

for path in "${POSSIBLE_PATHS[@]}"; do
    if [ -d "$path" ]; then
        SERVER_PATH="$path"
        echo "✅ Found WhatsApp MCP at: $SERVER_PATH"
        break
    fi
done

if [ -z "$SERVER_PATH" ]; then
    echo "❌ WhatsApp MCP server not found in expected locations:"
    printf "  - %s\n" "${POSSIBLE_PATHS[@]}"
    echo ""
    echo "🔧 Please ensure WhatsApp MCP is installed in Codespaces"
    echo "💡 Or update this script with the correct path"
    exit 1
fi

# Check if server is already running
if pgrep -f "whatsapp.*mcp" > /dev/null; then
    echo "✅ WhatsApp MCP server is already running"
    echo "📊 Status: $(pgrep -af "whatsapp.*mcp" | head -1)"
    exit 0
fi

# Check for required files
if [ ! -f "$SERVER_PATH/main.py" ] && [ ! -f "$SERVER_PATH/whatsapp_mcp/server.py" ]; then
    echo "❌ Server files not found in $SERVER_PATH"
    echo "📋 Expected: main.py or whatsapp_mcp/server.py"
    exit 1
fi

# Start the MCP server
echo "🖥️ Starting WhatsApp MCP server..."
cd "$SERVER_PATH"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Try different startup methods based on what's available
if [ -f "main.py" ]; then
    echo "📱 Starting via main.py..."
    nohup python main.py > /tmp/whatsapp-mcp-server.log 2>&1 &
elif [ -f "whatsapp_mcp/server.py" ]; then
    echo "📱 Starting via module..."
    nohup python -m whatsapp_mcp.server > /tmp/whatsapp-mcp-server.log 2>&1 &
else
    echo "❌ No valid startup file found"
    exit 1
fi

SERVER_PID=$!
echo $SERVER_PID > /tmp/whatsapp-mcp-server.pid

# Wait for startup
sleep 5

# Verify server is running
if pgrep -p $SERVER_PID > /dev/null 2>&1; then
    echo "✅ WhatsApp MCP server started successfully!"
    echo "🖥️ Server PID: $SERVER_PID"
    echo "📋 Log: /tmp/whatsapp-mcp-server.log"
    echo "🔧 To stop: kill $SERVER_PID"
    
    # Save PID for management
    echo "$SERVER_PID" > /tmp/whatsapp-mcp.pid
    
    # Show some log output
    echo "📄 Recent log output:"
    tail -5 /tmp/whatsapp-mcp-server.log 2>/dev/null || echo "No log output yet"
    
else
    echo "❌ Server failed to start"
    echo "📋 Check log: cat /tmp/whatsapp-mcp-server.log"
    exit 1
fi