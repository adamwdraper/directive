# Spec (per PR)

**Feature name**: Cursor Project Rules scaffolding and init prompts  
**One-line summary**: Scaffold a single `.cursor/rules/*.mdc` project rule and update `directive init` to ask a single question to add recommended Cursor MCP server config and Project Rules (default yes).

---

## Problem
Agents and collaborators can miss Directive’s AOP and Context unless they manually configure Cursor Rules. Also, `directive init` does not currently offer a guided setup for Cursor’s MCP server and Project Rules.

## Goal
Running `directive init` should optionally scaffold recommended Cursor Project Rules and add the project’s MCP server config. The CLI should ask one combined question that defaults to yes and never overwrite existing files.

## Success Criteria
- [ ] New projects: running `directive init` creates `.cursor/` with `mcp.json` (if accepted) and `.cursor/rules/directive-core-protocol.mdc` (if accepted), with clear console messages.
- [ ] Existing projects: no existing file is overwritten; the CLI reports skips and paths.
- [ ] The single prompt defaults to yes; pressing enter accepts.
- [ ] The rule content aligns with Directive’s AOP and Agent Context and references repo templates.

## User Story
As a developer, I want `directive init` to set up Cursor’s MCP server and a recommended Project Rule so that the agent consistently follows Directive’s protocol without manual steps.

## Flow / States
- Happy path: In a fresh repo, run `uv run directive init` → accept the combined prompt → `.cursor/mcp.json` and `.cursor/rules/directive-core-protocol.mdc` are created with explanations in stdout.
- Edge case: In an existing repo with `.cursor/mcp.json` or the rule present, init does not overwrite and reports which files were skipped.

## UX Links
- N/A (CLI-only)

## Requirements
- Must prompt once: “Add recommended Cursor setup (MCP server config + Project Rule)? (Y/n)”.
- Must default the combined prompt to Yes on enter.
- Must be non-destructive: never overwrite without explicit confirmation (initial version: always skip if exists).
- Must write human-readable messages indicating created vs skipped files and their paths.
- Must place the rule in `.cursor/rules/` as `directive-core-protocol.mdc` using MDC metadata (`description`, `alwaysApply: true`).
- The rule must reference existing Directive docs within its body: `@directive/reference/agent_operating_procedure.md`, `@directive/reference/agent_context.md`, and templates under `@directive/reference/templates/`.
- Implementation must copy pre-authored Cursor templates from packaged data (e.g., `directive/data/directive/cursor/**`) rather than hardcoded strings in the CLI.
- The combined prompt controls both actions together (no partial selection in this version).

## Acceptance Criteria
- Given a new project, when I run `directive init` and accept defaults, then `.cursor/mcp.json` and `.cursor/rules/directive-core-protocol.mdc` exist.
- Given an existing `.cursor/mcp.json`, when I run `directive init` and accept, then the file is not overwritten and I see a “skipped (already exists)” message.
- Given the rule file already exists, when I run `directive init` and accept, then the rule is not overwritten and I see a “skipped (already exists)” message.
- Given I answer “n” to the combined prompt, when I run `directive init`, then no `.cursor/mcp.json` and no `.cursor/rules/directive-core-protocol.mdc` are created.
- Negative case: If `.cursor/` cannot be created (permissions), the CLI prints a clear error and exits non-zero.

## Non-Goals
- Managing per-user (global) Cursor Rules.
- Introducing a JSON-based Rules config (only `.mdc` is in scope).
