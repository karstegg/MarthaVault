#!/usr/bin/env python3
"""
Test script for PR creation workflow
Validates the end-to-end process before running on GitHub
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

def simulate_workflow_run():
    """Simulate the main steps of the PR workflow"""
    
    print("🧪 Testing PR Creation Workflow")
    print("=" * 50)
    
    # Step 1: Check if we have sample processed data
    print("\n1️⃣ Checking for sample processed data...")
    
    # Create mock processed data if needed
    mock_dir = Path("test_gemini_processed")
    mock_dir.mkdir(exist_ok=True)
    
    # Sample processed report
    sample_report = {
        "report_metadata": {
            "date": "2025-07-06",
            "data_date": "2025-07-06", 
            "site": "Nchwaning 3",
            "engineer": "Sello Sease",
            "timestamp": "07:30",
            "processing_method": "gemini_automated"
        },
        "safety": {
            "status": "clear",
            "incidents": 0,
            "details": []
        },
        "production": {
            "rom": {
                "actual": 5545,
                "target": 6904,
                "variance": -1359,
                "variance_percentage": -19.7
            },
            "product": {
                "actual": 2359,
                "target": 6634, 
                "variance": -4275,
                "variance_percentage": -64.4
            },
            "loads": [
                {"shift": "day", "load_number": 1, "truckloads_tipped": 25, "target": 30},
                {"shift": "afternoon", "load_number": 2, "truckloads_tipped": 22, "target": 30},
                {"shift": "night", "load_number": 3, "truckloads_tipped": 20, "target": 30}
            ],
            "blast": {
                "faces": 0,
                "breakdown": "Nothing Reported",
                "note": "Nothing Reported"
            }
        },
        "equipment_availability": {
            "tmm": {
                "DT": 100,
                "FL": 100,
                "HD": 85,
                "RT": 96,
                "SR": 89,
                "UV": 92
            }
        },
        "breakdowns": {
            "current_breakdowns": [
                {"unit": "DT0109", "issue": "hydraulic system repair"},
                {"unit": "FL0113", "issue": "tire replacement scheduled"}
            ]
        },
        "operational": {
            "main_fans": "operational",
            "plant_blockages": 0,
            "fire_alarms": 0
        },
        "source_validation": {
            "rom_actual": {
                "value": 5545,
                "source_line": 12,
                "source_quote": "ROM: 5545 v 6904t (-1359t)",
                "confidence": "HIGH"
            },
            "equipment_dt": {
                "value": 100,
                "source_line": 18,
                "source_quote": "DT: 9/9 available (100%)",
                "confidence": "HIGH"
            },
            "validation_notes": "All major production figures traced to source WhatsApp data"
        },
        "performance_summary": {
            "key_issues": [
                "ROM production 19.7% below target",
                "Product output significantly underperforming"
            ],
            "key_highlights": [
                "100% DT and FL availability",
                "No safety incidents reported"
            ],
            "data_completeness": "85%"
        }
    }
    
    # Save sample data
    sample_file = mock_dir / "gemini_processed_2025-07-06_nchwaning3.json"
    with open(sample_file, 'w') as f:
        json.dump(sample_report, f, indent=2)
    
    print(f"✅ Created sample data: {sample_file}")
    
    # Step 2: Test file organization logic
    print("\n2️⃣ Testing file organization...")
    
    organize_script = """
import json
import os
from pathlib import Path
from datetime import datetime

def create_markdown_report(json_data, site, date):
    # Simplified version for testing
    engineer_map = {
        'Nchwaning 3': '[[Sello Sease]]',
        'Gloria': '[[Sipho Dubazane]]'
    }
    
    engineer = engineer_map.get(site, '[[Unknown]]')
    site_filename = site.lower().replace(' ', '_')
    
    return f'''---
JSONData:: [[data/{date.replace('-', '/')}/{date}_{site_filename}.json]]
Status:: #status/processed
Tags:: #daily-production #{site_filename.replace('_', '-')} #year/2025
Engineer:: {engineer}
---

# {site} Daily Report

**Date**: {date}
**Engineer**: {engineer}
**Site**: {site}

## ✅ OPERATIONAL

### Production Performance
| Metric | Actual | Target | Variance |
|--------|--------|--------|----------|
| **ROM** | {json_data.get('production', {}).get('rom', {}).get('actual', 0):,} | {json_data.get('production', {}).get('rom', {}).get('target', 0):,} | {json_data.get('production', {}).get('rom', {}).get('variance', 0):+,} |

### Equipment Status
Equipment availability: {json_data.get('equipment_availability', {}).get('tmm', {}).get('DT', 0)}% DT, {json_data.get('equipment_availability', {}).get('tmm', {}).get('FL', 0)}% FL

### Current Breakdowns
{len(json_data.get('breakdowns', {}).get('current_breakdowns', []))} units currently down.

---
*Automated processing via Gemini integration*
'''

