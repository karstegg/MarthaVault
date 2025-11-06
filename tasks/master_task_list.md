---
'Status:': Active
'Priority:': High
'Assignee:': Greg
'DueDate:': null
'Tags:': null
'LastUpdated:': 2025-10-06
permalink: tasks/master-task-list
---

# Master Task List

**Last Consolidated**: 2025-10-06
**Open Tasks**: 76
**Archived Tasks**: See [[tasks/archive/2025-Q3-completed.md]]

---

## Pending Tasks (Unscheduled)
- [x] Share HD54 fire investigation recommendations with Sfiso (WWW format) #task #year/2025 #priority/high #fire-safety ✅ 2025-11-05
- [x] PDI procedure review with Gerhard - add section to inspect fire suppression systems #task #year/2025 #priority/high #fire-safety ✅ 2025-11-05
- [ ] UV128 CAS installation and testing (arranged with [[Sipho Dubazane]] and Jade at Gloria) #task #year/2025 #priority/medium #CAS #site/Gloria
- [ ] Write motivation for extra electrical foreman at N3 #task #year/2025 #priority/medium #site/Nchwaning3
- [ ] Capture weekly charts #task #year/2025 #priority/medium
- [ ] Follow up re SA Cranes VO for 6 months extension by Emile (Central procurement) #task #year/2025 #priority/medium
- [ ] Update Vehicle List with latest information #task #year/2025 #priority/medium #admin
- [ ] HD RT action plan for Gloria - Assigned to [[Dubazane, Sipho]] #task #year/2025 #priority/high #site/Gloria
  - Note: Requested by [[Rudi Opperman]]
- [ ] Create response protocol document for new belt rip detector #task #year/2025 #priority/medium #safety #documentation
- [ ] Update BWE scope document - Assigned to [[Kotze, Johan]] #task #year/2025 #priority/medium #documentation
- [ ] BEV vent doors & fire doors - waiting on [[Mabona, Mduduzi]] for updated capital application #task #year/2025 #priority/high #BEV #capital
- [ ] BEV Bay 2 minisub - Assigned to [[Lourens van der Heerden]] #task #year/2025 #priority/high #BEV #capital
  - Action: Make minisubs stock items to fast-track procurement (bypass contract process)
  - Waiting on [[Mabona, Mduduzi]] for capital application finalization
- [ ] Kenru fire orders for SOT and Gloria - Assigned to [[Sipho Dubazane]] #task #year/2025 #priority/medium #site/Nchwaning2 #site/Gloria
- [ ] S2 & BEV Meeting - Order follow-up (Matthews from Epiroc) - Assigned to [[Michael Bester]] #task #year/2025 #priority/medium #site/Nchwaning2 #BEV
  - Note: One-month order for HD62/S2 optimization project
- [ ] DT & FL radio installations - apply for unplanned capital (N3 & N2) - Assigned to [[Sease, Sello]], assisted by [[Swanepoel, Pieter]] #task #year/2025 #priority/critical #site/Nchwaning3 #site/Nchwaning2 #capital #radios 📅 2025-11-30
  - Rudi approved in N3 ATR meeting (2025-10-23)
- [ ] Prepare monthly N3 infrastructure status presentation (Leaky Feeder, Illumination, Power, Blasting Boxes, Sperrosense) - Assigned to [[Sease, Sello]] #task #year/2025 #priority/high #site/Nchwaning3 #infrastructure 📅 2025-11-01
- [ ] Prepare interview questions for junior engineer position #task #year/2025 #priority/medium #recruitment #engineering 📅 2025-11-15
  - Reference: [[tasks/2025-10-29 – Junior Engineer Interview Questions.md]]
  - Context: Related to team capacity building (Q4 2025 strategic priority)

### BEV Equipment & Epiroc (Week 18-24 Oct Report) - Assigned to Philip Moller (Epiroc)
- [ ] DT171 - Replace A-frame bearing (5+ days down) - Assigned to Philip Moller (Epiroc) #task #year/2025 #priority/critical #BEV #equipment #Epiroc 📅 2025-10-28
  - Standing at parking bay awaiting repair
  - Reference: [[projects/BEV/2025-10-18 – BRMO Epiroc Weekly Report (Week 18-24 Oct).md]]
