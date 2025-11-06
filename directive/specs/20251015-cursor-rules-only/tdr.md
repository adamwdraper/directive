# Technical Design Review (TDR) — cursor-rules-only

**Author**: AI Agent  
**Date**: 2025-10-16  
**Links**: 
- Spec: `/directive/specs/cursor-rules-only/spec.md`
- Impact: `/directive/specs/cursor-rules-only/impact.md`

---

## 1. Summary

We are removing MCP server configuration files from the `directive init` workflow while preserving the Cursor project rules and the existing MCP server functionality. Currently, when users run `directive init` and accept Cursor setup, the CLI copies the entire `cursor/` directory from package data, which includes `mcp.json`, `servers/directive.sh`, and `rules/directive-core-protocol.mdc`. This change modifies the init process to copy only the `rules/` subdirectory, since agents don't require MCP server setup to work with directive. The MCP server code and `directive mcp serve` command remain fully functional for users who want to use them directly.

## 2. Decision Drivers & Non‑Goals

**Drivers:**
- Simplicity: Don't set up infrastructure users don't need for core directive workflow
- Clarity: Avoid implying that MCP server is required for directive to work
- Minimal disruption: Preserve MCP server code and functionality for those who use it
- Backward compatibility: Don't break existing repos that have MCP config

**Non‑Goals:**
- Removing or deprecating the MCP server implementation (`server.py`)
- Removing the `directive mcp serve` CLI command
- Providing automated migration or cleanup for existing MCP configurations
- Adding a new command to set up MCP configuration (users can do manually if needed)
- Creating comprehensive MCP setup documentation (out of scope for this PR)

## 3. Current State — Codebase Map (concise)

**Key modules:**
- `src/directive/cli.py`:
  - `cmd_init()` (lines 176-197): Handles initialization, calls `_copy_cursor_templates()`
  - `_copy_cursor_templates()` (lines 166-173): Copies entire `cursor/` directory from package data
  - `cmd_update()` (lines 200-218): Handles updates, calls `_ensure_cursor_launcher()` which creates MCP files
  - `cmd_mcp_serve()` (lines 221-234): Serves MCP server (unchanged by this feature)

**Package data structure:**
- `src/directive/data/directive/cursor/`:
  - `mcp.json` — MCP server configuration for Cursor IDE
  - `servers/directive.sh` — Bash launcher script for MCP server
  - `rules/directive-core-protocol.mdc` — Cursor project rule (the one we want to keep)

**Test coverage:**
- `tests/test_cli.py`: Tests for init, update, mcp serve commands
- Current tests verify full cursor/ directory is copied

**External contracts:**
- CLI output messages tell users "MCP server config + Project Rule" is being added
- File system contract: users expect certain files after `directive init`

## 4. Proposed Design (high level, implementation‑agnostic)

**Core approach:**
Replace the blanket `_copy_cursor_templates()` function with a selective copy that only handles the `rules/` subdirectory.

**Component responsibilities:**
1. **`cmd_init()`**: 
   - After copying directive/ folder, prompt user with updated text: "Add recommended Cursor Project Rules?"
   - On yes, copy only `.cursor/rules/` from package data
   - Update output message to reflect what was actually created

2. **`cmd_update()`**:
   - Remove the call to `_ensure_cursor_launcher()` which creates/overwrites MCP files
   - Only update directive/ folder contents
   - Do not touch any existing `.cursor/` files (MCP or otherwise)

3. **New function `_copy_cursor_rules_only()`**:
   - Copy only `rules/` subdirectory from package data
   - Target: `{repo_root}/.cursor/rules/`
   - Use existing `_copy_tree()` utility with `overwrite=False`

**Interfaces & data flow:**
```python
def _copy_cursor_rules_only(repo_root: Path, overwrite: bool = False) -> Tuple[int, int, List[str]]:
    """Copy only Cursor rules from package data, not MCP config.
    
    Returns: (copied_count, skipped_count, notes)
    """
    src = _package_data_root().joinpath("cursor", "rules")
    dst = repo_root.joinpath(".cursor", "rules")
    return _copy_tree(src, dst, overwrite=overwrite)
```

**Error handling:**
- If package data is missing rules directory, raise clear error
- Non-existent parent directories are created automatically by `_copy_tree()`
- Existing files are skipped (not overwritten) by default

**Idempotency:**
- Running `directive init` multiple times is safe (skips existing files)
- Running `directive update` does not modify `.cursor/` at all

## 5. Alternatives Considered

