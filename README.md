# MarthaVault: Intelligent AI-Powered Workspace

> **Vision**: Personal AI assistant that feels "intuitive" - understanding work patterns, domain expertise, and strategic priorities across months/years of interaction.

**Current Status**: Version 2.0 - Workspace Focus
**Next Evolution**: Intuition Layer Implementation
**Last Updated**: September 24, 2025

---

## 🧠 **Project Overview**

MarthaVault is an evolving AI-powered workspace management system that combines personal productivity, task management, and knowledge organization with intelligent automation. The system integrates Obsidian's knowledge management capabilities with Claude Code's AI assistance to create a seamless, learning-capable assistant for complex engineering workflows.

### **Core Philosophy**
- **Zero Disruption**: All existing workflows continue unchanged
- **Progressive Enhancement**: Add intelligence without breaking patterns
- **User Control**: Always maintain manual override capabilities
- **Source Grounding**: Citations required for all factual responses
- **Strategic Alignment**: Bias toward company/department objectives

---

## 🏗️ **System Architecture**

### **Current Architecture (v2.0)**
```
MarthaVault/
├── 🧠 Obsidian Vault (Knowledge Management)
├── 🤖 Claude Code CLI (AI Assistant)
├── 📁 Git Repository (Version Control)
├── 🔌 MCP Servers (WhatsApp, Memory)
├── 📊 Google Sheets Integration
└── 🎙️ Audio Transcription Tools
```

### **Future Architecture (Intuition Layer)**
```
Enhanced MarthaVault/
├── 🧠 Smart Memory Layer (MCP-based)
├── 👁️ Obsidian Watcher Plugin (Real-time indexing)
├── 🎯 Behavioral Intelligence (Reflex cache)
├── 🤖 Sub-Agent Architecture (Domain specialists)
├── 📈 Strategy Integration Engine
└── 🔄 Learning & Adaptation System
```

---

## 📂 **Repository Structure**

```
MarthaVault/
│
├── 📥 00_inbox/                    # Raw input processing
├── 📋 tasks/                       # Task management system
│   └── master_task_list.md
├── 📁 projects/                    # Active project folders
├── 👥 people/                      # Personnel directory
├── 📚 reference/                   # Knowledge base
│   ├── places/                     # Mine sites, locations
│   ├── equipment/                  # Equipment databases
│   └── company/                    # Organizational info
├── 💡 IDEAS/                       # Innovation pipeline
│   └── Martha Design n Evolution/ # System evolution docs
├── 📅 Schedule/                    # Calendar integration
├── 📄 Archive/                     # Historical content
├── 📱 Templates/                   # Note templates
├── 🎞️ media/                       # File attachments
│   ├── audio/                      # Audio transcriptions
│   ├── image/                      # Screenshots, diagrams
│   ├── documents/                  # PDFs, contracts
│   └── videos/                     # Video content
├── ⚙️ .claude/                     # CLI configuration
└── 🔧 .obsidian/                   # Vault settings
```

---

## ✨ **Key Features & Capabilities**

### **📋 Task Management**
- Master task list with priority scoring
- Obsidian Tasks integration
- Status tracking with due dates
- Strategic alignment scoring (future)

### **👥 People & Places**
- Personnel directory with roles and projects
- Mine site references and operational context
- Organizational hierarchy mapping
- Automated assignment logic

### **📱 Integrations**
- **WhatsApp MCP Server**: Production report processing
- **Google Sheets API**: History tracking and logging
- **Audio Transcription**: Meeting and field note processing
- **Production Reports Bridge**: Cross-repository data access

### **🏷️ Tagging & Organization**
- **Primary Tags**: `#meeting`, `#task`, `#idea`, `#decision`
- **Contextual Tags**: `#year/2025`, `#site/Nchwaning2`, `#priority/high`
- **Project Tags**: `#BEV`, `#CAPEX`, `#Safety`, `#Maintenance`
- **Auto-linking**: People, places, equipment, and concepts

---

## 🎯 **Current Implementation (v2.0)**

