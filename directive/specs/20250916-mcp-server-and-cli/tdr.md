# Technical Design Review (TDR) — MCP server and minimal CLI

**Author**: <agent or engineer>  
**Date**: <YYYY-MM-DD>  
**Links**: Spec (`/directive/specs/mcp-server-and-cli/spec.md`), Impact (`/directive/specs/mcp-server-and-cli/impact.md`), related issues/PRs, designs

---

## 1. Summary
Deliver a read‑only MCP server plus a tiny CLI so any coding agent can reliably fetch Directive guidance and templates at the exact moment of drafting. The MCP server exposes:
- Resources for listing and fetching files under `directive/`
- Three read‑only tools: `spec.template()`, `impact.template()`, `tdr.template()` that each return: a short Primer derived from the AOP, full `agent_operating_procedure.md`, full `agent_context.md`, and the corresponding template content (verbatim), along with resource paths.

The CLI (`uvx directive ...`) helps humans bootstrap/update `directive/` into a repo and optionally run the MCP server locally. The agent writes nothing via Directive; it uses its own tools. This keeps Directive safe, portable, and focused on consistent context delivery.

## 2. Decision Drivers & Non‑Goals
- Drivers: reduce friction (no copy/paste prompts), increase agent accuracy via standardized context, remain implementation‑agnostic and safe (read‑only), work across agent clients.
- Non‑Goals: file‑writing tools, GitHub App/Checks, schema compilers/state machines, IDE extensions beyond optional convenience.

## 3. Current State — Codebase Map (concise)
- `directive/agent_operating_procedure.md`, `directive/agent_context.md`, and templates exist; no MCP server or CLI yet.
- Python toolchain (Agent Context): Python 3.13, `uv` for packaging. No server framework chosen yet.
- No external contracts implemented yet; this TDR defines the initial MCP surface.

## 4. Proposed Design (high level, implementation‑agnostic)
Overall approach
- Provide a small Python MCP server that exposes Directive as read‑only context. Provide a CLI to install/update `directive/` and optionally start the server.

MCP Resources
- `directive.files.list()` → returns a listing (path, size, modified) scoped to `directive/**`.
- `directive.file.get(path)` → returns raw file contents for any file under `directive/`.

MCP Tools (read‑only templates)
- `spec.template()` → returns object:
  
  - `agentOperatingProcedure: { path, content }`
  - `agentContext: { path, content }`
  - `template: { path: "directive/templates/spec_template.md", content }`
  - `resources: [paths]`
- `impact.template()` → same shape with `impact_template.md`.
- `tdr.template()` → same shape with `tdr_template.md`.

CLI (humans only)
- `uvx directive init` → creates `directive/` if missing with default files/templates. Non‑destructive by default.
- `uvx directive update` → refreshes defaults where unchanged; prints a summary for modified files.
- `uvx directive mcp serve` → starts the MCP server in the current repo, rooted at `directive/`.

Error handling
- Missing template: tools return a helpful error listing available templates and suggesting `directive update`.
- Large files: tolerated initially; if sizes grow, consider streaming/chunking later.

Performance expectations
- All responses are small text files; target sub‑100ms local responses. No retries needed beyond transport.

## 5. Alternatives Considered
- Write‑capable tools (create files): more automation but higher risk and complexity; rejected for focus and safety.
- Summarized context: smaller payloads but risks losing crucial guidance; rejected—return full verbatim content.
- GitHub App first: powerful PR workflows but heavier setup; defer to later milestone.

## 6. Data Model & Contract Changes
MCP responses (illustrative JSON for `spec.template()`)
```
{
  "agentOperatingProcedure": { "path": "directive/agent_operating_procedure.md", "content": "...full text..." },
  "agentContext": { "path": "directive/agent_context.md", "content": "...full text..." },
  "template": { "path": "directive/templates/spec_template.md", "content": "...full text..." },
  "resources": [
    { "path": "directive/agent_operating_procedure.md" },
    { "path": "directive/agent_context.md" },
    { "path": "directive/templates/spec_template.md" }
  ]
}
```
Backward compatibility: surface is new; future versions must preserve keys or add with defaults.

## 7. Security, Privacy, Compliance
- Read‑only design: no file writes, minimizing risk.
- Path handling: restrict reads to `directive/**`; normalize and refuse paths outside root.
- No secrets processed; never include environment variables or tokens in responses.

## 8. Observability & Operations
- Logs: tool/resource calls, selected template, byte sizes, errors (no content logging).
- Metrics: call counts, latency, error rates, average payload size.
- Runbook: if tools fail due to missing files, run `uvx directive update`.

## 9. Rollout & Migration
- Phase 1: CLI (`init`, `update`) + MCP tools/resources local.
- Phase 2: optional IDE helper to auto‑start server; no behavior change.
- Revert: stop server; the repo remains with `directive/` files only.

## 10. Test Strategy & Spec Coverage (TDD)
- Unit: resource listing and file.get path scoping; template selection; Primer generation.
- Contract: golden tests assert `spec.template()/impact.template()/tdr.template()` return exact file bytes (no summarization) and include required keys.
- Negative: missing templates; empty `directive/`; long files still returned.
- CI: run unit/contract tests; lint/format; Python 3.13 via `uv`.

Spec→Test mapping
- AC: "Agent can discover Directive resources and fetch full contents ..." → contract tests for each tool.
- AC: "Bundle includes full AOP, Agent Context, template, and Primer" → golden fixture assertions.
- AC: "Helpful error when template missing" → negative test asserting error shape/message.

## 11. Risks & Open Questions
- Risk: response size growth → monitor; consider streaming later if needed.
- Risk: client MCP support variance → document minimal client versions; provide CLI fallback to print bundle.
- Open: Primer wording stability → source directly from AOP, keep short; allow teams to customize later.

## 12. Milestones / Plan (post‑approval)
1) Package data: include default templates/docs in wheel (DoD: files available via pkg resources).  
2) CLI: `init`, `update`, `mcp serve` (DoD: commands work end‑to‑end; non‑destructive by default).  
3) MCP resources: `directive.files.list`, `directive.file.get` (DoD: path scoping, tests).  
4) MCP tools: `spec.template`, `impact.template`, `tdr.template` (DoD: exact bytes return, Primer included).  
5) Tests + CI: unit/contract; `uv` workflow (DoD: green CI).  

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
