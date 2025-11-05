---
'Status:': Draft
'Priority:': High
'Assignee:': Greg
'Date:': 2025-09-08
'Tags:': null
permalink: operations/bevs/weekly-reports/2025-08-28-brmo-week-4-battery-and-charger-analysis
---

# BRMO Week 4 Battery and Charger Analysis - August 28 - September 3, 2025

**Source**: BRMO Weekly Report LIVE (Philip Moller, Epiroc)  
**Analysis Date**: September 8, 2025  
**Report Period**: August 28 - September 3, 2025

## 🔋 Battery Status Summary

### ST14 - B4 Battery Packs
- **Current Inventory**: 10 x ST14-B4 battery packs
- **Active Machines**: 6 x ST14 machines operational underground
- **Battery Ratio**: 1.6 batteries per machine (meets committed ratio)
- **Status**: Meeting minimum requirements but no buffer capacity

### MT42 - B5 Battery Packs  
- **Current Inventory**: 12 x MT42-B5 battery packs operational underground
- **Battery Ratio**: Above committed 1.6 ratio (surplus capacity)
- **Status**: Adequate inventory levels

## 🔌 Charger Infrastructure Crisis

### 160 kW Chargers - Critical Failures
| Charger | Module | Status | Issue |
|---------|---------|---------|--------|
| **Charger 4** | Module 1 | 🔴 **REMOVED** | Module faulty, needs replacement |
| **Charger 5** | Module 4 | 🔴 **REMOVED** | Module faulty, needs replacement |
| **Charger 7** | One Module | 🟡 **SWITCHED OFF** | Trips mini sub breaker when switched on |
| **Charger 8** | One Module | 🟡 **SWITCHED OFF** | Trips mini sub breaker when switched on |

### CCS Connector Cable Issues
- **Posts 3, 6, and 7**: CCS connector cables require replacement
- **Root Cause**: Worn out charger and CCS battery inlet connectors
- **Impact**: Increased charger stops and reduced charging efficiency

## 📊 Detailed Battery Pack Status (Week 4)

### ST14-B4 Battery Packs Status
| Battery ID | Status | Comment |
|------------|---------|---------|
| VPY-00011 | ✅ **Working** | Operational |
| VPY-00031 | 🔴 **Breakdown** | TMS replacement required - waiting for parts |
| VPY-00051 | ✅ **Working** | Operational |
| VPY-00048 | ✅ **Working** | Operational |
| VPY-00049 | ✅ **Working** | Operational |
| VPY-00088 | ✅ **Working** | Operational |
| VPY-00086 | ✅ **Working** | Operational |
| VPY-00076 | ✅ **Working** | Operational |
| VPY-00083 | ✅ **Working** | Operational |
| VPY-00041 | ✅ **Working** | Operational |

**Summary**: 9/10 ST14 batteries operational (90% availability)

### MT42-B5 Battery Packs Status
| Battery ID | Status | Comment |
|------------|---------|---------|
| VPX-00016 | ✅ **Working** | Underground operational |
| VPX-00015 | 🟡 **Surface** | Waiting to go underground |
| VPX-00023 | ✅ **Working** | Underground operational |
| VPX-00017 | ✅ **Working** | Underground operational |
| VPX-00010 | ✅ **Working** | Underground operational |
| VPX-00050 | ✅ **Working** | Underground operational |
| VPX-00031 | ✅ **Working** | Underground operational |
| VPX-00036 | ✅ **Working** | Underground operational |
| VPX-00028 | ✅ **Working** | Underground operational |
| VPX-00026 | ✅ **Working** | Underground operational |
| VPX-00024 | ✅ **Working** | Underground operational |
| VPX-00048 | ✅ **Working** | Underground operational |
| VPX-00044 | 🟡 **Surface** | On machine 8997901500 |

**Summary**: 10/12 MT42 batteries underground operational, 2 on surface (83% deployed)

## ⚡ Key Breakdown Analysis - Battery Related Issues

### Critical Battery/Electrical Breakdowns (Week 4)

#### FL108 - Main Battery Power Loss
- **Date**: Thursday, August 28 (Night shift)
- **Issue**: Female pins on X10:1 faulty, causing main battery to lose 24V
- **Action**: Harness replacement required, temporarily fixed
- **Downtime**: 4D20H34min (4 days, 20 hours, 34 minutes)
- **Impact**: **CRITICAL** - Extended multi-day breakdown

#### FL113 - BMS Error  
- **Date**: Wednesday, September 3 (Afternoon shift)
- **Issue**: Battery Management System error
- **Action**: Reset BMS error
- **Downtime**: 43 minutes
- **Impact**: Manageable - quick resolution

