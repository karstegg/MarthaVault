#!/bin/bash

# Codespace Gemini Listener
# This script runs in your codespace to process WhatsApp reports via repository dispatch events

echo "Starting WhatsApp Report Processing Listener..."

# Function to process reports
process_reports() {
    local date=$1
    local message=$2
    
    echo "Processing reports for date: $date"
    echo "Message: $message"
    
    # Set environment variables
    export GEMINI_API_KEY=$GEMINI_API_KEY
    
    # Change to the repository directory
    cd /workspaces/MarthaVault
    
    # Run Gemini with the WhatsApp MCP server
    echo "Running Gemini..."
    gemini --yolo --prompt "$message"
    
    echo "Processing complete!"
}

# Listen for repository dispatch events (simplified version)
# In practice, you could use GitHub webhooks or polling
echo "Listener ready. Run this script periodically or set up webhook handling."
echo "For manual execution, call: process_reports 'date' 'message'"

# Example usage (uncomment to test manually):
# process_reports "08/08/2025" "Process WhatsApp production reports for date: 08/08/2025. Engineers by site: Nchwaning 2: Johan Kotze, Nchwaning 3: Sello Sease, Gloria: Sipho Dubazane, Shafts & Winders: Xavier Peterson. Extract data from WhatsApp group: 27834418149-1537194373@g.us using the running WhatsApp MCP server. Create JSON files: daily_production/data/YYYY-MM-DD_[site].json. Create Markdown: daily_production/YYYY-MM-DD – [Site] Daily Report.md. Follow CLAUDE.md Section 10.1 requirements."