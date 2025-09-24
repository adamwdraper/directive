# Impact Analysis — Release Script Base-Branch Update

## Modules/packages likely touched
- `src/directive/release.py` (script flow and arguments)

## Contracts to update (APIs, events, schemas, migrations)
- CLI: new optional flag `--base-branch` (alias `-b`).

## Risks
- Git state errors if local base diverges (non-FF); script now exits early and prints guidance.  
- Network/remote availability needed for fetch/pull.

## Observability needs
- Script output should clearly state: selected base branch, whether it was fast-forwarded, and next steps on failure.
