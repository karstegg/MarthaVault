#!/usr/bin/env python3
"""
Gemini Integration Script for WhatsApp Production Reports
Connects GitHub extraction workflow to Gemini processing pipeline
"""

import google.generativeai as genai
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

def setup_gemini():
    """Configure Gemini API"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-pro')

def get_template_prompt(site, date, engineer, raw_content):
    """Generate template-compliant processing prompt"""
    
    # Determine template type and specific requirements
    if site.lower() in ['nchwaning 2', 'nchwaning 3', 'gloria']:
        template_type = "Standard Mine Site"
        schema_additions = ""
        
        if site.lower() == 'gloria':
            schema_additions = """
            "silo_levels": {
              "surface": {
                "silo_1": 0, "silo_2": 0, "silo_3": 0, "silo_4": 0
              },
              "underground": {
                "silo_74": 0, "silo_hg": 0, "silo_d": 0, "silo_lg": 0
              }
            },
            "specialized_equipment": {
              "manitou": {"available": 0, "total": 1, "availability": 0}
            },"""
    else:
        template_type = "Shafts & Winders"
        schema_additions = """
            "infrastructure": {
              "power_supply": {"stoppages": 0, "status": "operational"},
              "winders": {
                "nch2_pw": {"status": "operational", "operational": true, "type": "manwinder"},
                "nch3_pw": {"status": "operational", "operational": true, "type": "manwinder"},
                "gl_pw": {"status": "operational", "operational": true, "type": "manwinder"},
                "nch2_rw": {"status": "operational", "operational": true, "type": "rock_winder"}
              },
              "main_fans": {
                "gloria": {"status": "operational", "operational": true},
                "nchwaning2": {"status": "operational", "operational": true},
                "nchwaning3": {"status": "operational", "operational": true}
              }
            },
            "dam_levels": {
              "dd01": {"level": 0.0, "status": "good"},
              "dd02": {"level": 0.0, "status": "good"}
            },"""

    return f"""
You are a mining production report processor with CRITICAL data accuracy requirements.

🚨 MANDATORY: You must extract ONLY data that exists in the raw WhatsApp content. NEVER fabricate or estimate values.

Site: {site}
Date: {date}
Engineer: {engineer}
Template Type: {template_type}

Raw WhatsApp Content:
{raw_content}

📋 PROCESSING REQUIREMENTS:
1. ✅ Extract ONLY actual data from the WhatsApp message
2. ✅ Use null for missing numeric values
3. ✅ Use "Nothing Reported" for missing sections
4. ✅ Include source validation for all major figures
5. ✅ Follow exact JSON schema requirements

📊 DATA EXTRACTION GUIDELINES:
- **Safety**: Look for incident reports or confirm "clear" status
- **Production**: Extract ROM, Product, Decline with actual vs target
- **Equipment**: Parse TMM availability percentages and breakdowns
- **Loads**: Extract truckload counts by shift (Day/Afternoon/Night)
- **Blast**: Extract blast data or mark "Nothing Reported"
- **Infrastructure**: Power, fans, alarms status

🎯 EXACT JSON OUTPUT REQUIRED:
{{
  "report_metadata": {{
    "date": "{date}",
    "data_date": "{date}",
    "site": "{site}",
    "engineer": "{engineer}",
    "timestamp": "extracted_time_or_07:30",
    "processing_method": "gemini_automated"
  }},
  "safety": {{
    "status": "clear_or_incident",
    "incidents": 0,
    "details": []
  }},
  "production": {{
    "rom": {{
      "actual": null,
      "target": null,
      "variance": null,
      "variance_percentage": null
    }},
    "decline": {{
      "actual": null,
      "target": null,
      "variance": null,
      "variance_percentage": null
    }},
    "product": {{
      "actual": null,
      "target": null,
      "variance": null,
      "variance_percentage": null
    }},
    "loads": [
      {{"shift": "day", "load_number": 1, "truckloads_tipped": null, "target": null}},
      {{"shift": "afternoon", "load_number": 2, "truckloads_tipped": null, "target": null}},
      {{"shift": "night", "load_number": 3, "truckloads_tipped": null, "target": null}}
    ],
    "blast": {{
      "faces": null,
      "breakdown": "Nothing Reported",
      "note": "Nothing Reported"
    }}
  }},
  "equipment_availability": {{
    "tmm": {{
      "DT": null,
      "FL": null,
      "HD": null,
      "RT": null,
      "SR": null,
      "UV": null
    }},
    "specialized": []
  }},
  "shift_readiness": {{
    "production_tmm": {{
      "DT": {{"available": null, "total": null}},
      "FL": {{"available": null, "total": null}},
      "HD": {{"available": null, "total": null}},
      "RT": {{"available": null, "total": null}},
      "SR": {{"available": null, "total": null}},
      "UV": {{"available": null, "total": null}}
    }}
  }},
  "breakdowns": {{
    "current_breakdowns": []
  }},
  "operational": {{
    "main_fans": "operational",
    "plant_blockages": 0,
    "fire_alarms": 0
  }},{schema_additions}
  "source_validation": {{
    "rom_actual": {{
      "value": null,
      "source_line": "line_number_or_null",
      "source_quote": "exact_text_or_null",
      "confidence": "HIGH|MEDIUM|LOW|NONE"
    }},
    "equipment_dt": {{
      "value": null,
      "source_line": "line_number_or_null", 
      "source_quote": "exact_text_or_null",
      "confidence": "HIGH|MEDIUM|LOW|NONE"
    }},
    "validation_notes": "Any data extraction notes or concerns"
  }},
  "performance_summary": {{
    "key_issues": [],
    "key_highlights": [],
    "data_completeness": "percentage_of_expected_fields_with_data"
  }}
}}

