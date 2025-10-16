# Spec (per PR)

**Feature name**: cursor-rules-only  
**One-line summary**: Remove MCP server configuration from directive init while keeping Cursor project rules  

---

## Problem
The directive init process currently copies MCP server configuration (`.cursor/mcp.json`) and a launcher script (`.cursor/servers/directive.sh`) that are not needed for agents to work with directive. This creates unnecessary files and implies that an MCP server is required, when it's actually optional infrastructure that users may not need.

## Goal
When users run `directive init`, they should get only the essential files: the directive templates/reference docs and the Cursor project rules. The MCP server code remains in the codebase for users who want to use it directly, but it's not automatically configured during initialization.

## Success Criteria
- [ ] Running `directive init` creates directive/ folder and `.cursor/rules/` but NOT `.cursor/mcp.json` or `.cursor/servers/`
- [ ] MCP server code (`server.py`, `directive mcp serve` command) remains functional and unchanged
- [ ] Existing repos with MCP config are not broken by package updates

## User Story
As a developer using directive, I want `directive init` to set up only the core workflow files and Cursor rules, so that I don't get MCP server configuration that I don't need.

## Flow / States

**Happy path:**
1. User runs `directive init` in a new repo
2. System creates `directive/` folder with templates and reference docs
3. User accepts prompt to add Cursor setup
4. System creates only `.cursor/rules/directive-core-protocol.mdc`
5. System does NOT create `.cursor/mcp.json` or `.cursor/servers/directive.sh`

**Edge case - existing MCP config:**
1. User has existing `.cursor/mcp.json` from an old version
2. User runs `directive update`
3. System leaves existing MCP files unchanged (does not delete them)

## UX Links
- N/A (CLI command, no visual UI)

## Requirements
- Must copy only Cursor project rules during init (not MCP config)
- Must preserve existing MCP server functionality (`directive mcp serve` command)
- Must not break existing installations that have MCP config already set up
- Must update the package data structure to separate rules from MCP config

## Acceptance Criteria
- Given a new repo, when user runs `directive init` and accepts Cursor setup, then `.cursor/rules/` is created but `.cursor/mcp.json` and `.cursor/servers/` are NOT created
- Given an existing repo with MCP config, when user runs `directive update`, then existing `.cursor/mcp.json` is left unchanged (not deleted or overwritten)
- Given the package is installed, when user runs `directive mcp serve`, then the MCP server starts successfully (functionality preserved)
- Given the CLI is invoked, when user runs `directive init --help`, then no mention of MCP server appears in the help text or prompts

## Non-Goals
- Deleting or removing the MCP server implementation code (`server.py`)
- Removing the `directive mcp serve` CLI command
- Migrating or cleaning up existing MCP configurations in user repos
- Providing a new command to set up MCP configuration (users can do this manually if needed)