### **Workflow Patterns**
1. **📥 Intake & Triage**: Raw content → `00_inbox/` → `/triage` → organized folders
2. **📋 Task Management**: Individual tasks → `master_task_list.md` → status tracking
3. **👥 People-Centric**: Person mentions → auto-linked profiles → project context
4. **📱 Integration**: WhatsApp reports → MCP processing → structured filing

### **Command System**
- `/task` - Add to master task list with tagging
- `/triage` - Process inbox items with classification
- `/nn` or `/new-note` - Create structured notes
- Custom slash commands via `.claude/commands/`

### **File Conventions**
- **Format**: `YYYY-MM-DD – Title.md`
- **Front-matter**: Status, Priority, Assignee, DueDate, Tags
- **Timezone**: UTC+2 (Africa/Johannesburg)
- **Links**: `[[Lastname, Firstname]]` for people, `[[reference/places/SiteName]]` for locations

---

## 🚀 **Intuition Layer Roadmap**

### **Phase 0: Foundation Analysis** (Week 1)
- [x] Current vault analysis & workflow mapping
- [x] Sub-agent architecture research
- [x] Zero-disruption migration strategy design

### **Phase 1: MVP Foundation** (Week 2)
- [ ] Strategy layer implementation (`strategy/` folder)
- [ ] Enhanced MCP integration (Memory + Knowledge Graph)
- [ ] Core policy & skills setup (`system/policy.md`)

### **Phase 2: Obsidian Plugin** (Weeks 3-4)
- [ ] Real-time file monitoring with debouncing
- [ ] Metadata extraction using Obsidian API
- [ ] Hash-based change detection for efficiency
- [ ] Settings UI for MCP endpoints

### **Phase 3: Behavioral Intelligence** (Weeks 4-5)
- [ ] SQLite reflex cache implementation
- [ ] Confidence scoring algorithms
- [ ] Pattern matching (intent + entities + site)
- [ ] Sub-agent spawning for specialized skills

### **Phase 4: Advanced Integration** (Week 5-6)
- [ ] Strategic alignment in reflex decisions
- [ ] Strategy-biased agenda generation (`/predict-needs`)
- [ ] Advanced commands (`/mirror-vault`, `/learn-patterns`)
- [ ] Comprehensive workflow testing

### **Phase 5: Production Deployment** (Week 6+)
- [ ] Gradual migration execution
- [ ] Performance monitoring dashboard
- [ ] Continuous improvement processes
- [ ] Success metrics tracking

---

## 🎛️ **Sub-Agent Architecture**

### **Domain Specialists**
- **🔋 BEV Projects**: Battery safety & fire risk assessment
- **⚙️ Shaft Monitoring**: Maintenance schedules & inspections
- **💰 CAPEX**: Capital project management & approvals
- **📊 Production Reports**: Data analysis & trend identification
- **🛡️ Safety & Compliance**: Regulatory requirements & audits

### **Coordination Flow**
```
Main Claude CLI
      ↓
   Skill Detection
      ↓
Specialized Agent ← Domain Context (Claude.md inheritance)
      ↓
  Result Integration
      ↓
   User Response + Learning
```

---

## 📈 **Strategic Integration**

### **Priority Calculation Formula**
```
Base Priority = 0.30×Deadline + 0.25×ActiveProject + 0.15×KeyPeople
              + 0.10×Standard + 0.10×Recency + 0.05×Historical
              - 0.05×ArchivedPenalty

Strategy Multiplier:
- Direct objective link: 1 + ObjectiveWeight
- One hop via project: 1 + 0.5×ObjectiveWeight
- Focus-of-week: add FocusBoost

Final Priority = Base × Multiplier (capped at 2.0)
```

### **Strategy Components**
- `CompanyStrategy.md` - Long-term objectives
- `ActivePhase.md` - Current quarter focus
- `FocusOfWeek.md` - Tactical priorities

---

## 🔄 **Learning & Adaptation**

