# Impact Analysis — MCP Auto‑Start for Cursor

## Modules/packages likely touched
- `.cursor/mcp.json` (enable `autoStart` for the `Directive` server)

## Contracts to update (APIs, events, schemas, migrations)
- None. Editor configuration only; no public API or schema changes.

## Risks
- Security: None; no new secrets or permissions.
- Performance/Availability: Minimal startup overhead when opening the workspace.
- Data integrity: None.

## Observability needs
- Logs: Rely on Cursor’s MCP server start logs for diagnostics on failure.
- Metrics: None.
- Alerts: None.


