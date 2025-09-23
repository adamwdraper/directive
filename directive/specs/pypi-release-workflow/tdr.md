# Technical Design Review (TDR) — PyPI Release Workflow & Versioning Script

**Author**: <agent or engineer>  
**Date**: <YYYY-MM-DD>  
**Links**: Spec (`/directive/specs/pypi-release-workflow/spec.md`), Impact (`/directive/specs/pypi-release-workflow/impact.md`)

---

## 1. Summary
Introduce a small, deterministic release process: a console script to bump semantic versions and create a labeled release branch, and a GitHub Actions workflow that builds and publishes the package to PyPI only when a release branch PR is merged into `main`. This removes manual steps, reduces mistakes, and makes releases auditable.

## 2. Decision Drivers & Non‑Goals
- Drivers: repeatable releases; minimal local setup; secure token handling; clear audit trail.  
- Non‑Goals: changelog automation; pre‑releases; OIDC trusted publishing (initially); tag‑triggered releases.

## 3. Current State — Codebase Map (concise)
- Packaging: `pyproject.toml` with `hatchling`, current version `0.0.2`.  
- CLI/Server: `src/directive/` contains server and CLI; no release tooling or CI publish workflow.  
- Tests: `tests/` for server/cli; none for release tooling.

## 4. Proposed Design (high level, implementation‑agnostic)
- Console Script `directive-release`  
  - Args: `major|minor|patch`.  
  - Steps: validate clean working tree → parse `pyproject.toml` version → bump → update file → commit `chore(release): vX.Y.Z` → create branch `release/vX.Y.Z` → push origin.  
  - Guard: abort if version malformed or duplicate.
- GitHub Action `.github/workflows/release.yml`  
  - Trigger: `push` to `main`.  
  - Gate: verify the push merges a PR whose head ref starts with `release/` (query associated PRs for commit; `head.ref` prefix check).  
  - Build: `python -m pip install build twine`, build sdist/wheel with hatchling, `twine check` dists.  
  - Publish: `twine upload -u __token__ -p ${{ secrets.PYPI_API_TOKEN }}`.  
  - Optional: create annotated tag after successful publish (open question).

## 5. Alternatives Considered
- Tag‑triggered release: simpler gating, but risk of accidental tag push; deferred.  
- OIDC Trusted Publishing: more secure long‑term, but setup overhead now; plan later.  
- Subcommand in existing CLI vs separate script: chose separate console script for simplicity and least coupling.

## 6. Data Model & Contract Changes
- Console script interface: `directive-release <major|minor|patch>`; no library API changes.  
- No data schemas or migrations.

## 7. Security, Privacy, Compliance
- Secrets: use `PYPI_API_TOKEN` GitHub secret; never echo the token.  
- Principle of least privilege: restrict token to publish only.  
- Logs: avoid printing environment; show only non‑sensitive build/publish summaries.

## 8. Observability & Operations
- Logs: branch detection decision; built artifacts list; `twine check` output; upload result.  
- Alerts: rely on GitHub PR checks/notifications for failures; optionally add status badge.

## 9. Rollout & Migration
- Add script and workflow in one PR; dry‑run publish step behind branch gating before first real release.  
- Revert plan: disable workflow or revert merge; no data migration.

## 10. Test Strategy & Spec Coverage (TDD)
- Unit tests: version parsing/bumping; dirty tree guard (mock git); branch naming; commit message.  
- Integration (CI): action condition tests via mocked event payload or dedicated script unit tests; skip actual publish in CI tests.  
- Spec→Test mapping:  
  - AC1: running script creates `release/vX.Y.Z` with bumped version → unit test with temp repo.  
  - AC2: merging `release/*` triggers publish → CI gate unit tested via helper function; manual verification on first live run.  
  - Negative: malformed version and dirty tree → error and non‑zero exit.

## 11. Risks & Open Questions
- Risk: false positives/negatives in branch detection → mitigate with explicit prefix check and commit→PR lookup.  
- Risk: duplicate publish if workflow re‑runs → mitigate by checking if version already on PyPI before upload.  
- Open: Should CI create an annotated tag `vX.Y.Z` after publish?  
- Open: Keep pre‑releases out of scope for now?

## 12. Milestones / Plan (post‑approval)
1) Implement `directive-release` script and tests (DoD: unit tests green).  
2) Add workflow with gating; dry‑run path (DoD: CI runs build and check, skip upload without release branch).  
3) First live release: set `PYPI_API_TOKEN`, run `patch` bump, merge PR, verify PyPI.  
4) Optional follow‑ups: adopt OIDC trusted publishing; add annotated tags; changelog automation.

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
