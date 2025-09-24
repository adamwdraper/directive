# Spec (per PR)

**Feature name**: MCP Auto‑Start for Cursor
**One-line summary**: Ensure the `Directive` MCP server auto‑starts in Cursor by setting `autoStart: true` in `.cursor/mcp.json`.

---

## Problem
Today, the MCP server must be started manually, adding friction each time the workspace opens. This slows feedback loops and causes confusion when the assistant cannot access the server context until it is started.

## Goal
Make the MCP server available immediately when the workspace opens in Cursor by enabling auto‑start in the project’s `.cursor/mcp.json`.

## Success Criteria
- [ ] Opening the repository in Cursor starts the `Directive` MCP server automatically
- [ ] No manual start action is required in typical workflows
- [ ] No behavior changes outside of MCP startup

## User Story
As a developer using Cursor with the Directive MCP server, I want the server to start automatically when I open the project so I can use MCP capabilities without manual setup.

## Flow / States
- Happy path: Open project in Cursor → MCP server `Directive` auto‑starts via config → assistant can call tools immediately.
- Edge case: If the server fails to start (e.g., missing environment), Cursor shows an error; logs indicate the failure and next steps.

## UX Links
- N/A

## Requirements
- Must add `"autoStart": true` to the `Directive` server entry in `.cursor/mcp.json` under `mcpServers`.
- Must not change command, args, or transport for the existing server entry.
- Must maintain JSON structure and formatting.

## Acceptance Criteria
- Given the repo is opened in Cursor, when `.cursor/mcp.json` contains `autoStart: true` for `Directive`, then the MCP server starts automatically without manual action.
- Negative: Given a typo such as `autoRestart`, when the repo is opened, then the server does not auto‑start (ensuring we used the correct key `autoStart`).

## Non-Goals
- Introducing new servers, transports, or arguments.
- Changing global user settings (only the repo’s `.cursor/mcp.json` is updated).


