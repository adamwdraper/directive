# Implementation Summary — <Feature Name>

**Author**: <agent or engineer>  
**Start Date**: <YYYY-MM-DD>  
**Last Updated**: <YYYY-MM-DD>  
**Status**: <In Progress | Complete>  
**Branch**: `feature/<spec-name>`  
**Links**: Spec (`/directive/specs/<feature>/spec.md`), TDR (`/directive/specs/<feature>/tdr.md`)

---

## Overview
Brief summary of what was actually implemented in this PR. Keep this updated as the implementation evolves.

## Files Changed

### New Files
- `path/to/new/file.py` — <brief description of purpose>
- `path/to/test/file_test.py` — <test coverage for new file>

### Modified Files
- `path/to/modified/file.py` — <what changed and why>
- `path/to/another/modified.py` — <what changed and why>

### Deleted Files
- `path/to/deleted/file.py` — <reason for deletion>

## Key Implementation Decisions

### Decision 1: <Title>
**Context**: <Why this decision needed to be made>  
**Choice**: <What was decided>  
**Rationale**: <Why this approach was chosen>  
**Differs from TDR?**: <Yes/No — if yes, explain why>

### Decision 2: <Title>
**Context**: <Why this decision needed to be made>  
**Choice**: <What was decided>  
**Rationale**: <Why this approach was chosen>  
**Differs from TDR?**: <Yes/No — if yes, explain why>

## Dependencies

### Added
- `package-name==version` — <why it was added>

### Updated
- `package-name` from `old-version` to `new-version` — <why it was updated>

### Removed
- `package-name` — <why it was removed>

## Database/Data Changes

### Migrations
- `migration_file_name.py` — <what it does>

### Schema Changes
- Table/Collection: `table_name`
  - Added columns/fields: <list>
  - Modified columns/fields: <list>
  - Indexes added: <list>

### Data Backfills
- <Description of any data migration or backfill required>

## API/Contract Changes

### New Endpoints/Events
- `POST /api/v1/resource` — <description>
- Event: `resource.created` — <description>

### Modified Endpoints/Events
- `GET /api/v1/resource` — <what changed>

### Deprecated Endpoints/Events
- `GET /api/v1/old-resource` — <deprecation timeline>

## Testing

### Test Coverage
- **Unit tests**: <number> tests added, covering <modules/functions>
- **Integration tests**: <number> tests added, covering <workflows>
- **E2E tests**: <number> tests added, covering <user scenarios>

### Test Files
- `tests/test_feature.py` — <what it tests>
- `tests/integration/test_feature_integration.py` — <what it tests>

### Spec → Test Mapping
Map each acceptance criterion from the spec to test IDs:
- Spec AC 1: "Given X when Y then Z" → `test_feature::test_scenario_1`
- Spec AC 2: "Given X when Y then Z" → `test_feature::test_scenario_2`

### Manual Testing Notes
- <Any manual testing performed>
- <Steps to reproduce/verify>
- <Screenshots or output if relevant>

## Configuration Changes

### Environment Variables
- `NEW_CONFIG_VAR` — <description and default value>

### Feature Flags
- `feature.new_capability` — <description, default state, rollout plan>

### Config Files
- `config/settings.yaml` — <what changed>

## Observability

### Logging
- Added logs: <where and what is logged>
- Log levels used: <DEBUG/INFO/WARNING/ERROR>

### Metrics
- New metrics: `metric.name` — <description>
- Modified metrics: `metric.name` — <what changed>

### Dashboards
- Created dashboard: `<dashboard-name>` — <link or description>
- Updated dashboard: `<dashboard-name>` — <what was added>

### Alerts
- New alerts: `<alert-name>` — <conditions and severity>

## Security Considerations

### Changes Impacting Security
- <Any authentication/authorization changes>
- <Any new secrets or credentials>
- <Any new external integrations>

### Mitigations Implemented
- <Security measures taken>

## Performance Impact

### Expected Performance Characteristics
- <Latency expectations>
- <Throughput expectations>
- <Resource utilization>

### Performance Testing Results
- <Benchmark results if available>
- <Load testing results if performed>

## Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes (list below):
  - <Description of breaking change>
  - <Migration path for users>

## Rollout Notes

### Deployment Steps
1. <Step-by-step deployment instructions>
2. <Any required manual steps>

### Rollback Plan
- <How to rollback if issues arise>
- <What data/state needs to be considered>

### Feature Flag Strategy
- <How feature will be rolled out>
- <Percentage rollout plan if applicable>

## Known Issues / Technical Debt
- <Any known limitations or technical debt introduced>
- <Future improvements planned>
- <Workarounds or temporary solutions>

## Deviations from TDR
If the implementation differs significantly from the TDR, document:
- **What changed**: <description>
- **Why it changed**: <rationale>
- **Impact**: <what this means for the system>
- **TDR updated?**: <Yes/No — if yes, reference TDR section>

## Commit History Summary
Brief summary of major commits in chronological order:
- `<commit-hash>` — `test: add failing test for <feature>`
- `<commit-hash>` — `feat: implement <feature>`
- `<commit-hash>` — `refactor: improve <aspect>`

## Review Notes
Notes for reviewers on what to focus on:
- <Specific areas needing careful review>
- <Complex logic or algorithms>
- <Security-sensitive code>

---

**Update Instructions**: Update this document as you code. Before submitting PR, ensure all sections accurately reflect the final implementation.

