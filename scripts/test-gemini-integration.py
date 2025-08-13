#!/usr/bin/env python3
"""
Test Script for Local Gemini Integration
Validates the integration pipeline before running on GitHub Actions
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("🔧 Environment Check:")
    
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        print("✅ GEMINI_API_KEY is set")
        # Check if it looks like a valid key (starts with expected prefix)
        if gemini_key.startswith('AI'):
            print("✅ API key format looks correct")
        else:
            print("⚠️ API key format may be incorrect")
    else:
        print("❌ GEMINI_API_KEY not set")
        print("   Set it with: export GEMINI_API_KEY='your-api-key'")
        return False
    
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Dependencies Check:")
    
    required_packages = [
        'google.generativeai',
        'json',
        'pathlib',
        'argparse'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('.', '-'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Install missing packages:")
        print("   pip install google-generativeai")
        return False
    
    return True

def check_integration_script():
    """Check if our integration script exists and is valid"""
    print("\n📄 Integration Script Check:")
    
    script_path = Path("scripts/integrate-gemini-processing.py")
    
    if script_path.exists():
        print(f"✅ Integration script found: {script_path}")
        
        # Check script content
        with open(script_path, 'r') as f:
            content = f.read()
            
        if 'setup_gemini' in content:
            print("✅ Gemini setup function found")
        else:
            print("❌ Gemini setup function missing")
            return False
            
        if 'get_template_prompt' in content:
            print("✅ Template prompt function found")
        else:
            print("❌ Template prompt function missing")
            return False
            
        return True
    else:
        print(f"❌ Integration script not found: {script_path}")
        return False

def check_sample_data():
    """Check if we have sample data to test with"""
    print("\n📊 Sample Data Check:")
    
    data_dir = Path("daily_production/data")
    
    if data_dir.exists():
        json_files = list(data_dir.rglob("*.json"))
        if json_files:
            print(f"✅ Found {len(json_files)} JSON files for testing")
            print(f"   Sample: {json_files[0].name}")
            return True
        else:
            print("❌ No JSON files found in daily_production/data")
    else:
        print("❌ daily_production/data directory not found")
    
    # Create mock data for testing
    print("💡 Creating mock test data...")
    create_mock_data()
    return True

def create_mock_data():
    """Create mock test data for validation"""
    
    mock_dir = Path("test_data")
    mock_dir.mkdir(exist_ok=True)
    
    mock_data = {
        "report_metadata": {
            "site": "Nchwaning 3",
            "engineer": "Sello Sease",
            "report_date": "2025-07-06",
            "data_date": "2025-07-06",
            "extraction_timestamp": "2025-07-06T08:00:00Z",
            "message_count": 1
        },
        "raw_content": """*Central section*
Shift A
Overtime 
6/07/2025

*Safety*
All clear

*Production*
ROM: 5545 v 6904t (-1359t)
Product: 2359 v 6634t (-4275t)

*Equipment*
DT: 9/9 available (100%)
FL: 6/6 available (100%)

*Blast*
Nothing reported

*Operational*
Plant blockages: None
Fire alarms: None""",
        "individual_messages": [
            {
                "timestamp": "2025-07-06T07:30:00Z",
                "chat_jid": "120363204285087803@g.us",
                "sender": "27123456789@s.whatsapp.net",
                "content": "Central section report...",
                "site": "Nchwaning 3",
                "report_date": "2025-07-06"
            }
        ]
    }
    
    test_file = mock_dir / "2025-07-06_nchwaning3_test.json"
    
    import json
    with open(test_file, 'w') as f:
        json.dump(mock_data, f, indent=2)
    
    print(f"✅ Created mock test file: {test_file}")

def run_test_processing():
    """Run a test processing with mock data"""
    print("\n🧪 Test Processing:")
    
    # Import our integration script
    sys.path.append('scripts')
    
    try:
        from pathlib import Path
        import subprocess
        
        # Run the integration script on test data
        cmd = [
            sys.executable, 
            "scripts/integrate-gemini-processing.py",
            "--input-dir", "test_data",
            "--output-dir", "test_output",
            "--test-mode"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Test processing completed successfully")
            print("Output:")
            print(result.stdout)
            
            # Check if output was created
            output_dir = Path("test_output")
            if output_dir.exists():
                output_files = list(output_dir.glob("*.json"))
                if output_files:
                    print(f"✅ Generated {len(output_files)} output files")
                    return True
                else:
                    print("❌ No output files generated")
            else:
                print("❌ Output directory not created")
        else:
            print("❌ Test processing failed")
            print("Error output:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Test processing error: {e}")
    
    return False

def main():
    """Run all validation checks"""
    print("🚀 Gemini Integration Validation")
    print("=" * 50)
    
    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_dependencies),
        ("Integration Script", check_integration_script),
        ("Sample Data", check_sample_data),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n✅ All checks passed! Running test processing...")
        if run_test_processing():
            print("\n🎉 Integration validation successful!")
            print("\n📋 Next Steps:")
            print("1. Commit the integration script and workflow")
            print("2. Test the GitHub Actions workflow manually")
            print("3. Process actual July 6-21 data")
        else:
            print("\n❌ Test processing failed")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())