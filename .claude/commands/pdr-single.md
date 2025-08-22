# /pdr-single $ARGUMENTS

Process daily production reports sequentially in a single Claude session for token efficiency.

## Usage
`/pdr-single` - Auto-scan 00_inbox/ for production reports and process them sequentially
`/pdr-single [report_text]` - Process a single daily production report (inline text)

## Process Flow

### 0. Sequential Processing (Default Behavior)
When `/pdr-single` is called without arguments:
- Scan `00_inbox/` for files containing production report data
- Look for WhatsApp message formats, text files, or markdown files
- Identify reports by keywords: "Safety:", "Production:", "ROM:", site names (Nchwaning, Gloria)
- Process each report sequentially in the same session (token efficient)
- Move processed files to appropriate daily_production folders

### 1. Parse Report Metadata & Date Confirmation
- **CRITICAL**: Message date = report date (when received)
- **ALWAYS ASK USER TO CONFIRM** report date vs data date before proceeding unless explicitly stated upfront
- Extract data date (performance period) - typically previous day's operations
- Identify mine site and engineer
- Determine report type (daily/weekend/special)
- **Example**: Message sent 31-07-2025 = report date, data usually covers 30-07-2025 operations

### 2. Parse Content by Site Type

#### Standard Mine Sites (Nchwaning 2, Nchwaning 3, Gloria)
- **Safety**: Status and incident details
- **Production**: ROM, Decline, Product vs targets with variance calculations
- **Loads**: Truckloads tipped by shift (Day/Afternoon/Night shifts)
- **Blast**: Faces/quantity blasted (include breakdown like "12 Mn + 4 waste")
- **Equipment Availability**: TMM percentages (DT, FL, HD, RT, SR, UV)
- **Equipment Readiness**: Start-of-shift equipment availability (not staffing)
- **Breakdowns**: Current equipment issues with specific unit numbers
- **Operational**: Plant blockages, fire alarms

#### 🚨 CRITICAL EQUIPMENT CODE VALIDATION
**MANDATORY BEFORE PROCESSING**: Validate ALL equipment codes against reference
- **RT = Roof Bolter** (NOT Rock Truck - no such equipment exists!)
- **DT = Dump Truck** (material transport)
- **FL = Front Loader** (loading equipment)
- **HD = Hydraulic Drill** (drilling equipment)
- **SR = Scaler** (scaling equipment)
- **REJECT any reference to "Rock Truck" - use "Roof Bolter" for RT codes**

#### Gloria-Specific Elements
- **Silo Levels**: Surface (1-4) and Underground (74, HG, D, LG) percentages
- **Manitou**: Availability status (rare when operational)
- **Main Fans**: Status

#### Shafts & Winders (Xavier's Format)
- **Power Supply**: Stoppage status
- **Winders**: Individual shaft status (Nch2 PW/RW, Nch3 PW, GL PW)
- **Main Fans**: By site status
- **Lamprooms**: By site status  
- **Dam Levels**: DD01/DD02 weekly tracking
- **Ore Pass Levels**: Weekly percentage tracking
- **Production**: Weekly summary with targets
- **Fire SCADA Alarms**: Count and type

### 3. Equipment Code Validation
Reference `daily_production/equipment_codes.md`:
- **TMM**: DT, FL, HD, RT, SR, UV
- **Specialized**: GD (grader), DZ (dozer), LD (delivery)
- **Common Errors**: GR → GD, validate against reference

### 4. Create Dual Format Output

#### JSON Database (`data/YYYY-MM-DD_[site].json`)
```json
{
  "report_metadata": {
    "date": "report_date",
    "data_date": "performance_date", 
    "site": "site_name",
    "engineer": "engineer_name"
  },
  "safety": {"status": "clear/incident", "incidents": 0, "details": []},
  "production": {"rom": {}, "product": {}, "loads": [{"shift": "day/afternoon/night", "load_number": 1, "truckloads_tipped": 0}], "blast": {}},
  "equipment_availability": {"tmm": {}, "specialized": []},
  "breakdowns": {"current_breakdowns": []},
  "performance_summary": {"key_issues": [], "key_highlights": []}
}
```

#### Markdown Report (`YYYY-MM-DD – [Site] Daily Report.md`)
**MUST FOLLOW STANDARDIZED TEMPLATE STRUCTURE:**

**Use appropriate template from Report Templates folder:**
- **Mine Sites (N2, N3, Gloria)**: `Report Templates/Standard Mine Site Report Template.md`
- **Infrastructure (S&W)**: `Report Templates/Shafts & Winders Report Template.md`