- [ ] Follow up on Strata delays impacting FL112 availability (~24hrs lost) - Assigned to Philip Moller (Epiroc) #task #year/2025 #priority/high #BEV #3rd-party #Epiroc 📅 2025-10-30
- [ ] Renew NCH3 Certiq/Mobilaris support contract (CRITICAL - blocks S2 optimization) - Assigned to Philip Moller (Epiroc) #task #year/2025 #priority/critical #Certiq #site/Nchwaning3 #contract #Epiroc 📅 2025-11-01
- [ ] Complete BEV machines CAS L9 software upgrades at N3 - Assigned to Philip Moller (Epiroc) #task #year/2025 #priority/high #BEV #CAS #site/Nchwaning3 #Epiroc 📅 2025-11-05
- [ ] Complete Gloria ST14 software updates for CAS L9 - Assigned to [[van Niekerk, Hennie]] #task #year/2025 #priority/high #CAS #site/Gloria 📅 2025-11-05

## MarthaVault System Development (Agent Skills, Plugins, Context Management)

### Phase: Agent Skills Implementation
- [ ] Complete article review: Plugins (`Customize Claude Code with plugins.md`) #task #year/2025 #priority/high #system #MarthaVault
  - Reference: [[personal/projects/MarthaVault Intuition Layer/2025-10-19 - Claude Code Plugins Discussion Summary]]
- [ ] Complete article review: Context Management (`Managing context on the Claude Developer Platform.md`) #task #year/2025 #priority/high #system #MarthaVault
  - Reference: [[personal/projects/MarthaVault Intuition Layer/2025-10-19 - Context Management Discussion Summary]]
- [ ] Complete article review: Fast Context / Code Search (`Introducing SWE-grep...`) #task #year/2025 #priority/high #system #MarthaVault

### Phase 1: Skills - Create Individual Skills
- [ ] Create `marthavault-triage` skill (Proof of Concept) #task #year/2025 #priority/high #system #MarthaVault
  - Note: Implement ~/.claude/skills/marthavault-triage/ with validate_frontmatter.py, generate_filename.py, mirror_task.py
  - Reference: [[personal/projects/MarthaVault Intuition Layer/2025-10-19 - Agent Skills Discussion Summary]]
- [ ] Create `marthavault-tasks` skill #task #year/2025 #priority/high #system #MarthaVault
- [ ] Create `memory-query-patterns` skill #task #year/2025 #priority/high #system #MarthaVault

### Phase 2: Hooks + Subagents - PRIORITY
- [ ] Implement Memory Update Subagent (agents/memory-update-agent.md) #task #year/2025 #priority/critical #system #MarthaVault
  - Benefit: Real-time memory sync, replaces `/sync-vault`
  - Reference: [[personal/projects/MarthaVault Intuition Layer/2025-10-19 - Claude Code Plugins Discussion Summary]]
- [ ] Implement Post-File-Change Hook (hooks/post-file-change.md) #task #year/2025 #priority/critical #system #MarthaVault
  - Benefit: Automatic, incremental memory updates
- [ ] Implement Post-Task-Creation Hook (hooks/post-task-creation.md) #task #year/2025 #priority/high #system #MarthaVault
  - Benefit: Automatic task mirroring
- [ ] Implement Memory Query Subagent (agents/memory-query-agent.md) #task #year/2025 #priority/high #system #MarthaVault
  - Benefit: Intelligent context retrieval from Graph vs Basic Memory

### Context Management Implementation
- [ ] Verify Context Editing (test with 30+ file triage session) #task #year/2025 #priority/high #system #MarthaVault
  - Reference: [[personal/projects/MarthaVault Intuition Layer/2025-10-19 - Context Management Discussion Summary]]
- [ ] Check Memory Tool Availability in Claude Code (/tools list) #task #year/2025 #priority/high #system #MarthaVault
- [ ] Configure Memory Tool storage directory (C:\Users\10064957\.martha\memory\) #task #year/2025 #priority/high #system #MarthaVault
- [ ] Test Memory Tool basic operations (CRUD) #task #year/2025 #priority/high #system #MarthaVault
- [ ] Integration testing: Context Editing + Memory Tool + MCP systems #task #year/2025 #priority/high #system #MarthaVault

