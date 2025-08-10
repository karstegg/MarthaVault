#!/usr/bin/env python3
"""
Test the Codespace direct processing system for August 9th
This tests the complete pipeline: WhatsApp MCP → Gemini → Reports → Git
"""

import sys
import os
import subprocess
from datetime import datetime

def test_codespace_processing():
    """Test the complete Codespace processing pipeline"""
    
    target_date = "2025-08-09"
    
    print("🧪 TESTING CODESPACE DIRECT PROCESSING")
    print("=" * 50)
    print(f"Target Date: {target_date}")
    print(f"Test Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Check if we're in the right environment
    codespaces_env = os.getenv('CODESPACES')
    if codespaces_env:
        print(f"✅ Running in Codespaces: {codespaces_env}")
    else:
        print("⚠️  Not in Codespaces - will test with simulated data")
    
    # Check required environment variables
    print("\n🔍 Environment Check:")
    required_vars = ['GEMINI_API_KEY', 'GITHUB_TOKEN']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {'*' * (len(value) - 8) + value[-8:]}")
        else:
            print(f"  ❌ {var}: Not found")
    
    # Check if WhatsApp MCP server is running
    print("\n📱 WhatsApp MCP Server Check:")
    try:
        result = subprocess.run(['pgrep', '-f', 'whatsapp-mcp'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("  ✅ WhatsApp MCP server is running")
        else:
            print("  ⚠️  WhatsApp MCP server not detected (will use simulated data)")
    except:
        print("  ⚠️  Cannot check MCP server status (will use simulated data)")
    
    # Execute the processing script
    print(f"\n🚀 Running Codespace Direct Processing for {target_date}...")
    print("-" * 50)
    
    try:
        # Change to the repository root
        repo_root = "/workspaces/MarthaVault" if codespaces_env else "C:/Users/10064957/My Drive/GDVault/MarthaVault"
        
        if codespaces_env:
            os.chdir(repo_root)
            script_path = ".devcontainer/codespace-direct-processing.py"
        else:
            script_path = os.path.join(repo_root, ".devcontainer", "codespace-direct-processing.py")
        
        # Run the processing script
        result = subprocess.run([
            'python3' if codespaces_env else 'python',
            script_path,
            target_date
        ], capture_output=True, text=True, timeout=600)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n🎉 SUCCESS: Codespace processing completed!")
            return True
        else:
            print(f"\n❌ FAILED: Processing returned code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n⏱️ TIMEOUT: Processing took too long (10+ minutes)")
        return False
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        return False

def verify_results(target_date="2025-08-09"):
    """Verify that the processing created the expected files"""
    
    print("\n🔍 VERIFYING RESULTS:")
    print("-" * 30)
    
    codespaces_env = os.getenv('CODESPACES')
    repo_root = "/workspaces/MarthaVault" if codespaces_env else "C:/Users/10064957/My Drive/GDVault/MarthaVault"
    
    # Check expected file locations
    date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    year_month = date_obj.strftime("%Y-%m")
    day = date_obj.strftime("%d")
    
    expected_dir = os.path.join(repo_root, "daily_production", "data", year_month, day)
    
    expected_files = [
        f"{target_date}_gloria.json",
        f"{target_date}_nchwaning3.json", 
        f"{target_date}_shafts-winders.json",
        f"{target_date} - Gloria Daily Report.md",
        f"{target_date} - Nchwaning 3 Daily Report.md",
        f"{target_date} - Shafts & Winders Daily Report.md"
    ]
    
    print(f"📂 Expected directory: {expected_dir}")
    
    if os.path.exists(expected_dir):
        print("✅ Report directory exists")
        
        for filename in expected_files:
            filepath = os.path.join(expected_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✅ {filename} ({size} bytes)")
            else:
                print(f"  ❌ {filename} (missing)")
    else:
        print("❌ Report directory does not exist")
    
    # Check git status
    try:
        os.chdir(repo_root)
        result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                              capture_output=True, text=True)
        print(f"\n📝 Recent commits:")
        for line in result.stdout.split('\n')[:3]:
            if line.strip():
                print(f"  {line}")
    except:
        print("⚠️  Could not check git status")

def main():
    print("🎯 CODESPACE DIRECT PROCESSING TEST")
    print("This tests the complete autonomous pipeline:")
    print("  1. WhatsApp MCP data extraction")
    print("  2. Gemini processing with correct templates")
    print("  3. Structured report generation") 
    print("  4. Git commit and push")
    print()
    
    success = test_codespace_processing()
    
    if success:
        verify_results()
        print("\n🏆 TEST PASSED: Codespace direct processing works!")
    else:
        print("\n❌ TEST FAILED: Review the output above for issues")
        
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())