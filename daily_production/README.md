# Daily Production Reporting System

## Overview
This system captures daily production reports from all mine sites in both human-readable Markdown and machine-readable JSON formats for analysis and trending.

## File Structure
```
daily_production/
├── README.md                           # This file
├── data/                              # JSON database files
│   └── YYYY-MM-DD_site.json          # Structured data for analysis
└── YYYY-MM-DD – Site Daily Report.md # Human-readable reports
```

## JSON Schema
Each JSON file contains standardized fields for:
- **Report metadata**: Date, site, engineer, timestamps
- **Safety**: Status, incidents, notes
- **Production**: ROM, product output, loads, blast performance
- **Equipment availability**: TMM percentages, specialized equipment
- **Shift readiness**: Equipment counts and readiness percentages
- **Utility vehicles**: Status by category (emulsion, logistics, manlifts)
- **Breakdowns**: Detailed equipment issues
- **Operational metrics**: Blockages, alarms, incidents
- **Performance summary**: Key issues and overall status

## Usage Examples

### Search for equipment issues:
```bash
grep -r "brake" data/*.json
```

### Find production shortfalls:
```bash
jq '.production.rom | select(.variance_percent < -10)' data/*.json
```

### Equipment availability trends:
```bash
jq '.equipment_availability.tmm.dump_trucks.availability_percent' data/*.json
```

## Mine Sites
- **Nchwaning 2** - Engineer: [[Sikelela Nzuza]]
- **Gloria** - Engineer: [[Sipho Dubazane]]  
- **Nchwaning 3** - Engineer: [[Sello Simon Siase]]

## Data Analysis
The JSON format enables:
- Time-series analysis of production trends
- Equipment reliability tracking
- Safety incident monitoring
- Performance benchmarking across sites
- Automated reporting and alerts

#daily-production #database #json #mining #analysis #year/2025