### Fast Context & Code Search Integration
- [x] Verify Fast Context works for markdown #task #year/2025 #priority/high #system #MarthaVault
  - Reference: [[personal/projects/MarthaVault Intuition Layer/2025-10-19 - Fast Context and Code Search Discussion Summary]]
  - Status: CONFIRMED
- [x] Test vault-wide search #task #year/2025 #priority/high #system #MarthaVault
  - Status: CONFIRMED (BEV search: 487 matches, 104 files)
- [ ] Test complex cross-reference queries (person mentions, tags, strategic alignment) #task #year/2025 #priority/medium #system #MarthaVault
- [ ] Measure productivity impact (time saved, flow maintenance) #task #year/2025 #priority/medium #system #MarthaVault
- [ ] Integrate Fast Context into daily workflows (standup prep, status checks, meeting context) #task #year/2025 #priority/medium #system #MarthaVault
- [ ] Optimize vault for Fast Context (tagging consistency, frontmatter, naming conventions) #task #year/2025 #priority/low #system #MarthaVault
- [ ] Document Fast Context patterns and optimal query phrasing #task #year/2025 #priority/low #system #MarthaVault

## Monday Recurring Tasks (Weekly)
- [ ] Approve all job cards on JDE 📅 2025-10-13 #task #year/2025 #priority/high #recurring #admin
- [x] Check and approve timesheets on Firefly 📅 2025-10-13 #task #year/2025 #priority/high #recurring #admin
- [ ] Approve leave requests on Oracle 📅 2025-10-13 #task #year/2025 #priority/high #recurring #admin
- [x] Complete Weekly Engineering Report 📅 2025-10-13 #task #year/2025 #priority/critical #recurring

