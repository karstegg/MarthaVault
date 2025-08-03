# Standard Mine Site Report Template

**Applies to**: Nchwaning 2, Nchwaning 3, Gloria  
**Use this template** for all daily production reports from mine sites  

## Markdown Template Structure

```markdown
---
JSONData:: [[YYYY-MM-DD_[site].json]]
---

# [Site Name] Daily Report
**Date**: Month DD, YYYY (Data from Month DD, YYYY)  
**Engineer**: [[Engineer Name]]  
**Site**: [Site Name]  

## [🟢✅🟡⚠️🔴🚨] [STATUS SUMMARY]

### Safety Status
[✅ **CLEAR** - No incidents reported] OR [🔴 **INCIDENT** - [Details]]

### Production Performance
[🟢🟡🔴] **[PERFORMANCE SUMMARY]**

| Metric | Actual | Target | Variance | Performance |
|--------|--------|--------|----------|-------------|
| **ROM** | X,XXXt | X,XXXt | ±XXXt | **XX.X% ([above/below] target)** [🟢⚠️🔴] |
| **Decline** | X,XXXt | X,XXXt | ±XXXt | **XX.X% ([above/below] target)** [🟢⚠️🔴] |
| **Product** | X,XXXt | X,XXXt | ±XXXt | **XX.X% ([above/below] target)** [🟢⚠️🔴] |

#### Load & Haul Fleet Performance (Truckloads Tipped by Shift)
| Shift | Loads | Target | Performance |
|-------|-------|--------|-------------|
| Day | XX | XX | **XX%** [🟢⚠️🔴] |
| Afternoon | XX | XX | **XX%** [🟢⚠️🔴] |
| Night | XX | XX | **XX%** [🟢⚠️🔴] |
| **Total** | **XXX** | **XXX** | **XX%** |

[Additional load performance details, staging information, or shift-specific notes]

#### Blast Performance
- **[Specific blast data]** OR **Nothing Reported**

### Equipment Status

#### TMM Availability
| Equipment | Availability | Status |
|-----------|-------------|---------|
| **DT** | **XX%** | [🟢✅⚠️🔴] [Status description] |
| **FL** | **XX%** | [🟢✅⚠️🔴] [Status description] |
| **HD** | **XX%** | [🟢✅⚠️🔴] [Status description] |
| **RT** | **XX%** | [🟢✅⚠️🔴] [Status description] |
| **SR** | **XX%** | [🟢✅⚠️🔴] [Status description] |

**Poor Performance Analysis:**
- **[Equipment Type]**: [Specific reasons for low availability - maintenance issues, breakdowns, etc.]
- **[Equipment Type]**: [Specific reasons for low availability]

#### Equipment Readiness (Start of Shift)
- **DT**: X/X available (XX%) [🟢⚠️🔴]
- **FL**: X/X available (XX%) [🟢⚠️🔴]
- **HD**: X/X available (XX%) [🟢⚠️🔴]
- **RT**: X/X available (XX%) [🟢⚠️🔴]
- **SR**: X/X available (XX%) [🟢⚠️🔴]

### Current Breakdowns (X Units)

#### [Equipment Type] Equipment Issues
- **[Unit ID]**: [Issue description]
- **[Unit ID]**: [Issue description]

#### [Equipment Type] Equipment Issues
- **[Unit ID]**: [Issue description]

### Support Equipment Summary
- **Emulsion UV**: XX% [🟢⚠️🔴] OR **Nothing Reported**
- **Logistics UV**: XX% [🟢⚠️🔴] OR **Nothing Reported**
- **Sampling UV**: XX% [🟢⚠️🔴] OR **Nothing Reported**
- **Survey UV**: XX% [🟢⚠️🔴] OR **Nothing Reported**
- **Specialized Equipment**: [Equipment Name] XX% [🟢🔴] [Status]
- **Specialized Equipment**: [Equipment Name] XX% [🟢🔴] [Status]

### Infrastructure Status
- **Main Fans**: [Status] [🟢🔴] OR **Nothing Reported**
- **Plant Blockages**: [None/Count] [🟢🔴]
- **Fire Alarms**: [None/Active locations] [🟢🔴]

## Performance Summary
- **Safety**: [Status description] [🟢🔴]
- **Production**: [Status description] [🟢🔴⚠️]
- **Equipment**: [Status description] [🟢🔴⚠️]
- **Operations**: [Status description] [🟢🔴⚠️]

## Supplemental Information

### Silo Management (Gloria Only)
#### Surface Silos
| Silo | Level | Status |
|------|-------|--------|
| Silo 1 | XX% | [🟢⚠️🔴] [Status] |
| Silo 2 | XX% | [🟢⚠️🔴] [Status] |
| Silo 3 | XX% | [🟢⚠️🔴] [Status] |
| Silo 4 | XX% | [🟢⚠️🔴] [Status] |

#### Underground Silos
| Silo | Level | Status |
|------|-------|--------|
| Silo 74 | XX% | [🟢⚠️🔴] [Status] |
| Silo HG | XX% | [🟢⚠️🔴] [Status] |
| Silo D | XX% | [🟢⚠️🔴] [Status] |
| Silo LG | XX% | [🟢⚠️🔴] [Status] |

### [Additional Site-Specific Information]
[Any other site-specific details, equipment notes, or operational context]

---
*Report processed: YYYY-MM-DD | Data period: YYYY-MM-DD | Source: WhatsApp HH:MM*

#daily-production #[site-tag] #[status-tag] #[engineer-tag] #year/YYYY
```