**Standard Template Structure (All Mine Sites):**
```markdown
---
JSONData:: [[YYYY-MM-DD_site.json]]
---

# [Site] Daily Report
**Date**: Report Date (Data from Data Date)
**Engineer**: [[Engineer Name]]
**Site**: [Site Name]

## [STATUS EMOJI] [STATUS DESCRIPTION]

### Safety Status
[Clear/Incident with details]

### Production Performance
[Performance table with ROM, Decline, Product]

#### Load & Haul Fleet Performance (Truckloads Tipped by Shift)
[Shift performance table with Day/Afternoon/Night]

#### Blast Performance
[Blast details or "Nothing Reported"]

### Equipment Status

#### TMM Availability
[Equipment availability table with performance analysis]

#### Poor Performance Analysis (if applicable)
[Analysis of equipment below 80% threshold]

#### Equipment Readiness (Start of Shift)
[Start of shift equipment status]

### Current Breakdowns ([X] Units)
[Breakdown details by equipment type]

### Support Equipment Summary
[UV and specialized equipment status]

### Infrastructure Status
[Main fans, plant blockages, fire alarms]

## Performance Summary
[4-point bullet summary: Safety, Production, Equipment, Operations]

## Supplemental Information
[Site-specific details in organized subsections]
```

**Key Changes from Old Format:**
- **NO task-oriented front-matter** (Status, Priority, Assignee, DueDate)
- **ONLY JSONData link** in front-matter
- **NO Critical Actions sections** (informational reports only)
- **Load performance** must be "Truckloads Tipped by Shift" format
- **Equipment readiness** refers to equipment availability, not staffing
- **Support Equipment Summary** replaces "UV Availability Summary"
- **Consistent table formats** as per template specifications

### 5. Date Logic (UPDATED PROTOCOL)
- **CRITICAL RULE**: Message date = report date (when received)
- **File Naming**: Use report date (YYYY-MM-DD format from message date)
- **Data Date**: Usually previous day's operations (confirm with user)
- **Content Dating**: Reference both report date and data date clearly
- **Example**: Message sent 31-07-2025 (report date) contains 30-07-2025 data (operations date)
- **User Confirmation Required**: Always confirm dates unless explicitly stated upfront

### 6. Analysis & Alerts
- **Critical Thresholds**: 
  - Production <80% of target
  - Equipment availability <70%
  - Safety incidents
- **Trend Identification**: Compare with previous reports
- **Missing Data**: Report as "Nothing Reported" for consistency

### 7. Engineer Assignment
Auto-assign based on site:
- **Nchwaning 2**: [[Johan Kotze]] (acting for [[Sikilela Nzuza]])
- **Nchwaning 3**: [[Sello Sease]]  
- **Gloria**: [[Sipho Dubazane]]
- **Shafts & Winders**: [[Xavier Peterson]]

### 8. Sequential Processing Logic
When multiple reports are detected:
1. **Identify Report Types**: Scan content for site keywords
2. **Process in Order**: Handle each site report sequentially:
   - Process Nchwaning 2 reports first
   - Process Nchwaning 3 reports second
   - Process Gloria reports third
   - Process Shafts & Winders reports last
3. **Maintain Context**: Keep processing state across reports in same session
4. **Summarize**: Provide consolidated processing summary after all reports

### 9. Error Handling
- **Missing Reports**: Track and flag outstanding reports
- **Data Validation**: Check for unusual values or missing fields
- **Equipment Codes**: Validate against reference, flag errors
- **Follow-up**: Create tasks for missing or problem reports
- **Processing Errors**: Handle individual report errors gracefully

## Output Confirmation
### Auto-Inbox Mode (Sequential Processing)
"✅ Scanned inbox: Found [X] reports - Processing sequentially..."
"📊 Processing [Site1] report for [date]..."
"📊 Processing [Site2] report for [date]..."
"✅ Sequential processing complete: All [X] reports processed for [date]"

### Single Report Mode  
"✅ Processed [Site] report for [date] - [key_status] (#tags)"

## Template Reference
**CRITICAL**: Always use the appropriate template from the Report Templates folder:

### Standard Mine Site Template
**File**: `Report Templates/Standard Mine Site Report Template.md`
**Use for**: Nchwaning 2, Nchwaning 3, Gloria reports
**Key Features**: 
- TMM Availability table with Poor Performance Analysis
- Load & Haul Fleet Performance (Truckloads Tipped by Shift) table format
- Support Equipment Summary section
- Site-specific Supplemental Information (Gloria silo management)

### Shafts & Winders Template  
**File**: `Report Templates/Shafts & Winders Report Template.md`
**Use for**: Infrastructure reports from Xavier Peterson
**Key Features**:
- Infrastructure Availability table (Power, Winders, Fans, Lamprooms)
- Winders Performance table with Type column (Manwinder vs Rock Winder)
- Water Management and Ore Pass Management in Supplemental Information
- Department Responsibilities section explaining winder types

### Template Compliance Rules
1. **Front-matter**: ONLY JSONData link, NO task fields
2. **Structure**: Follow exact section order from templates
3. **Tables**: Use exact table formats from templates
4. **Terminology**: "Equipment readiness" = equipment availability, NOT staffing
5. **Load Performance**: Must be "Truckloads Tipped by Shift" format
6. **Critical Actions**: REMOVE from informational reports

## Integration
- Update `daily_production/README.md` with new reports
- Cross-reference with equipment issues in other systems
- Flag critical issues for management attention

#daily-production #processing #automation #mining #reports #year/2025 #sequential #templates