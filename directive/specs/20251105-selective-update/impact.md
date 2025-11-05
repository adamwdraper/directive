# Impact Analysis — Selective Update for Directive-Maintained Files

**Spec ID**: 20251105  
**Created**: 2025-11-05  

## Modules/packages likely touched
- `src/directive/cli.py` — `cmd_update()` function needs complete refactor
  - Current behavior: non-destructive copy of all files
  - New behavior: selective overwrite of maintained files only
- `src/directive/bundles.py` — may need helper to identify "maintained files" list
- `src/directive/data/directive/` — package data structure (no changes needed, just reference)
- `.cursor/rules/` — will be updated during update command
- Tests: `tests/test_cli.py` — need new tests for selective update behavior

## Contracts to update (APIs, events, schemas, migrations)

### CLI Command Behavior Enhancement
- **Command**: `directive update`
- **Breaking change**: NO
  - Old: Non-destructive copy only (only adds new files, never updates existing)
  - New: Selective overwrite of maintained files (actually updates templates/AOP/cursor rules)
  - Current behavior is essentially non-functional for updates (always reports "0 copied, N skipped")
- **User impact**: 
  - Positive: Users can now actually get updates to templates and AOP
  - Minor: Users who customized templates, AOP, or cursor rules will see those overwritten (but this is the desired behavior)
- **Documentation needs**: 
  - CHANGELOG entry explaining new functionality
  - Document which files are "maintained" vs "project-specific"
  - Warn users not to customize maintained files

### New User Interaction
- Confirmation prompt with preview of files to be overwritten
- Must handle TTY vs non-TTY environments
- Output format changes (more detailed feedback about what was actually updated)

## Risks

### Security
- **Low risk**: No security concerns
- File writes are restricted to known paths within directive/ and .cursor/
- No new external inputs or data handling

### Performance/Availability
- **Low risk**: CLI tool, local file operations only
- Negligible performance impact (copying ~5-10 small text files)
- No availability concerns (not a service)

### Data integrity
- **Medium risk**: User customizations will be lost
  - **Mitigation 1**: Clear preview before overwriting shows exactly what will change
  - **Mitigation 2**: Confirmation prompt (cancellable)
  - **Mitigation 3**: Documentation warns users not to customize maintained files
  - **Mitigation 4**: agent_context.md and specs/ are explicitly protected (never overwritten)
- **Low risk**: Incorrect file selection could overwrite user data
  - **Mitigation**: Hardcoded list of maintained files (not dynamic discovery)
  - **Mitigation**: Comprehensive tests covering edge cases

### Backward Compatibility
- **Low risk**: Enhancement to existing `directive update` behavior, not breaking
  - Current command essentially does nothing useful (only copies new files)
  - New behavior makes the command actually functional for its intended purpose
  - Confirmation prompt protects users from accidental overwrites
  - **Note**: Not a breaking change, but document clearly in CHANGELOG as new feature

## Observability needs

### Logs
- Not applicable (CLI tool, user sees direct output)
- All feedback provided via stdout/stderr

### Metrics
- Not applicable (no telemetry in CLI tool)

### Alerts
- Not applicable (local CLI execution)

### User Feedback Requirements
- **Before action**: Clear preview of files to be overwritten
- **During action**: Progress indication (optional, files are small)
- **After action**: Summary of what was actually updated
- **On error**: Clear error messages if directive/ missing or file operations fail

