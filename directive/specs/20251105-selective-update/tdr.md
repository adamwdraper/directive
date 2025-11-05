# Technical Design Review (TDR) — Selective Update for Directive-Maintained Files

**Spec ID**: 20251105  
**Created**: 2025-11-05  
**Author**: AI Agent  
**Links**: 
- Spec: `/directive/specs/20251105-selective-update/spec.md`
- Impact: `/directive/specs/20251105-selective-update/impact.md`

---

## 1. Summary

We are enhancing the existing `directive update` command to actually update files when new Directive versions are released. Currently, `directive update` only copies new files that don't exist (using `overwrite=False`), making it essentially non-functional after initial `directive init`. 

The enhancement will selectively overwrite Directive-maintained files (templates, AOP, cursor rules) while preserving project-specific content (specs and agent_context.md). Users will see a clear preview of what will be overwritten and can cancel before any changes occur.

## 2. Decision Drivers & Non‑Goals

**Drivers:**
- User request: "how can we make it easy for anyone to update directive when we release new templates and agent operating procedure"
- Current `directive update` is non-functional (always "0 copied, N skipped")
- Users need to stay in sync with Directive improvements without manual file comparison
- Must protect project-specific content while updating framework files

**Non‑Goals:**
- Intelligent merging or diffing of changes (simple overwrite only)
- Backup/restore functionality 
- Updating MCP server config (.cursor/mcp.json, .cursor/servers/)
- Selective update of individual files (all maintained files updated together)
- Version-aware migrations or compatibility checks

## 3. Current State — Codebase Map (concise)

**Key modules:**
- `src/directive/cli.py`:
  - `cmd_update()` (line 216-230): Current implementation with `overwrite=False`
  - `cmd_init()` (line 192-213): Initializes directive/ and optionally .cursor/
  - `_copy_tree()` (line 60-78): Recursive copy with optional overwrite
  - `_ask_yes_no()` (line 22-47): TTY-aware confirmation prompt (already exists!)
  - `_package_data_root()` (line 50-57): Returns path to packaged defaults
- `src/directive/bundles.py`: Helpers for reading directive files (may not need changes)
- `src/directive/data/directive/`: Package data bundled with installation
  - `reference/agent_operating_procedure.md`
  - `reference/agent_context.md`
  - `reference/templates/*.md` (4 templates)
  - `cursor/rules/*.mdc`

**Existing utilities we can reuse:**
- `_copy_tree()`: Already has `overwrite` parameter
- `_ask_yes_no()`: Already handles TTY vs non-TTY
- `_package_data_root()`: Already returns source path

**Current behavior:**
```python
# Line 223 in cli.py
copied, skipped, notes = _copy_tree(defaults, target, overwrite=False)
```
After initial init, this always results in "copied 0, skipped N" because all files exist.

## 4. Proposed Design (high level, implementation‑agnostic)

### Core Approach

Define a **hardcoded list** of "maintained files" that Directive owns and should always overwrite on update. All other files are project-specific and should never be touched.

**Maintained files (relative to package data root):**
- `reference/agent_operating_procedure.md`
- `reference/templates/spec_template.md`
- `reference/templates/impact_template.md`
- `reference/templates/tdr_template.md`
- `reference/templates/implementation_summary_template.md`

**Cursor rules (separate location):**
- `.cursor/rules/directive-core-protocol.mdc`
- Any other `.cursor/rules/*.mdc` files from package

**Protected files (never overwrite):**
- `reference/agent_context.md` (project-specific)
- `specs/**` (entire directory - project history)
- Any user-created files not in package

### Update Flow

```
1. Check directive/ exists (exit if not)
2. Build list of files to update (maintained files only)
3. For each file, check if it exists and will be overwritten
4. Display preview:
   - Files that WILL be overwritten
   - Files that will NOT be modified
5. Prompt for confirmation (Y/n, default Yes)
6. If confirmed:
   - Copy maintained files from directive/reference/
   - Copy maintained cursor rules from cursor/rules/
   - Use overwrite=True for these specific files
7. Display summary of what was updated
```

### New Helper Function

```python
def _get_maintained_files() -> Dict[str, List[str]]:
    """Return dict of maintained file paths by category.
    
    Returns:
        {
            'directive': ['reference/agent_operating_procedure.md', ...],
            'cursor_rules': ['rules/directive-core-protocol.mdc', ...]
        }
    """
```