## Monthly Recurring Tasks
- [ ] Process VFL Schedule when received (extract Greg's assignments to calendar) 📅 2025-11-01 #task #year/2025 #priority/medium #recurring #SHEQ #VFL
  - Note: Apply VFL Schedule Processing skill - see [[system/skills/vfl-schedule-processing.md]]

---

## URGENT & OVERDUE TASKS

### Fire Safety - HD0054 Incident (CRITICAL)
- [ ] Review HD0054 Fire Investigation Report (Alexis Basson) 📅 2025-10-07 #task #year/2025 #priority/critical #fire_safety
  - Note: Independent fire expert report. Actions from this report must be extracted and tracked
- [ ] HD0054 Fire - Identify and document all outstanding close-out actions 📅 2025-10-09 #task #year/2025 #priority/critical #fire_safety
  - Note: Consolidate all HD0054 actions from audits, investigations, and DMRE feedback
- [ ] DMRE Actions Status Update (HD54 fire + additional infra) 📅 2025-10-08 #task #year/2025 #priority/critical #compliance #DMRE
  - Note: Status report for DMRE on HD54 close-out and infrastructure actions

### Recruitment (CRITICAL)
- [x] JPE Recruitment Motivation - Follow up on status 📅 2025-10-07 #task #year/2025 #priority/critical #recruitment
  - Note: Asked [[Rudi Opperman]] on WhatsApp. No response yet. Need 2 JPEs for DPF project
- [x] Follow up on approvals for JPE recruitment memo 📅 2025-10-08 #task #year/2025 #priority/critical #recruitment
  - Status: Completed - approvals received
- [ ] Place advertisement for Junior Project Engineers position #task #year/2025 #priority/high #recruitment
  - Note: Follows approval for appointments
- [ ] Draft N3 Electrical Foreman Recruitment Motivation 📅 2025-10-07 #task #year/2025 #priority/critical #recruitment #site/Nchwaning3
  - Note: Second Electrical Supervisor for N3 - motivation to increase complement to 2x foremen

### Capital Projects (HIGH)
- [ ] SHERQ Bakkies Capex - Follow up or escalate to [[Garth Schreiner]] for Signhub routing 📅 2025-10-07 #task #year/2025 #priority/high #capital
  - Project: SHERQ LDVs
  - Note: Requested by [[Johan Vermeulen]]. Capex compiled, under review
- [ ] Track progress on SK grader capital application 📅 2025-10-10 #task #year/2025 #priority/medium #capital
  - Assigned to: [[Nzuza, Sikelela]]
  - Note: Grader from Aard. Delegated to SK via email 2025-10-06
- [/] Prepare 6 month extension variation order for SA Crane contract #task #priority/medium 📅 2025-10-14 #year/2025 #contract #SA_Cranes
  - Status: In progress - Emile received, routing for approvals
- [x] Send VO documentation to Emile at Central Logistics Hub #task #priority/medium 📅 2025-10-14 #year/2025 #contract #SA_Cranes

### FY25/26 Capital TMM Replacement Programme (CRITICAL)
**See**: [[Capital TMM Procurement Tracker FY25-26]] for full tracker (29 units, R157.3M)

#### Gloria - URGENT Replacements (Sipho & John)
- [x] Gloria DT0105/DT0106 dump truck replacement - Finalize specs 📅 2025-10-31 ✅ 2025-11-04 #task #year/2025 #priority/critical #capital #site/Gloria
  - Assigned to: [[Dubazane, Sipho]] (Engineer), [[Eiler, John]] (Planner)
  - Equipment: 2x MT 436 LP (2015 models - 10 years old) → Elphinstone AD30
  - Budget: R40.3M
  - Note: OLDEST PRODUCTION TMM IN FY25/26 PLAN - Bundle order for volume discount
  - Completed: Specs finalized 2025-11-04
- [ ] Gloria DT0105/DT0106 - Request Epiroc quotations 📅 2025-11-30 #task #year/2025 #priority/critical #capital #site/Gloria
  - Assigned to: [[Eiler, John]]
  - Note: 2-unit bundle quotation
- [x] Gloria DT0105/DT0106 - Place purchase orders 📅 2025-12-15 ✅ 2025-11-04 #task #year/2025 #priority/critical #capital #site/Gloria
  - Assigned to: [[Dubazane, Sipho]]
  - Note: Orders placed 2025-11-04 (6 weeks early!)
  - Delivery: Expected end November 2025 (faster than typical 18-month lead time)

#### Nchwaning 3 - Production TMM (Sello, Kagisho, Joyce)
- [ ] N3 RT0039 roof bolter replacement - Finalize specs 📅 2025-10-31 #task #year/2025 #priority/critical #capital #site/Nchwaning3
  - Assigned to: [[Sease, Sello]] (Engineer), [[Goeieman, Kagisho]] (Planner)
  - Equipment: Boltec 235H (2014 - 11 years old)
  - Budget: R19.3M
  - Note: SAFETY-CRITICAL EQUIPMENT
- [ ] N3 RT0039 - Request Epiroc quotations 📅 2025-11-30 #task #year/2025 #priority/critical #capital #site/Nchwaning3
  - Assigned to: [[Goeieman, Kagisho]]
- [ ] N3 Scalers (SR0024/0028/0030) - Bundle specifications 📅 2025-11-15 #task #year/2025 #priority/high #capital #site/Nchwaning3
  - Assigned to: [[Sease, Sello]], [[Diale, Joyce]]
  - Equipment: 3x Super 220E → Scaler 220 E, 4-Wheeler
  - Budget: R18.4M (bundle discount opportunity)
  - Note: Central Section, N3, North Section deployments
- [ ] N3 Scalers - Request bundle quotations 📅 2025-12-15 #task #year/2025 #priority/high #capital #site/Nchwaning3
  - Assigned to: [[Diale, Joyce]]
- [ ] N3 DT0143 dump truck replacement - Finalize specs 📅 2025-11-30 #task #year/2025 #priority/high #capital #site/Nchwaning3
  - Assigned to: [[Sease, Sello]], [[Goeieman, Kagisho]]
  - Equipment: AD45 → AD30 (standardization)
  - Budget: R20.2M

#### Nchwaning 2 - Critical Replacements (SK & Wikus)
- [ ] N2 LD0199 light vehicle replacement - Finalize specs 📅 2025-11-30 #task #year/2025 #priority/critical #capital #site/Nchwaning2
  - Assigned to: [[Nzuza, Sikelela]] (Engineer), [[Wikus]] (Planner)
  - Equipment: 4x4 2.5D (2007 - 18 YEARS OLD) → L/Cruiser 4x4 UG Spec
  - Budget: R2.9M
  - Location: N2 SHERQ
  - Note: OLDEST VEHICLE IN ENTIRE FY25/26 PLAN
- [ ] N2 L/Cruiser 5-unit bundle - Finalize specs 📅 2025-12-31 #task #year/2025 #priority/high #capital #site/Nchwaning2
  - Assigned to: [[Nzuza, Sikelela]], [[Wikus]]
  - Equipment: LD0341/0411/0414/0415/0199 (5 units)
  - Budget: R14.6M
  - Note: Bundle for volume discount (~R1.1M potential savings)

#### Overall Programme Management
- [ ] Capital TMM FY25/26 - Monthly progress review 📅 2025-11-07 #task #year/2025 #priority/high #capital #recurring
  - Assigned to: [[Chris]] (Asset Care Engineer), [[Rahab]] (Chief Planner oversight)
  - Note: First monthly review - track all 29 units, budget vs actual
  - Reference: [[Capital TMM Procurement Tracker FY25-26]]

---

## BEV PROGRAMME

### BEV Fire Safety Programme (Nchwaning 3) - CRITICAL PRIORITY
- [ ] Audit BEV storage areas for compliance with OEM specifications #task #year/2025 #BEV #storage #audit #priority/critical #site/Nchwaning3 📅 2025-10-15
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Review current BEV storage procedures against Epiroc recommendations #task #year/2025 #BEV #fire-safety #epiroc #priority/critical #site/Nchwaning3 📅 2025-10-15
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Implement enhanced lockout/tagout procedures for BEV maintenance #task #year/2025 #BEV #safety #lockout #priority/critical #site/Nchwaning3 📅 2025-10-20
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Review BEV fire risk assessment #task #BEV #fire-safety #priority/high #year/2025 #site/Nchwaning3 📅 2025-10-10
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Complete fire risk immediate actions #task #BEV #fire-safety #priority/high #year/2025 #site/Nchwaning3 📅 2025-10-10
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Finalize fire procedure for operators #task #BEV #fire-safety #priority/high #year/2025 #site/Nchwaning3 📅 2025-10-15
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Coordinate fire training with [[Koekemoer, Willie]] (Training Manager) #task #year/2025 #BEV #fire-safety #priority/high #site/Nchwaning3 📅 2025-10-18
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Coordinate with Mine Rescue Services on Li-Ion fire response protocols #task #year/2025 #BEV #mine-rescue #fire-safety #priority/high #site/Nchwaning3 📅 2025-10-25
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Update BEV Fire Risk Assessment incorporating Epiroc findings #task #year/2025 #BEV #risk-assessment #priority/medium #site/Nchwaning3 📅 2025-10-30
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme
- [ ] Enhance staff training program on Li-Ion battery safety #task #year/2025 #BEV #training #safety #priority/medium #site/Nchwaning3 📅 2025-10-31
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Battery Fire Safety Programme

### BEV Charging Bay #2 Project (Nchwaning 3)
- [/] Place charger order by end of week #task #BEV #chargers #order #priority/high #year/2025 #site/Nchwaning3 📅 2025-10-11
  - Assigned to: [[Goeieman, Kagisho]] (N3 Planner)
  - Project: BEV Charging Bay #2 project
  - Note: Check proposal from [[Kishore Jeebodh]] and place order urgently
- [x] Confirm delivery timeline with vendor #task #BEV #chargers #delivery #priority/medium #year/2025 #site/Nchwaning3 📅 2025-10-15
  - Assigned to: [[Johnny Hollenbach]]
  - Project: BEV Charging Bay #2 project

### BEV Operations
- [/] Set up BaaS battery availability measurement system #task #BaaS #battery #availability #year/2025 #site/Nchwaning3
  - Assigned to: [[Chris Ross]], [[Rahab Makolomakwa]]
  - Project: BEV battery performance monitoring
  - Note: Mail sent to Chris Ross, Ronnie, and Phillip. Must track availability independently to verify Epiroc invoicing (penalties for low availability, payment above threshold)

### BEV Maintenance & Reliability (from Weekly Reports)
- [ ] Follow up on DT 162 dropbox delivery from Kathu workshop #task #BEV #priority/high #maintenance #year/2025 #site/Nchwaning3 📅 2025-10-18
  - Assigned to: [[Sease, Sello]], [[Piet]]
  - Note: Extended breakdown (5+ days) - dropbox and motor replacement required
  - Source: [[projects/BEV/WeeklyReports/2025-10-04 - BEV Weekly Report Summary (Epiroc)]]
- [ ] Order charger modules for Charger 4 Module 1 and Charger 5 Module 4 #task #BEV #priority/high #chargers #year/2025 #site/Nchwaning3 📅 2025-10-18
  - Assigned to: [[Sease, Sello]], [[Piet]]
  - Note: Faulty modules affecting charging capacity
  - Source: [[projects/BEV/WeeklyReports/2025-10-04 - BEV Weekly Report Summary (Epiroc)]]
- [ ] Order upgraded spring sets for CCS connector cable replacements (Posts 3, 6, 7) #task #BEV #priority/medium #chargers #year/2025 #site/Nchwaning3 📅 2025-10-21
  - Assigned to: [[Sease, Sello]], [[Piet]]
  - Note: 300A cables received, awaiting spring sets
  - Source: [[projects/BEV/WeeklyReports/2025-10-04 - BEV Weekly Report Summary (Epiroc)]]
- [ ] Schedule BEV machines CAS L9 software upgrades #task #BEV #priority/medium #CAS #year/2025 #site/Nchwaning3 📅 2025-10-25
  - Assigned to: [[Moller, Phillip]] (Epiroc Site Manager)
  - Note: All other fleet complete, BEV machines pending
  - Source: [[projects/BEV/WeeklyReports/2025-10-04 - BEV Weekly Report Summary (Epiroc)]]
- [ ] Review NCH3 Certiq & Mobilaris support contract before S2 optimization #task #BEV #priority/medium #Certiq #year/2025 #site/Nchwaning3 📅 2025-10-31
  - Assigned to: [[Karsten, Gregory]]
  - Note: Support contract expired, needs review
  - Source: [[projects/BEV/WeeklyReports/2025-10-04 - BEV Weekly Report Summary (Epiroc)]]
- [ ] Monitor Strata interference investigation progress (loader-truck crawling) #task #BEV #priority/high #Strata #year/2025 #site/Nchwaning3 📅 2025-10-11
  - Assigned to: [[van Niekerk, Hennie]]
  - Note: FL98 had new IM installed, wiring rerouted. Suspected external frequencies affecting system
  - Source: [[projects/BEV/WeeklyReports/2025-10-04 - BEV Weekly Report Summary (Epiroc)]]

---

## HD0054 FIRE ACTIONS (Nchwaning 3)

- [ ] Fit Lubri Vent systems on all S2 drill rigs #task #safety #HD54 #fire-prevention #lubrivent #year/2025 #site/Nchwaning3 #priority/high 📅 2025-10-15
  - Assigned to: [[Sello Sease]]
  - Note: Critical fire prevention action from HD0054 incident
- [ ] Add fire suppression system checks to pre-start procedures #task #safety #fire-suppression #pre-start #procedures #year/2025 #priority/medium 📅 2025-10-10
  - Assigned to: [[Chris Ross]]
  - Note: Procedural change to prevent future incidents

---

## CAPITAL & EQUIPMENT PROJECTS

### Nchwaning 2
- [x] N2 Substation Project - Follow up with [[Rudi Opperman]] and [[Roelie Prinsloo]] after James Collins feedback 📅 2025-10-08 #task #year/2025 #priority/high #capital #site/Nchwaning2
  - Project: Underground main incomer substation upgrade project
  - Note: Complete - Roelie can proceed with deviation note motivation to bypass tender process
  - Key people: [[Roelie Prinsloo]], [[Nzuza, Sikelela]], [[Anton Koorzen]], [[Jaco du Toit]] from [[Iritron]]
- [x] N2 LHD Issues - Coordinate documentation with [[Lourens van Heerden]] 📅 2025-10-08 #task #year/2025 #priority/medium #site/Nchwaning2
- [ ] Complete two-way radio vendor evaluation (60 units for N2 shaft) #task #capital #radios #N2-shaft #priority/low #year/2025 #site/Nchwaning2
  - Note: From monthly mining planning meeting. Need unplanned capex application
- [ ] Calculate emergency generator capacity for N2 #task #year/2025 #site/Nchwaning2 #priority/low

### Nchwaning 3
- [/] Follow up on leaky feeder vendor onboarding and project start #task #leaky-feeder #priority/high #year/2025 #site/Nchwaning3
  - Status: In progress - order routing for approval
  - Note: Contract finalized 2025-10-03
  - Action: Check with [[Lizette]] if order is placed

### Gloria
- [ ] Capital Project: Gloria Chute Replacement #task #year/2025 #capital #site/Gloria #priority/medium
  - Assigned to: [[Dubazane, Sipho]]
  - Note: Sipho managing this project

### Multi-Site / Unspecified
- [ ] Illumination capital - discuss with [[Rudi Opperman]] and get estimates from Engineers #task #capital #illumination #year/2025 #priority/medium
  - Note: Underground illumination installations. Part of DMR action
- [ ] Complete capital vote closures #task #capital #vote-closures #year/2025 #priority/low
- [ ] Implement DPF on all Diesel Machines starting with CAT AD30s #task #year/2025 #priority/high #emissions
  - Note: Diesel Particulate Filters. Reason for 2 JPEs recruitment
  - Project: DPF Project
- [ ] Gerhard to obtain quote from Barlows for DPF implementation #task #year/2025 #priority/medium #emissions
  - Assigned to: [[Gerhard van den Berg]]
  - Project: DPF Project

---

## SAFETY & COMPLIANCE

### WTW Audit Outstanding Actions
- [ ] WTW-N2: Implement lifter plug protocol at Gloria 120N/124W - EXPLOSION RISK #task #WTW-audit #safety #site/Gloria #priority/critical #year/2025 📅 2025-10-15
  - Note: Critical safety item - explosion risk
- [ ] WTW-N27: Emergency structural assessment Gloria decline entrance cracks #task #WTW-audit #structural #site/Gloria #priority/critical #year/2025 📅 2025-10-15
  - Note: Structural integrity concern
- [ ] WTW-N7: Schedule room integrity tests Gloria 90Y gas suppression systems #task #WTW-audit #fire-protection #site/Gloria #priority/critical #year/2025 📅 2025-10-20
  - Note: Fire suppression compliance
- [ ] WTW-N12: Audit in-house bonding/earthing equipment SANAS certification #task #WTW-audit #SANAS #electrical #priority/critical #year/2025 📅 2025-10-20
- [ ] WTW-P62: Follow up SA Cranes SANAS accreditation for lifting equipment certificates #task #WTW-audit #SANAS #SA-Cranes #lifting-equipment #priority/high #year/2025 📅 2025-10-15
- [ ] WTW-P73: Confirm lightning protection systems SANAS certification (SANS 10313/62305) #task #WTW-audit #SANAS #lightning-protection #priority/high #year/2025 📅 2025-10-15
- [ ] WTW-N13: Verify BTU battery protection system SANAS compliance (Gloria substations) #task #WTW-audit #SANAS #BTU #electrical #site/Gloria #priority/high #year/2025 📅 2025-10-15

### General Safety & Compliance
- [ ] Lifting Equipment vs Jacking analysis #task #priority/high #equipment #year/2025 📅 2025-10-20
  - Assigned to: [[Johnny Hollenbach]]
  - Note: Requested procedures from Murray and Roberts for benchmarking
  - Priority: HIGH (escalated 2025-10-15)
- [ ] Review Tyre management procedure #task #year/2025 #safety #maintenance #priority/medium 📅 2025-10-20
  - Note: Action from Scaler incident
- [ ] Review Scaler risk assessment with OEM and stakeholders (visibility) #task #year/2025 #safety #risk-assessment #OEM #priority/medium 📅 2025-10-30
  - Note: Action from Scaler incident - improve visibility
- [ ] Provide DMR Inspector feedback on brake test ramp requirement vs compliance bay status #task #priority/high #year/2025 #compliance #safety #DMR #brake-testing 📅 2025-10-15
  - Note: DMR feedback report response
- [ ] Communicate change management process to all regarding changes #task #year/2025 #safety #change-management #DMRE #priority/medium 📅 2025-10-18
  - Note: DMRE Actions - procedural communication
- [ ] Audit on all Fermels for fire risk #task #year/2025 #fire-safety #audit #priority/medium 📅 2025-10-25
  - Note: Action from N3 incident
- [ ] Aard UV brackets and pump safety interlock valves #task #year/2025 #safety #priority/medium 📅 2025-10-18
  - Note: Follow up with engineers, then write instruction
- [ ] Apply to DMR for Exemption for special signals #task #year/2025 #DMR #priority/medium 📅 2025-10-20
  - Note: Xavier to follow up (action already initiated)
- [ ] Compile report for Scaler audit (SR 30 11_5) #task #year/2025 #audit #priority/medium 📅 2025-10-25
  - Note: SR 30 11_5 is the audit reference
- [ ] Compliance: Chapter 8 S&W Regulation 16 Review 📅 2025-10-15 #task #year/2025 #priority/medium #compliance
  - Note: New winder regulations. Need to understand implementation requirements

### DMR/DMRE Actions
- [ ] Outstanding DMR actions: Drill Torque and speed measurements on Bolters #task #year/2025 #priority/high #DMR 📅 2025-10-20
  - Assigned to: [[Johnny Hollenbach]]
  - Note: From DMR visit - compliance requirement

---

## CAS PROJECT

- [ ] Review all scaler risk assessments and TMM hazard rating documents #task #year/2025 #priority/high #CAS_Project #safety 📅 2025-10-20
  - Note: Understand scaler CAS rating methodology
- [ ] Clarify scope for "Audit of all other TMMs" task #task #year/2025 #priority/medium #CAS_Project 📅 2025-10-15
  - Note: CLARIFICATION NEEDED - which TMMs? What's the audit scope? Related to CAS project?

---

## EQUIPMENT & MAINTENANCE

- [ ] Fire Door Capital project - Get specifics from [[Mduduzi Mabona]] #task #year/2025 #priority/medium #capital 📅 2025-10-15
  - Assigned to: [[Mduduzi Mabona]] (EIT managing)
  - Note: CLARIFICATION NEEDED - which doors? Which site? Scope?
- [ ] Tappet cover melting point investigation - Follow up with Christo vd Westhuizen #task #year/2025 #priority/medium 📅 2025-10-10
  - Note: Waiting for lab melting point test results
- [ ] VO for SA Cranes (6-month variation order) #task #year/2025 #priority/high #SA_Cranes 📅 2025-10-15
  - Note: Need to issue 6-month Variation Order for current contract

---

## DELEGATION & FOLLOW-UP

- [ ] [[Dubazane, Sipho]] to draft instructions on breakdowns in decline #task #year/2025 #priority/medium #site/Gloria 📅 2025-10-15
  - Assigned to: [[Dubazane, Sipho]]
- [ ] Actions from Friday meeting with N2 Eng Team #task #year/2025 #site/Nchwaning2 #priority/high 📅 2025-10-08
  - Note: Follow-up actions from engineering team meeting - need to extract specific tasks

---

## LOW PRIORITY / IDEAS

- [ ] Add battery performance slide to weekly report generator #task #year/2025 #priority/low #idea #BEV
  - Note: Future enhancement - track battery performance trends and long-standing breakdowns

---

## PERSONAL PROJECTS

- [ ] Manually delete MCP-Microsoft-Office folder from MarthaVault (Google Drive locked) #task #personal #cleanup #priority/low #year/2025

---

## NOTES & CLARIFICATIONS NEEDED

**Tasks requiring clarification** (follow up with stakeholders):

1. **Line 17 (CAS)**: "Audit of all other TMMs" - Which TMMs? Full scope?
2. **Fire Door Capital**: Get site/door specifics from Mduduzi
3. **VO for SA Cranes**: Confirm 6-month VO details
4. **WTW Audit reference codes**: Confirm N2, N27, N7, N12, P62, P73, N13 are correct audit finding numbers
5. **N2 LHD Issues**: Get specifics from Lourens on what documentation is needed

**Completed tasks archived**: See [[tasks/archive/2025-Q3-completed.md]] for 108 completed tasks (Aug-Oct 2025)

**Duplicates removed**: 35+ duplicate tasks consolidated during 2025-10-06 cleanup

---

**Last Updated**: 2025-10-06 by Claude Code (consolidation & cleanup)
**Next Review**: 2025-10-13 (weekly)