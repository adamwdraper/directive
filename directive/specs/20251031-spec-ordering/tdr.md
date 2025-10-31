# Technical Design Review (TDR) — Spec Ordering System

**Author**: AI Agent  
**Date**: 2025-10-31  
**Links**: 
- Spec: `/directive/specs/20251031-spec-ordering/spec.md`
- Impact: `/directive/specs/20251031-spec-ordering/impact.md`

---

## 1. Summary

We are implementing a date-based ordering system for spec directories to provide chronological organization of project specifications. Currently, spec directories are sorted alphabetically by name, making it difficult to understand project evolution over time. 

This change introduces a `YYYYMMDD-feature-name/` naming convention for spec directories and adds metadata fields (Spec ID, Created date) to all spec document templates. The agent will automatically use the current date when creating new specs, eliminating the need for sequential numbering or directory scanning.

## 2. Decision Drivers & Non‑Goals

**Drivers:**
- Need for chronological ordering of specs without manual tracking
- Simplicity for AI agents (deterministic naming based on date)
- Human-readable directory names
- Zero dependencies or runtime code changes

**Non‑Goals:**
- Migration or renaming of existing unprefixed specs
- Status tracking within specs (keeping metadata minimal)
- CI/CD enforcement of naming convention
- Complex dependency tracking between specs

## 3. Current State — Codebase Map (concise)

**Key modules/files:**
- `/directive/reference/templates/spec_template.md` - Template for new specs
- `/directive/reference/templates/impact_template.md` - Template for impact analysis
- `/directive/reference/templates/tdr_template.md` - Template for TDRs
- `/directive/reference/agent_operating_procedure.md` - Agent workflow documentation
- `/directive/reference/agent_context.md` - Agent context and best practices

**Existing structure:**
- Templates have no metadata fields
- No ordering convention documented
- Existing specs will remain unprefixed

**External contracts:**
- None - this is purely internal documentation structure

**Observability:**
- None - static documentation only

## 4. Proposed Design (high level, implementation‑agnostic)

**Approach:**

1. **Template Updates** - Add metadata header to all three templates:
   ```markdown
   **Spec ID**: YYYYMMDD
   **Created**: YYYY-MM-DD
   ```

2. **Directory Naming Convention** - `YYYYMMDD-feature-name/`
   - Agent uses current date from context
   - Format: `20251031-spec-ordering/`
   - Multiple specs same day: distinct feature names differentiate them

3. **Branch Naming Convention** - `feature/YYYYMMDD-feature-name`
   - Matches directory name for consistency
   - Example: `feature/20251031-spec-ordering`

4. **Documentation Updates**:
   - Update `agent_operating_procedure.md` with YYYYMMDD convention
   - Document backward compatibility with unprefixed specs
   - Provide examples of correct usage

**Interfaces:**
- Template contract: All new specs include Spec ID and Created metadata
- Directory contract: All new spec directories use YYYYMMDD prefix
- Branch contract: Feature branches match spec directory names

**Error Handling:**
- Backward compatibility: Unprefixed specs continue to work
- Multiple same-day specs: Feature names must be distinct
- Manual creation: Documentation provides clear guidance

**Performance:**
- No runtime impact - filesystem naming only
- Agent doesn't need to scan directories to determine next number

## 5. Alternatives Considered

**Option A: Sequential 4-digit numbering (0001-9999)**
- Pros: Compact, clear ordering
- Cons: Requires scanning directories to find next number; potential conflicts
- Why not chosen: Date-based is deterministic and self-documenting

**Option B: Full ISO timestamp (YYYY-MM-DD-HHMM)**
- Pros: Truly unique, includes time
- Cons: Overly verbose, unnecessary precision for specs
- Why not chosen: Date-only is sufficient; same-day specs are rare

**Option C: Metadata-only (no directory prefix)**
- Pros: Clean directory names
- Cons: Not visible in file browser; requires reading files to determine order
- Why not chosen: Want ordering visible at filesystem level

**Option D: Central manifest/index file**
- Pros: Single source of truth
- Cons: Manual maintenance, merge conflicts, can get out of sync
- Why not chosen: Date prefix is self-maintaining

**Chosen Option: YYYYMMDD prefix**
- Best balance of readability, determinism, and simplicity
- Agent always knows current date from context
- Self-documenting with visible creation date
- No scanning or coordination required

## 6. Data Model & Contract Changes

**Template Contracts:**

New metadata fields added to all three templates (spec, impact, TDR):

```markdown
**Spec ID**: YYYYMMDD
**Created**: YYYY-MM-DD
```

**Directory Naming Contract:**
- Format: `YYYYMMDD-feature-name/`
- Example: `20251031-spec-ordering/`
- Constraint: YYYYMMDD must match actual creation date

