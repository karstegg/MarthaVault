#!/usr/bin/env python3
"""
Direct Gemini processing for 2025-07-17 WhatsApp production data
"""

import google.generativeai as genai
import json
import os
from datetime import datetime

def setup_gemini():
    """Configure Gemini API"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-pro')

def read_source_data(filename):
    """Read the WhatsApp source data"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def identify_site_from_content(content):
    """Identify which site the message is from based on content"""
    if 'Gloria Report' in content or 'leaving Gloria' in content:
        return 'Gloria', 'Sipho Dubazane'
    elif 'S&W' in content and 'Shafts & Winders' in content:
        return 'Shafts & Winders', 'Xavier Peterson'
    elif 'Nchwaning 3' in content or '120363204285087803@g.us' in content:
        return 'Nchwaning 3', 'Sello Sease'
    elif 'N2' in content or 'Nchwaning 2' in content:
        return 'Nchwaning 2', 'Sikilela Nzuza'
    else:
        return 'Unknown', 'Unknown'

def extract_individual_reports(content):
    """Extract individual reports from the combined content"""
    reports = []
    
    # Split by message boundaries
    messages = content.split('Message ')
    
    for message in messages[1:]:  # Skip the header
        lines = message.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Extract timestamp and content
        header = lines[0].strip(':')
        message_content = '\n'.join(lines[1:])
        
        # Skip very short messages or non-production messages
        if len(message_content) < 50:
            continue
            
        # Skip birthday messages and other non-production content
        if 'Happy Birthday' in message_content or 'hunting' in message_content.lower():
            continue
            
        site, engineer = identify_site_from_content(message_content)
        
        if site != 'Unknown':
            reports.append({
                'site': site,
                'engineer': engineer,
                'content': message_content,
                'timestamp': header
            })
    
    return reports

def get_processing_prompt(site, date, engineer, content):
    """Generate site-specific processing prompt"""
    
    # Set correct data date (report received 17th contains 16th data)
    data_date = "2025-07-16"
    
    if site.lower() in ['gloria']:
        schema_additions = '''
            "silo_levels": {
              "surface": {
                "silo_1": null, "silo_2": null, "silo_3": null, "silo_4": null
              },
              "underground": {
                "silo_74": null, "silo_hg": null, "silo_d": null, "silo_lg": null
              }
            },'''
    elif site.lower() == 'shafts & winders':
        schema_additions = '''
            "infrastructure": {
              "power_supply": {"stoppages": 0, "status": "operational"},
              "winders": {
                "nch2_pw": {"status": "operational", "operational": true},
                "nch3_pw": {"status": "operational", "operational": true},
                "gl_pw": {"status": "operational", "operational": true},
                "nch2_rw": {"status": "operational", "operational": true}
              },
              "main_fans": {
                "gloria": {"status": "operational", "operational": true},
                "nchwaning2": {"status": "operational", "operational": true},
                "nchwaning3": {"status": "operational", "operational": true}
              }
            },
            "dam_levels": {
              "dd01": {"level": null, "status": "unknown"},
              "dd02": {"level": null, "status": "unknown"}
            },
            "ore_pass_levels": {
              "level": null,
              "status": "unknown"
            },'''
    else:
        schema_additions = ''

    return f"""
You are a mining production report processor with CRITICAL data accuracy requirements.

MANDATORY: Extract ONLY data that exists in the raw WhatsApp content. NEVER fabricate values.

Site: {site}
Report Date: {date} (when report was received)
Data Date: {data_date} (operations data from previous day)
Engineer: {engineer}

CRITICAL EQUIPMENT CODES:
- RT = Roof Bolter (NOT Rock Truck - no such equipment exists)
- DT = Dump Truck
- FL = Front Loader  
- HD = Hydraulic Drill
- SR = Scaler

Raw WhatsApp Content:
{content}

PROCESSING REQUIREMENTS:
1. Extract ONLY actual data from the WhatsApp message
2. Use null for missing numeric values
3. Include source validation with line numbers and exact quotes
4. Follow equipment code validation (RT = Roof Bolter)
5. Use correct dating (report_date={date}, data_date={data_date})

OUTPUT EXACT JSON:
{{
  "report_metadata": {{
    "date": "{date}",
    "data_date": "{data_date}",
    "site": "{site}",
    "engineer": "{engineer}",
    "timestamp": "extracted_from_message",
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
    }}
  }},
  "shift_readiness": {{
    "production_tmm": {{
      "DT": {{"available": null, "total": null}},
      "FL": {{"available": null, "total": null}},
      "HD": {{"available": null, "total": null}},
      "RT": {{"available": null, "total": null}},
      "SR": {{"available": null, "total": null}}
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
      "source_line": null,
      "source_quote": null,
      "confidence": "NONE"
    }},
    "equipment_dt": {{
      "value": null,
      "source_line": null,
      "source_quote": null,
      "confidence": "NONE"
    }},
    "validation_notes": "Data extraction notes"
  }},
  "performance_summary": {{
    "key_issues": [],
    "key_highlights": [],
    "data_completeness": "percentage_estimate"
  }}
}}

Return ONLY the JSON object. No markdown, no explanations.
"""

