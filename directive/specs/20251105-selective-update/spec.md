# Spec (per PR)

**Spec ID**: 20251105  
**Created**: 2025-11-05  

**Feature name**: Selective Update for Directive-Maintained Files  
**One-line summary**: Allow users to safely update Directive-maintained files (templates, AOP, cursor rules) when new versions are released, while preserving project-specific content (specs and agent context).  

---

## Problem
When Directive releases updated templates, agent operating procedures, or cursor rules, users currently have to manually identify which files to update. The current `directive update` command copies everything non-destructively, meaning users never get updates to files they've already initialized. Users need an easy way to pull the latest Directive-maintained files while preserving only their project-specific content (specs and agent context).

## Goal
Users can run `directive update` to refresh all Directive-maintained files (templates, AOP, and cursor rules), while preserving only their project-specific content (specs and agent context).

## Success Criteria
- [ ] Users can update templates, AOP, and cursor rules with a single command
- [ ] Project-specific content (agent_context.md and specs) is never overwritten
- [ ] Users see a clear preview of exactly which files will be overwritten before any changes occur
- [ ] Users can cancel the update after seeing the preview
- [ ] Updates work seamlessly across version upgrades

## User Story
As a Directive user, I want to easily pull the latest templates, agent operating procedures, and cursor rules when new versions are released, so that I can benefit from improvements without manually comparing files or worrying about losing my project-specific content (specs and agent context).

## Flow / States

**Happy Path:**
1. User runs `directive update`
2. Command checks if directive/ exists
3. Command displays list of files that will be overwritten:
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
   ```
4. Command asks for confirmation (Y/n, default Yes)
5. If confirmed, files are overwritten with latest versions from package
6. Success message shows what was actually updated

**Edge Case - No directive/ directory:**
1. User has no `directive/` directory yet
2. Command detects this and suggests running `directive init` first
3. Exits gracefully with helpful message

**Edge Case - Non-interactive mode:**
1. User runs command in CI/non-TTY environment
2. Command shows what would be updated
3. Auto-confirms with default (Yes) and proceeds

## UX Links
N/A - CLI only feature

## Requirements
- Must show a clear preview of which files will be overwritten before making any changes
- Must ask for user confirmation before overwriting (with sensible default)
- Must update these Directive-maintained files with overwrite:
  - `directive/reference/agent_operating_procedure.md`
  - `directive/reference/templates/spec_template.md`
  - `directive/reference/templates/impact_template.md`
  - `directive/reference/templates/tdr_template.md`
  - `directive/reference/templates/implementation_summary_template.md`
  - `.cursor/rules/directive-core-protocol.mdc` (and any other cursor rules from package)
- Must NOT overwrite project-specific content:
  - `directive/reference/agent_context.md` (project-specific context)
  - `directive/specs/` directory (project history)
  - Any other user-created files not in the package
- Must work whether or not directive/ already exists
- Must provide clear feedback about what was actually updated after completion
- Must handle non-interactive mode gracefully (CI/scripts)

## Acceptance Criteria
- Given a directive/ directory exists, when user runs `directive update`, then a preview of files to be overwritten is shown before any changes
- Given the preview is shown, when user confirms (Y), then templates, AOP, and cursor rules are overwritten and success message shows what was updated
- Given the preview is shown, when user declines (n), then no files are modified and command exits gracefully
- Given command runs in non-interactive mode, when `directive update` is called, then it auto-confirms and proceeds with updates
- Given directive/ doesn't exist, when user runs `directive update`, then command exits with helpful message to run `directive init`
- Given `agent_context.md` has custom content, when user runs `directive update`, then `agent_context.md` is unchanged
- Given `.cursor/rules/` has Directive rules, when user runs `directive update`, then cursor rules are overwritten with latest from package
- Given `directive/specs/` has project history, when user runs `directive update`, then specs directory is unchanged

## Non-Goals
- Intelligent merging of template changes (simple overwrite only)
- Backup/restore functionality for overwritten files
- Updating `.cursor/mcp.json` or `.cursor/servers/` (MCP setup remains one-time via `init`)
- Version-aware updates or migration scripts
- Selective update of individual files (all-or-nothing update of maintained files)

