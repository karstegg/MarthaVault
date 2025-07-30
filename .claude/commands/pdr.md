# /pdr $ARGUMENTS

Process daily production reports from WhatsApp messages into structured format.

## Usage
`/pdr` - Auto-scan 00_inbox/ for production reports and process them (uses parallel agents for multiple reports)
`/pdr [report_text]` - Process a single daily production report (inline text)
`/pdr batch` - Process multiple reports from 00_inbox/ (legacy command)

## Process Flow

### 0. Auto-Inbox Detection & Parallel Processing (Default Behavior)
When `/pdr` is called without arguments:
- Scan `00_inbox/` for files containing production report data
- Look for WhatsApp message formats, text files, or markdown files
- Identify reports by keywords: "Safety:", "Production:", "ROM:", site names (Nchwaning, Gloria)
- **Single Report**: Process directly with main agent
- **Multiple Reports**: Launch parallel specialized agents for concurrent processing:
  - **pdr-nchwaning2**: Processes Nchwaning 2 reports
  - **pdr-nchwaning3**: Processes Nchwaning 3 reports  
  - **pdr-gloria**: Processes Gloria reports
  - **pdr-shafts-winders**: Processes Shafts & Winders reports
- Move processed files to appropriate daily_production folders

### 1. Parse Report Metadata
- Extract report date (when received)
- Extract data date (performance period) 
- Identify mine site and engineer
- Determine report type (daily/weekend/special)

### 2. Parse Content by Site Type

#### Standard Mine Sites (Nchwaning 2, Nchwaning 3, Gloria)
- **Safety**: Status and incident details
- **Production**: ROM, Decline, Product vs targets with variance calculations
- **Loads**: Individual load performance data
- **Blast**: Faces/quantity blasted (include breakdown like "12 Mn + 4 waste")
- **Equipment Availability**: TMM percentages (DT, FL, HD, RT, SR, UV)
- **Shift Readiness**: Start-of-shift equipment counts
- **Breakdowns**: Current equipment issues with specific unit numbers
- **Operational**: Plant blockages, fire alarms

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
  "production": {"rom": {}, "product": {}, "loads": [], "blast": {}},
  "equipment_availability": {"tmm": {}, "specialized": []},
  "breakdowns": {"current_breakdowns": []},
  "performance_summary": {"key_issues": [], "key_highlights": []}
}
```

#### Markdown Report (`YYYY-MM-DD – [Site] Daily Report.md`)
- **Header**: Status, Priority, Assignee, JSON link
- **Safety Status**: Clear/incident with details
- **Production Performance**: Metrics with variance analysis
- **Equipment Status**: Availability and breakdowns
- **Critical Issues**: Highlighted performance problems
- **Key Highlights**: Positive performance notes

### 5. Date Logic
- **File Naming**: Use report date (when received)
- **Content Dating**: Reference both report date and data date
- **Example**: Report received 30th July contains 29th July data

### 6. Analysis & Alerts
- **Critical Thresholds**: 
  - Production <80% of target
  - Equipment availability <70%
  - Safety incidents
- **Trend Identification**: Compare with previous reports
- **Missing Data**: Flag incomplete information

### 7. Engineer Assignment
Auto-assign based on site:
- **Nchwaning 2**: [[Johan Kotze]] (acting for [[Sikilela Nzuza]])
- **Nchwaning 3**: [[Sello Sease]]  
- **Gloria**: [[Sipho Dubazane]]
- **Shafts & Winders**: [[Xavier Peterson]]

### 8. Parallel Agent Processing Logic
When multiple reports are detected:
1. **Identify Report Types**: Scan content for site keywords
2. **Launch Concurrent Agents**: Start specialized agents based on detected sites
   ```
   CONCURRENT CALLS:
   - Task(description="Process N2 report", prompt="[N2_report_content]", subagent_type="pdr-nchwaning2")
   - Task(description="Process N3 report", prompt="[N3_report_content]", subagent_type="pdr-nchwaning3")  
   - Task(description="Process Gloria report", prompt="[Gloria_report_content]", subagent_type="pdr-gloria")
   - Task(description="Process S&W report", prompt="[SW_report_content]", subagent_type="pdr-shafts-winders")
   ```
3. **Collect Results**: Gather all agent outputs
4. **Summarize**: Provide consolidated processing summary

### 9. Error Handling
- **Missing Reports**: Track and flag outstanding reports
- **Data Validation**: Check for unusual values or missing fields
- **Equipment Codes**: Validate against reference, flag errors
- **Follow-up**: Create tasks for missing or problem reports
- **Agent Failures**: Handle individual agent errors gracefully

## Output Confirmation
### Auto-Inbox Mode (Parallel Processing)
"✅ Scanned inbox: Found [X] reports - Launching parallel agents for [Site1], [Site2], [Site3]..."
[Concurrent agent outputs]
"✅ Parallel processing complete: All [X] reports processed for [date]"

### Auto-Inbox Mode (Single Report)
"✅ Scanned inbox: Found 1 report - Processed [Site] for [date] - [status]"

### Single Report Mode  
"✅ Processed [Site] report for [date] - [key_status] (#tags)"

## Integration
- Update `daily_production/README.md` with new reports
- Cross-reference with equipment issues in other systems
- Flag critical issues for management attention

#daily-production #processing #automation #mining #reports #year/2025