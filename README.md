# Directive: Spec‑first approach to working with AI coding agents

A lightweight, implementation‑agnostic workflow for building software with AI coding agents.  
It separates **product intent** (Spec) from **engineering constraints** (Agent Context) and enforces an **analyze → design → TDD** loop.

## Workflow

Use this flow whenever you ask an agent to write code.

Step 1 — Spec (collaborative, behavior/UX‑only)
- Include in context:
  - `/docs/agent_operating_procedure.md`
  - `/docs/agent_context.md`
  - `/docs/templates/spec_template.md`
- Copy/paste prompt:
```
Create /specs/<feature>/ (if missing) and scaffold /specs/<feature>/spec.md from the Spec template. Collaborate with me to draft the Spec: behavior/UX only, clear acceptance criteria, and include UX links. Ask questions until unambiguous.
```

Step 2 — Impact Analysis (approve before TDR)
- Include in context:
  - `/specs/<feature>/spec.md`
  - `/docs/agent_operating_procedure.md`
  - `/docs/agent_context.md`
  - `/docs/templates/impact_template.md`
- Copy/paste prompt:
```
Produce /specs/<feature>/impact.md using the Impact template. Call out touched modules, contract changes (APIs/events/schemas/migrations), risks, and observability needs. Keep it concise and actionable.
```

Step 3 — Technical Design Review (TDR) (approve before coding)
- Include in context:
  - `/specs/<feature>/spec.md`
  - `/specs/<feature>/impact.md`
  - `/docs/agent_operating_procedure.md`
  - `/docs/agent_context.md`
  - `/docs/templates/tdr_template.md`
- Copy/paste prompt:
```
Draft /specs/<feature>/tdr.md using the TDR template. Be decisive about interfaces and behavior. Include Codebase Map (brief), data contracts, error handling, observability, rollout, and Spec→Test mapping. Wait for my approval before coding.
```

Step 4 — Coding via TDD (after TDR approval)
- Include in context:
  - `/specs/<feature>/spec.md`, `/specs/<feature>/impact.md`, `/specs/<feature>/tdr.md`
  - `/docs/agent_operating_procedure.md`, `/docs/agent_context.md`
- Copy/paste prompt:
```
Implement via TDD: write a failing test per Spec acceptance criterion (mapped in the TDR), confirm failure, implement the minimal change, and refactor. Follow agent_context.md conventions (tooling, lint, types, security). Keep CI green.
```

Gates: Spec → Impact → TDR → TDD (no code before TDR approval).

## Repository Layout
```
spec-first-agent-kit/
├─ README.md
├─ specs/
│  ├─ <feature>/
│  │  ├─ spec.md                           # filled from template (behavior/UX only)
│  │  ├─ impact.md                         # agent-produced impact analysis
│  │  └─ tdr.md                            # agent-produced TDR (approved before coding)
│  └─ examples/
│     └─ reset-password/
│        ├─ spec.md
│        ├─ impact.md
│        └─ tdr.md
├─ docs/
│  ├─ agent_context.md                     # persistent stack, TDD rules, conventions
│  ├─ agent_operating_procedure.md         # step-by-step workflow (AOP)
│  └─ templates/
│     ├─ spec_template.md
│     ├─ impact_template.md
│     └─ tdr_template.md
└─ .github/
   └─ pull_request_template.md             # reviewer checklist
```

 
