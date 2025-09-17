# feat: MCP tools discovery (tools/list) and execution (tools/call)

## Summary
Adds MCP-compliant `tools/list` and `tools/call` to the stdio server so MCP-aware clients (e.g., Cursor) can discover Directive tools with titles/descriptions and execute them. Preserves existing custom methods for back-compat. Updates README with a brief discovery note.

## Links
- Spec: `directive/specs/mcp-tools-discovery/spec.md`
- Impact: `directive/specs/mcp-tools-discovery/impact.md`
- TDR: `directive/specs/mcp-tools-discovery/tdr.md`

## Changes
- Server (`src/directive/server.py`):
  - Add `tools/list` returning five tool descriptors with `name`, `title`, `description`, `inputSchema`:
    - `directive/files.list` — List Directive Files (no params)
    - `directive/file.get` — Read Directive File (`{ path: string }`)
    - `directive/spec.template` — Spec Template Bundle (no params)
    - `directive/impact.template` — Impact Template Bundle (no params)
    - `directive/tdr.template` — TDR Template Bundle (no params)
  - Add `tools/call` that dispatches to existing logic and returns MCP-style content array with embedded JSON as text
  - Keep prior custom methods (`spec.template`, etc.) for compatibility
- Tests (`tests/test_server.py`):
  - Add discovery test for `tools/list`
  - Add execution tests for `tools/call` (spec.template, file.get, files.list)
- Docs (`README.md`):
  - Note that MCP-aware IDEs can auto-discover tools once the server is running

## Acceptance Criteria Coverage
- `tools/list` returns five tools with the required fields  
- `tools/call` executes each tool and returns correct payloads (bundles, file read, file list)  
- Back-compat methods still function  
- Tests: 7 passed locally with `uv run pytest`

## How to Try Locally
```
uv add directive
uv run directive init
uv run directive mcp serve
```
- In your MCP-aware IDE, configure the command to launch the stdio server (`uv run directive mcp serve`). The agent should discover tools automatically.
- Optional: call once manually using the existing test harness or an MCP client.

## Notes
- Read-only by design.  
- We return JSON embedded in a single `text` content item for simplicity; can add structured content types later if needed.  
- `resources/*` APIs are out of scope for this PR and can be added later.
