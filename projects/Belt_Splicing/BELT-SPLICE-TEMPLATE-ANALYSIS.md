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
- Price - In Position
- Price - Out of Position

**Khumani Data Sample:**
```
Shell Diameter: 400, Face: 700, Qty: 16, In Position: [R rate], Out of Position: [R rate]
Shell Diameter: 500, Face: 900, Qty: 17, In Position: [R rate], Out of Position: [R rate]
[... extensive list of all combinations ...]
```

### **Table 7: Conveyor Pulley Detail (Embedded Ceramic Lagging)**
- Same Shell Diameter and Face dimensions
- Only for drive applications (NOT head/tail)
- Specifications: Nilos strip lagging, 12mm thick, 4-piece diamond pattern
- Qty and pricing

---

## What We Need to ADD to Our Scope

From Lourens and the Khumani template, we should include:

### 1. **Labour Rates** ❌ NOT IN KHUMANI - Need to determine:
- Standard labour rate per hour
- Overtime multipliers (1.5x, 2.0x)
- Public holiday rates
- Standby crew monthly retainer rates

### 2. **Equipment/Consumables Pricing** ✅ IN KHUMANI - Need from contractor:
- Generator hire rates (220V, 380V)
- Vehicle travel rates
- Splicing kit costs
- Lagging material costs

### 3. **Service-Level Specifications** ✅ IN KHUMANI - Our requirements:
- Warranty periods for different belt types
- Quality assurance/QA requirements
- Monthly condition monitoring reports
- Response time for breakdowns (±2 hours)
- Training requirements

### 4. **Safety & Compliance** ✅ IN KHUMANI - Mandatory:
- Lockout/tag-out procedures
- Permit-to-work system
- Risk assessments (pre-work)
- MSDS sheets for hazardous materials
- PPE requirements
- Vehicle and equipment testing

### 5. **Performance KPIs** ✅ IN KHUMANI - Need to define:
- Safety metrics
- Schedule compliance
- Quality metrics
- Equipment availability targets

---

## Template Structure for Engineers

**We should create an Excel template with these worksheets:**

### **Worksheet 1: Site Overview**
- Site Name (N2 / N3 / Gloria / S&W)
- Engineer Contact
- Email
- Phone
- Date Completed

### **Worksheet 2: Conveyor Belt Inventory**
| Conveyor Name | Belt Type | Width (mm) | Class | Ply | Cover | Quantity | Notes |
|---|---|---|---|---|---|---|---|
| CV10 | Plylon / Steel Cord | [number] | [rating] | [number] | [6/3 or 10/4] | [number] | [description] |

### **Worksheet 3: Pulley Lagging - Standard Rubber**
| Conveyor Name | Pulley Position | Shell Diameter (mm) | Face Width (mm) | Lagging Type | Quantity | Notes |
|---|---|---|---|---|---|---|
| CV10 | Drive | 630 | 1200 | Grip 60 x 10mm | 2 | [location/notes] |

### **Worksheet 4: Pulley Lagging - Ceramic** (if applicable)
| Conveyor Name | Pulley Position | Shell Diameter (mm) | Face Width (mm) | Quantity | Notes |
|---|---|---|---|---|---|
| CV10 | Drive | 630 | 1200 | 1 | [location/notes] |

### **Worksheet 5: Maintenance Requirements**
- Current idler replacement frequency
- Life expectancy audits needed (Yes/No, frequency)
- 24/7 standby crew required (Yes/No)
- Current downtime issues
- Conveyor condition notes

### **Worksheet 6: Instructions & Examples**
- How to fill out the template
- Example entries
- Contact information
- Submission deadline

---

## Additional Information to Request

**From Michael Bester (Plant Engineer):**
1. Standard labour rates we should expect from contractor
2. Budget constraints per site
3. Contract duration preference (1 yr / 2 yr / 3 yr)
4. Priority conveyors (which ones are critical?)
5. Planned capital upgrades (new conveyors coming?)

---

## Next Steps

1. ✅ Create Excel template with above worksheets
2. ✅ Update email to include Michael Bester
3. ✅ Attach template to email request
4. Send to: Sipho, Sikelela, Sello, Xavier, Michael
5. Set deadline: Friday 28 November
