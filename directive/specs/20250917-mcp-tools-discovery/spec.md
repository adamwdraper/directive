# Spec (per PR)

**Feature name**: MCP tools discovery and descriptions for Directive  
**One-line summary**: Expose Directive’s read-only capabilities via MCP `tools/list` with clear titles/descriptions and route execution via `tools/call` so LLMs can reliably discover and use them.

---

## Problem
Agents currently can’t discover Directive’s tools because the server only exposes custom JSON-RPC methods (e.g., `spec.template`) and does not implement MCP `tools/list`. Without discovery metadata (name, title, description, input schema), clients can’t advertise our tools and LLMs can’t choose them confidently.

## Goal
- Implement MCP-compliant tool discovery for Directive so clients can list our tools and present meaningful descriptions.  
- Provide `tools/call` dispatch so discovered tool names can be executed without changing our internal logic.

## Success Criteria
- [ ] `tools/list` returns a stable set of tool descriptors with `name`, `title`, `description`, and `inputSchema` that accurately document usage.  
- [ ] `tools/call` executes the corresponding existing behavior and returns the same payloads currently produced by our custom methods.  
- [ ] Tool descriptions make it obvious when to use Spec/Impact/TDR bundles vs file listing/reading.

## User Story
As an AI coding agent connected to the Directive MCP server, I want a clear catalog of Directive tools with human-readable descriptions and input schemas so that I can confidently pick the right tool (e.g., Spec vs Impact vs TDR) and execute it with the correct arguments.

## Flow / States
Happy path:
1. Client initializes the Directive MCP server session.  
2. Client calls `tools/list` and caches the returned tool descriptors.  
3. When the user asks to draft a Spec, the LLM selects `directive/spec.template` and the client invokes `tools/call` with no arguments.  
4. The server returns a bundle containing AOP, Agent Context, the Spec template, and a concise Primer.  
5. Similar flow for Impact/TDR drafting; for direct reads, the LLM selects file tools.

## Requirements
- Implement `tools/list` (no params) returning descriptors for the following tools:
  - `directive/files.list`  
    - Title: "List Directive Files"  
    - Description: "List all files under the repository’s `directive/` directory (context and templates)."  
    - Input schema: `{ "type": "object", "additionalProperties": false, "properties": {} }`.
  - `directive/file.get`  
    - Title: "Read Directive File"  
    - Description: "Read a file under `directive/` by path and return its full contents verbatim."  
    - Input schema: `{ "type": "object", "additionalProperties": false, "properties": { "path": { "type": "string", "description": "Path under directive/ (e.g., directive/agent_context.md)" } }, "required": ["path"] }`.
  - `directive/spec.template`  
    - Title: "Spec Template Bundle"  
    - Description: "Return Agent Operating Procedure, Agent Context, and the Spec template, plus a concise Primer for drafting a new Spec."  
    - Input schema: `{ "type": "object", "additionalProperties": false, "properties": {} }`.
  - `directive/impact.template`  
    - Title: "Impact Template Bundle"  
    - Description: "Return Agent Operating Procedure, Agent Context, and the Impact template, plus a concise Primer for drafting an Impact analysis."  
    - Input schema: `{ "type": "object", "additionalProperties": false, "properties": {} }`.
  - `directive/tdr.template`  
    - Title: "TDR Template Bundle"  
    - Description: "Return Agent Operating Procedure, Agent Context, and the TDR template, plus a concise Primer for drafting a Technical Design Review."  
    - Input schema: `{ "type": "object", "additionalProperties": false, "properties": {} }`.

- Implement `tools/call` dispatching to existing logic without changing outputs:
  - `directive/files.list` → existing `list_directive_files()` with result `{ files: string[] }`.
  - `directive/file.get` → existing `read_directive_file()` with param validation, result `{ path, content }`.
  - `directive/spec.template` → existing `build_template_bundle('spec_template.md')`.
  - `directive/impact.template` → existing `build_template_bundle('impact_template.md')`.
  - `directive/tdr.template` → existing `build_template_bundle('tdr_template.md')`.

- Error handling:
  - Invalid tool name → MCP tool error with `name` not found.  
  - Validation errors (e.g., missing `path`) → MCP tool error with message and field hint.  
  - Missing files/templates → retain existing helpful messages (e.g., suggest `directive update`).

- Initialization:
  - During `initialize`, declare tools capability. If not implementing live updates, omit `listChanged` notifications for now.

- Non-breaking:
  - Preserve current custom method handlers for backwards compatibility for this release. MCP-aware clients should prefer `tools/list` + `tools/call`.

## Acceptance Criteria
- Given the server is running, when a client sends `tools/list`, then the response includes exactly five tools with the names specified above and each tool has `name`, `title`, `description`, and `inputSchema` fields.  
- Given `tools/list` response is cached, when the client sends `tools/call` with `name: "directive/spec.template"` and empty arguments, then the server returns a bundle whose fields match the current `build_template_bundle('spec_template.md')` output.  
- Given a `path` is provided to `directive/file.get` that exists under `directive/`, when the client sends `tools/call`, then the server returns `{ path, content }` where `content` matches the on-disk file verbatim.  
- Given `path` is missing or not a string for `directive/file.get`, when the client sends `tools/call`, then the server returns a tool error explaining the validation issue.  
- Given a required template file is missing, when the client calls a template bundle tool, then the server returns a helpful error that lists available templates and suggests running `directive update`.

## Non-Goals
- Implementing MCP `resources/*` in this change (may be added later as first-class resources).  
- Implementing live `notifications/tools/list_changed` (can be added when tool surface is dynamic).  
- Allowing any write operations (remains strictly read-only).
