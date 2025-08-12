---
name: Production Reports Automation
about: Trigger automated processing of missing production reports
title: 'Process Production Reports: [DATE RANGE]'
labels: ['production-reports', 'automation']
assignees: ''

---

## Production Report Automation Request

### Date Range
**Start Date**: YYYY-MM-DD
**End Date**: YYYY-MM-DD

### Processing Details
- [ ] Extract WhatsApp production data from database
- [ ] Create structured report files for all identified mine sites
- [ ] Apply Gemini-CLI processing for data structuring
- [ ] Generate dual-format output (JSON + Markdown)
- [ ] Validate reports for completeness and accuracy

### Expected Sites
- [ ] Gloria Mine
- [ ] Nchwaning 2 Mine  
- [ ] Nchwaning 3 Mine
- [ ] Shafts & Winders

### Processing Method
This issue will trigger the automated GitHub Actions workflow:
1. **Phase 1**: WhatsApp data extraction via Codespace connection
2. **Phase 2**: Gemini-CLI integration for report structuring  
3. **Phase 3**: Create pull request with processed reports
4. **Phase 4**: Claude Cloud review and validation

### Quality Assurance Requirements
- [ ] All production figures traced to WhatsApp source data
- [ ] Equipment codes validated against established database
- [ ] Safety incidents properly categorized
- [ ] Template compliance verified (Standard Mine Site / S&W)
- [ ] Source data validation section included

### Additional Notes
<!-- Add any specific requirements, date constraints, or processing notes -->

---

**🤖 Automation Trigger**: Creating this issue with `production-reports` label will automatically start the processing workflow.

**📅 Default Range**: If no specific dates provided, system will process July 6-21, 2025.

**⚠️ Manual Review**: All automated reports require manual verification before final approval.