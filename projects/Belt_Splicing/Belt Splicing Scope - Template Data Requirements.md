---
title: Belt Splicing Scope - Template Data Requirements
type: note
permalink: projects/belt-splicing/belt-splicing-scope-template-data-requirements
tags:
- project
- belt-splicing
- template
- requirements
---

# Belt Splicing Scope - Template Data Requirements

## Analysis of Khumani Scope Tables

Based on Fanele's document from Khumani, the following detailed tables are included:

### **Table 1: Equipment Rates**
- Generator 220V (rate per activity)
- Generator 380V (rate per activity)
- Travel Rate for Vehicle
- Labour rates (Normal, Overtime 1.5x, Public Holiday/Sunday 2.0x)
- Rates per team of 5

### **Table 2-4: Standby Crew Rates** (separate for Parsons, Load-out, King & Bruce)
- Supervisor (1x, hourly rate, 185 monthly hours)
- Splicer (1x, hourly rate, 185 monthly hours)
- Semi-Skilled (2x, hourly rate, 185 monthly hours)
- Skilled Assistant (1x, hourly rate, 185 monthly hours)

### **Table 5: CRITICAL - Conveyor Belt Detail**
**This is the key table we need from each site**

Headers:
- Type (Plylon / Steel Cord)
- Width (mm)
- Class
- Ply
- Cover
- Quantity
- Hot Splice - New Installation Per Roll (Rate)
- Hot Splice (Only) & Inserts (Rate)

**Khumani Data Sample:**
```
Type: Plylon, Width: 600, Class: 630, Ply: 3, Cover: 6/3, Qty: 14
Type: Plylon, Width: 600, Class: 1000, Ply: 3, Cover: 6/3, Qty: 1
Type: Steel Cord, Width: 1050, Class: 2500, Ply: N/A, Cover: 10/4, Qty: 1
Type: Steel Cord, Width: 1200, Class: 1600, Ply: N/A, Cover: 10/4, Qty: 2
[... and many more configurations ...]
```

**BRMO Requirement:** We need engineers to list ONLY their active belts, not all possible combinations.

### **Table 6: CRITICAL - Conveyor Pulley Detail (Standard Rubber Lagging)**

Headers:
- Shore degree & specification (Grip 60 x 10mm for ≤900mm / Grip 70 x 12mm for >900mm)
- Shell Diameter (400, 500, 630, 800, 1000, 1250 mm)
- Shell Face (700, 900, 1050, 1200, 1350, 1500, 1700, 2000 mm)
- Quantity

**Key specifications:**
- For pulleys ≤900mm face width: Grip 60 x 10mm lagging
- For pulleys >900mm face width: Grip 70 x 12mm lagging

### **Table 7: Ceramic Lagging Pulleys**
- Embedded ceramic lagging (Nilos, 12mm, 4-piece diamond) - DRIVE applications ONLY
- Shell Diameter & Face Width configurations
- Quantity

---

## What We're Asking From Each Site

Using the BRMO_Belt_Splicing_Scope_Template.xlsx:

1. **Site Overview** - Basic info about site location and engineer contact
2. **Belt Inventory Sheet** - List every active conveyor belt with specifications
3. **Pulley Lagging - Rubber Sheet** - All standard rubber lagging pulleys at site
4. **Pulley Lagging - Ceramic Sheet** - Any ceramic lagging pulleys (if applicable)
5. **Maintenance Requirements** - Answers about current practices and needs

---

## Consolidation Plan

After receiving responses from all 5 sites (Sipho, Sikelela, Sello, Xavier, Michael), we will:

1. Consolidate all belt inventory data into one master list
2. Consolidate all pulley lagging data (rubber and ceramic) into one master list
3. Identify common requirements and maintenance patterns
4. Create single BRMO scope document incorporating:
   - Consolidated equipment inventory
   - Khumani's pricing and labour rates
   - BRMO-specific maintenance requirements
   - Service conditions and warranty terms

---

## Related Files
- Template: `BRMO_Belt_Splicing_Scope_Template.xlsx` (6 worksheets)
- Khumani original: `Conveyor Belt Splicing Scope (Tracked changes) 2025.docx`
- Email tracking: `2025-11-24 – EMAIL TRACKING - Week Actions.md`
