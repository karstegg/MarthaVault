# Equipment Relationship Graph
<!-- Equipment dependencies and failure patterns -->

## Equipment Hierarchy

### HD Series (Heavy Duty)
```
HD54 (N3) 
├── Engineer: [[Simon Sease]]
├── Location: [[Nchwaning 3]]
├── Issues: Lubri vent pending
├── Related: HD61, HD62
└── Priority: High

HD61 (N3)
├── Engineer: [[Simon Sease]]  
├── Location: [[Nchwaning 3]]
├── Issues: Lubri vent pending
└── Related: HD54, HD62

HD62 (N3)
├── Engineer: [[Simon Sease]]
├── Location: [[Nchwaning 3]]
├── Issues: Hydraulic failures (2025-09-22)
└── Status: Under investigation
```

### Critical Equipment Patterns
```
Fire Suppression → affects → All TMM Equipment
├── BEVs (Battery Electric Vehicles)
├── HD Series machines
├── Drill Rigs (DT code)
└── LHDs (Load-Haul-Dump)

N2 Manwinder
├── Type: Rock Winder
├── Issue: Hydraulics
├── Assigned: [[Xavier Peterson]]
└── Due: 2025-09-27
```

## Failure Pattern Recognition

### Hydraulic Issues (Recurring)
- HD62 → N3 → September 2025
- N2 Manwinder → S&W → September 2025
- **Pattern**: Post-winter hydraulic failures
- **Action**: Preventive checks before winter 2026

### Fire Safety Gaps
- BEV Workshop → Missing suppression
- Pre-start checks → No fire system verification
- **Root Cause**: Rapid BEV deployment without safety update
- **Solution**: Comprehensive fire safety integration

## Quick Lookups
- By TMM Code: `DT` (Drill), `FL` (Fleet), `HD` (Heavy Duty), `RT` (?) , `SR` (Service), `UV` (Utility Vehicle)
- By Site: N2, N3, Gloria, S&W
- By System: Hydraulic, Electrical, Fire, Mechanical