### Modified `cmd_update()` Signature

```python
def cmd_update(args: argparse.Namespace) -> int:
    """Update Directive-maintained files (templates, AOP, cursor rules).
    
    Shows preview, prompts for confirmation, then selectively overwrites
    only the files that Directive maintains. Project-specific content
    (agent_context.md, specs/) is never touched.
    """
```

### Interfaces & Data Contracts

**Input:** 
- Command: `directive update [--verbose]`
- Existing `--verbose` flag shows detailed file list

**Output (stdout):**
```
The following files will be updated (overwritten):
- directive/reference/agent_operating_procedure.md
- directive/reference/templates/spec_template.md
- directive/reference/templates/impact_template.md
- directive/reference/templates/tdr_template.md
- directive/reference/templates/implementation_summary_template.md
- .cursor/rules/directive-core-protocol.mdc

Files that will NOT be modified:
- directive/reference/agent_context.md (your project-specific context)
- directive/specs/ (your project history)

Proceed with update? (Y/n) 
```

**Output (after confirmation):**
```
Updated 6 files:
✓ directive/reference/agent_operating_procedure.md
✓ directive/reference/templates/spec_template.md
✓ directive/reference/templates/impact_template.md
✓ directive/reference/templates/tdr_template.md
✓ directive/reference/templates/implementation_summary_template.md
✓ .cursor/rules/directive-core-protocol.mdc
```

**Error cases:**
- No `directive/` directory: "No directive/ found. Run 'directive init' first."
- User declines: "Update cancelled." (exit 0)
- File operation fails: Specific error message (exit 1)

### Error Handling

- Graceful exit if directive/ doesn't exist
- Graceful exit if user declines confirmation
- Atomic-ish: If any file copy fails, report error but continue with others
- Show clear error messages for I/O failures

### Idempotency

- Command can be run multiple times safely
- Files will be overwritten with same content if no package changes
- No side effects if user cancels

## 5. Alternatives Considered

### Option A: Git-like diff/merge
**Approach:** Show diffs, allow selective merge  
**Pros:** Maximum flexibility, no data loss  
**Cons:** Complex UI for CLI, requires diff library, harder to test  
**Decision:** Rejected - over-engineered for simple use case

### Option B: Automatic backup before overwrite
**Approach:** Copy existing files to `.directive.backup/` before overwriting  
**Pros:** Safety net for customizations  
**Cons:** Clutters directory, user confusion about which files to use  
**Decision:** Rejected - preview + confirmation is sufficient

### Option C: Non-destructive addition only (current behavior)
**Approach:** Keep `overwrite=False`  
**Pros:** No risk of data loss  
**Cons:** Doesn't solve the problem - users can't get updates  
**Decision:** Rejected - this is what we're trying to fix

### Option D: Separate command (e.g., `directive sync`)
**Approach:** New command for updates, keep `update` as-is  
**Pros:** Backward compatible  
**Cons:** Confusing to have two update commands  
**Decision:** Rejected - better to fix existing command

### ✅ Chosen: Option E (Selective overwrite with preview)
**Approach:** Hardcoded list of maintained files, preview before overwrite  
**Pros:** Simple, clear, solves problem, safe with confirmation  
**Cons:** None significant  
**Why chosen:** Best balance of simplicity, safety, and functionality

## 6. Data Model & Contract Changes

**N/A** - This is a local file operation tool. No databases, APIs, or external contracts.

**File structure (unchanged):**
```
repo/
├── directive/
│   ├── reference/
│   │   ├── agent_operating_procedure.md  ← MAINTAINED (overwrite)
│   │   ├── agent_context.md              ← PROTECTED (never touch)
│   │   └── templates/
│   │       ├── spec_template.md          ← MAINTAINED (overwrite)
│   │       ├── impact_template.md        ← MAINTAINED (overwrite)
│   │       ├── tdr_template.md           ← MAINTAINED (overwrite)
│   │       └── implementation_summary_template.md ← MAINTAINED (overwrite)
│   └── specs/                            ← PROTECTED (never touch)
│       └── 20251105-feature/
│           ├── spec.md
│           ├── impact.md
│           └── tdr.md
└── .cursor/
    ├── rules/
    │   └── directive-core-protocol.mdc   ← MAINTAINED (overwrite)
    ├── mcp.json                          ← PROTECTED (one-time setup)
    └── servers/                          ← PROTECTED (one-time setup)
```

