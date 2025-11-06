# Impact Analysis — MCP tools discovery and descriptions for Directive

## Modules/packages likely touched
- `src/directive/server.py`
  - Add MCP `tools/list` endpoint and return tool descriptors (name, title, description, inputSchema)
  - Add MCP `tools/call` dispatcher mapping tool names to existing handlers
  - Optionally declare tools capability during `initialize`
- `src/directive/bundles.py`
  - No functional changes; continue to power bundle responses
- `tests/`
  - Add tests covering `tools/list` schema and `tools/call` happy paths and validation errors
- `README.md`
  - Brief mention that MCP-aware IDEs/agents can discover and call tools automatically
- `directive/specs/mcp-tools-discovery/*`
  - Spec (done), Impact (this), TDR (next)

## Contracts to update (APIs, events, schemas, migrations)
- JSON-RPC MCP methods (new):
  - `tools/list` → `{ tools: ToolDescriptor[] }` where each descriptor has `{ name, title, description, inputSchema }`
  - `tools/call` → `{ content: Content[] }` (return bundle JSON as `type: "text"` for now)
- Tool names (stable, namespaced):
  - `directive/files.list`
  - `directive/file.get`
  - `directive/spec.template`
  - `directive/impact.template`
  - `directive/tdr.template`
- Input schemas:
  - Empty objects for template bundle tools
  - `{ path: string }` for `directive/file.get` (validate path under `directive/`)
- Backwards compatibility:
  - Keep existing custom methods (`spec.template`, etc.) for now; prefer MCP tools in clients

## Risks
- Protocol compatibility: MCP evolves; ensure names and response shape are acceptable to common clients (Cursor, etc.)
- Content format: returning large JSON as a single `text` block may be token-heavy; consider `application/json` content type later
- Security: path traversal protection in `file.get` must remain strict
- Error handling: clear, actionable errors (e.g., suggest `directive update`) without leaking internals
- Drift between `tools/list` descriptors and actual handler behavior if not covered by tests
- IDE integration variance: different clients may expect different optional fields (titles, descriptions length)

## Observability needs
- Logs:
  - Tool calls: name, duration, success/failure, truncated error messages
  - Validation failures (e.g., bad `path`) with reason
- Metrics (if added later):
  - Counter per tool call and error
  - Latency histogram per tool
- Debug toggle (env var) to enable verbose logging without changing behavior
