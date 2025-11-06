# feat: MCP server and minimal CLI (read-only) per TDR

## Summary
Implements a minimal, read-only MCP server and a tiny `directive` CLI to make the repo’s Directive guidance/templates easily consumable by coding agents and humans. This follows the TDR at `directive/specs/mcp-server-and-cli/tdr.md`.

## Links
- Spec: `directive/specs/mcp-server-and-cli/spec.md`
- Impact: `directive/specs/mcp-server-and-cli/impact.md`
- TDR: `directive/specs/mcp-server-and-cli/tdr.md`

## Changes
- CLI `directive` with commands:
  - `init`: non-destructively scaffold `directive/` from packaged defaults
  - `update`: add any missing defaults
  - `mcp serve`: start a minimal stdio JSON-RPC server
  - `bundle <template>`: print a read-only drafting bundle (AOP + Agent Context + template + Primer)
- Packaged defaults under `src/directive/data/directive/` (AOP + templates) and wired into CLI init/update
- Bundles API (`directive.bundles`) returning:
  - `agentOperatingProcedure`, `agentContext`, `template`, `resources`
- Minimal stdio server exposing MCP-like surface:
  - `directive.files.list`
  - `directive.file.get`
  - `spec.template`, `impact.template`, `tdr.template`
- `pyproject.toml`: console script `directive`, include packaged data

## Acceptance Criteria Coverage
- Read-only tools return verbatim file contents and include a short Primer
- Resources scoped to `directive/**`
- Helpful error when template missing + list available templates

## Test Results (uv)
```
uv run --with pytest pytest -q
# 5 passed in 0.17s
```

## How to Try Locally
```
# Install
uv pip install -e .

# Initialize defaults (non-destructive)
directive init

# Print a bundle for spec drafting
directive bundle spec_template.md

# Start the stdio server (optional)
directive mcp serve
```

## Notes
- Read-only design; no file writes from agent-facing tools
- Path handling prevents escaping outside `directive/`
- Simple JSON-RPC framing; can be swapped for official MCP lib later without breaking external behavior
