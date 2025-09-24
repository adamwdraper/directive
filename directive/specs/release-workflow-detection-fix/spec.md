# Spec (per PR)

**Feature name**: Release Workflow Detection Fix  
**One-line summary**: Make PyPI release workflow reliably trigger on PR merges to main (including squash) using a simple PR-closed gate.

---

## Problem
The publish workflow didn’t consistently trigger after merging a `release/*` PR into `main`, particularly with squash merges. This causes missed releases and manual intervention.

## Goal
Ensure the release workflow reliably runs when a release branch PR is merged into `main`, regardless of merge strategy, using GitHub’s PR closed event and a clear head-branch prefix gate.

## Success Criteria
- [ ] Merging a `release/*` PR into `main` triggers the workflow every time (squash/merge/rebase).  
- [ ] No complex commit→PR lookups or heuristics required.  

## User Story
As a maintainer, I want the release workflow to run reliably after merging a release PR, so I don’t need to debug CI triggers or publish manually.

## Flow / States
- On PR closed event: if merged and `head.ref` starts with `release/`, publish.  

## Requirements
- Must trigger on `pull_request: closed` for `main`.  
- Must gate the job with `merged == true` and `startsWith(head.ref, 'release/')`.  
- Must keep publishing idempotent (no duplicate publishes).

## Acceptance Criteria
- Given a squash merge of `release/vX.Y.Z` into `main`, when the workflow runs, then it builds and publishes to PyPI.  
- Negative: Given a PR closed without merge, workflow does not publish.  

## Non-Goals
- Push-to-main detection.  
- Manual dispatch.  
- Changing packaging or versioning semantics.  
- Adding changelog automation or tags.
