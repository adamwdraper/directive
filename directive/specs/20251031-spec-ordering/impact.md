# Impact Analysis — Spec Ordering System

## Modules/packages likely touched
- `/directive/reference/templates/spec_template.md` - Add metadata fields (Spec ID, Created)
- `/directive/reference/templates/impact_template.md` - Add metadata fields for consistency
- `/directive/reference/templates/tdr_template.md` - Add metadata fields for consistency
- `/directive/reference/agent_operating_procedure.md` - Document the YYYYMMDD naming convention
- `/directive/reference/agent_context.md` - May need updates to reference new convention

## Contracts to update (APIs, events, schemas, migrations)
- **Spec template contract**: New required metadata fields in all spec documents
  - `**Spec ID**: YYYYMMDD`
  - `**Created**: YYYY-MM-DD`
- **Directory naming contract**: All new specs must use `YYYYMMDD-feature-name/` format
- **Branch naming contract**: Should match spec directory `feature/YYYYMMDD-feature-name`
- **Backward compatibility**: Existing unprefixed specs remain valid (no breaking changes)

## Risks
- **Security**: None - purely organizational/naming changes
- **Performance/Availability**: None - filesystem naming has no performance impact
- **Data integrity**: 
  - Low risk: Existing unprefixed specs will sort alphabetically before dated specs (acceptable behavior)
  - Edge case: Multiple specs created same day need distinct feature names (already handled by descriptive naming)
  - Risk: Manual spec creation might not follow YYYYMMDD format
  - Mitigation: Clear documentation in agent_operating_procedure.md

## Observability needs
- **Logs**: None - no runtime behavior changes
- **Metrics**: None - static file/directory changes
- **Alerts**: None - no operational concerns

