#!/usr/bin/env python3
"""
Simple test of template-compliant Gemini processing
"""

import google.generativeai as genai
import os
import json

# Configure Gemini
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'your-api-key-here'))
model = genai.GenerativeModel('gemini-1.5-pro')

# Sample July 6 WhatsApp message (from our extraction)
sample_message = """*Central section*
Shift A
Overtime 
5&6/07/2025

*Safety*
Prominent structure noted across 41W support

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
Fire alarms: None
"""

# Template-compliant prompt
site = "Nchwaning 3"
date = "2025-07-06"
engineer = "Sello Sease"

prompt = f"""
You are a mining production report processor that must follow EXACT template compliance.

🎯 CRITICAL: You must follow the official reporting templates EXACTLY. Do not deviate from the structure.

Site: {site}
Date: {date} 
Engineer: {engineer}
Template Type: Standard Mine Site

Raw WhatsApp Content:
{sample_message}

📋 MANDATORY REQUIREMENTS:
1. ✅ Extract ONLY data that exists in the raw content - NEVER fabricate or estimate
2. ✅ Use "Nothing Reported" for missing sections
3. ✅ Follow the EXACT JSON schema from the official templates
4. ✅ Apply correct site-specific requirements
5. ✅ Use proper status indicators: 🟢 (good), ⚠️ (warning), 🔴 (critical)

📄 OUTPUT FORMAT:

You must provide TWO separate outputs:

**1. JSON DATA:**
{{
  "report_metadata": {{
    "date": "{date}",
    "data_date": "{date}",
    "site": "{site}",
    "engineer": "{engineer}",
    "timestamp": "07:30"
  }},
  "safety": {{
    "status": "clear/incident",
    "incidents": 0,
    "details": []
  }},
  "production": {{
    "rom": {{
      "actual": 0,
      "target": 0,
      "variance": 0,
      "variance_percentage": 0.0
    }},
    "product": {{
      "actual": 0,
      "target": 0,
      "variance": 0,
      "variance_percentage": 0.0
    }},
    "loads": [
      {{"shift": "day", "load_number": 1, "truckloads_tipped": 0, "target": 0}},
      {{"shift": "afternoon", "load_number": 2, "truckloads_tipped": 0, "target": 0}},
      {{"shift": "night", "load_number": 3, "truckloads_tipped": 0, "target": 0}}
    ],
    "blast": {{
      "faces": 0,
      "breakdown": "description",
      "note": "details or Nothing Reported"
    }}
  }},
  "equipment_availability": {{
    "tmm": {{
      "DT": 0,
      "FL": 0,
      "HD": 0,
      "RT": 0,
      "SR": 0
    }}
  }},
  "breakdowns": {{
    "current_breakdowns": []
  }},
  "operational": {{
    "main_fans": "operational",
    "plant_blockages": 0,
    "fire_alarms": 0
  }},
  "performance_summary": {{
    "key_issues": [],
    "key_highlights": []
  }}
}}

**2. MARKDOWN REPORT:**

---
JSONData:: [[{date}_nchwaning3.json]]
---

# {site} Daily Report
**Date**: {date} (Data from {date})
**Engineer**: [[{engineer}]]
**Site**: {site}

## [🟢✅🟡⚠️🔴🚨] [STATUS SUMMARY]

### Safety Status
[✅ **CLEAR** - No incidents reported] OR [🔴 **INCIDENT** - [Details]]

### Production Performance
[🟢🟡🔴] **[PERFORMANCE SUMMARY]**

| Metric | Actual | Target | Variance | Performance |
|--------|--------|--------|----------|-------------|
| **ROM** | X,XXXt | X,XXXt | ±XXXt | **XX.X% ([above/below] target)** [🟢⚠️🔴] |
| **Product** | X,XXXt | X,XXXt | ±XXXt | **XX.X% ([above/below] target)** [🟢⚠️🔴] |

#### Load & Haul Fleet Performance (Truckloads Tipped by Shift)
| Shift | Loads | Target | Performance |
|-------|-------|--------|-------------|
| Day | XX | XX | **XX%** [🟢⚠️🔴] |
| Afternoon | XX | XX | **XX%** [🟢⚠️🔴] |
| Night | XX | XX | **XX%** [🟢⚠️🔴] |
| **Total** | **XXX** | **XXX** | **XX%** |

#### Blast Performance
- **[Specific blast data]** OR **Nothing Reported**

### Equipment Status

#### TMM Availability
| Equipment | Availability | Status |
|-----------|-------------|--------|
| **DT** | **XX%** | [🟢✅⚠️🔴] [Status description] |
| **FL** | **XX%** | [🟢✅⚠️🔴] [Status description] |

#### Equipment Readiness (Start of Shift)
- **DT**: X/X available (XX%) [🟢⚠️🔴]
- **FL**: X/X available (XX%) [🟢⚠️🔴]

### Current Breakdowns (X Units)
[List any equipment issues or "None reported"]

### Infrastructure Status
- **Main Fans**: [Status] [🟢🔴] OR **Nothing Reported**
- **Plant Blockages**: [None/Count] [🟢🔴]
- **Fire Alarms**: [None/Active locations] [🟢🔴]

## Performance Summary
- **Safety**: [Status description] [🟢🔴]
- **Production**: [Status description] [🟢🔴⚠️]
- **Equipment**: [Status description] [🟢🔴⚠️]
- **Operations**: [Status description] [🟢🔴⚠️]

---
*Report processed: {date} | Data period: {date} | Source: WhatsApp 07:30*

#daily-production #nchwaning3 #sello-sease #year/2025

🚫 CRITICAL: Extract ONLY data present in the raw WhatsApp content. Use "Nothing Reported" for missing sections. NEVER fabricate data.
"""

if __name__ == "__main__":
    print("🚀 Testing Template-Compliant Gemini Processing...")
    print(f"📊 Processing {site} report for {date}")
    print("📝 Input:", sample_message[:100] + "...")
    
    try:
        response = model.generate_content(prompt)
        print("\n" + "="*80)
        print("🎯 GEMINI RESPONSE:")
        print("="*80)
        print(response.text)
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error: {e}")