**Option A: Selective copy with current package structure** ✅ CHOSEN
- Pros: Minimal code changes, preserves package data structure, simple
- Cons: MCP files remain in package data but unused by init
- Decision: Chosen because it's the simplest approach and preserves MCP artifacts for documentation/manual setup

**Option B: Reorganize package data into `cursor-rules/` and `cursor-mcp/`**
- Pros: Clearer separation, no unused files in rules path
- Cons: Requires updating package data paths, more complex migration, breaks any hardcoded paths
- Decision: Rejected due to unnecessary complexity

**Option C: Add `--with-mcp` flag to init**
- Pros: Preserves old behavior as opt-in, flexible
- Cons: Adds CLI complexity, maintains code we're trying to deprecate, no clear use case
- Decision: Rejected because MCP setup can be done manually if needed

**Option D: Move MCP files to documentation/examples directory**
- Pros: Makes it clear they're optional, reduces package data size slightly
- Cons: Breaks any existing references, requires updating docs
- Decision: Deferred to future PR if needed

## 6. Data Model & Contract Changes

**File system contract changes (BREAKING):**

Before (v0.0.8):
```
directive init → creates:
  directive/
  .cursor/mcp.json
  .cursor/servers/directive.sh
  .cursor/rules/directive-core-protocol.mdc
```

After (v0.1.0):
```
directive init → creates:
  directive/
  .cursor/rules/directive-core-protocol.mdc
```

**CLI output changes:**

Before:
```
Prompt: "Add recommended Cursor setup (MCP server config + Project Rule)?"
Output: "Prepared .cursor/ (created 3, skipped 0)"
```

After:
```
Prompt: "Add recommended Cursor Project Rules?"
Output: "Created .cursor/rules/ (copied 1, skipped 0)"
```

**Backward compatibility:**
- Existing repos with `.cursor/mcp.json` continue to work unchanged
- `directive update` will NOT delete or modify existing MCP files
- `directive mcp serve` continues to work for all users (old and new repos)
- Version bump to 0.1.0 to signal minor breaking change in init behavior

**Deprecation plan:**
- No deprecation needed (MCP server code stays, just not auto-configured)
- Could add migration guide in CHANGELOG for users who want MCP setup

## 7. Security, Privacy, Compliance

**AuthN/AuthZ:**
- Not applicable (CLI tool, no authentication)

**Secrets management:**
- No change. MCP server launcher script doesn't contain secrets

**Threat model:**
- Reduced attack surface: fewer files created automatically
- No new vulnerabilities introduced
- MCP server code still available if users explicitly want it

**PII handling:**
- Not applicable

## 8. Observability & Operations

**Logs to add:**
- Update CLI output in `cmd_init()` to say "Created .cursor/rules/" instead of "Prepared .cursor/"
- Verbose mode should list specific rule files copied
- No changes to MCP server logs (unchanged code)

**Metrics/Traces:**
- Not applicable (CLI tool, no telemetry)

**Dashboards/Alerts:**
- Not applicable

**Runbooks:**
- Update README to document:
  - New init behavior (rules only, no MCP)
  - How to manually set up MCP server if desired
  - Existing repos with MCP continue to work

## 9. Rollout & Migration

**Feature flags:**
- Not applicable (CLI tool distributed via package updates)

**Migration strategy:**
- No migration needed for existing users
- Users who upgrade package and run `directive update` will NOT have their existing MCP files modified
- New users will need to manually set up MCP if they want it (document in README)

**Revert plan:**
- If needed, can release patch version that restores old behavior
- No data loss risk (only affects new initializations)

**Blast radius:**
- Low: Only affects new `directive init` runs
- Existing repos unaffected
- MCP server functionality unchanged

## 10. Test Strategy & Spec Coverage (TDD)

**TDD commitment:**
Write failing tests first, verify they fail, implement minimal code to pass, refactor.

**Spec→Test mapping:**

| Acceptance Criterion | Test ID | Test Type |
|---------------------|---------|-----------|
| Given new repo, when init with Cursor setup, then rules created but NOT mcp.json/servers | `test_init_creates_rules_not_mcp` | Integration |
| Given existing repo with MCP, when update, then existing mcp.json unchanged | `test_update_preserves_existing_mcp` | Integration |
| Given package installed, when mcp serve, then server starts successfully | `test_mcp_serve_still_works` | Unit |
| Given CLI invoked, when init --help, then no MCP mention in prompts | `test_init_prompt_no_mcp_mention` | Integration |

**Test details:**

