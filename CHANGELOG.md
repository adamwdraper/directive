# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

