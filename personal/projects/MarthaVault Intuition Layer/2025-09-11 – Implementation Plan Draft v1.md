---
Status:: Draft
Priority:: High
Assignee:: Greg
DueDate:: 
Tags:: #year/2025 #project #personal #AI #implementation-plan #strategic
---

# MarthaVault Intuition Layer - Implementation Plan Draft v1

## Executive Summary
Comprehensive 6-phase plan to implement adaptive learning AI assistant with persistent memory. Builds on existing MCP infrastructure while preserving all current workflows. Integrates company strategy, sub-agent architecture, and behavioral learning for truly intuitive AI assistance.

## Architecture Alignment Analysis
**Excellent alignment** found between existing framework (IDEAS/2025-09-10) and GPT-5 technical discussion:
- ✅ **MCP sidecars**: Basic Memory + Knowledge Graph (identical approach)
- ✅ **Obsidian plugin**: In-app preference over external processes  
- ✅ **Behavioral stack**: Reflex cache + skills + policy + gatekeeper
- ✅ **Source grounding**: 100% citation requirements maintained

**Key enhancements from GPT-5:**
- Strategy integration with priority multiplication
- Sub-agent architecture with specialized contexts
- Advanced confidence-based learning

---

## Phase 0: Foundation Analysis & Migration Planning (Week 1)
**Goal**: Understand current state and design zero-disruption migration strategy

