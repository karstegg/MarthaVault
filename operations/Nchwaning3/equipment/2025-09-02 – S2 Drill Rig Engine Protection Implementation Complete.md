---
'Status:': Completed
'Priority:': High
'Assignee:': Greg
'DueDate:': 2025-09-02
'Tags:': null
permalink: operations/nchwaning3/equipment/2025-09-02-s2-drill-rig-engine-protection-implementation-complete
---

# S2 Drill Rig Engine Protection Implementation - Post HD0054 Fire

## Background
Following the HD0054 fire incident investigation, one key finding was that Deutz engines on S2 drill rigs lacked engine protection cut-out functionality. While alarms existed, operators could continue running overheating engines.

## Implementation Summary
**Date Completed**: 2025-09-02
**Scope**: All 8 S2 Drill Rigs at Nchwaning3
**Technician**: With equipment technician support

## New Protection Parameters
- **Over-temperature**: Engine power reduction at >105°C, >118°C, cut-out at >119°C
- **Low oil pressure**: Cut-out when pressure ≤0 (30s delay, 5s warning)  
- **High charge air temperature**: Cut-out when >114°C
- **Power reduction**: 25% reduction at each escalation step

## Implementation Process
1. **New settings files** obtained from Deutz manufacturer (Germany)
2. **Parameter upload** to each engine ECU via flashing process
3. **Physical testing** of all three protection parameters per unit
4. **Validation** of cut-out functionality on each drill rig

## Equipment Status - All Units Completed ✓

### HD49
- **Location**: Workshop
- **Status**: Flashed and tested - no issues
- **File**: [[HD49 Engine Protection Update]]

### HD50  
- **Location**: Central Workshop
- **Initial Issues**: ECU problems, required spare ECU installation
- **Status**: Successfully flashed, new batteries installed, minor errors cleared
- **Test Results**: Cut-out verified at >118°C / <900 kPa / >118°C
- **File**: [[HD50 Engine Protection Update]]

### HD51
- **Status**: Flashed successfully after charging power pack
- **Issues**: Battery was flat initially
- **Result**: Charged and tested fine
- **File**: [[HD51 Engine Protection Update]]

### HD52
- **Location**: Central Workshop  
- **Status**: Flashed and tested - no issues
- **File**: [[HD52 Engine Protection Update]]

### HD61
- **Process**: Flashed Deutz engine ECU, cut-out working
- **Time**: ±15 minutes to flash and test
- **Testing**: All three parameters successfully simulated and verified
- **Engine Response**: Cut-out after ~30s (low oil pressure), ~5s delay
- **File**: [[HD61 Engine Protection Update]]

### HD62
- **Location**: MW waiting place
- **Status**: Flashed and tested - no issues  
- **File**: [[HD62 Engine Protection Update]]

## Compliance Status
- **DMR Requirement**: ✓ Completed
- **All S2 Drill Rigs**: ✓ 8/8 units updated
- **Testing Verification**: ✓ All parameters tested physically
- **Documentation**: ✓ Complete

## Related Documentation
- **Fire Incident**: [[operations/Safety/Safety Incidents/2025-08-20 HD0054 Fire/2025-08-20 HD0054 Major Fire Incident Report]]
- **Reference Images**: 
  - ![[media/image/2025/2025-09-02_S2_Engine_Protection_Implementation_Page1.png]]
  - ![[media/image/2025/2025-09-02_S2_Engine_Protection_Implementation_Page2.jpg]]

## Actions Complete
No further actions required - implementation successful across all units.