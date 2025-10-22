# Rule: Assignment Detection and Person Note Creation

## Assignment Detection Patterns

Automatically detect assignees from these phrase patterns:

### Direct Assignment
- "for [Person Name]"
- "[Person Name] to..."
- "ask [Person Name] to..."
- "assign to [Person Name]"
- "[Person Name] will..."
- "[Person Name] should..."

### Examples
- "Draft inspection checklist **for Jane Smith**" → Assignee: Jane Smith
- "**Sipho to** review the blast counts" → Assignee: Sipho Dubazane
- "**Ask Xavier** about the winder status" → Assignee: Xavier Peterson
- "**SK will** complete the GES paperwork" → Assignee: Sikelela Nzuza

## Assignee Front-Matter

When assignment is detected, add to front-matter:

```yaml
---
Assignee:: [[Lastname, Firstname]]
---
```

**Format**: Always use `[[Lastname, Firstname]]` wiki-link format.

## Person Note Creation

If the person note does not exist, create it automatically:

**Location**: `people/Lastname, Firstname.md`

**Template**:
```yaml
---
Status:: #status/active
Type:: #person
Role:: 
Team::
Email::
Phone::
Started::
Tags:: #person #year/2025
---

# Firstname Lastname

## Role


## Contact
- **Email**: 
- **Phone**: 
- **Location**: 

## Projects


## Notes

```

## Known Personnel (Auto-Complete)

When these names are detected, use full details:

### Engineering Team
- **Gregory Karsten** (Greg) - Senior Production Engineer
  - File: `people/Karsten, Gregory.md`
  - Role: Senior Production Engineer
  - Team: Engineering Management
  
- **Sipho Dubazane** - Engineer at Gloria
  - File: `people/Dubazane, Sipho.md`
  - Role: Site Engineer
  - Team: Gloria Mine
  
- **Sikelela Nzuza** (SK) - Engineer at Nchwaning 2
  - File: `people/Nzuza, Sikelela.md`
  - Role: Site Engineer
  - Team: Nchwaning 2
  
- **Sello Simon Sease** (Simon) - Engineer at Nchwaning 3
  - File: `people/Sease, Sello Simon.md`
  - Role: Site Engineer
  - Team: Nchwaning 3
  
- **Xavier Peterson** - Engineer for Shafts & Winders
  - File: `people/Peterson, Xavier.md`
  - Role: Shafts & Winders Engineer
  - Team: S&W Operations

### Management
- **Rudy Opperman** - Operations Manager
  - File: `people/Opperman, Rudy.md`
  
- **Sello Taku** - Engineering Manager
  - File: `people/Taku, Sello.md`

## Nickname Mapping

Map common nicknames to full names:

- **Greg** → Gregory Karsten
- **SK** → Sikelela Nzuza
- **Simon** → Sello Simon Sease

## Assignment Workflow

1. **Detect assignment phrase** in content
2. **Extract person name** from phrase
3. **Check if person note exists** in `people/` folder
4. **Create person note** if missing (using template)
5. **Add assignee to front-matter** using wiki-link format
6. **Link to person note** in content where appropriate

## Multiple Assignees

For tasks with multiple assignees:

```yaml
---
Assignee:: [[Karsten, Gregory]], [[Dubazane, Sipho]]
---
```

Or create separate tasks:

```markdown
- [ ] Review procedures - Greg #task #priority/high
- [ ] Implement changes - Sipho #task #priority/high
```

## Integration with Tasks

When creating tasks with assignments:

```markdown
- [ ] Complete BEV fire safety review #task #priority/critical 📅 2025-10-20
  - Assignee: [[Karsten, Gregory]]
  - Project: [[BEV Fire Safety Program]]
```

## Integration with Triage

During `/triage`, assignment detection:

1. **Scan content** for assignment phrases
2. **Extract assignee names**
3. **Check for existing person notes**
4. **Create missing person notes** with template
5. **Add assignee to front-matter**
6. **Create wiki-links** in content

## Person Note Maintenance

**Keep person notes updated** with:
- Current role and team
- Contact information
- Active projects
- Recent interactions
- Key responsibilities

**Link person notes** to:
- Projects they're involved in
- Tasks assigned to them
- Meetings they attend
- Decisions they make

## Best Practices

1. **Always use full names** in person notes (Lastname, Firstname)
2. **Use nicknames in content** for readability (Greg, SK, Simon)
3. **Map nicknames to full names** for consistency
4. **Create person notes proactively** when new people appear
5. **Link liberally** to person notes from tasks and projects
6. **Keep contact info current** in person notes
7. **Document relationships** (reports to, manages, works with)