## 7. Security, Privacy, Compliance

**AuthN/AuthZ:** N/A - Local CLI tool, no network operations

**Secrets management:** N/A - No secrets handled

**PII handling:** N/A - No user data collected

**Threat model:**
- **Threat:** Malicious package could overwrite files  
  **Mitigation:** User must explicitly install package via pip/pipx; preview shows what will change
- **Threat:** Path traversal in file operations  
  **Mitigation:** Existing `_normalize_and_validate_path()` in bundles.py prevents escapes

**Overall risk:** Very low - local file operations in known paths

## 8. Observability & Operations

**N/A** - CLI tool outputs directly to user's terminal

**Logs/metrics/traces:** Not applicable (no server component)

**User feedback:**
- Preview before action (list of files)
- Confirmation prompt
- Summary after completion
- Verbose mode for detailed output

## 9. Rollout & Migration

### Release Strategy

**Version bump:** Minor version (e.g., 0.1.0 → 0.2.0)  
- Not a breaking change (enhancement)
- Significant new functionality

**CHANGELOG entry:**
```markdown
### Added
- `directive update` now actually updates Directive-maintained files (templates, AOP, cursor rules)
  - Shows preview of files to be overwritten before making changes
  - Prompts for confirmation (cancellable)
  - Protects project-specific content (agent_context.md, specs/)
  
### Changed
- `directive update` behavior: previously only added new files (non-destructive), now selectively overwrites maintained files
```

**Documentation updates:**
- README: Explain which files are "maintained" vs "project-specific"
- Warn users not to customize templates, AOP, or cursor rules (use agent_context.md instead)
- Document update workflow: `directive update` when new version released

### Migration Plan

**No migration needed** - Enhancement to existing command

**User communication:**
- Release notes highlighting new functionality
- Example output in documentation
- Warning about customizations being overwritten

### Revert Plan

**If issues arise:**
1. Users can decline the update when prompted
2. Package can be rolled back via pip/pipx
3. Users can manually restore files from git if they've overwritten something

**Blast radius:** Individual user repos only (no shared services)

## 10. Test Strategy & Spec Coverage (TDD)

### TDD Commitment

Write failing tests first, confirm failure, implement minimal code to pass, refactor while keeping tests green.

### Spec→Test Mapping

| Acceptance Criterion | Test ID(s) |
|---------------------|-----------|
| Given directive/ exists, when user runs update, then preview shown before changes | `test_update_shows_preview` |
| Given preview shown, when user confirms (Y), then files overwritten + success message | `test_update_confirms_and_overwrites` |
| Given preview shown, when user declines (n), then no files modified + graceful exit | `test_update_declines_no_changes` |
| Given non-interactive mode, when update called, then auto-confirms and proceeds | `test_update_noninteractive_autoconfirms` |
| Given no directive/, when update called, then helpful error + suggest init | `test_update_no_directive_dir` |
| Given custom agent_context.md, when update called, then agent_context unchanged | `test_update_preserves_agent_context` |
| Given cursor rules exist, when update called, then cursor rules overwritten | `test_update_overwrites_cursor_rules` |
| Given specs/ has history, when update called, then specs unchanged | `test_update_preserves_specs` |

### Test Tiers

**Unit tests (tests/test_cli.py):**
- `test_update_shows_preview` - Verify preview output format
- `test_update_confirms_and_overwrites` - Verify files actually updated
- `test_update_declines_no_changes` - Verify no changes on decline
- `test_update_noninteractive_autoconfirms` - Verify auto-confirm in non-TTY
- `test_update_no_directive_dir` - Verify error when directive/ missing
- `test_update_preserves_agent_context` - Verify agent_context.md never touched
- `test_update_overwrites_cursor_rules` - Verify cursor rules updated
- `test_update_preserves_specs` - Verify specs/ never touched
- `test_update_verbose_flag` - Verify verbose output
- `test_update_partial_cursor_rules` - Verify works if .cursor/rules/ doesn't exist yet

**Negative & edge cases:**
- No directive/ directory
- directive/ exists but empty
- Some maintained files missing (should create them)
- User declines confirmation
- Non-interactive mode (CI/scripts)
- Permission errors on file write
- .cursor/ directory doesn't exist (should create rules/ subdirectory)
- Only directive/ exists, no .cursor/ (should still update directive/ files)

**Performance tests:** N/A - Small file copies, negligible performance impact