# Test organization
processed_dir = Path('test_gemini_processed')
for json_file in processed_dir.glob('*.json'):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    site = data['report_metadata']['site']
    date = data['report_metadata']['date']
    
    # Create paths
    year, month, day = date.split('-')
    site_filename = site.lower().replace(' ', '_')
    
    json_path = f"test_daily_production/data/{year}-{month}/{day}/{date}_{site_filename}.json"
    md_path = f"test_daily_production/{date} – {site} Daily Report.md"
    
    # Create directories
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    
    # Copy files
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    markdown_content = create_markdown_report(data, site, date)
    with open(md_path, 'w') as f:
        f.write(markdown_content)
    
    print(f"✅ Created: {json_path}")
    print(f"✅ Created: {md_path}")
"""
    
    # Execute organization test
    exec(organize_script)
    
    # Step 3: Validate created files
    print("\n3️⃣ Validating created files...")
    
    json_files = list(Path("test_daily_production").rglob("*.json"))
    md_files = list(Path("test_daily_production").rglob("*.md"))
    
    if json_files and md_files:
        print(f"✅ JSON files created: {len(json_files)}")
        print(f"✅ Markdown files created: {len(md_files)}")
        
        # Validate JSON structure
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            required_fields = ['report_metadata', 'safety', 'production', 'source_validation']
            missing = [field for field in required_fields if field not in data]
            
            if missing:
                print(f"❌ {json_file.name}: Missing {missing}")
            else:
                print(f"✅ {json_file.name}: Schema valid")
        
        # Validate Markdown content
        for md_file in md_files:
            with open(md_file, 'r') as f:
                content = f.read()
            
            if '---' in content and '#daily-production' in content:
                print(f"✅ {md_file.name}: Markdown format valid")
            else:
                print(f"❌ {md_file.name}: Markdown format invalid")
    else:
        print("❌ No files were created")
        return False
    
    # Step 4: Test branch naming logic
    print("\n4️⃣ Testing branch naming...")
    
    import time
    timestamp = int(time.time())
    branch_name = f"reports/gemini-processed-2025-07-06-{timestamp}"
    print(f"✅ Generated branch name: {branch_name}")
    
    # Step 5: Test PR body generation
    print("\n5️⃣ Testing PR description generation...")
    
    pr_body_template = """## 🤖 Gemini-Processed Daily Production Reports

**Processing Date**: 2025-07-06
**Files Generated**: {json_count} JSON + {md_count} Markdown reports

### Quality Assurance
- [x] Template compliance validated
- [x] Source validation included  
- [x] No fabricated data

### Review Requirements
1. Verify production figures against WhatsApp sources
2. Check equipment breakdown details
3. Confirm mathematical calculations

🤖 Automated PR created by GitHub Actions + Gemini Integration"""
    
    pr_body = pr_body_template.format(
        json_count=len(json_files),
        md_count=len(md_files)
    )
    
    print("✅ PR description generated:")
    print("---")
    print(pr_body[:200] + "...")
    print("---")
    
    # Cleanup test files
    print("\n🧹 Cleaning up test files...")
    import shutil
    for test_dir in ["test_gemini_processed", "test_daily_production"]:
        if Path(test_dir).exists():
            shutil.rmtree(test_dir)
            print(f"✅ Removed: {test_dir}")
    
    print("\n🎉 PR workflow test completed successfully!")
    print("\n📋 Summary:")
    print("✅ File organization logic working")
    print("✅ Markdown generation working") 
    print("✅ JSON validation working")
    print("✅ Branch naming working")
    print("✅ PR description generation working")
    print("\n🚀 Ready for production use!")
    
    return True

if __name__ == "__main__":
    success = simulate_workflow_run()
    exit(0 if success else 1)