**Branch Naming Contract:**
- Format: `feature/YYYYMMDD-feature-name`
- Must match spec directory name

**Backward Compatibility:**
- Existing unprefixed specs remain as-is
- Will sort alphabetically before dated specs
- No breaking changes
- No migration planned

**Deprecation Plan:**
- Not applicable - old specs remain unchanged

## 7. Security, Privacy, Compliance

**AuthN/AuthZ:**
- Not applicable - documentation structure only

**Secrets & PII:**
- Not applicable - no sensitive data

**Threat Model:**
- No security implications
- Purely organizational/naming changes

## 8. Observability & Operations

**Logs/Metrics/Traces:**
- None needed - static files only

**Dashboards/Alerts:**
- None needed - no runtime behavior

**Runbooks/SLOs:**
- Not applicable - documentation structure

## 9. Rollout & Migration

**Feature Flags:**
- None needed - immediate adoption for new specs

**Migration Strategy:**
- New specs: Use YYYYMMDD format immediately
- Existing specs: Remain unprefixed (no changes)

**Revert Plan:**
- Low risk - changes are primarily documentation
- Revert: Update templates back to original format
- Blast radius: None - no runtime systems affected

**Rollout Approach:**
1. Update templates (this PR)
2. Update agent documentation (this PR)
3. Create first dated spec (this spec itself - `20251031-spec-ordering/`)
4. All future specs use new convention

## 10. Test Strategy & Spec Coverage (TDD)

**TDD Commitment:**
Since this feature involves template and documentation updates rather than code, testing approach is different:

**Validation Strategy:**
1. Template validation: Verify templates render correctly with metadata
2. Naming validation: Confirm directory naming follows YYYYMMDD format
3. Documentation review: Ensure agent_operating_procedure.md is clear
4. Manual verification: Create test spec using new convention

**Spec → Test Mapping:**

| Acceptance Criterion | Test/Validation |
|---------------------|-----------------|
| Agent creates directory with YYYYMMDD prefix | Manual: Create test spec, verify directory name format |
| Spec includes all metadata fields | Manual: Verify spec.md has Spec ID and Created |
| Multiple specs sort chronologically | Manual: List directory, verify sort order |
| Existing unprefixed specs continue to work | Manual: Verify existing specs are accessible |
| Same-day specs are distinguishable | Manual: Create two specs same date, verify clarity |

**Test Tiers:**
- **Documentation Tests**: Verify templates have correct structure
- **Manual Integration**: Create actual spec using new process
- **Backward Compatibility**: Reference existing unprefixed specs

**Negative & Edge Cases:**
- Multiple specs created same date (handled by distinct feature names)
- Manual creation not following format (mitigated by documentation)
- Existing unprefixed specs (backward compatible)

**Performance Tests:**
- Not applicable - static files

**CI:**
- Could add future validation: regex check on spec directory names
- Not critical for initial implementation

## 11. Risks & Open Questions

**Known Risks:**

1. **Risk**: Manual spec creation might not follow YYYYMMDD format
   - **Mitigation**: Clear documentation in agent_operating_procedure.md
   - **Likelihood**: Low - agent handles most spec creation
   
2. **Risk**: Existing unprefixed specs sort before dated specs
   - **Mitigation**: Document this behavior; optional migration
   - **Likelihood**: Expected behavior, not a bug

3. **Risk**: Date might not reflect actual work start date if spec created late
   - **Mitigation**: Document that date reflects spec creation, not work start
   - **Likelihood**: Acceptable - creation date is still meaningful

**Open Questions:**
- None - design is straightforward

## 12. Milestones / Plan (post‑approval)

**Task 1: Update Templates**
- [ ] Update `spec_template.md` with metadata fields
- [ ] Update `impact_template.md` with metadata fields
- [ ] Update `tdr_template.md` with metadata fields
- DoD: All templates include Spec ID and Created fields

**Task 2: Update Agent Documentation**
- [ ] Update `agent_operating_procedure.md` with YYYYMMDD convention
- [ ] Add examples of correct directory/branch naming
- [ ] Document backward compatibility with unprefixed specs
- DoD: Documentation clearly explains new convention

**Task 3: Verify This Spec**
- [ ] Ensure this spec (20251031-spec-ordering) follows new format
- [ ] Verify metadata is correctly filled
- DoD: This spec serves as reference example

**Task 4: Review Agent Context (Optional)**
- [ ] Review `agent_context.md` to see if any references needed
- DoD: Agent context updated if relevant

**Dependencies:**
- None - self-contained changes

**Owners:**
- Agent + Engineer (collaborative implementation)

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.