🚫 CRITICAL: Return ONLY the JSON object. No markdown, no explanations, just the JSON.
"""

def process_extracted_data(model, input_file, output_dir):
    """Process a single extracted JSON file through Gemini"""
    
    print(f"📊 Processing: {input_file.name}")
    
    # Load extracted data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get required metadata
    metadata = data.get('report_metadata', {})
    site = metadata.get('site', 'Unknown')
    date = metadata.get('report_date', metadata.get('date', 'Unknown'))
    engineer = metadata.get('engineer', 'Unknown')
    
    # Get raw WhatsApp content
    raw_content = data.get('raw_content', '')
    if not raw_content:
        print(f"❌ No raw content found in {input_file.name}")
        return False
    
    # Generate processing prompt
    prompt = get_template_prompt(site, date, engineer, raw_content)
    
    try:
        # Process with Gemini
        print(f"🤖 Sending to Gemini-1.5-Pro...")
        response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text.strip()
        
        # Clean up response (remove any markdown formatting)
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # Parse JSON
        processed_data = json.loads(response_text.strip())
        
        # Create output filename
        output_file = output_dir / f"gemini_processed_{input_file.name}"
        
        # Save processed data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Processed: {output_file.name}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error for {input_file.name}: {e}")
        print(f"Raw response: {response.text[:200]}...")
        return False
    except Exception as e:
        print(f"❌ Processing error for {input_file.name}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Process WhatsApp extraction data through Gemini')
    parser.add_argument('--input-dir', default='daily_production/data', 
                       help='Directory containing extracted JSON files')
    parser.add_argument('--output-dir', default='daily_production/gemini_processed',
                       help='Directory for processed output files')
    parser.add_argument('--date-filter', help='Process only files for specific date (YYYY-MM-DD)')
    parser.add_argument('--site-filter', help='Process only files for specific site')
    parser.add_argument('--test-mode', action='store_true', help='Process only first file found')
    
    args = parser.parse_args()
    
    # Setup directories
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return 1
    
    # Setup Gemini
    try:
        model = setup_gemini()
        print("✅ Gemini-1.5-Pro configured")
    except Exception as e:
        print(f"❌ Gemini setup failed: {e}")
        return 1
    
    # Find files to process
    pattern = "*.json"
    if args.date_filter:
        pattern = f"*{args.date_filter}*.json"
    if args.site_filter:
        pattern = f"*{args.site_filter.lower().replace(' ', '_')}*.json"
    
    files_to_process = list(input_dir.rglob(pattern))
    
    if not files_to_process:
        print(f"❌ No files found matching pattern: {pattern}")
        return 1
    
    if args.test_mode:
        files_to_process = files_to_process[:1]
        print(f"🧪 Test mode: processing only {files_to_process[0].name}")
    
    print(f"📂 Found {len(files_to_process)} files to process")
    
    # Process files
    success_count = 0
    total_count = len(files_to_process)
    
    for file_path in files_to_process:
        if process_extracted_data(model, file_path, output_dir):
            success_count += 1
    
    # Summary
    print(f"\n📈 Processing Summary:")
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count > 0:
        print(f"📁 Output directory: {output_dir}")
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())