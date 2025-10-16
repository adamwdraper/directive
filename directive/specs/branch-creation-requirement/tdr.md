# Technical Design Review (TDR) — Branch Creation Requirement and Implementation Summary

**Author**: AI Agent  
**Date**: 2025-10-14  
**Links**: 
- Spec: `/directive/specs/branch-creation-requirement/spec.md`
- Impact: `/directive/specs/branch-creation-requirement/impact.md`

---

## 1. Summary

We are updating the Agent Operating Procedure (AOP) to enforce two critical workflow improvements:
1. **Branch Creation Requirement**: Explicitly require agents to create a feature branch (format: `feature/<spec-name>`) before beginning any work on a spec, ensuring isolation from main branch
2. **Implementation Summary**: Introduce a new deliverable document (`implementation.md`) that tracks actual implementation details, created when coding begins and updated throughout development until PR merge

This ensures proper Git workflow hygiene and provides a clear bridge between design intent (TDR) and actual implementation, making PR reviews more effective.

## 2. Decision Drivers & Non‑Goals

### Drivers
- **Risk Mitigation**: Prevent accidental commits directly to main branch
- **Code Review Quality**: Provide reviewers with clear documentation of what was actually built vs. designed
- **Process Consistency**: Standardize the development workflow across all specs
- **Traceability**: Maintain a living record of implementation decisions, file changes, and deviations from TDR

### Non‑Goals
- Automated enforcement mechanisms (future enhancement)
- Retroactive application to existing/completed specs
- Changes to Git repository settings or branch protection rules
- Implementation of new MCP tools (optional, not required for this spec)

## 3. Current State — Codebase Map (concise)

### Key Modules
- **Documentation**: 
  - `directive/reference/agent_operating_procedure.md` — The AOP workflow document (working copy)
  - `directive/reference/templates/` — Contains spec, impact, TDR templates
  - `src/directive/data/directive/reference/` — Packaged copies of documentation

- **Core Services**:
  - `src/directive/bundles.py` — Builds template bundles (AOP + context + template)
  - `src/directive/server.py` — MCP server exposing templates and files
  - `src/directive/cli.py` — CLI for init, update, bundle, mcp serve commands

- **Testing**:
  - `tests/test_bundles.py` — Tests template bundle construction
  - `tests/test_server.py` — Tests MCP server tool calls
  - `tests/test_cli.py` — Tests CLI commands

### Data Models
- Template Bundle structure:
  ```json
  {
    "agentOperatingProcedure": {"path": "...", "content": "..."},
    "agentContext": {"path": "...", "content": "..."},
    "template": {"path": "...", "content": "..."},
    "resources": [...]
  }
  ```

### External Interfaces
- **MCP Protocol**: Tools exposed via MCP server
  - `directive/templates.spec` — Spec template bundle
  - `directive/templates.impact` — Impact template bundle
  - `directive/templates.tdr` — TDR template bundle
  - `directive/files.list` — List all directive files
  - `directive/files.get` — Read a specific directive file

### Configuration
- Templates located in two places (dual source of truth):
  - Development: `directive/reference/templates/`
  - Package data: `src/directive/data/directive/reference/templates/`
- Package version: 0.0.9 (from pyproject.toml)

### Testing Setup
- pytest-based test suite
- Tests run via `pytest` command
- No CI/CD configuration visible in codebase (may exist in GitHub Actions)

## 4. Proposed Design (high level, implementation‑agnostic)

### Overview
Update the AOP document to add two new requirements, and introduce a new template. The implementation is purely documentation-based with no code changes required (though optional MCP tool enhancement is possible).

### Changes to AOP Document

#### 1. Add Branch Creation Step
**Location**: Before Step 1 (Repo Recon) or as Step 0  
**Content**:
```markdown
## Step 0 — Branch Creation (Git Workflow)

Before beginning work on a spec, create a new feature branch:

1. Ensure you're starting from an up-to-date main branch:
   ```
   git checkout main
   git pull origin main
   ```

2. Create a new feature branch using the naming convention:
   ```
   git checkout -b feature/<spec-name>
   ```
   where `<spec-name>` matches the spec folder name in `/directive/specs/<spec-name>/`

3. Verify you're on the correct branch before proceeding:
   ```
   git branch --show-current
   ```

**Gate**: All subsequent work (impact analysis, TDR, implementation) must occur on this feature branch, never on main.
```

