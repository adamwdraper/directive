# Spec (per PR)

**Feature name**: Release Script Base-Branch Update  
**One-line summary**: Ensure the release script checks out and fast-forwards the base branch before bumping; add `--base-branch` flag.

---

## Problem
Release branches could be cut from an out-of-date local branch, leading to stale releases or conflicts when merging.

## Goal
Automatically update the base branch (default `main`) before bumping the version and creating a release branch, and allow overriding the base via a flag.

## Success Criteria
- [ ] Running `directive-release patch` checks out `main` and fast-forwards to `origin/main` before changing files.  
- [ ] Passing `--base-branch foo` updates and cuts from `foo` instead.  

## User Story
As a maintainer, I want release branches cut from the latest base so that merges are clean and releases include the intended commits.

## Flow / States
- Script flow: validate clean tree → update base branch (checkout + `git pull --ff-only`) → read bump → write version → create `release/vX.Y.Z` → push → open PR.

## Requirements
- Must fetch and fast-forward only; fail if non-fast-forward required.  
- Must create a local base branch if missing, tracking `origin/<base>`.  
- Must default to `main` and accept `--base-branch`/`-b` override.

## Acceptance Criteria
- Given the local `main` is behind, when running `directive-release patch`, then the script fast-forwards `main` and proceeds.  
- Given no local `main`, when running the script, then it creates it tracking `origin/main` and proceeds.  
- Negative: Given a non-FF update is required, the script fails with a clear message.  

## Non-Goals
- Rebase/merge automation.  
- Changing versioning or branch naming.