### 0.1 Current Vault Analysis
**Activities:**
- Scan existing folder structure and organization patterns
- Document current workflows (how /task, /triage, /nn commands work in practice)
- Analyze tagging system (#site, #year, primary tags) and linking patterns
- Map current integrations (WhatsApp MCP, memory systems, production reports)
- Identify preservation priorities (workflows that must NOT break)

**Deliverables:**
- Current state documentation
- Workflow preservation requirements
- Integration points mapping

### 0.2 Sub-Agent Architecture Research  
**Activities:**
- Verify Claude.md context inheritance in sub-agents
- Test specialized agent spawning with domain-specific knowledge
- Design sub-agent skill card architecture
- Plan integration between main Claude CLI and specialized agents

**Deliverables:**
- Sub-agent technical specification
- Context passing mechanisms
- Agent coordination protocols

### 0.3 Migration Strategy Design
**Activities:**
- Design zero-disruption layering approach
- Ensure backward compatibility with existing commands
- Plan progressive enhancement timeline
- Create rollback strategy for issue recovery

**Deliverables:**
- Migration strategy document
- Compatibility matrix
- Risk mitigation plan

---

## Phase 1: MVP Foundation (Week 2)  
**Goal**: Implement core infrastructure without changing current workflows

### 1.1 Strategy Layer Implementation
**Activities:**
- Create `strategy/` folder structure per framework specification
- Implement `CompanyStrategy.md` and `ActivePhase.md` templates
- Add strategic alignment detection to existing priority scoring
- Test strategy integration with current vault notes

**Technical Specification:**
```markdown
strategy/ActivePhase.md:
---
Type:: StrategyPhase
Phase:: Q4-2025
Objectives::
  - id: #objective/electrification_rollout
    weight: 1.00
  - id: #objective/safety_retrofits  
    weight: 0.85
Decay:: 0.005
---
```

**Deliverables:**
- Strategy schema implementation
- Priority scoring with strategy multipliers
- Testing results with existing vault content

### 1.2 Enhanced MCP Integration
**Activities:**
- Validate existing Basic Memory + Knowledge Graph connections
- Implement enhanced API contracts from GPT-5 specification
- Add strategic objective linking to graph relationships
- Test priority scoring with strategy multipliers

**API Contracts:**
```json
// Memory Service
upsert_document: { path, mtime_iso, sha256, text }
search_snippets: { query, noteIds?, k } → [{ path, lineStart, lineEnd, text, score }]

// Graph Service  
upsert_nodes_and_edges: { noteId, props: {...}, edges: [{ type, toId }] }
neighborhood: { entities: [...], time?: {from,to}, k } → [{ noteId, score }]
```

**Deliverables:**
- Enhanced MCP API implementation
- Strategic relationship modeling
- Performance testing results

### 1.3 Core Policy & Skills Setup
**Activities:**
- Create `system/` folder structure per framework
- Implement `system/policy.md` with current standards
- Create first two skill cards: Inbox→Triage and Daily Note (UTC+2)
- Maintain 100% compatibility with existing /commands

**Policy Template:**
```markdown
system/policy.md:
## Core Rules (always-on)
- Front-matter: Status, Priority, Assignee, DueDate, Tags
- One primary tag: #task | #meeting | #idea | #decision  
- File naming: YYYY-MM-DD – Title.md
- Timezone: UTC+2 (Africa/Johannesburg)
- Citations: Always include source paths/line ranges
- Strategy: Prefer work linked to active objectives
```

**Deliverables:**
- Policy framework implementation
- Initial skill card templates
- Command compatibility verification

---

## Phase 2: Obsidian Plugin Development (Weeks 3-4)
**Goal**: Automated vault indexing while preserving existing workflows

### 2.1 Plugin Architecture (Based on Framework Specification)
**Activities:**
- Implement file event listeners with debouncing (500-1000ms)
- Create metadata extraction using Obsidian API
- Build hash cache system `{path: contentHash, mtime}` for efficiency
- Design settings UI for MCP endpoints and configuration

**Technical Requirements:**
- Triggers: create/modify/rename/delete of `.md` files
- Ignore: `.obsidian/` and temporary files
- Debounce: 500-1000ms to batch rapid changes
- Cache: Avoid redundant API calls

**Deliverables:**
- Functional Obsidian plugin
- Settings interface
- Performance optimization

### 2.2 Integration with Existing Patterns
**Activities:**
- Preserve tagging system: #year/2025, single primary tag rule
- Maintain file naming: YYYY-MM-DD – Title.md format
- Respect link patterns: [[Lastname, Firstname]], #site/locations
- Keep current front-matter: Status, Priority, Assignee, DueDate, Tags

**Compatibility Matrix:**
- ✅ Current tagging preserved
- ✅ File naming unchanged  
- ✅ Link patterns maintained
- ✅ Front-matter standards kept
- ✅ Existing commands work unchanged

**Deliverables:**
- Pattern preservation verification
- Compatibility testing results
- Integration validation

### 2.3 Sub-Agent Integration Planning
**Activities:**
- Design skill → sub-agent mapping strategy
- Implement Claude.md context passing for specialized agents
- Create domain-specific agent spawning (BEV, Shaft Monitoring, etc.)
- Test agent coordination and context sharing

**Sub-Agent Domains:**
- BEV projects and fire safety
- Shaft monitoring and maintenance
- CAPEX and project management
- Production reports and analysis
- Safety and compliance

**Deliverables:**
- Sub-agent architecture implementation
- Domain-specific context templates
- Agent coordination testing

---

## Phase 3: Behavioral Intelligence & Learning (Weeks 4-5)
**Goal**: Implement "intuition" with self-evolving concepts

### 3.1 Reflex Cache Implementation
**Activities:**
- Implement local SQLite storage in `.obsidian/plugins/intuition/`
- Create confidence scoring based on user acceptance/edit patterns
- Build pattern matching: intent + entities + site + time window
- Set conservative thresholds for auto-execution

**Confidence Thresholds (Conservative Start):**
- ≥ 0.80 + strategy-aligned + non-destructive: Auto-execute
- 0.60-0.79: Soft confirmation ("Run usual BEV summary?")
- < 0.60 or destructive: Deliberate path with citations
- Never auto-execute on first occurrence

**Deliverables:**
- Reflex cache system
- Confidence scoring algorithm
- Threshold calibration

### 3.2 Skills Library with Sub-Agents
**Activities:**
- Implement skill cards from framework specification
- Create sub-agent spawning for specialized skills
- Add domain expertise: BEV, Shaft Monitoring, CAPEX, Fire Risk
- Test skill → sub-agent → result flow

**Initial Skills:**
- Inbox→Triage normalizer
- Daily Note (UTC+2) composer
- BEV incident summary generator
- Meeting→Actions extractor
- Site status report compiler

**Deliverables:**
- Skills library implementation
- Sub-agent skill execution
- Domain expertise validation

### 3.3 Learning Integration (Self-Evolving Research)
**Activities:**
- Implement feedback loop from user edits/acceptance
- Add confidence adjustment based on success rates
- Create pattern recognition improvement mechanisms
- Build "sleep pass" for nightly learning consolidation

**Learning Mechanisms:**
- Track acceptance vs edit rates per skill
- Adjust confidence thresholds based on performance
- Identify successful patterns for strengthening
- Decay unused or poorly performing reflexes

**Deliverables:**
- Learning system implementation
- Feedback loop validation
- Performance improvement tracking

---

## Phase 4: Advanced Integration & Testing (Week 5-6)
**Goal**: Full system integration with advanced features

### 4.1 Advanced Strategy Integration
**Activities:**
- Implement `FocusOfWeek.md` for tactical priorities
- Add strategic alignment detection in reflex decisions
- Create strategy-biased agenda generation (/predict-needs command)
- Test strategic priority multiplication in real scenarios

**Strategic Priority Formula:**
```
score = 0.30*DeadlineProximity + 0.25*ActiveProject + 0.15*KeyPeopleFrequency 
      + 0.10*StandardProcess + 0.10*Recency + 0.05*Historical + 0.05*ArchivedPenalty

Strategy Multiplier:
- Direct objective link: 1 + ObjectiveWeight
- One hop via project: 1 + 0.5*ObjectiveWeight  
- Focus-of-week: add Focus.boost

Final: priority = score * Multiplier (capped at 2.0)
```

**Deliverables:**
- Advanced strategy integration
- Priority scoring validation
- Strategic alignment testing

### 4.2 Workflow Integration Testing
**Activities:**
- Comprehensive testing with existing vault patterns
- WhatsApp MCP integration with production reports
- Cross-system compatibility verification
- Performance optimization and response time measurement

**Testing Scenarios:**
- Daily workflow simulation
- Production report processing
- Project status updates
- Meeting note generation
- Task management workflows

**Deliverables:**
- Integration testing results
- Performance benchmarks
- Compatibility verification

### 4.3 Advanced Commands Implementation
**Activities:**
- `/mirror-vault`: Full vault rescan capability
- `/learn-patterns`: Manual learning consolidation
- `/predict-needs`: Strategy-biased agenda generation
- `/optimize-workflow`: Analysis of edit patterns and reflex tuning

**Command Specifications:**
```bash
/mirror-vault     # Emergency full rescan (use sparingly)
/learn-patterns   # Manual sleep pass execution
/predict-needs    # 24-72h agenda with strategy bias
/optimize-workflow # Edit hotspots and threshold tuning
```

**Deliverables:**
- Advanced command implementation
- User interface design
- Documentation and help system

---

## Phase 5: Production Deployment & Optimization (Week 6+)
**Goal**: Live deployment with monitoring and continuous improvement

### 5.1 Migration Execution
**Activities:**
- Gradual rollout starting with non-critical workflows
- User acceptance testing with real work patterns
- Performance monitoring and optimization
- Issue tracking and rapid resolution

**Rollout Strategy:**
1. Start with inbox triage and daily notes
2. Add meeting and task workflows
3. Enable production report processing
4. Full strategic alignment activation

**Deliverables:**
- Production deployment
- User training materials
- Support documentation

### 5.2 Learning & Adaptation
**Activities:**
- Monitor success metrics from Strategic Analysis
- Calibrate confidence thresholds based on real usage
- Measure strategic alignment effectiveness
- Optimize performance and response times

**Success Metrics Monitoring:**
- **Speed**: Median response time for common workflows
- **Quality**: Acceptance rate with minimal edits
- **Learning**: Pattern recognition improvement over time
- **Strategic Alignment**: High-priority actions linked to objectives

**Deliverables:**
- Performance monitoring dashboard
- Success metrics tracking
- Continuous improvement process

---

## Technical Architecture Summary

### **Memory & Graph Services (MCP)**
- Basic Memory: Document chunks with embeddings + file/line anchors
- Knowledge Graph: Property graph with people/sites/projects/tasks relationships
- Strategic integration: Objective linking and priority multiplication

### **Obsidian Watcher Plugin**
- Real-time file event monitoring with debouncing
- Metadata extraction using Obsidian API
- Automatic MCP service updates
- Hash-based change detection for efficiency

### **Behavioral Intelligence Stack**
- **Reflex Cache**: Q→A patterns with confidence scoring
- **Skills Library**: Domain-specific "how Greg does it" templates
- **Policy Memory**: Always-on rules for consistency
- **Gatekeeper**: Confidence-based routing (fast vs deliberate)

### **Sub-Agent Architecture**
- Specialized Claude.md contexts for domain expertise
- Skill → sub-agent spawning for complex workflows
- Coordinated execution with main Claude CLI

### **Learning System**
- User feedback integration (edits, acceptance, rejection)
- Confidence threshold adaptation
- Pattern strengthening and decay
- Nightly consolidation ("sleep pass")

---

## Risk Mitigation & Success Factors

### **Zero-Disruption Approach**
- All existing workflows continue unchanged
- Progressive enhancement without breaking patterns
- 100% backward compatibility with current commands
- Git-based rollback for easy reversion

### **Source-Grounded Integrity**
- Mandatory citations for all factual claims
- File/line anchor requirements
- No AI hallucination tolerance
- Transparent reasoning paths

### **Conservative Learning**
- High confidence requirements for auto-execution
- User approval for ambiguous cases
- Manual override capabilities
- Safe failure modes

### **Strategic Integration**
- Company/department strategy as first-class priorities
- Objective-based work prioritization
- Tactical focus adjustment capabilities
- Alignment measurement and optimization

---

## Next Steps

1. **Review and Refinement**
   - Share with GPT-5 for technical review
   - Iterate based on feedback and recommendations
   - Finalize technical specifications

2. **Phase 0 Execution**
   - Begin current vault analysis
   - Research sub-agent architecture
   - Design migration strategy

3. **Implementation Kickoff**
   - Establish development environment
   - Set up testing framework
   - Begin Phase 1 development

---

*This implementation plan represents the evolution of MarthaVault from static knowledge repository to intelligent, adaptive AI assistant while preserving all existing workflows and maintaining source-grounded integrity.*