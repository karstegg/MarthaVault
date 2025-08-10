#!/usr/bin/env python3
"""
Execute August 9th report processing using the complete Codespace pipeline
This demonstrates the autonomous system working end-to-end
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    target_date = "2025-08-09"
    
    print("🚀 AUTONOMOUS AUGUST 9TH REPROCESSING")
    print("=" * 50)
    print()
    print("🎯 What this does:")
    print("  ✅ Extracts live WhatsApp messages from MCP server")
    print("  ✅ Processes with Gemini using correct Report Templates")
    print("  ✅ Creates structured JSON and Markdown reports")
    print("  ✅ Commits directly to master branch")
    print("  ✅ Overwrites existing incorrect August 9th files")
    print()
    
    # Check environment
    codespaces_env = os.getenv('CODESPACES')
    if not codespaces_env:
        print("❌ This script must run in GitHub Codespaces")
        print("💡 The WhatsApp MCP server is only available in Codespaces")
        return 1
    
    print(f"✅ Running in Codespaces: {codespaces_env}")
    
    # Check required tools
    gemini_key = os.getenv('GEMINI_API_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found")
        return 1
    if not github_token:
        print("❌ GITHUB_TOKEN not found")
        return 1
        
    print("✅ Environment variables configured")
    
    # Change to repository root
    repo_root = "/workspaces/MarthaVault"
    os.chdir(repo_root)
    
    # Ensure we're on master branch
    print("\n🌿 Ensuring master branch...")
    try:
        subprocess.run(['git', 'checkout', 'master'], check=True)
        subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
        print("✅ On master branch and up to date")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operations failed: {e}")
        return 1
    
    # Run the direct processing
    print(f"\n🔄 Running Codespace direct processing for {target_date}...")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            'python3',
            '.devcontainer/codespace-direct-processing.py',
            target_date
        ], check=True, text=True)
        
        print("✅ Processing completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Processing failed: {e}")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return 1
    
    # Verify results
    print("\n🔍 Verifying results...")
    
    # Check for created files
    date_path = f"daily_production/data/2025-08/09"
    expected_files = [
        f"{target_date}_gloria.json",
        f"{target_date}_nchwaning3.json",
        f"{target_date}_shafts-winders.json",
        f"{target_date} - Gloria Daily Report.md",
        f"{target_date} - Nchwaning 3 Daily Report.md", 
        f"{target_date} - Shafts & Winders Daily Report.md"
    ]
    
    all_exist = True
    for filename in expected_files:
        filepath = f"{date_path}/{filename}"
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✅ {filename} ({size} bytes)")
        else:
            print(f"  ❌ {filename} (missing)")
            all_exist = False
    
    if all_exist:
        print("\n🎉 SUCCESS: All expected files created!")
        
        # Show recent commit
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                  capture_output=True, text=True)
            print(f"\n📝 Latest commit:")
            print(f"  {result.stdout.strip()}")
        except:
            pass
            
        print("\n✅ Autonomous August 9th processing completed successfully!")
        print("\n🔗 Results available at:")
        print("  - Local files: daily_production/data/2025-08/09/")
        print("  - GitHub: https://github.com/karstegg/MarthaVault/tree/master/daily_production/data/2025-08/09")
        
        return 0
    else:
        print("\n❌ Some files were not created - check the processing output")
        return 1

if __name__ == "__main__":
    sys.exit(main())