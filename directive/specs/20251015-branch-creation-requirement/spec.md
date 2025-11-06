# Spec (per PR)

**Feature name**: Branch Creation Requirement and Implementation Summary in AOP  
**One-line summary**: Ensure all spec work happens on dedicated feature branches with tracked implementation summaries  

---

## Problem
The current Agent Operating Procedure has two gaps:

1. **No branch creation requirement**: The AOP doesn't explicitly require creating a new branch before starting work on a spec. This creates a risk that code changes could be made directly on the main branch, which violates standard Git workflow best practices and could lead to:
   - Uncommitted changes blocking branch switches
   - Accidental commits directly to main
   - Difficulty in code review and rollback
   - Unclear separation between different features being developed

2. **No implementation tracking**: There's no requirement to document what was actually implemented. Once coding begins, there's no living document that tracks:
   - Which files were modified/created/deleted
   - Key implementation decisions made during coding
   - Testing coverage added
   - Dependencies or migrations introduced
   
   This makes PR reviews harder and creates a gap between the TDR (design intent) and the actual implementation.

## Goal
The AOP should:
1. Explicitly require creating a new feature branch as the first step before beginning any spec work, ensuring all development happens in isolated branches that can be properly reviewed and merged via pull requests
2. Require creation of an implementation summary document (with template) that gets created when coding starts and updated throughout implementation, providing a clear record of what was actually built

## Success Criteria
- [ ] The AOP document clearly states that a new branch must be created before starting work
- [ ] The branch naming convention is specified (e.g., `feature/<spec-name>`)
- [ ] The branch creation step is positioned early in the workflow, before any code is written
- [ ] A new implementation summary template is created at `/directive/reference/templates/implementation_summary_template.md`
- [ ] The AOP requires creating an implementation summary when coding begins (Step 4)
- [ ] The AOP specifies that the implementation summary should be updated as work progresses
- [ ] The implementation summary is saved alongside other spec documents at `/directive/specs/<feature>/implementation_summary.md`

## User Story
As an agent following the AOP, I want clear instructions to create a new branch for each spec and maintain an implementation summary, so that I work in isolation, don't accidentally modify the main branch, and provide clear documentation of what was actually implemented for reviewers.

## Flow / States
**Happy path:**
1. Agent receives a new spec or starts work on an existing spec
2. Agent checks current branch (should be main initially)
3. Agent creates a new branch from main with naming convention `feature/<spec-name>`
4. Agent proceeds with the standard AOP workflow (impact analysis, TDR)
5. After TDR approval, when coding begins, agent creates `implementation_summary.md` in the spec folder
6. As agent writes code, agent updates the implementation summary with changes made
7. Before PR submission, agent ensures implementation summary is complete and accurate

**Edge case - Already on branch:**
1. Agent is already on a feature branch
2. Agent should verify they're on the correct branch for the current spec, or return to main and create the appropriate branch

**Edge case - Implementation changes direction:**
1. During coding, implementation differs from TDR
2. Agent updates both the TDR (with rationale for changes) and the implementation summary (with actual changes made)

## UX Links
N/A - This is a process documentation change

## Requirements
- Must add a branch creation step to the AOP
- Must specify branch naming convention (`feature/<spec-name>`)
- Must position branch creation before any code modifications
- Must create an implementation summary template
- Must add implementation summary creation to Step 4 (TDD Execution) in the AOP
- Must specify that implementation summary should be updated as work progresses
- Must specify that implementation summary should be accurate before PR merge
- Must not conflict with existing AOP workflow steps

## Acceptance Criteria

### Branch Creation
- Given an agent starting work on a new spec, when they read the AOP, then they see an explicit instruction to create a new feature branch before proceeding
- Given an agent following the AOP, when they reach the implementation phase (Step 4), then they are already on a feature branch, not main
- Given the branch naming convention, when an agent creates a branch, then it follows the format `feature/<spec-name>` where `<spec-name>` matches the spec folder name

### Implementation Summary
- Given an agent beginning implementation (Step 4), when they start coding, then they first create `/directive/specs/<feature>/implementation_summary.md` using the implementation summary template
- Given an agent making code changes, when they complete a meaningful unit of work (e.g., a test passing, a feature implemented), then they update the implementation summary with the changes
- Given an agent completing implementation, when they prepare to submit a PR, then the implementation summary accurately reflects all files changed, decisions made, tests added, and dependencies modified
- Given a reviewer reading the PR, when they check the spec folder, then they find an implementation summary that clearly documents what was actually built vs. what was designed in the TDR

## Non-Goals
- Automated enforcement of branch creation (could be a future enhancement)
- Automated enforcement of implementation summary updates (could be a future enhancement)
- Changes to the existing step numbering or major restructuring of the AOP
- Branch protection rules or Git configuration (those are repository settings, not AOP content)
- Detailed code-level documentation (that belongs in code comments and docstrings, not the implementation summary)

