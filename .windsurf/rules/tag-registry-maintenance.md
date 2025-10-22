# Rule: Tag Registry Maintenance

## Master Tags Registry

**Location**: `reference/tags.md`

This is the canonical list of all tags with definitions, usage examples, and relationships.

## Tag Application Rules

1. Use **exactly one** primary tag: `#meeting` | `#task` | `#idea` | `#decision`
2. Add `#year/2025`
3. Add `#site/<name>` when relevant (e.g., `#site/Nchwaning2`, `#site/Nchwaning3`, `#site/Gloria`, `#site/S&W`)
4. Infer extra tags from content (project names, systems)
5. **Always** update the tags registry when creating new tags

## Registry Structure

```markdown
# Tags Registry

## Primary Tags
- `#meeting` - Meeting notes, discussions, decisions
- `#task` - Action items, todos, assignments  
- `#idea` - Concepts, innovations, future considerations
- `#decision` - Formal decisions, approvals, commitments

## Site Tags  
- `#site/Nchwaning2` - Nchwaning 2 mine operations
- `#site/Nchwaning3` - Nchwaning 3 mine operations
- `#site/Gloria` - Gloria mine operations
- `#site/S&W` - Shafts & Winders operations

## Priority Tags
- `#priority/critical` 🔴 - Immediate action required
- `#priority/high` 🟡 - Important, near-term
- `#priority/medium` 🟢 - Standard priority
- `#priority/low` ⚪ - Nice to have

## Project Tags
- `#BEV` - Battery Electric Vehicle project
- `#Pump_123` - Specific pump maintenance project
- [Auto-generated from project folders]

## System Tags
- `#recurring` - Repeating tasks/meetings
- `#personal` - Personal, non-work items
- `#year/2025` - Year-based organization
```

## Tag Creation Process

When creating a new tag:

1. **Check registry first** - Avoid duplicates
2. **Use consistent naming**:
   - Lowercase with underscores: `#fire_safety`
   - Site prefix: `#site/LocationName`
   - Priority prefix: `#priority/level`
   - Year prefix: `#year/YYYY`
3. **Update registry** - Add to appropriate category with definition
4. **Cross-reference** - Link related tags where relevant

## Tag Naming Conventions

**Good tag names**:
- `#BEV` - Short, clear acronym
- `#fire_safety` - Descriptive, underscored
- `#site/Nchwaning2` - Categorized with prefix
- `#priority/high` - Hierarchical structure

**Bad tag names**:
- `#BEV-Project` - Redundant suffix
- `#Fire Safety` - Spaces not allowed
- `#n2` - Too cryptic
- `#HighPriority` - CamelCase (use lowercase)

## Registry Maintenance

**When to update**:
- Creating new project folders → Add project tag
- First mention of new topic → Add topic tag
- New priority level → Add priority tag
- New location → Add site tag

**How to update**:
1. Open `reference/tags.md`
2. Find appropriate category
3. Add new tag with definition
4. Include usage example if helpful
5. Link related tags

## Tag Categories

**Primary** - Content type classification
**Site** - Location-based organization
**Priority** - Urgency and importance
**Project** - Project-based grouping
**System** - Workflow and process tags
**Status** - State tracking (#status/active, #status/complete, etc.)
**Year** - Temporal organization

## Integration with Workflows

**During `/triage`**:
- Apply primary tag based on content type
- Add site tag if location mentioned
- Add project tags from folder placement
- Check registry for existing tags
- Update registry if new tags created

**During task creation**:
- Always include `#task` and `#year/2025`
- Add priority tag: `#priority/critical|high|medium|low`
- Add project/context tags
- Update registry for new project tags

## Best Practices

1. **Be consistent** - Use existing tags when possible
2. **Be specific** - Create new tags when needed
3. **Be organized** - Keep registry updated
4. **Be descriptive** - Tag definitions should be clear
5. **Be hierarchical** - Use prefixes for categorization
