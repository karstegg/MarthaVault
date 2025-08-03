# Shafts & Winders Report Template

**Applies to**: Mine Winders, Shafts, and Main Fans across all three mine sites  
**Engineer**: [[Xavier Peterson]]  
**Responsibility**: Manwinders, Rock Winder (Nchwaning 2 ore hoisting), and Main Fans infrastructure  
**Use this template** for all Shafts & Winders daily/weekly reports  

## Markdown Template Structure

```markdown
---
JSONData:: [[YYYY-MM-DD_shafts_winders.json]]
---

# Shafts & Winders [Daily/Weekly] Report
**Date**: Month DD, YYYY ([Report Type] - Data [period])  
**Engineer**: [[Xavier Peterson]]  

## [🟢✅🟡⚠️🔴] [INFRASTRUCTURE STATUS SUMMARY]

### Safety Status
✅ **CLEAR** - No incidents reported

### Infrastructure Status
[🟢🟡🔴] **[SYSTEMS STATUS SUMMARY]**

#### Power Supply
- **Status**: [No Stoppages/Issues] [🟢🔴]
- **Operational**: [Description]

#### Winders (All Sites)
| Winder | Site | Type | Status |
|--------|------|------|--------|
| **Nch2 PW** | Nchwaning 2 | Manwinder | [🟢🔴] [Status] |
| **Nch3 PW** | Nchwaning 3 | Manwinder | [🟢🔴] [Status] |
| **GL PW** | Gloria | Manwinder | [🟢🔴] [Status] |
| **Nch2 RW** | Nchwaning 2 | Rock Winder (Ore Hoisting) | [🟢🔴] [Status] |

#### Main Fans (All Sites)
| Site | Status |
|------|--------|
| **Gloria** | [🟢🔴] [Status] |
| **Nchwaning 2** | [🟢🔴] [Status] |
| **Nchwaning 3** | [🟢🔴] [Status] |

#### Lamprooms (All Sites)
| Site | Status |
|------|--------|
| **Gloria** | [🟢🔴] [Status] |
| **Nchwaning 2** | [🟢🔴] [Status] |
| **Nchwaning 3** | [🟢🔴] [Status] |

### Water Management

#### Dam Levels ([Daily/Weekly] Tracking)
| Dam | [Day/Period] | Status |
|-----|-------------|--------|
| **DD01** | **XX.X%** | [🟢⚠️🔴] [Status] |
| **DD02** | **XX.X%** | [🟢⚠️🔴] [Status] |

#### Ore Pass Levels
- **[Day/Period]**: XX.X%
- **[Tracking Period]**: [Description/trend]

### Production [Daily/Weekly] Performance

#### [Daily Production Summary / Weekly Production Schedule]
| Day | Actual | Target | Variance | Performance | Status |
|-----|--------|--------|----------|-------------|--------|
| **[Day]** | **X,XXXt** | **X,XXXt** | **±XXXt** | **XXX.X%** | [🟢⚠️🔴] [Status] |

### Operational Status
- **Fire SCADA Alarms**: [Count] [🟢🔴]
- **Block Chutes**: [None/Count] [🟢🔴]

## Actions Required

1. **[⚠️📊📋] [PRIORITY]**: [Action description]
2. **[⚠️📊📋] [PRIORITY]**: [Action description]


## Supplemental Information

### Department Responsibilities
**Shafts & Winders** manages critical infrastructure across all three mine sites:
- **Manwinders**: Personnel transport systems (Nch2 PW, Nch3 PW, GL PW)
- **Rock Winder**: Nchwaning 2 ore hoisting from underground to surface silos (Nch2 RW)
- **Main Fans**: Ventilation systems essential for underground safety
- **Support Infrastructure**: Power supply, lamprooms, and related systems

### [Weekly Infrastructure Overview / Daily Details]
- **Power Systems**: [Status] [🟢🔴]
- **Winding Systems**: [Status] [🟢🔴]
- **Ventilation**: [Status] [🟢🔴]
- **Safety Systems**: [Status] [🟢🔴]
- **Water Management**: [Status] [🟢🔴]

### [Analysis/Trends Section]
[Detailed analysis of patterns, trends, or specific technical details]

---
*Report processed: YYYY-MM-DD | Data period: [period] | Source: WhatsApp HH:MM*

#daily-production #shafts-winders #infrastructure #xavier-peterson #[status-tag] #year/YYYY
```

## JSON Template Structure

