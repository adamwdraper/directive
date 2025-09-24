# Technical Design Review (TDR) — Release Script Base-Branch Update

**Author**: <agent or engineer>  
**Date**: <YYYY-MM-DD>  
**Links**: Spec (`/directive/specs/release-script-base-branch/spec.md`), Impact (`/directive/specs/release-script-base-branch/impact.md`)

---

## 1. Summary
Update the release script to ensure it cuts release branches from an up-to-date base by checking out the base branch and fast-forwarding to origin. Add a `--base-branch` flag.

## 2. Decision Drivers & Non‑Goals
- Drivers: correctness of release content; less human error.  
- Non‑Goals: automatic rebases/merges; changing versioning or CI triggers.

## 3. Current State — Codebase Map (concise)
- `src/directive/release.py`: bumps version, creates `release/vX.Y.Z`, pushes, opens PR; no base update.

## 4. Proposed Design (high level, implementation‑agnostic)
- Add `update_base_branch(base)`:
  - `git fetch origin --prune`
  - `git checkout <base>` (create local from `origin/<base>` if missing)
  - `git pull --ff-only origin <base>`
- Insert before writing `pyproject.toml`.
- CLI: add `--base-branch/-b` with default `main`.

## 5. Alternatives Considered
- Rebase local base automatically — risk of conflicts and unexpected history; rejected.  
- Only warn if out-of-date — still error-prone; rejected.

## 6. Data Model & Contract Changes
- CLI option addition only.

## 7. Security, Privacy, Compliance
- No new secrets. Uses existing git remote; safe operations.

## 8. Observability & Operations
- Print base branch and progress messages; rely on git exit codes for failures.

## 9. Rollout & Migration
- Single script change; immediate effect after release.

## 10. Test Strategy & Spec Coverage (TDD)
- Unit: command assembly may be mocked; ensure function ordering (update before bump).  
- Integration (manual): run on a repo with outdated local main to observe ff-only behavior.

## 11. Risks & Open Questions
- Risk: local changes on base block ff-only; acceptable — user must reconcile first.  
- Open: add environment flag to skip base update for advanced workflows?

## 12. Milestones / Plan (post‑approval)
1) Implement `update_base_branch` + CLI flag.  
2) Merge and validate on next release cut.  
3) Optionally add skip flag if requested.

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