#### 2. Update Deliverables Section
**Location**: After "Deliverables (before any code)" section  
**Addition**:
```markdown
## Deliverables (during implementation)
4. **Implementation Summary** — save as `/directive/specs/<feature>/implementation.md` — created when coding begins, updated throughout development
```

#### 3. Update Template List
**Location**: Note at top of AOP referencing templates  
**Addition**:
```markdown
- Implementation: `/directive/reference/templates/implementation_template.md`
```

#### 4. Update Step 4 (TDD Execution Rhythm)
**Location**: Current Step 4  
**Additions**:
- Add initial step: "**Before first test**: Create `/directive/specs/<feature>/implementation.md` using the implementation template"
- Add ongoing requirement: "**After each significant change**: Update implementation summary with files modified, decisions made, tests added"
- Add completion requirement: "**Before PR submission**: Ensure implementation summary is complete and accurate"

### Implementation Template Structure
Already created at `directive/reference/templates/implementation_template.md` with sections:
- Overview
- Files Changed (new, modified, deleted)
- Key Implementation Decisions (with TDR deviation tracking)
- Dependencies, Database/Data Changes, API/Contract Changes
- Testing (coverage, spec-to-test mapping)
- Configuration Changes, Observability, Security
- Performance Impact, Breaking Changes, Rollout Notes
- Known Issues/Technical Debt, Deviations from TDR
- Commit History Summary, Review Notes

### File Deployment
1. Template already exists in: `directive/reference/templates/implementation_template.md`
2. Must be copied to package data: `src/directive/data/directive/reference/templates/implementation_template.md`
3. AOP updates must be mirrored in both locations:
   - `directive/reference/agent_operating_procedure.md`
   - `src/directive/data/directive/reference/agent_operating_procedure.md`

### Optional Enhancement: New MCP Tool
**Not required for this spec, but could be added in future**:
- Tool name: `directive/templates.implementation`
- Behavior: Identical to other template tools, returns bundle with implementation template
- Would require updates to:
  - `src/directive/server.py` — Add tool descriptor and handler
  - `tests/test_server.py` — Add test coverage

## 5. Alternatives Considered

### Alternative 1: Automated Branch Enforcement
**Approach**: Add CLI command that checks current branch and fails if on main  
**Pros**: Would prevent mistakes automatically  
**Cons**: Adds complexity, requires integration into workflow, may be annoying for advanced users  
**Decision**: Rejected for now, can be added as future enhancement if adoption issues arise

### Alternative 2: Single Template Location
**Approach**: Only maintain templates in package data, not in directive/ folder  
**Pros**: Single source of truth  
**Cons**: Breaks current architecture where directive/ is the working copy and src/directive/data/ is the packaged copy  
**Decision**: Rejected, maintain current dual-location pattern for consistency

### Alternative 3: Implementation Summary as Part of TDR
**Approach**: Instead of separate file, add "Implementation Notes" section to TDR  
**Pros**: Fewer files, design and implementation in one place  
**Cons**: TDR should remain implementation-agnostic design document; mixing concerns makes TDR harder to review pre-implementation  
**Decision**: Rejected, separate concerns between design (TDR) and actual implementation (implementation.md)

### Alternative 4: Git Hook for Branch Enforcement
**Approach**: Pre-commit hook that prevents commits to main  
**Pros**: Strong enforcement at Git level  
**Cons**: Requires repository setup, outside scope of Directive package, may conflict with existing hooks  
**Decision**: Rejected, this is repository configuration not Directive's responsibility

## 6. Data Model & Contract Changes

### No Data Model Changes
This is purely documentation; no database or data storage changes.

### File System Contracts
**New File**: `/directive/specs/<feature>/implementation.md` — Created per-spec during Step 4  
**New Template**: `directive/reference/templates/implementation_template.md` — Already created  
**Updated File**: `directive/reference/agent_operating_procedure.md` — Modified with new steps