1. **`test_init_creates_rules_not_mcp`**
   - Given: Fresh temp directory (no existing .cursor/)
   - When: Run `directive init`, accept Cursor setup
   - Then: 
     - Assert `.cursor/rules/directive-core-protocol.mdc` exists
     - Assert `.cursor/mcp.json` does NOT exist
     - Assert `.cursor/servers/` does NOT exist

2. **`test_update_preserves_existing_mcp`**
   - Given: Temp directory with pre-existing `.cursor/mcp.json`
   - When: Run `directive update`
   - Then:
     - Assert `.cursor/mcp.json` still exists with original content
     - Assert file not overwritten or deleted

3. **`test_mcp_serve_still_works`**
   - Given: Package installed
   - When: Call `cmd_mcp_serve()` in test
   - Then: No errors raised (or mock FastMCP app and verify it's called)

4. **`test_init_prompt_no_mcp_mention`**
   - Given: Mock user input
   - When: Run `directive init` and capture output
   - Then: Assert prompt text is "Add recommended Cursor Project Rules?" (no mention of MCP)

**Negative & edge cases:**
- Test init when `.cursor/rules/` already exists → should skip, not error
- Test init declining Cursor setup → should not create `.cursor/` at all
- Test update when no `.cursor/` exists → should only update directive/, no error

**Performance tests:**
- Not applicable (file copy operations, fast enough)

**CI requirements:**
- All tests run in CI via pytest
- Must pass before merge

## 11. Risks & Open Questions

**Risks:**

1. **Risk**: External documentation or tutorials reference MCP setup after init
   - **Mitigation**: Update README and add CHANGELOG entry explaining change
   - **Severity**: Low (can document manual setup)

2. **Risk**: Users expect MCP server to work after init
   - **Mitigation**: Clear messaging in output and docs that MCP is optional
   - **Severity**: Medium (could cause confusion)

3. **Risk**: Breaking automated scripts that depend on init creating MCP files
   - **Mitigation**: Version bump to 0.1.0 signals breaking change
   - **Severity**: Low (unlikely to have automated scripts depending on this)

**Open Questions:**

1. ❓ Should we add a note in the CLI output about how to set up MCP if users want it?
   - **Proposed resolution**: Add a line in README, keep CLI output simple
   - **Owner**: Adam to decide

2. ❓ Should we keep `_ensure_cursor_launcher()` function for future use or delete it?
   - **Proposed resolution**: Keep it but mark as unused (could be useful for docs/examples)
   - **Owner**: TDR review

3. ❓ Should we remove MCP files from package data entirely or leave them?
   - **Proposed resolution**: Leave them (no harm, could be useful for manual setup)
   - **Owner**: TDR review

## 12. Milestones / Plan (post‑approval)

**Task 1: Write failing tests**
- [ ] Implement `test_init_creates_rules_not_mcp` (expect failure)
- [ ] Implement `test_update_preserves_existing_mcp` (expect failure)
- [ ] Implement `test_mcp_serve_still_works` (should pass already)
- [ ] Implement `test_init_prompt_no_mcp_mention` (expect failure)
- [ ] Run tests, confirm failures (except mcp_serve test)
- **DoD**: All tests written, failing tests fail for right reasons

**Task 2: Implement `_copy_cursor_rules_only()` function**
- [ ] Add new function in `cli.py` with signature from design
- [ ] Use `_copy_tree()` to copy only rules subdirectory
- [ ] Add docstring
- **DoD**: Function exists, linted, documented

**Task 3: Update `cmd_init()` to use new function**
- [ ] Replace `_copy_cursor_templates()` call with `_copy_cursor_rules_only()`
- [ ] Update prompt text to "Add recommended Cursor Project Rules?"
- [ ] Update output message to "Created .cursor/rules/"
- **DoD**: Init uses new function, messages updated

**Task 4: Update `cmd_update()` to not touch Cursor files**
- [ ] Remove `_ensure_cursor_launcher()` call
- [ ] Update output message (no longer mentions .cursor/)
- **DoD**: Update doesn't modify .cursor/ directory

**Task 5: Run tests and refactor**
- [ ] Run all tests, verify they pass
- [ ] Check test coverage
- [ ] Refactor if needed (e.g., extract message constants)
- [ ] Run linter, fix issues
- **DoD**: All tests green, lint clean, coverage maintained

**Task 6: Update documentation**
- [ ] Update README to explain new init behavior
- [ ] Add CHANGELOG entry for breaking change
- [ ] Document manual MCP setup if users want it
- [ ] Bump version to 0.1.0 in pyproject.toml
- **DoD**: Docs updated, version bumped

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved.

