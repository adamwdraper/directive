# Impact Analysis — Branch Creation Requirement and Implementation Summary

## Modules/packages likely touched

### Documentation Files
- `directive/reference/agent_operating_procedure.md` — Add branch creation step and implementation summary requirement
- `directive/reference/templates/implementation_template.md` — Already created, needs to be deployed to package data

### Package Data (src/directive/data/)
- `src/directive/data/directive/reference/agent_operating_procedure.md` — Mirror of AOP, needs same updates
- `src/directive/data/directive/reference/templates/implementation_template.md` — New template needs to be added here for packaging

### Optional: MCP Server Enhancement
- `src/directive/server.py` — Could add `directive/templates.implementation` tool (optional, low priority)
- `src/directive/bundles.py` — Could add implementation template bundle function (optional)

### Tests
- `tests/test_bundles.py` — May need updates if we add implementation template bundle
- `tests/test_server.py` — May need updates if we add new MCP tool
- New test file or additions to verify AOP changes are present

## Contracts to update (APIs, events, schemas, migrations)

### MCP Tools (Optional Enhancement)
If we decide to add an MCP tool for implementation template:
- **New tool**: `directive/templates.implementation`
  - Input: None (empty object)
  - Output: JSON bundle with AOP, context, and implementation template
  - Description: "Return Agent Operating Procedure, Agent Context, and the Implementation template, plus a concise Primer for tracking implementation."

### File System Contracts
- **New file location**: `directive/reference/templates/implementation_template.md` (already created)
- **Packaged location**: `src/directive/data/directive/reference/templates/implementation_template.md` (needs creation)

### AOP Document Structure
- **New deliverable**: Implementation summary added to "Deliverables" section
- **New step content**: Step 0 (branch creation) or integrated into existing Step 4 (TDD Execution)
- **Updated references**: Template list should include implementation_template.md

## Risks

### Security
- **Low Risk**: This is purely documentation changes, no security implications
- No new external inputs or data handling

### Performance/Availability
- **Low Risk**: Documentation changes have no runtime performance impact
- Optional MCP tool would be identical in performance to existing template tools
- Template file size is ~6KB, negligible impact on bundle size

### Data integrity
- **Low Risk**: No data storage or persistence changes
- File system operations are read-only (template serving)

### Adoption & Usage Risks
- **Medium Risk**: Agents may not follow the new branch creation requirement without enforcement
  - Mitigation: Clear, prominent placement in AOP with bold text
  - Future enhancement: Could add CLI command to verify on correct branch
- **Low Risk**: Implementation summary may be forgotten or not updated during development
  - Mitigation: Make it part of Step 4 (when coding begins) with clear reminder
  - Future enhancement: Could add CI check to verify implementation_summary.md exists in spec folder

### Documentation Consistency
- **Medium Risk**: Two copies of AOP exist (directive/ and src/directive/data/directive/)
  - Mitigation: Ensure both are updated identically
  - Consider: Add test or CI check to verify they're in sync
  
### Backward Compatibility
- **Low Risk**: Existing specs don't have implementation_summary.md files
  - Mitigation: This is forward-looking, applies to new specs only
  - No need to retroactively add implementation summaries to completed work

## Observability needs

### Logs
- No new logging required
- CLI operations already log file operations

### Metrics
- Not applicable for documentation changes
- Could track (in future): Number of specs with/without implementation_summary.md

### Alerts
- Not applicable

### Testing Observability
- Existing test coverage should catch missing template files
- Consider: Add test to verify implementation_template.md exists in both locations
- Consider: Add test to parse AOP and verify branch creation and implementation summary steps are present

