# Impact Analysis — Release Workflow Detection Fix

## Modules/packages likely touched
- `.github/workflows/release.yml` (triggers and gating logic)

## Contracts to update (APIs, events, schemas, migrations)
- CI contract: workflow now listens only to `pull_request: closed` for `main` with a head-ref prefix gate `release/`.

## Risks
- Data integrity:
  - Duplicate publish if re-run; twine upload should no-op on existing versions, but add guard if needed later.
- Reliability:
  - None expected; simplified trigger reduces false negatives.

## Observability needs
- Logs:
  - Default action logs (build, check, upload) are sufficient for this change.
- Alerts:
  - Rely on PR checks; optionally add a status badge.