### Package Data Contracts
**New File**: `src/directive/data/directive/reference/templates/implementation_template.md`  
**Updated File**: `src/directive/data/directive/reference/agent_operating_procedure.md`

### No API Changes
Existing MCP tools remain unchanged. Optional addition of `directive/templates.implementation` tool is out of scope.

### Backward Compatibility
- ✅ Existing specs without implementation.md remain valid
- ✅ Existing tools continue to work unchanged
- ✅ Existing template bundles continue to work
- ✅ No breaking changes to any interfaces

## 7. Security, Privacy, Compliance

### No Security Impact
- No new authentication or authorization mechanisms
- No secrets or credentials involved
- No external service integrations
- No user data handling

### Documentation Review
- AOP and template contain no sensitive information
- Implementation template includes sections for security considerations (good practice)

## 8. Observability & Operations

### Logs
No logging changes needed. Existing CLI and MCP server logging covers file operations.

### Metrics
No metrics collection. Future enhancement could track:
- Number of specs with implementation.md
- Completeness score for implementation summaries

### Dashboards/Alerts
Not applicable for documentation changes.

### Operations Impact
- **Deployment**: Copy files during package build (hatchling already handles src/directive/data/)
- **Rollback**: Simple file reversion if needed
- **Monitoring**: No special monitoring required

## 9. Rollout & Migration

### Rollout Strategy
1. **Phase 1**: Update documentation files (this PR)
   - Update AOP in both locations
   - Add implementation template to both locations
   - Update package version (0.0.9 → 0.0.10 or 0.1.0)
   
2. **Phase 2**: Release to PyPI
   - Package and publish new version
   - Users get updates via `uv add directive@latest` or `directive update`

3. **Phase 3**: Adoption
   - New specs automatically see updated AOP via MCP server
   - No breaking changes, immediate adoption possible
   - Monitor adoption through spec reviews

### Feature Flags
Not applicable — documentation changes are always active.

### Data Migration
Not applicable — no data to migrate.

### Revert Plan
If issues arise:
1. Revert AOP changes in both locations
2. Remove implementation template from both locations
3. Publish patch version
4. Blast radius: Only affects agents starting new specs; existing work unaffected

## 10. Test Strategy & Spec Coverage (TDD)

### TDD Commitment
We commit to TDD principles: write failing tests first, confirm failure, implement, refactor.

### Spec → Test Mapping

| Spec Acceptance Criterion | Test ID | Test Type |
|---------------------------|---------|-----------|
| Branch Creation: AOP contains explicit branch creation instruction | `test_aop_contains_branch_creation_step` | Unit |
| Branch Creation: Branch naming convention specified in AOP | `test_aop_specifies_branch_naming` | Unit |
| Branch Creation: Branch creation positioned before Step 4 | `test_aop_branch_creation_before_implementation` | Unit |
| Implementation Summary: Template exists at correct path | `test_implementation_template_exists` | Unit |
| Implementation Summary: Template exists in package data | `test_implementation_template_in_package_data` | Unit |
| Implementation Summary: AOP requires creation in Step 4 | `test_aop_requires_implementation_summary` | Unit |
| Implementation Summary: AOP specifies updates during work | `test_aop_specifies_implementation_updates` | Unit |
| Implementation Summary: Saved at correct location per spec | `test_aop_specifies_implementation_location` | Unit |
| Implementation Summary: Reviewers can find clear documentation | `test_implementation_template_has_review_section` | Unit |

### Test Tiers

#### Unit Tests
- **test_aop_content.py** (new file):
  - Verify AOP contains branch creation step
  - Verify AOP contains implementation summary requirement
  - Verify AOP references implementation template
  - Verify branch naming convention is documented
  
- **test_bundles.py** (existing, additions):
  - Verify implementation_template.md is listed in directive files
  - Optional: Test building implementation template bundle if we add it

- **test_server.py** (existing, optional additions):
  - Optional: Test new `directive/templates.implementation` tool if we add it

#### Integration Tests
- **test_template_sync.py** (new file):
  - Verify AOP content matches between directive/ and src/directive/data/directive/
  - Verify implementation template matches between locations
  - Fail build if templates are out of sync

