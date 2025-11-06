# Spec (per PR)

**Feature name**: MCP server and minimal CLI for Directive  
**One-line summary**: Enable agents to discover and use Directive via MCP, and enable humans to bootstrap/update `directive/` with a tiny CLI.  

---

## Problem
Today, users copy/paste prompts and manually manage context files. This is error‑prone and inconsistent across IDEs/agents. We need a frictionless way for any coding agent to: (a) read Directive guidance/templates from the repo, and (b) perform common actions (create spec, generate impact/tdr) without user shell steps.  

## Goal
Ship a minimal, file‑driven UX so that:  
1) An agent can say “create a new spec” and fetch the full AOP, Agent Context, and Spec template via MCP (read‑only) to guide drafting.  
2) A human can initialize or update `directive/` content with a single command, no manual file scaffolding.  

## Success Criteria
- [ ] Agent can discover Directive resources and fetch full contents of AOP, Agent Context, and the Spec/Impact/TDR templates via dedicated read‑only tools to guide drafting (without writing files).  
- [ ] CLI can initialize `directive/` in a repo that lacks it, without overwriting edited files by default.  
- [ ] All Directive artifacts live under `directive/` and are commit‑ready.  
- [ ] Zero copy/paste prompts required to start a new spec in supported IDEs/agents (via MCP).  

## User Story
As an engineer, I want to say “create a new spec” to my coding agent and have it fetch the right guidance and template, then help me draft behavior‑only content, so that I can move quickly without managing templates or paths.  

## Flow / States
Happy path:  
1. User: “Create a new spec called mcp-server-and-cli.”  
2. Agent calls `spec.template()` which returns AOP, Agent Context, and the Spec template (plus Primer), then proposes a behavior‑only draft.  
3. User saves/commits the spec via their usual workflow or CLI (agent does not write files).  
4. When ready, user requests Impact; agent fetches the Impact template and drafts collaboratively.  

Edge case (template missing):  
- Agent lists available templates; if none, informs the user to run CLI `init`/`update` to install defaults.  

## UX Links
- Designs: n/a  
- Prototype: n/a  
- Copy/Content: `directive/reference/agent_context.md`, `directive/reference/agent_operating_procedure.md`  

## Requirements
- Must be file‑driven and self‑contained under `directive/`.  
- Must provide an MCP resource surface so agents can read `directive/` files (context and templates).  
- Must provide three read‑only MCP tools that return full contents (no summarization) plus a Primer and resource paths:  
  - `spec.template()` → AOP + Agent Context + `spec_template.md`  
  - `impact.template()` → AOP + Agent Context + `impact_template.md`  
  - `tdr.template()` → AOP + Agent Context + `tdr_template.md`  
- Must include a short "Primer" string in every bundle response, derived from the AOP (e.g., “Do not write code before TDR approval. Follow Spec → Impact → TDR → TDD.”), to act as immediate guidance for the agent.  
- Must provide a minimal CLI with `init` and `update` (and `mcp serve` as an optional convenience) to help humans bootstrap/update `directive/`.  
- Must not require schemas or a state machine; gates can be inferred by file presence by the human/CI, not enforced here.  
- Must show helpful errors if required files are missing and suggest remedies.  

## Acceptance Criteria
- Given a repo without `directive/`, when a human runs “init” via the CLI, then a `directive/` directory is created with `reference/agent_context.md`, `reference/agent_operating_procedure.md`, `reference/templates/`, and an empty `specs/` folder, without overwriting existing files by default.  
- Given `directive/` exists, when an agent requests a spec drafting bundle (e.g., `context.bundle(template='spec_template.md')`), then the response includes the full contents of `directive/reference/agent_operating_procedure.md`, `directive/reference/agent_context.md`, and `directive/reference/templates/spec_template.md`, plus their paths.  
- Given `directive/reference/templates/spec_template.md` is present, when the agent calls `spec.template()`, then the returned template content matches the on‑disk file verbatim (no summarization).  
- Given `directive/reference/templates/impact_template.md` is present, when the agent calls `impact.template()`, then the returned template content matches the on‑disk file verbatim (no summarization).  
- Given `directive/reference/templates/tdr_template.md` is present, when the agent calls `tdr.template()`, then the returned template content matches the on‑disk file verbatim (no summarization).  
  
- Given a feature spec folder already exists, when the agent requests a bundle for the same feature, then the tool returns the same full docs and template without attempting any writes, and may include a helpful note that the spec path already exists.  
- Given the template file is missing, when the agent requests a bundle, then the tool returns a helpful error listing available templates and suggests running the CLI `update` to restore defaults.  
- Given the MCP server is running, when an agent queries available resources, then it can list and fetch files under `directive/` (context and templates).  

## Non-Goals
- Implementing Impact/TDR generation tools beyond creating the spec file (those will be separate follow‑up specs/PRs).  
- GitHub App or Checks integration.  
- Schema validation or policy engines.  
