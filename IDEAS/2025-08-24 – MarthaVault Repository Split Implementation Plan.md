---
Status:: #status/new
Priority:: #priority/high
Assignee:: [[Greg Karsten]]
DueDate:: 2025-08-25
---

# MarthaVault Repository Split Implementation Plan

**Date**: August 24, 2025  
**Type**: Implementation Plan  
**Project**: Repository Architecture Optimization  
**Scope**: Split MarthaVault into specialized repositories

## Executive Summary

This document outlines the comprehensive plan to split the current MarthaVault repository into two specialized repositories: **ProductionReports** (automated production data processing) and **MarthaVault** (work task management). This separation will create clear boundaries, improve system reliability, and establish single points of control for different operational functions.

## Background & Current State

### Current MarthaVault Architecture
MarthaVault currently serves as a unified Obsidian knowledge management system containing:

**Production Data Processing:**
- Daily production reports from Assmang Black Rock mining operations
- WhatsApp MCP integration for automated data extraction
- GitHub Actions workflows for Gemini 2.5 Flash processing
- Codespace integration for real-time data access
- Complex automation pipelines with strict data validation

**Work Task Management:**
- Personal and work task tracking
- Project management for mining operations
- Personnel directory and organizational context
- Ideas management and strategic planning
- Traditional knowledge management workflows

### Technical Infrastructure
- **AI Agent Architecture**: Gemini 2.5 Flash (processing) + Claude-Desktop (coordination) + Claude-Cloud (review)
- **Data Pipeline**: WhatsApp → JSON/Markdown → GitHub → Review → Merge
- **Cost**: $0/day using FREE Gemini 2.5 Flash vs expensive Claude API
- **Integration**: 24/7 WhatsApp bridge, Codespace SSH access, automated PR workflows

## Business Case for Split

### 1. **Operational Separation**
- **Production data** requires 24/7 reliability for mining operations
- **Task management** operates on different schedules and priorities
- Mixed responsibilities create unnecessary complexity and risk

### 2. **Risk Management**
- Personal vault changes shouldn't affect critical production workflows
- Production automation needs isolated, controlled environment
- Single point of failure currently exists in unified repository

### 3. **Access Control & Security**
- Production data may require different access permissions
- Task management contains personal/strategic information
- Separation enables granular security controls

### 4. **Performance & Scalability**
- Production processing optimized for data throughput
- Task management optimized for knowledge management
- Each system can scale independently

### 5. **Maintenance & Development**
- Production workflows require enterprise-grade stability
- Task management allows for experimental features
- Reduces testing complexity and deployment risk

## Detailed Implementation Plan

### Phase 1: Repository Creation & Duplication

#### Step 1.1: Create ProductionReports Repository
```bash
# Duplicate entire MarthaVault repository
git clone https://github.com/karstegg/MarthaVault.git ProductionReports
cd ProductionReports
git remote set-url origin https://github.com/karstegg/ProductionReports.git
git push -u origin main
```

#### Step 1.2: Verify Infrastructure Transfer
- Confirm all GitHub Actions workflows are present
- Verify Codespace configurations are intact
- Test WhatsApp MCP integration functionality
- Validate all secrets and environment variables

### Phase 2: ProductionReports Specialization

#### Step 2.1: Remove Task Management Content
**Folders to DELETE from ProductionReports:**
- `tasks/` - Task management files
- `projects/` - Project folders  
- `personal/` - Personal content
- `IDEAS/` - Idea management
- `Schedule/` - Scheduling content
- `Archive/` - Archived task content
- `Adjudication_Committee_Meetings/` - Meeting records
- `Standby lists/` - Operational scheduling
- `Templates/` - Task templates
- `commit_messages/` - Development artifacts
- `testing/` - Development testing files

#### Step 2.2: Retain Production Infrastructure
**Keep in ProductionReports:**
- `.github/workflows/` - All GitHub Actions workflows
- `whatsapp-mcp-server/` - WhatsApp integration
- `daily_production/` - Production data and processing
- `reference/equipment/` - Fleet database, equipment codes
- `reference/locations/` - Mine sites, operational areas
- `people/` - Engineer assignments (minimal copy for processing context)
- `.devcontainer/` - Development container configurations
- `scripts/` - Production processing scripts
- All Codespace configurations and secrets