```json
{
  "report_metadata": {
    "date": "YYYY-MM-DD",
    "data_date": "YYYY-MM-DD",
    "site": "Shafts & Winders",
    "engineer": "Xavier Peterson",
    "timestamp": "HH:MM",
    "report_type": "Daily/Weekly Report"
  },
  "safety": {
    "status": "clear",
    "incidents": 0,
    "details": []
  },
  "infrastructure": {
    "power_supply": {
      "stoppages": 0,
      "status": "operational"
    },
    "winders": {
      "nch2_pw": {"status": "operational/issues", "operational": true, "type": "manwinder"},
      "nch3_pw": {"status": "operational/issues", "operational": true, "type": "manwinder"},
      "gl_pw": {"status": "operational/issues", "operational": true, "type": "manwinder"},
      "nch2_rw": {"status": "operational/issues", "operational": true, "type": "rock_winder", "function": "ore_hoisting"}
    },
    "main_fans": {
      "gloria": {"status": "operational/issues", "operational": true},
      "nchwaning2": {"status": "operational/issues", "operational": true},
      "nchwaning3": {"status": "operational/issues", "operational": true}
    },
    "lamprooms": {
      "gloria": {"status": "operational/issues", "operational": true},
      "nchwaning2": {"status": "operational/issues", "operational": true},
      "nchwaning3": {"status": "operational/issues", "operational": true}
    }
  },
  "dam_levels": {
    "dd01": {
      "level": 0.0,
      "status": "good/warning/critical"
    },
    "dd02": {
      "level": 0.0,
      "status": "good/warning/critical"
    }
  },
  "ore_pass_levels": {
    "current_level": 0.0,
    "trend": "stable/declining/improving"
  },
  "production": {
    "daily_summary": [
      {
        "day": "day_name",
        "actual": 0,
        "target": 0,
        "variance": 0,
        "variance_percentage": 0.0
      }
    ]
  },
  "operational": {
    "fire_scada_alarms": 0,
    "block_chutes": 0
  },
  "performance_summary": {
    "key_issues": [],
    "key_highlights": []
  }
}
```

## Weekly vs Daily Report Variations

### Weekly Report Format
For comprehensive weekly infrastructure summaries:

#### Extended Dam Level Tracking
```markdown
#### Dam Levels (Complete Weekly Data)
| Dam | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Status |
|-----|-----|-----|-----|-----|-----|-----|-----|--------|
| **DD01** | XX.X% | XX.X% | XX.X% | XX.X% | XX.X% | XX.X% | XX.X% | [🟢⚠️🔴] |
| **DD02** | XX.X% | XX.X% | XX.X% | XX.X% | XX.X% | XX.X% | XX.X% | [🟢⚠️🔴] |
```

#### Extended Production Schedule
```markdown
#### Weekly Production Schedule
| Day | Actual | Target | Variance | Performance | Status |
|-----|--------|--------|----------|-------------|--------|
| Monday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
| Tuesday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
| Wednesday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
| Thursday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
| Friday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
| Saturday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
| Sunday | X,XXXt | X,XXXt | ±XXXt | XXX.X% | [🟢⚠️🔴] |
```

### Daily Report Format
For focused daily infrastructure status:

#### Simplified Tables
- Single day focus with yesterday/today/tomorrow context
- Abbreviated equipment status tables
- Highlight of daily issues only

## Extended JSON for Weekly Reports

```json
{
  "dam_levels": {
    "dd01": {
      "monday": 0.0, "tuesday": 0.0, "wednesday": 0.0, "thursday": 0.0,
      "friday": 0.0, "saturday": 0.0, "sunday": 0.0
    },
    "dd02": {
      "monday": 0.0, "tuesday": 0.0, "wednesday": 0.0, "thursday": 0.0,
      "friday": 0.0, "saturday": 0.0, "sunday": 0.0
    }
  },
  "ore_pass_levels": {
    "monday": 0.0, "tuesday": 0.0, "wednesday": 0.0, "thursday": 0.0,
    "friday": 0.0, "saturday": 0.0, "sunday": 0.0
  },
  "production": {
    "weekly_schedule": {
      "monday": {"actual": 0, "target": 0, "variance": 0},
      "tuesday": {"actual": 0, "target": 0, "variance": 0},
      "wednesday": {"actual": 0, "target": 0, "variance": 0},
      "thursday": {"actual": 0, "target": 0, "variance": 0},
      "friday": {"actual": 0, "target": 0, "variance": 0},
      "saturday": {"actual": 0, "target": 0, "variance": 0},
      "sunday": {"actual": 0, "target": 0, "variance": 0}
    }
  }
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

### Infrastructure Focus Areas

#### Critical Systems Monitoring
1. **Power Supply** - Any stoppages affect all operations
2. **Winders** - Essential for material transport
3. **Main Fans** - Critical for ventilation safety
4. **Lamprooms** - Safety and communication systems

#### Water & Materials Management
1. **Dam Levels** - DD01 (primary), DD02 (secondary)
2. **Ore Pass Levels** - Material flow indicators
3. **Production Coordination** - Support for mine operations

### Missing Information Protocol
- Use **"Nothing Reported"** for any missing sections
- Maintain section structure even if no data available
- Add infrastructure-specific details to Supplemental Information

### Special Notes for S&W Reports
- **Weekly reports** typically more comprehensive than daily
- **Infrastructure focus** rather than equipment breakdowns
- **System reliability** metrics emphasized
- **Cross-site coordination** details important

#daily-production #templates #shafts-winders #infrastructure #xavier-peterson #year/2025