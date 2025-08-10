#!/bin/bash
# Batch process missing reports from Codespaces using WhatsApp MCP data

set -e

echo "🚀 Automated WhatsApp Report Processing from Codespaces"
echo "=================================================="

# Ensure we're in the right directory
cd /workspaces/MarthaVault

# Ensure WhatsApp MCP server is running
echo "🔍 Checking WhatsApp MCP server status..."
if ! pgrep -f "whatsapp-mcp" > /dev/null; then
    echo "🔄 Starting WhatsApp MCP server..."
    /workspaces/MarthaVault/.devcontainer/start-whatsapp-mcp.sh
    sleep 10
fi

echo "✅ WhatsApp MCP server is running"

# Function to process a single date
process_date() {
    local date=$1
    echo ""
    echo "📅 Processing date: $date"
    echo "------------------------"
    
    python3 /workspaces/MarthaVault/.devcontainer/extract-whatsapp-reports.py "$date"
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully triggered processing for $date"
        # Wait a bit between requests to avoid rate limiting
        sleep 30
    else
        echo "❌ Failed to process $date"
    fi
}

# Main processing function
main() {
    local target_date=""
    
    # Check if specific date provided
    if [ $# -eq 1 ]; then
        target_date=$1
        echo "🎯 Processing specific date: $target_date"
        process_date "$target_date"
        return
    fi
    
    # Auto-detect missing dates
    echo "🤖 Auto-detecting missing dates..."
    
    # Use smart detection script
    missing_dates_json=$(python3 /workspaces/MarthaVault/.devcontainer/auto-detect-missing-reports.py --json)
    
    if [ -z "$missing_dates_json" ] || [ "$missing_dates_json" = "[]" ]; then
        echo "✅ No missing dates detected"
        echo "📊 All recent reports appear to be up to date"
        return
    fi
    
    # Parse JSON array into bash array
    readarray -t missing_dates < <(echo "$missing_dates_json" | python3 -c "
import sys, json
dates = json.load(sys.stdin)
for date in dates:
    print(date)
")
    
    if [ ${#missing_dates[@]} -eq 0 ]; then
        echo "✅ No dates require processing"
        return
    fi
    
    echo "📋 Auto-detected ${#missing_dates[@]} missing dates:"
    printf "  - %s\n" "${missing_dates[@]}"
    echo ""
    
    # Ask for confirmation
    read -p "🤔 Process these dates? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "⏸️ Processing cancelled"
        return
    fi
    
    echo "🚀 Starting batch processing..."
    
    for date in "${missing_dates[@]}"; do
        process_date "$date"
    done
    
    echo ""
    echo "🎉 Batch processing completed!"
    echo "📊 Processed ${#missing_dates[@]} dates"
    echo "🔍 Check GitHub Actions for workflow progress"
}

# Usage information
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage:"
    echo "  $0                    # Process all missing July dates"
    echo "  $0 YYYY-MM-DD        # Process specific date"
    echo "  $0 --help            # Show this help"
    exit 0
fi

# Run main function
main "$@"