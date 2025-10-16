# Impact Analysis — cursor-rules-only

## Modules/packages likely touched
- `src/directive/cli.py`
  - `cmd_init()` — Update to copy only rules, not full cursor/ directory
  - `_copy_cursor_templates()` — Modify or replace to selectively copy rules
  - `cmd_update()` — Ensure update doesn't force MCP config on users
  - Help text / prompts that mention "MCP server config"
  
- `src/directive/data/directive/cursor/`
  - Package data structure needs reorganization to separate:
    - `rules/` (included in init)
    - `mcp.json` and `servers/` (excluded from init, available via docs or manual setup)
  - Option 1: Keep current structure, add selective copy logic
  - Option 2: Split into `cursor-rules/` and `cursor-mcp/` at package data level

- `tests/test_cli.py`
  - Update tests for `directive init` to verify rules are created but MCP files are not
  - Verify `directive update` doesn't overwrite or delete existing MCP config
  - Add test to ensure MCP server command still works independently

## Contracts to update (APIs, events, schemas, migrations)
- **CLI behavior contract** (user-facing):
  - `directive init` prompt changes from "Add recommended Cursor setup (MCP server config + Project Rule)?" 
    to "Add recommended Cursor Project Rules?"
  - Output message changes to reflect only rules being created
  - No command-line arguments or flags change
  
- **Package data structure** (internal):
  - If reorganizing package data, ensure `_package_data_root()` still resolves correctly
  - Maintain backward compatibility: don't break `directive mcp serve` which may reference package data
  
- **File system contract** (what init creates):
  - Previously created: `.cursor/mcp.json`, `.cursor/servers/directive.sh`, `.cursor/rules/directive-core-protocol.mdc`
  - Now creates: `.cursor/rules/directive-core-protocol.mdc` only
  - Breaking change for any external scripts/docs that assume MCP files exist after init

## Risks
- **Security**: 
  - Low risk. Removing automatic MCP server setup reduces attack surface slightly
  - No new security concerns introduced
  
- **Performance/Availability**: 
  - No impact. Feature is about file copying during init, not runtime behavior
  
- **Data integrity**: 
  - Risk: Users with existing `.cursor/mcp.json` might be confused if behavior changes
  - Mitigation: `directive update` should not delete existing MCP files, only skip them
  - Risk: Documentation or external tutorials might reference MCP setup in init
  - Mitigation: Update README and any release notes to clarify new behavior

- **Backward compatibility**:
  - Repos initialized with old versions will have MCP files that continue to work
  - Repos initialized with new version won't have MCP files, but can add them manually if needed
  - Consider: Should we add a `--with-mcp` flag to init for users who want the old behavior?

- **Developer experience**:
  - Users who want MCP server will need manual setup steps (could document in README)
  - Could cause confusion if users expect MCP server to "just work" after init

## Observability needs
- **Logs**: 
  - CLI output messages should clearly state what was created: "Created .cursor/rules/" not "Prepared .cursor/"
  - Verbose mode should list exactly which files were copied
  
- **Metrics**: 
  - N/A (CLI tool, no telemetry)
  
- **Alerts**:
  - N/A (CLI tool, no runtime monitoring)

- **Testing observability**:
  - Tests should explicitly verify presence of `.cursor/rules/` and absence of `.cursor/mcp.json` and `.cursor/servers/`
  - Tests should verify `directive mcp serve` still works (MCP code not broken)

