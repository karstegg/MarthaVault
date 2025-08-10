#!/bin/bash
# WhatsApp MCP Server Setup for Codespaces
# Checks existing installation and only sets up what's missing

set -e

echo "🔍 Checking WhatsApp MCP Server setup..."

# Check if WhatsApp MCP is already installed in the expected location
EXISTING_MCP_PATH="/workspaces/MarthaVault/whatsapp-mcp-server"
EXISTING_MCP_GLOBAL="/workspaces/whatsapp-mcp-server"
EXISTING_MCP_ROOT="/workspaces/whatsapp-mcp"

MCP_PATH=""

# Find existing WhatsApp MCP installation
if [ -d "$EXISTING_MCP_PATH" ]; then
    MCP_PATH="$EXISTING_MCP_PATH"
    echo "✅ Found existing WhatsApp MCP at: $MCP_PATH"
elif [ -d "$EXISTING_MCP_GLOBAL" ]; then
    MCP_PATH="$EXISTING_MCP_GLOBAL"
    echo "✅ Found existing WhatsApp MCP at: $MCP_PATH"
elif [ -d "$EXISTING_MCP_ROOT" ]; then
    MCP_PATH="$EXISTING_MCP_ROOT"
    echo "✅ Found existing WhatsApp MCP at: $MCP_PATH"
else
    echo "❌ No existing WhatsApp MCP installation found"
    echo "📋 Expected locations:"
    echo "  - $EXISTING_MCP_PATH"
    echo "  - $EXISTING_MCP_GLOBAL"
    echo "  - $EXISTING_MCP_ROOT"
    echo ""
    echo "⚠️ Please ensure WhatsApp MCP is installed in Codespaces first"
    echo "🔧 Or update this script with the correct path"
    exit 1
fi

# Create symlink for standardized access if needed
STANDARD_PATH="/workspaces/MarthaVault/whatsapp-mcp-server"
if [ "$MCP_PATH" != "$STANDARD_PATH" ] && [ ! -L "$STANDARD_PATH" ]; then
    echo "🔗 Creating symlink for standardized access..."
    ln -sf "$MCP_PATH" "$STANDARD_PATH"
    echo "✅ Symlink created: $STANDARD_PATH -> $MCP_PATH"
fi

# Ensure dependencies are installed
echo "🐍 Checking Python dependencies..."
cd "$MCP_PATH"
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found in $MCP_PATH"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Virtual environment already exists"
fi

# Create session directory for WhatsApp authentication
mkdir -p /workspaces/sessions/whatsapp
chmod 755 /workspaces/sessions/whatsapp

# Create service configuration
echo "⚙️ Creating service configuration..."
cat > /tmp/whatsapp-mcp-config.json << EOF
{
    "whatsapp_mcp": {
        "server_path": "$MCP_PATH",
        "standard_path": "$STANDARD_PATH",
        "log_level": "INFO",
        "auto_restart": true,
        "session_dir": "/workspaces/sessions/whatsapp"
    }
}
EOF

echo "✅ WhatsApp MCP setup verified!"
echo "📋 Configuration:"
echo "  - MCP Server: $MCP_PATH"
echo "  - Standard Link: $STANDARD_PATH"
echo "  - Sessions: /workspaces/sessions/whatsapp/"
echo "  - Config: /tmp/whatsapp-mcp-config.json"
echo ""
echo "🚀 Ready to start WhatsApp MCP server"