#### Step 2.3: Update ProductionReports CLAUDE.md
Create specialized configuration focusing on:
- Production data processing workflows
- Data validation requirements (critical after PR #7 failure)
- Equipment code validation and BEV classification
- Engineer-site mapping and report processing
- GitHub Actions automation instructions
- WhatsApp MCP integration guidelines

### Phase 3: MarthaVault Simplification

#### Step 3.1: Remove Production Automation
**DELETE from MarthaVault:**
- `.github/workflows/` - **Entire folder** (all GitHub Actions)
- `whatsapp-mcp-server/` - WhatsApp integration
- `daily_production/` - Production data
- `.devcontainer/` - Development containers
- Production-related scripts and configurations

#### Step 3.2: Retain Task Management
**Keep in MarthaVault:**
- `tasks/` - Task management system
- `projects/` - Project management
- `people/` - Personnel management
- `personal/` - Personal content
- `IDEAS/` - Idea management
- `reference/` - Reference materials
- `Schedule/` - Scheduling and meetings
- `Archive/` - Historical content
- Basic Git functionality for backup/versioning

#### Step 3.3: Update MarthaVault CLAUDE.md
Simplify configuration to focus on:
- Task management workflows
- Project organization
- Personnel tracking
- Idea management
- Traditional Obsidian knowledge management
- Remove all production automation references

### Phase 4: Infrastructure Migration

#### Step 4.1: Codespace Reassignment
- Update Codespace connection to point to ProductionReports repository
- Transfer all production-related secrets and configurations
- Test WhatsApp MCP bridge connectivity from new repository

#### Step 4.2: GitHub Actions Configuration
- Verify all production workflows function in ProductionReports
- Update repository references in workflow files
- Test end-to-end automation pipeline

#### Step 4.3: Cross-Repository Linking
- Configure MarthaVault to link to ProductionReports for report viewing
- Maintain minimal people/ data in ProductionReports for processing context
- Establish clear boundaries for data access

### Phase 5: Validation & Testing

#### Step 5.1: Production Workflow Testing
- Test complete production report processing pipeline
- Verify data validation and source verification requirements
- Confirm GitHub Actions automation functions correctly

#### Step 5.2: Task Management Testing
- Verify MarthaVault functions as traditional knowledge management system
- Test task tracking and project management workflows
- Confirm no production automation remains

#### Step 5.3: Integration Testing
- Test cross-repository linking functionality
- Verify data boundaries are maintained
- Confirm single point of control for production data

## Post-Implementation Architecture

### ProductionReports Repository
**Purpose**: Automated production data processing for Assmang Black Rock mining operations

**Core Functions:**
- Daily production report automation
- WhatsApp data extraction and processing
- Data validation and quality control
- GitHub Actions workflows
- Codespace integration

**Key Features:**
- 24/7 automated processing
- Strict data validation (post-PR #7 requirements)
- Multi-site production tracking
- Equipment and personnel integration

### MarthaVault Repository
**Purpose**: Work task management and knowledge organization

**Core Functions:**
- Task and project management
- Personnel and organizational tracking
- Idea management and strategic planning
- Traditional knowledge management

**Key Features:**
- Obsidian-based organization
- Basic Git backup and versioning
- Cross-linking and relationship management
- Personal and work content separation

## Risk Mitigation

### Technical Risks
- **Workflow Disruption**: Gradual migration with rollback capability
- **Data Loss**: Complete backup before any changes
- **Integration Failure**: Thorough testing at each phase

### Operational Risks
- **Production Downtime**: Maintain current system until new system validated
- **Access Issues**: Clear documentation and handover procedures
- **Training Requirements**: Comprehensive documentation for new architecture

## Success Criteria

### Immediate Success Indicators
- [ ] ProductionReports repository created with full automation intact
- [ ] MarthaVault simplified to task management only
- [ ] All production workflows function in new repository
- [ ] No duplicate automation capabilities exist

### Long-term Success Indicators
- [ ] Improved system reliability and performance
- [ ] Clear separation of concerns maintained
- [ ] Independent scaling and development possible
- [ ] Reduced maintenance complexity

## Timeline

**Week 1 (August 25-31, 2025):**
- Phase 1: Repository creation and duplication
- Phase 2: Initial specialization

**Week 2 (September 1-7, 2025):**
- Phase 3: Infrastructure migration
- Phase 4: Testing and validation

**Week 3 (September 8-14, 2025):**
- Phase 5: Final validation and documentation
- Go-live and monitoring

## Rollback Plan

If issues arise during implementation:
1. **Immediate**: Revert to original MarthaVault repository
2. **Short-term**: Maintain parallel systems until issues resolved
3. **Long-term**: Redesign split approach based on lessons learned

## Conclusion

This repository split represents a strategic optimization of the MarthaVault system, creating specialized repositories that can evolve independently while maintaining their core functions. The separation will improve reliability, security, and maintainability while preserving all existing functionality.

The implementation plan provides a structured approach with clear phases, validation steps, and risk mitigation strategies to ensure a successful transition to the new architecture.

## Related Documentation

- `CLAUDE.md` - Current system configuration
- `GEMINI_2.5_FLASH_BREAKTHROUGH_COMPLETE_SOLUTION.md` - Production automation details
- `WHATSAPP_MCP_COMPLETE_SETUP.md` - WhatsApp integration setup
- `GITHUB_ACTIONS_CODESPACE_INTEGRATION_GUIDE.md` - Infrastructure integration

#idea #repository-split #architecture #production-automation #task-management #implementation-plan #priority/high #year/2025
