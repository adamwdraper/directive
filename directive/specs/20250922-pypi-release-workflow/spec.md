# Spec (per PR)

**Feature name**: PyPI Release Workflow & Versioning Script  
**One-line summary**: Add a release process with a console script to bump semantic versions and create release branches, plus a GitHub Actions workflow that builds and publishes to PyPI when release branches are merged.

---

## Problem
Releases are currently manual and error-prone. There is no standardized way to bump versions, create release branches, or automatically publish to PyPI upon merging a release. This slows down delivery, increases mistakes, and makes provenance unclear.

## Goal
Provide a simple, reproducible release process:
- A console script developers can run locally to bump version (major/minor/patch) in `pyproject.toml`, create a labeled release branch, and push it.
- A GitHub Actions workflow that builds the distribution, verifies it, and publishes to PyPI when a release branch is merged into `main`.

## Success Criteria
- [ ] Running a single command (e.g., `uv run directive-release minor`) updates `pyproject.toml`, commits, and pushes `release/vX.Y.Z`  
- [ ] Only merging a `release/*` branch into `main` triggers publishing to PyPI  
- [ ] Publishing uses `PYPI_API_TOKEN` secret (no plaintext credentials in repo)  

## User Story
As a maintainer, I want a reliable release workflow with semantic versioning so that I can publish new versions to PyPI safely and quickly.

## Flow / States
- Happy path:
  1) Maintainer runs console script with bump type: `major | minor | patch`.
  2) Script parses current version in `pyproject.toml` (currently `0.0.2`), computes next version (true SemVer even <1.0.0), updates file, commits with message `chore(release): vX.Y.Z`, creates `release/vX.Y.Z` branch, and pushes it.
  3) PR from `release/vX.Y.Z` to `main` is reviewed and merged (any merge strategy permitted).
  4) On merge to `main` from a `release/*` branch, GitHub Actions builds wheel/sdist, checks metadata, and publishes to PyPI using `PYPI_API_TOKEN`.
- Edge case:
  - If the version in `pyproject.toml` already equals the intended next version, the script aborts with a clear message and no commit.

## UX Links
- N/A

## Requirements
- Must provide a console script `directive-release` with a single arg: `major|minor|patch`.
- Must update `project.version` in `pyproject.toml` and no other files.
- Must create and push a branch labeled as a release branch, defaulting to `release/vX.Y.Z`.
- Must not create git tags locally; CI may handle tagging post-publish (see open question).
- Must include a GitHub Actions workflow that:
  - Triggers on `push` to `main` only.
  - Guards execution by confirming the pushed commit merges a PR whose head branch starts with a release label (e.g., `release/`). Implementation detail: query associated PRs for the commit via GitHub API and verify `head.ref` prefix.
  - Builds with `hatchling` per project setup and validates the dist with `twine check`.
  - Publishes to PyPI using `PYPI_API_TOKEN` secret.
- Must not publish on tag push or regular pushes to `main` that are not merges from a release branch.
- Must fail fast with clear logs on build or publish errors.

## Acceptance Criteria
- Given a repo on a clean `main`, when I run `directive-release patch`, then a new branch `release/v0.0.3` exists with `pyproject.toml` bumped to `0.0.3` and pushed to origin.
- Given a merged PR from `release/v0.0.3` into `main`, when the workflow completes on the merge commit, then `0.0.3` is available on PyPI under `directive`.
- Negative: Given the working tree is dirty, when I run the script, then it aborts with a message asking to commit or stash changes first.
- Negative: Given `pyproject.toml` version is malformed, when I run the script, then it exits non-zero with a helpful error.

## Non-Goals
- Automated changelog generation.
- Multi-branch release trains or backports.
- Signing artifacts beyond PyPI’s standard upload path.
- Rewriting historical tags.

## Open Questions
- Should CI create an annotated tag `vX.Y.Z` on `main` after a successful publish, or skip tagging entirely?