def process_report(model, site, engineer, content, date):
    """Process a single report through Gemini"""
    
    print(f"Processing {site} report from {engineer}...")
    
    prompt = get_processing_prompt(site, date, engineer, content)
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # Parse JSON
        processed_data = json.loads(response_text.strip())
        
        return processed_data
        
    except Exception as e:
        print(f"Error processing {site}: {e}")
        return None

def create_markdown_report(json_data, output_file):
    """Create markdown report from JSON data"""
    
    metadata = json_data['report_metadata']
    safety = json_data['safety']
    production = json_data['production']
    equipment = json_data['equipment_availability']
    operational = json_data['operational']
    
    site = metadata['site']
    date = metadata['date']
    engineer = metadata['engineer']
    data_date = metadata['data_date']
    
    content = f"""# {date} – {site} Daily Report

## Report Metadata
- **Site**: {site}
- **Engineer**: {engineer}
- **Report Date**: {date}
- **Data Date**: {data_date} (previous day operations)
- **Processing**: {metadata['processing_method']}

## Safety Status
- **Status**: {safety['status']}
- **Incidents**: {safety['incidents']}

## Production Summary
### ROM Production
- **Actual**: {production['rom']['actual']} tons
- **Target**: {production['rom']['target']} tons
- **Variance**: {production['rom']['variance']} tons

### Product Production
- **Actual**: {production['product']['actual']} tons
- **Target**: {production['product']['target']} tons
- **Variance**: {production['product']['variance']} tons

### Decline Production
- **Actual**: {production['decline']['actual']} tons
- **Target**: {production['decline']['target']} tons
- **Variance**: {production['decline']['variance']} tons

## Equipment Availability
- **Dump Trucks (DT)**: {equipment['tmm']['DT']}%
- **Front Loaders (FL)**: {equipment['tmm']['FL']}%
- **Hydraulic Drills (HD)**: {equipment['tmm']['HD']}%
- **Roof Bolters (RT)**: {equipment['tmm']['RT']}%
- **Scalers (SR)**: {equipment['tmm']['SR']}%

## Operational Status
- **Main Fans**: {operational['main_fans']}
- **Plant Blockages**: {operational['plant_blockages']}
- **Fire Alarms**: {operational['fire_alarms']}

## Data Validation
- **Validation Notes**: {json_data['source_validation']['validation_notes']}
- **Data Completeness**: {json_data['performance_summary']['data_completeness']}

## Key Issues
{chr(10).join(f"- {issue}" for issue in json_data['performance_summary']['key_issues'])}

## Key Highlights
{chr(10).join(f"- {highlight}" for highlight in json_data['performance_summary']['key_highlights'])}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("Processing 2025-07-17 WhatsApp production data with Gemini...")
    
    # Setup
    model = setup_gemini()
    source_file = "temp_whatsapp_2025-07-17.txt"
    date = "2025-07-17"
    
    # Read source data
    content = read_source_data(source_file)
    
    # Extract individual reports
    reports = extract_individual_reports(content)
    
    print(f"Found {len(reports)} production reports to process")
    
    # Create output directories
    os.makedirs("daily_production/data/2025-07/17", exist_ok=True)
    
    # Process each report
    processed_count = 0
    for report in reports:
        site = report['site']
        engineer = report['engineer']
        content = report['content']
        
        # Process with Gemini
        processed_data = process_report(model, site, engineer, content, date)
        
        if processed_data:
            # Save JSON
            site_safe = site.lower().replace(' ', '_').replace('&', 'and')
            json_file = f"daily_production/data/2025-07/17/2025-07-17_{site_safe}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            
            # Save Markdown
            md_file = f"daily_production/data/2025-07/17/2025-07-17 – {site} Daily Report.md"
            create_markdown_report(processed_data, md_file)
            
            print(f"✅ Created {json_file}")
            print(f"✅ Created {md_file}")
            processed_count += 1
        else:
            print(f"❌ Failed to process {site}")
    
    print(f"\nProcessing complete: {processed_count}/{len(reports)} reports processed")
    
    # Clean up temporary file
    if os.path.exists(source_file):
        os.remove(source_file)
        print(f"🗑️ Cleaned up {source_file}")

if __name__ == "__main__":
    main()