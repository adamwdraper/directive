# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Selective Update Functionality**: `directive update` now actually updates Directive-maintained files
  - Shows clear preview of files to be overwritten before making any changes
  - Prompts for confirmation (cancellable) before proceeding
  - Updates maintained files: templates, `agent_operating_procedure.md`, cursor rules
  - Protects project-specific content: `agent_context.md`, `specs/` directory
  - Handles non-interactive mode (auto-confirms for CI/scripts)

### Changed
- **`directive update` behavior enhancement** (not breaking):
  - **Old behavior**: Only copied new files that didn't exist (essentially non-functional after initial `init`)
  - **New behavior**: Selectively overwrites Directive-maintained files with latest from package
  - Files that WILL be updated: `agent_operating_procedure.md`, all templates, cursor rules
  - Files that will NOT be touched: `agent_context.md` (your context), `specs/` (your history)
  - Preview example:
    ```
    The following files will be updated (overwritten):
      - directive/reference/agent_operating_procedure.md
      - directive/reference/templates/*.md
      - .cursor/rules/directive-core-protocol.mdc
    
    Files that will NOT be modified:
      - directive/reference/agent_context.md (your project-specific context)
      - directive/specs/ (your project history)
    
    Proceed with update? (Y/n)
    ```

### Documentation
- Updated implementation guides to clarify which files are "maintained" vs "project-specific"
- Users should not customize templates or AOP directly (use `agent_context.md` for project customizations)
- Running `directive update` after upgrading keeps you in sync with latest Directive improvements

## [0.1.0] - 2025-10-16

### Changed
- **BREAKING**: `directive init` no longer creates MCP server configuration files
  - Previously created: `.cursor/mcp.json`, `.cursor/servers/directive.sh`
  - Now creates only: `.cursor/rules/directive-core-protocol.mdc`
  - Rationale: MCP server is optional infrastructure, not required for core directive workflow
- Updated CLI prompt from "Add recommended Cursor setup (MCP server config + Project Rule)?" to "Add recommended Cursor Project Rules?"
- `directive update` no longer modifies `.cursor/` directory to avoid touching user's Cursor configuration

### Maintained
- MCP server functionality (`directive mcp serve`) remains fully functional and unchanged
- Existing repositories with MCP configuration will continue to work without any changes
- All MCP server code preserved for users who want to use it

### Migration Guide
- **For existing users**: No action needed. Your existing `.cursor/mcp.json` will continue to work.
- **For new users who want MCP**: Manually create `.cursor/mcp.json` with the configuration shown in README.md
- **For users upgrading**: Running `directive update` will not delete your existing MCP files

## [0.0.9] - 2025-10-XX

### Previous releases
(See git history for details of earlier versions)

