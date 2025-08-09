#!/bin/bash
echo "Setting up WhatsApp MCP..."
git clone https://github.com/lharries/whatsapp-mcp.git
cd whatsapp-mcp/whatsapp-bridge
go build -o bridge main.go
cd ../whatsapp-mcp-server
pip install -r requirements.txt
echo "Setup complete!"