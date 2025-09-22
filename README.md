# Directive: Spec‑first approach to working with AI coding agents

Write specs, not chats.

A spec‑first approach to increase coding agent accuracy and developer efficiency. It replaces ad‑hoc back‑and‑forth with concise, versioned specs that become the canonical history of your work.

Problems this aims to solve:
- **Improving agent accuracy and developer efficiency**: Clear specs reduce ambiguity and rework, speed up iterations, and align expectations between humans and agents.
- **Replacing chatty back‑and‑forth with upfront, versioned specs**: Author concise specs first to avoid prompt drift; keep a single source of truth that onboards collaborators quickly.
- **Specs as durable, reviewable artifacts and canonical history**: Spec → Impact → TDR live in the repo, capturing decisions and enabling traceability; Spec→Test mapping turns requirements into verification.

How it works (brief): Work is gated by explicit review checkpoints — **Spec → Impact → TDR** — with no code before approval. After approval, follow strict TDD with Spec→Test mapping. Everything lives in‑repo and is exposed via a tiny MCP server for IDEs like Cursor. See the supporting background in [Research & Rationale](#research--rationale).

## Quickstart (CLI + MCP)

- Install (using uv):
  - In a project: `uv add directive` (adds to `pyproject.toml` and `uv.lock`)
- Initialize defaults in your repo:
  - `uv run directive init` (non-destructive; creates `directive/` with AOP, Context, and templates)
- Configure your MCP-aware IDE/agent to launch the server:
  - Command: `uv run directive mcp serve` (stdio)
  - Tools are auto-discovered via `tools/list`; the agent will fetch Spec/Impact/TDR templates and context automatically.
- (Optional) Inspect a bundle directly:
  - `uv run directive bundle spec_template.md` (prints a JSON bundle to stdout)

### Exposed tools (discovered automatically)
- `directive/templates.spec`: Spec bundle (AOP, Agent Context, Spec template, Primer)
- `directive/templates.impact`: Impact bundle
- `directive/templates.tdr`: TDR bundle
- `directive/files.get`: Read a file under `directive/` by path
- `directive/files.list`: List files under `directive/`

### Using with Cursor (MCP)
1. Ensure your project has Directive installed and initialized:
   - `uv add directive`
   - `uv run directive init`
2. MCP config for Cursor (auto‑created by `directive init` if missing):
   - `uv run directive init` will create `.cursor/mcp.json` and `.cursor/servers/directive.sh` if they don't exist.
   - If you already have `.cursor/mcp.json`, copy/merge the following JSON into your existing file:

```
{
  "mcpServers": {
    "Directive": {
      "type": "stdio",
      "command": "/usr/bin/env",
      "args": ["-S", "uv", "run", "-q", "-m", "directive.cli", "mcp", "serve"],
      "transport": "stdio"
    }
  }
}
```

3. Commit the file (`git add .cursor/mcp.json && git commit -m "docs: add Cursor MCP config"`).
4. Reload Cursor (or Reload Window). Cursor will start/stop the server per workspace automatically.
5. Sanity check in this workspace:
   - Open an AI chat and ask: "Create a new spec"
   - You should see tools discovered and the Spec template bundle used
6. Troubleshooting:
   - Ensure `uv` is on your PATH (e.g., `uv --version`)
   - Confirm the command runs locally: `uv run directive mcp serve` (it is a quiet stdio server)

## Workflow

Use this flow whenever you ask an agent to write code.

Step 1 — Spec (collaborative, behavior/UX‑only)
- If your agent supports MCP: ensure the server is configured to run; the agent will fetch AOP, Agent Context, and the Spec template automatically.
- Or include manually: include the single directory `/directive/reference/` in context (it contains AOP, Agent Context, and templates).
- Copy/paste prompt:
```
Create /directive/specs/<feature>/ (if missing) and scaffold /directive/specs/<feature>/spec.md from the Spec template. Collaborate with me to draft the Spec: behavior/UX only, clear acceptance criteria, and include UX links. Ask questions until unambiguous.
```

Step 2 — Impact Analysis (approve before TDR)
- If your agent supports MCP: ensure the server is configured to run; the agent will fetch AOP, Agent Context, and the Impact template automatically (include your authored Spec as well).
- Or include manually: include the single directory `/directive/reference/` plus your authored Spec (`/directive/specs/<feature>/spec.md`).
- Copy/paste prompt:
```
Produce /directive/specs/<feature>/impact.md using the Impact template. Call out touched modules, contract changes (APIs/events/schemas/migrations), risks, and observability needs. Keep it concise and actionable.
```

Step 3 — Technical Design Review (TDR) (approve before coding)
- If your agent supports MCP: ensure the server is configured to run; the agent will fetch AOP, Agent Context, and the TDR template automatically (include your authored Spec and Impact as well).
- Or include manually: include the single directory `/directive/reference/` plus your authored Spec and Impact.
- Copy/paste prompt:
```
Draft /directive/specs/<feature>/tdr.md using the TDR template. Be decisive about interfaces and behavior. Include Codebase Map (brief), data contracts, error handling, observability, rollout, and Spec→Test mapping. Wait for my approval before coding.
```

Step 4 — Coding via TDD (after TDR approval)
- Include in context:
  - `/directive/specs/<feature>/spec.md`, `/directive/specs/<feature>/impact.md`, `/directive/specs/<feature>/tdr.md`
  - `/directive/agent_operating_procedure.md`, `/directive/agent_context.md`
- Copy/paste prompt:
```
Implement via TDD: write a failing test per Spec acceptance criterion (mapped in the TDR), confirm failure, implement the minimal change, and refactor. Follow agent_context.md conventions (tooling, lint, types, security). Keep CI green.
```

Gates: Spec → Impact → TDR → TDD (no code before TDR approval).
 
## Research & Rationale

This framework is grounded in current best practices for **spec‑driven development** with AI coding agents. Below is a distilled summary of the sources we align to and the principles that inform the workflow.

---

### Key Practices from the Field

### 1. Make the Spec the Source of Truth
- Specs live in the repo, not in ephemeral chats.  
- They drive planning, tasks, and validation.  
- GitHub’s **Spec Kit** formalizes this into a 4-phase loop: **Specify → Plan → Tasks → Implement**.  
- Specs aren’t static — they are executable artifacts that evolve with the codebase.  
🔗 [Spec Kit (GitHub Blog)](https://github.blog/news-insights/product-news/spec-kit/)

---

### 2. Separate the Stable “What” from the Flexible “How”
- Capture **what** the system must do in product terms (user outcomes, interfaces, acceptance criteria).  
- Keep **how** it is built flexible and expressed later in technical design docs.  
- Example: Kiro’s approach outputs `requirements.md`, `design.md`, and `tasks.md` separately.  
🔗 [Kiro: Spec-First Development](https://kirorun.notion.site/Kiro-Spec-First-Development-Docs)

---

### 3. Tie Every Requirement to a Test (“Executable Specs”)
- Every spec clause must map to a test, often written in **Given–When–Then** (BDD style).  
- Track **spec coverage** (all spec items tested) in addition to code coverage.  
- This ensures agents are judged against explicit requirements, not guesses.  
🔗 [Executable Specifications & BDD (Cucumber)](https://cucumber.io/docs/bdd/)

---

### 4. Use the Agent to Draft the Spec, Humans to Edit
- Approaches like **“Vibe Specs”** let the LLM propose the first draft through Q&A.  
- Humans then critique, clarify, and cut scope creep.  
- The refined spec becomes the north star for implementation.  
🔗 [Vibe Spec Method](https://vibespec.org/)

---

### 5. Practice “Context Engineering,” Not Just Prompting
- Agents perform better when given **durable, file-based context packs**:  
  - Rules/conventions  
  - Example code patterns  
  - Data contracts and schemas  
  - Documentation links  
- Repos that include a **global rules file** plus examples see much higher fidelity.  
🔗 [Context Engineering (GitHub Copilot best practices)](https://github.blog/ai-and-ml/context-engineering-for-agents/)

---

### 6. Choose Method by Risk/Complexity; Enforce Verification
- For low-risk features: lightweight specs may suffice.  
- For high-risk or complex builds: follow **Spec-Then-Code**, with rigorous review gates.  
- Use **multi-AI cross-review** or human checkpoints where the blast radius is large.  
🔗 [Spec-Then-Code Methodology](https://www.spec.dev/spec-then-code)

---

### 7. Industry is Moving Toward Templates
- Beyond open-source tools, groups like **TM Forum** have published formal **AI Agent Specification Templates** for enterprise contexts.  
- Standardization is arriving, which signals the importance of shared spec formats.  
🔗 [TM Forum AI Agent Specification Template](https://www.tmforum.org/)

---

### 8. A Pragmatic Solo/Dev Flow Works Today
- A repeatable loop many developers use:  
  1. Brainstorm a spec  
  2. Generate a step-by-step plan  
  3. Execute with a codegen agent in **small, testable chunks**  
  4. Keep artifacts checked into the repo (`spec.md`, `prompt_plan.md`, `todo.md`).  
🔗 [Solo Dev Spec Loop (Indie Hackers)](https://www.indiehackers.com/post/spec-driven-ai-development)

---

### Takeaway
- Specs must be **concise, testable, and versioned**.  
- AI agents thrive when specs are paired with **context packs** and a **TDD-first workflow**.  
- The winning approach is not over-specifying implementation, but rigorously specifying **outcomes, contracts, and tests**.