#### DT147 - Battery Connection Failure
- **Date**: Wednesday, September 3 (Afternoon shift)  
- **Issue**: Battery not connecting to system
- **Action**: Changed battery pack
- **Downtime**: 49 minutes
- **Impact**: Resolved with spare battery

#### DT171 - High Voltage System Issues
- **Date**: Tuesday, September 2 (Morning shift)
- **Issue**: D510 Module Sensor Voltage Error X12, short circuit cable to bucket down proxy
- **Downtime**: 22H41min (22 hours, 41 minutes)
- **Impact**: **SEVERE** - Nearly full day lost

- **Date**: Wednesday, September 3 (Afternoon shift)
- **Issue**: High voltage plug pin stuck inside connector
- **Action**: Pin extracted
- **Downtime**: 8H46min (8 hours, 46 minutes)
- **Impact**: **MAJOR** - Extended electrical repair

## ⚠️ Infrastructure Issues and Trends

### Charging Infrastructure Challenges
1. **Module Failures**: 2 charger modules failed and removed for replacement
2. **Electrical Issues**: 2 charger modules switched off due to breaker trips  
3. **Cable Wear**: 3 CCS connector cables scheduled for replacement
4. **Net Impact**: Reduced charging module capacity requiring management

### Battery-Related Maintenance Issues
- **Week 1-3**: Routine battery incidents
- **Week 4**: **Increased maintenance requirements**
  - FL108: Extended downtime (battery power system issue)
  - DT171: Electrical system repairs required
  - Several BMS and connection issues

### Infrastructure Degradation Root Causes
1. **Component Aging**: Worn charger modules and connectors
2. **Electrical Stress**: Circuit breaker trips indicating overload/fault conditions
3. **Cable Deterioration**: CCS connector cable wear from repeated use
4. **Maintenance Backlog**: Multiple simultaneous failures suggest deferred maintenance

## 📈 Maintenance Actions and Interventions

### Completed Actions
- **Battery Damage Audits**: Completed with quotations sent to BRMO
- **DCDC Campaign Planning**: Technician onboarding initiated

### Planned Actions
- **DCDC Campaign**: Kick off pending technician availability
- **Module Replacements**: Charger 4 Module 1 and Charger 5 Module 4
- **Cable Replacement**: Posts 3, 6, and 7 CCS connectors
- **Artisan Onboarding**: Additional technicians for DC/DC campaign

### Investigation Priorities
- **Charger Stops**: Investigating increased frequency 
- **Connector Wear**: Root cause analysis of CCS inlet degradation
- **Electrical Faults**: Circuit breaker trip analysis

## 🎯 Critical Action Requirements

### Immediate (48 Hours)
1. **Emergency Module Procurement**: Replace failed charger modules
2. **Cable Replacement**: CCS connector cables for Posts 3, 6, 7
3. **Electrical Investigation**: Root cause analysis for breaker trips

### Short-term (1-2 Weeks)  
1. **DCDC Campaign**: Launch with onboarded technicians
2. **Preventive Maintenance**: Proactive connector and cable inspection
3. **Spare Parts**: Ensure adequate battery and charger component inventory

### Strategic (1 Month)
1. **Infrastructure Redundancy**: Backup charging capacity implementation
2. **Predictive Maintenance**: Transition from reactive to predictive model
3. **Technology Refresh**: Evaluate newer charging and battery technologies

## 📊 Impact Assessment

### Operational Impact
- **Charging Capacity**: Reduced by ~50% due to module failures
- **Fleet Availability**: Multiple machines experiencing extended battery-related downtime
- **Production Impact**: Significant capacity reduction during critical production periods

### Financial Impact
- **Emergency Repairs**: Unplanned module and cable replacements
- **Lost Production**: Extended downtime during peak operational demand
- **Escalated Maintenance**: Premium costs for expedited repairs

### Strategic Considerations
- **Infrastructure Planning**: Multiple charger modules requiring attention
- **Fleet Management**: Increased maintenance scheduling needed
- **Operational Planning**: Managing reduced charging capacity during repairs

---

**Conclusion**: Week 4 shows increased maintenance requirements for BEV infrastructure, with several charger modules and battery systems needing attention. Proactive maintenance planning and component replacement will help maintain operational efficiency.

## Related Documentation
- [[2025-08-28 – BRMO Weekly Report LIVE Week 4 Summary]]
- [[projects/BEV/BEV Charging Bay 2/]]
- [[operations/BEV/Weekly_Reports/]]