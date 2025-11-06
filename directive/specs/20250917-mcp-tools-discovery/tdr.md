# Technical Design Review (TDR) — MCP tools discovery and descriptions for Directive

**Author**: <agent>  
**Date**: <YYYY-MM-DD>  
**Links**: Spec (`/directive/specs/mcp-tools-discovery/spec.md`), Impact (`/directive/specs/mcp-tools-discovery/impact.md`), related PRs

---

## 1. Summary
Add MCP-compliant `tools/list` and `tools/call` to the stdio server so MCP-aware clients can discover Directive tools (with titles/descriptions/input schemas) and execute them. Preserve existing custom methods for backward compatibility. Strictly read-only.

## 2. Decision Drivers & Non‑Goals
- Drivers: Improve agent UX and discoverability; align with MCP client expectations (e.g., Cursor).  
- Non‑Goals: Implement MCP `resources/*` in this iteration; any write operations.

## 3. Current State — Codebase Map (concise)
- `src/directive/server.py`: stdio JSON-RPC loop; custom methods for file list/get and template bundles.  
- `src/directive/bundles.py`: path normalization, file read helpers, bundle builder.  
- `tests/test_server.py`, `tests/test_cli.py`: coverage for current methods and CLI.

## 4. Proposed Design (high level, implementation‑agnostic)
- Extend the JSON-RPC handler to support two MCP methods:
  - `tools/list`: return static descriptors for five tools.  
  - `tools/call`: route by `params.name` to existing logic; validate `params.arguments` via minimal checks.
- Tool descriptors (namespaced, stable):
  - `directive/files.list` — List Directive Files  
    - Description: List all files under `directive/`. Input: `{}`.
  - `directive/file.get` — Read Directive File  
    - Description: Read a file under `directive/` by `path`. Input: `{ path: string }`.
  - `directive/spec.template` — Spec Template Bundle  
    - Description: Return AOP, Agent Context, Spec template, and a concise Primer. Input: `{}`.
  - `directive/impact.template` — Impact Template Bundle  
    - Description: Return AOP, Agent Context, Impact template, and a concise Primer. Input: `{}`.
  - `directive/tdr.template` — TDR Template Bundle  
    - Description: Return AOP, Agent Context, TDR template, and a concise Primer. Input: `{}`.
- `tools/call` result format: wrap current outputs in MCP content array with a single `text` item containing JSON (bundle or file payload). Keep simple for now.
- Error handling: map current exceptions to MCP error with readable messages.

## 5. Alternatives Considered
- Fully adopt an MCP library now — Pros: stricter schema compliance; Cons: added dependency, bigger change.  
- Add `resources/*` in the same PR — Pros: richer client integration; Cons: scope creep.  
- Chosen: minimal additions (`tools/list`, `tools/call`) with current stdio framing.

## 6. Data Model & Contract Changes
- New methods:
  - `tools/list` → `{ tools: [{ name, title, description, inputSchema }] }`
  - `tools/call` → `{ content: [{ type: "text", text: string }] }`
- Tool names and input schemas per Spec.  
- Backward compatibility: keep existing custom methods.

## 7. Security, Privacy, Compliance
- Validate `path` strictly under `directive/` using existing normalization.  
- No secrets handled.  
- Limit error details to messages suitable for end users.

## 8. Observability & Operations
- Log tool name, duration, and outcome (success/error).  
- Keep logging off by default; enable via env flag if needed.

## 9. Rollout & Migration
- Feature flag not required; additive methods.  
- Rollout: minor release.  
- Revert: remove methods; low blast radius.

## 10. Test Strategy & Spec Coverage (TDD)
- Unit tests (new):
  - `tools/list` returns five tools with required fields and schemas.  
  - `tools/call` for each tool → happy path result shape.  
  - Validation error for `directive/file.get` with missing/invalid `path`.  
  - Missing template → helpful error preserved.  
- Contract tests: assert tool names and schema objects match Spec exactly.

## 11. Risks & Open Questions
- Risk: Some clients expect non-text content types; acceptable to start with `text`.  
- Open: Add `resources/*` later? Likely yes, as a separate spec/PR.

## 12. Milestones / Plan (post‑approval)
- Add `tools/list` descriptors and `tools/call` routing in `server.py`.  
- Add tests for listing and calling.  
- Update README (one line) noting MCP-aware clients can discover tools.

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
