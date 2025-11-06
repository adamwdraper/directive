# Technical Design Review (TDR) — Cursor Project Rule and Combined Init Prompt

**Author**: agent  
**Date**: 2025-09-25  
**Links**: Spec (`/directive/specs/cursor-project-rules-and-init/spec.md`), Impact (`/directive/specs/cursor-project-rules-and-init/impact.md`)

---

## 1. Summary
Add a single combined CLI prompt to `directive init` that, if accepted (default Yes), scaffolds by copying pre-authored templates from packaged data:
- `.cursor/mcp.json` to autostart the Directive MCP server
- `.cursor/rules/directive-core-protocol.mdc` with always-on guidance aligning with AOP and Agent Context
- `.cursor/servers/directive.sh` launcher script
The operation is idempotent and non-destructive.

## 2. Decision Drivers & Non‑Goals
- Drivers: Reduce setup friction; ensure agents consistently follow Directive protocol in Cursor.
- Non‑Goals: Global user rules management; JSON-based rules config; partial selection between MCP and rules.

## 3. Current State — Codebase Map (concise)
- Key module: `src/directive/cli.py` provides the `init` command and scaffolding utilities.
- Existing data/resources: `directive/reference/agent_operating_procedure.md`, `directive/reference/agent_context.md`, templates under `directive/reference/templates/`.
- External contracts: Cursor expects project rules at `.cursor/rules/*.mdc` and MCP config at `.cursor/mcp.json`.

## 4. Proposed Design (high level, implementation‑agnostic)
- Add a single yes/no prompt (default Yes):
  - Text: “Add recommended Cursor setup (MCP server config + Project Rule)? (Y/n)”
- If accepted:
  - Ensure `.cursor/` and `.cursor/rules/` directories exist.
  - Copy packaged templates from `directive/data/directive/cursor/**` into `.cursor/` (skip-if-exists):
    - `mcp.json`
    - `servers/directive.sh`
    - `rules/directive-core-protocol.mdc`
- All file writes are skip-if-exists; print created vs skipped paths.
- If declined: do nothing and print a short message.

## 5. Alternatives Considered
- Separate prompts for MCP and Rules: more flexibility but more cognitive load; not chosen.
- Autogenerating multiple rules: overkill for first iteration; start with core rule only.
- Hardcoding file contents in CLI: less maintainable; prefer template files that are easier to edit and review.

## 6. Data Model & Contract Changes
- None. CLI UX only.

## 7. Security, Privacy, Compliance
- No secrets are written. MCP config uses commands/args only.
- No PII; no telemetry.

## 8. Observability & Operations
- N/A beyond clear CLI stdout messaging.

## 9. Rollout & Migration
- No migration needed. Safe to run multiple times.
- If users already have files, we skip and inform.

## 10. Test Strategy & Spec Coverage (TDD)
- Unit tests for `init` behavior:
  - Accept default (Yes): creates directories and files when absent.
  - Existing files: skips with messages, no overwrite.
  - Decline (No): creates nothing.
- Spec→Test mapping:
  - AC-1: New project creates both files → test_init_accept_creates_files
  - AC-2: Existing mcp.json skipped → test_init_skips_existing_mcp
  - AC-3: Existing rule skipped → test_init_skips_existing_rule
  - AC-4: Decline combined prompt → test_init_decline_creates_nothing
  - AC-5: Permission error → test_init_permissions_error

## 11. Risks & Open Questions
- Risk: Path differences on Windows vs Unix. Mitigation: use `pathlib` consistently.
- Open: Exact wording of the rule and prompt; confirm final copy during implementation.

## 12. Milestones / Plan (post‑approval)
- Add combined prompt to `init`; implement template copy; write tests.
- Verify non-destructive behavior; update README if needed.

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
