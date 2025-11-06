# Technical Design Review (TDR) — MCP Auto‑Start for Cursor

**Author**: <agent or engineer>  
**Date**: <YYYY-MM-DD>  
**Links**: Spec (`/directive/specs/mcp-autostart/spec.md`), Impact (`/directive/specs/mcp-autostart/impact.md`)

---

## 1. Summary
Enable automatic startup of the `Directive` MCP server in Cursor by setting `autoStart: true` in `.cursor/mcp.json`. This removes the manual step to start the server and makes MCP capabilities available immediately.

## 2. Decision Drivers & Non‑Goals
- Drivers: reduce friction; ensure consistent availability of MCP tools on project open.
- Non‑Goals: adding/removing servers; changing transports or arguments; modifying global user settings.

## 3. Current State — Codebase Map (concise)
- `.cursor/mcp.json` defines `mcpServers.Directive` with `type`, `command`, `args`, and `transport` but no `autoStart` flag.

## 4. Proposed Design (high level, implementation‑agnostic)
- Add `"autoStart": true` to the `Directive` server block in `.cursor/mcp.json`.
- Do not alter command/args/transport.

## 5. Alternatives Considered
- Manual start: acceptable but adds repeated friction; rejected.
- Custom scripts or extensions: unnecessary for a single‑flag change.

## 6. Data Model & Contract Changes
- None.

## 7. Security, Privacy, Compliance
- No additional surface area; same server process started automatically.

## 8. Observability & Operations
- Use Cursor’s server start logs for troubleshooting failed starts.

## 9. Rollout & Migration
- Single change in repo config; no migration required.

## 10. Test Strategy & Spec Coverage (TDD)
- Manual check: open repo in Cursor and verify server auto‑starts.
- Negative check: confirm a wrong key (e.g., `autoRestart`) does not auto‑start (ensures correctness of `autoStart`).

## 11. Risks & Open Questions
- Minimal risk; ensure JSON remains valid.

## 12. Milestones / Plan (post‑approval)
1) Add spec/impact/tdr.  
2) Update `.cursor/mcp.json` with `autoStart: true`.  
3) Open PR and verify by reopening workspace.

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.