## JSON Template Structure

```json
{
  "report_metadata": {
    "date": "YYYY-MM-DD",
    "data_date": "YYYY-MM-DD",
    "site": "Site Name",
    "engineer": "Engineer Name",
    "timestamp": "HH:MM"
  },
  "safety": {
    "status": "clear/incident",
    "incidents": 0,
    "details": []
  },
  "production": {
    "rom": {
      "actual": 0,
      "target": 0,
      "variance": 0,
      "variance_percentage": 0.0
    },
    "decline": {
      "actual": 0,
      "target": 0,
      "variance": 0,
      "variance_percentage": 0.0
    },
    "product": {
      "actual": 0,
      "target": 0,
      "variance": 0,
      "variance_percentage": 0.0
    },
    "loads": [
      {"shift": "day", "load_number": 1, "truckloads_tipped": 0, "target": 0},
      {"shift": "afternoon", "load_number": 2, "truckloads_tipped": 0, "target": 0},
      {"shift": "night", "load_number": 3, "truckloads_tipped": 0, "target": 0}
    ],
    "blast": {
      "faces": 0,
      "breakdown": "description",
      "note": "details or Nothing Reported"
    }
  },
  "equipment_availability": {
    "tmm": {
      "DT": 0,
      "FL": 0,
      "HD": 0,
      "RT": 0,
      "SR": 0
    },
    "specialized": [
      {"code": "equipment_code", "availability": 0}
    ]
  },
  "shift_readiness": {
    "production_tmm": {
      "DT": {"available": 0, "total": 0},
      "FL": {"available": 0, "total": 0},
      "HD": {"available": 0, "total": 0},
      "RT": {"available": 0, "total": 0},
      "SR": {"available": 0, "total": 0}
    }
  },
  "breakdowns": {
    "current_breakdowns": [
      {"unit": "unit_id", "issue": "description"}
    ]
  },
  "operational": {
    "main_fans": "status",
    "plant_blockages": 0,
    "fire_alarms": 0
  },
  "performance_summary": {
    "key_issues": [],
    "key_highlights": []
  }
}
```

## Site-Specific Additions

### Gloria Mine JSON Additions
```json
"silo_levels": {
  "surface": {
    "silo_1": 0, "silo_2": 0, "silo_3": 0, "silo_4": 0
  },
  "underground": {
    "silo_74": 0, "silo_hg": 0, "silo_d": 0, "silo_lg": 0
  }
},
"specialized_equipment": {
  "manitou": {"available": 0, "total": 1, "availability": 0},
  "manlifts": {"available": 0, "total": 0, "availability": 0}
}
```

## Usage Guidelines

### Status Icons & Colors
- **🟢✅** = Good/Excellent/Operational
- **🟡⚠️** = Warning/Below optimal/Attention needed  
- **🔴** = Critical/Problem/Below threshold
- **🚨** = Emergency/Safety incident/Immediate action

### Priority Levels
- **🔴 URGENT** = Immediate action required
- **🔴 HIGH** = High priority action  
- **⚠️ MEDIUM** = Medium priority attention
- **📊 FOLLOW-UP** = Monitoring/data gathering required
- **📋 ROUTINE** = Standard operational task

### Missing Information Protocol
- Use **"Nothing Reported"** for any missing sections
- Maintain section structure even if no data available
- Add site-specific elements to Supplemental Information

### Equipment Readiness Note
- Refers to equipment availability, **NOT staffing levels**
- Shows how many machines are available vs total fleet size
- Example: "6/9 available (67%)" means 6 machines available out of 9 total

### Load Performance Understanding
- **Load 1** = **Day Shift** truckloads tipped by load & haul fleet
- **Load 2** = **Afternoon Shift** truckloads tipped by load & haul fleet
- **Load 3** = **Night Shift** truckloads tipped by load & haul fleet
- Always specify "truckloads" and "by shift" for clarity

#daily-production #templates #mine-sites #nchwaning2 #nchwaning3 #gloria #year/2025