### Negative & Edge Cases
- **Missing template**: `build_template_bundle("implementation_template.md")` should work or raise clear error
- **Malformed AOP**: Parser should handle AOP with new sections gracefully
- **Empty spec folder**: Implementation.md creation is responsibility of agent, not enforced by code

### Performance Tests
Not applicable — documentation operations are trivial performance-wise.

### CI Requirements
- All tests must pass before merge
- Consider: Add linter to verify markdown formatting
- Consider: Add spell checker for documentation

## 11. Risks & Open Questions

### Risks

1. **Adoption Risk** (Medium)
   - Risk: Agents may not follow new requirements without enforcement
   - Mitigation: Prominent placement in AOP with bold text; clear gate language
   - Future mitigation: Add CLI verification command

2. **Documentation Drift** (Medium)
   - Risk: Two copies of AOP could get out of sync
   - Mitigation: Add test to verify content matches
   - Future mitigation: Consider single source of truth with copy script

3. **Incomplete Implementation Summaries** (Low)
   - Risk: Agents may create but not update implementation.md
   - Mitigation: Explicit reminders in Step 4; make it part of review checklist
   - Future mitigation: Could add completeness scoring or CI check

### Open Questions

1. **Q**: Should we add a new MCP tool `directive/templates.implementation`?
   - **Proposed answer**: No, not required. Agents can use `directive/files.get` to fetch it, or we add it in a future enhancement.
   - **Path to resolve**: Implement core functionality first, gather feedback, add tool if needed.

2. **Q**: Should we increment to 0.0.10 or 0.1.0?
   - **Proposed answer**: 0.1.0 — this is a minor feature addition (new template, new workflow requirement)
   - **Path to resolve**: Update pyproject.toml version to 0.1.0

3. **Q**: Should we enforce template synchronization at build time?
   - **Proposed answer**: Yes, add test to verify templates match between locations
   - **Path to resolve**: Add integration test in test_template_sync.py

## 12. Milestones / Plan (post‑approval)

### Task Breakdown

**Task 1: Update AOP Document**
- DoD: 
  - [ ] Branch creation step added as Step 0
  - [ ] Implementation summary added to deliverables
  - [ ] Step 4 updated with implementation.md creation/update requirements
  - [ ] Template list includes implementation_template.md
  - [ ] Changes made to both directive/ and src/directive/data/directive/ locations
  - [ ] Tests written and passing

**Task 2: Deploy Implementation Template**
- DoD:
  - [ ] implementation_template.md copied to src/directive/data/directive/reference/templates/
  - [ ] Template is identical in both locations
  - [ ] Test verifies template exists in both locations
  - [ ] Tests passing

**Task 3: Add Template Synchronization Tests**
- DoD:
  - [ ] Test verifies AOP content matches between locations
  - [ ] Test verifies implementation template matches between locations
  - [ ] Test fails if content drifts
  - [ ] Tests passing

**Task 4: Add AOP Content Validation Tests**
- DoD:
  - [ ] Tests verify branch creation step present
  - [ ] Tests verify implementation summary requirements present
  - [ ] Tests verify all template references correct
  - [ ] All spec acceptance criteria mapped to passing tests
  - [ ] Tests passing

**Task 5: Update Package Version**
- DoD:
  - [ ] pyproject.toml version updated to 0.1.0
  - [ ] README updated if necessary (version references, workflow description)
  - [ ] Tests passing

**Task 6: Documentation Review**
- DoD:
  - [ ] Spec reviewed and accepted
  - [ ] Impact analysis reviewed and accepted
  - [ ] TDR reviewed and approved (this document)
  - [ ] All acceptance criteria met
  - [ ] Ready for implementation

### Dependencies
- No external dependencies
- No blocking issues
- Can begin implementation immediately after TDR approval

---

## Review Checklist (pre‑implementation)
- [x] Codebase Map is accurate and concise
- [x] Impact Analysis lists all contracts & data changes
- [x] TDR includes Test Strategy with TDD plan and Spec→Test mapping
- [x] Open questions are explicit with proposed next steps

**Approval Gate**: Do not start coding until this TDR is reviewed and approved.