**CI:** All tests run on push, must pass to merge

### Test Setup Patterns

```python
def test_update_confirms_and_overwrites(tmp_path):
    """Test that confirmed update actually overwrites maintained files."""
    # Setup: Create directive/ with old content
    directive_dir = tmp_path / "directive"
    directive_dir.mkdir()
    aop_file = directive_dir / "reference" / "agent_operating_procedure.md"
    aop_file.parent.mkdir(parents=True)
    aop_file.write_text("OLD CONTENT")
    
    # Mock user input: "Y" (confirm)
    with mock.patch('builtins.input', return_value='Y'):
        result = cmd_update(args)
    
    # Assert: File was overwritten with new content
    assert aop_file.read_text() != "OLD CONTENT"
    assert "Updated 5 files" in captured_output
```

## 11. Risks & Open Questions

### Risks

**Risk 1: User loses customizations**
- **Severity:** Medium
- **Likelihood:** Medium (if users customize maintained files)
- **Mitigation:** 
  - Preview clearly shows what will be overwritten
  - Confirmation prompt allows cancellation
  - Documentation warns against customizing maintained files
  - agent_context.md is the designated place for project customizations

**Risk 2: Files missing from package**
- **Severity:** Low
- **Likelihood:** Low (controlled by our package)
- **Mitigation:** Tests verify all maintained files exist in package

**Risk 3: Confusion about which files are maintained**
- **Severity:** Low
- **Likelihood:** Medium
- **Mitigation:** Clear documentation, preview shows the list every time

### Open Questions

**Q1: Should we add a `--dry-run` flag?**
- **Proposed answer:** No, preview already shows what will happen
- **Decision:** Keep it simple for now, can add later if requested

**Q2: Should we update cursor rules even if .cursor/ doesn't exist?**
- **Proposed answer:** Yes, create .cursor/rules/ and copy files
- **Reasoning:** User might have deleted it, good to restore

**Q3: What if new templates are added in future versions?**
- **Proposed answer:** Hardcoded list needs manual update, which is fine
- **Reasoning:** Template additions are rare, intentional changes

## 12. Milestones / Plan (post‑approval)

### Task Breakdown

**Task 1: Define maintained files list**
- [ ] Add `_get_maintained_files()` helper function
- [ ] Return dict with 'directive' and 'cursor_rules' categories
- [ ] Test: `test_get_maintained_files_returns_correct_list`
- **DoD:** Function returns complete list, test passes

**Task 2: Add preview functionality**
- [ ] Add `_show_update_preview()` function
- [ ] Display files to be overwritten
- [ ] Display files that won't be modified
- [ ] Test: `test_update_shows_preview`
- **DoD:** Preview output matches spec format, test passes

**Task 3: Refactor `cmd_update()` for selective overwrite**
- [ ] Check directive/ exists
- [ ] Call preview function
- [ ] Call existing `_ask_yes_no()` for confirmation
- [ ] Copy directive/ maintained files with overwrite=True
- [ ] Copy cursor rules with overwrite=True
- [ ] Display success summary
- [ ] Tests: `test_update_confirms_and_overwrites`, `test_update_declines_no_changes`
- **DoD:** All acceptance criteria tests pass, linter clean

**Task 4: Handle edge cases**
- [ ] No directive/ directory → error message
- [ ] No .cursor/ directory → create it
- [ ] Non-interactive mode → auto-confirm
- [ ] Verbose flag → detailed output
- [ ] Tests: `test_update_no_directive_dir`, `test_update_noninteractive_autoconfirms`, etc.
- **DoD:** All edge case tests pass

**Task 5: Verify protection of project files**
- [ ] Tests: `test_update_preserves_agent_context`, `test_update_preserves_specs`
- [ ] Manually verify specs/ and agent_context.md never touched
- **DoD:** Protection tests pass, manual verification complete

**Task 6: Documentation**
- [ ] Update CLI help text for `directive update`
- [ ] Add CHANGELOG entry
- [ ] Update README with maintained vs project-specific file list
- **DoD:** Docs reviewed and approved

### Dependencies

- No external dependencies
- Uses existing utilities (`_ask_yes_no`, `_copy_tree`, `_package_data_root`)

### Owners

- Implementation: AI Agent + Engineer review
- Testing: AI Agent (TDD)
- Documentation: AI Agent
- Approval: Engineer

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.

