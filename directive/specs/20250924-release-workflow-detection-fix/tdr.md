# Technical Design Review (TDR) — Release Workflow Detection Fix

**Author**: <agent or engineer>  
**Date**: <YYYY-MM-DD>  
**Links**: Spec (`/directive/specs/release-workflow-detection-fix/spec.md`), Impact (`/directive/specs/release-workflow-detection-fix/impact.md`)

---

## 1. Summary
Make the PyPI release workflow reliably detect merges of `release/*` branches into `main` across all merge strategies using a single PR-closed trigger with a job-level gate.

## 2. Decision Drivers & Non‑Goals
- Drivers: reliability across squash/merge/rebase; minimal complexity.  
- Non‑Goals: push-to-main detection; manual dispatch; changing packaging/versioning.

## 3. Current State — Codebase Map (concise)
- `.github/workflows/release.yml` exists; previously attempted multiple triggers and detection heuristics.

## 4. Proposed Design (high level, implementation‑agnostic)
- Trigger on `pull_request: closed` for `main`.  
- Job-level `if`: `github.event.pull_request.merged == true && startsWith(github.event.pull_request.head.ref, 'release/')`.  
- Steps: checkout → setup Python → install build deps → build → twine check → twine upload.

## 5. Alternatives Considered
- Push-to-main commit→PR lookup and heuristics — more brittle and complex; rejected.  
- Manual dispatch — useful fallback, but unnecessary with reliable PR-closed trigger; omitted for simplicity.

## 6. Data Model & Contract Changes
- CI event contract only; no app data models.

## 7. Security, Privacy, Compliance
- Secrets: `PYPI_API_TOKEN` only; avoid echoing.  
- Permissions: read-only contents sufficient for build/upload; no extra scopes.

## 8. Observability & Operations
- Default logs sufficient; no additional metrics required for this change.

## 9. Rollout & Migration
- Single workflow edit; low blast radius.  
- Revert by restoring previous workflow version if needed.

## 10. Test Strategy & Spec Coverage (TDD)
- Validate by merging a `release/*` PR and confirm publish runs.  
- Negative: close PR without merge; job should not run.

## 11. Risks & Open Questions
- Risk: None significant; simplified logic is standard practice.  
- Open: Add preflight check to skip upload if version already exists on PyPI?

## 12. Milestones / Plan (post‑approval)
1) Replace workflow triggers and add job-level gate.  
2) Merge and validate on next release PR.  
3) Optionally add idempotency preflight in a follow-up.

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