### **Confidence-Based Routing**
- **≥ 0.80** + strategy-aligned: Auto-execute
- **0.60-0.79**: Soft confirmation ("Run usual BEV summary?")
- **< 0.60**: Deliberate path with citations
- **Never** auto-execute on first occurrence

### **Learning Mechanisms**
- User edit pattern analysis
- Success rate tracking per skill
- Confidence threshold adaptation
- Pattern strengthening/decay
- Nightly consolidation passes ("sleep")

---

## 🛡️ **Security & Risk Management**

### **Data Protection**
- Local SQLite storage (no cloud AI training)
- Git-based version control & rollback
- Source-grounded responses only
- Mandatory citation requirements

### **Rollback Strategy**
```
Issue Detected → Immediate revert to v2.0
       ↓
Parallel systems until resolved
       ↓
Redesign based on lessons learned
```

---

## 📊 **Success Metrics & KPIs**

### **Performance Targets**
- **⚡ Speed**: <3s median response for common workflows
- **✅ Quality**: >85% acceptance rate for reflexes
- **📈 Learning**: Confidence improvements over 30 days
- **🎯 Strategic**: >70% high-priority actions linked to objectives
- **🔄 Compatibility**: 100% existing workflow preservation

### **Quality Assurance**
- <5% hallucination/citation errors
- Source-grounded response requirements
- User satisfaction with AI assistance
- Workflow efficiency improvements

---

## 🗂️ **Canvas Documentation System**

Visual representations of the system architecture and workflows:

- **`MarthaVault Overview Canvas.canvas`** - Main project overview
- **`MarthaVault Architecture Canvas.canvas`** - Technical deep-dive
- **`MarthaVault Implementation Canvas.canvas`** - Development roadmap
- **`MarthaVault Workflow Canvas.canvas`** - User interaction patterns

*Navigate between canvases using Obsidian's file explorer or quick switcher (Ctrl+O)*

---

## 🏛️ **Project History**

### **Repository Split (August 2025) ✅**
- **MarthaVault**: Task management & workspace (this repository)
- **ProductionReports**: Automated production data processing
- **Benefits**: Clear separation of concerns, improved reliability, independent scaling

### **Original Martha Concept**
- Single interface for engineering workflow
- Structured mode activation with trigger phrases
- Long-term memory with summaries + Drive integration
- **Workflow Loop**: Capture → Process → Record → Move → Recall

### **Version Evolution**
- **v1.0**: Original Martha concept with manual workflows
- **v2.0**: Current workspace focus with basic automation
- **v3.0**: Planned Intuition Layer with adaptive learning

---

## 👥 **Project Team**

- **Lead**: Greg Karsten (architecture, requirements, testing)
- **Technical Advisor**: GPT-5 (implementation strategy, technical review)
- **AI Assistant**: Claude Code (development execution, documentation)

---

## 🚀 **Getting Started**

### **Prerequisites**
- Obsidian desktop application
- Claude Code CLI access
- Node.js (for future plugin development)
- Git for version control

### **Initial Setup**
1. Clone the MarthaVault repository
2. Open as Obsidian vault
3. Configure Claude Code integration
4. Review CLAUDE.md for system instructions

### **Daily Workflow**
1. Check `00_inbox/` for new items
2. Run `/triage` to process overnight content
3. Review `tasks/master_task_list.md` priorities
4. Check `Schedule/` for today's meetings
5. Update project status in relevant folders

---

## 🔗 **Related Documentation**

- **`CLAUDE.md`** - System configuration and instructions
- **`IDEAS/Martha Design n Evolution/`** - Technical evolution documents
- **`personal/projects/MarthaVault Intuition Layer/`** - Implementation planning
- **Canvas files** - Visual system documentation

---

## 📝 **Contributing**

This is a personal workspace management system. The documentation serves as a reference for the system's evolution and capabilities. All development follows the zero-disruption principle to maintain workflow continuity.

---

## 🏷️ **Tags**

#project #AI #productivity #task-management #knowledge-management #obsidian #claude-code #automation #strategic-planning #workflow-optimization

---

*Last updated: September 24, 2025 - README created to document comprehensive MarthaVault system architecture and roadmap*