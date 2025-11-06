# Impact Analysis — PyPI Release Workflow & Versioning Script

## Modules/packages likely touched
- `pyproject.toml` (update `project.version` via script)
- New console script entry point (e.g., `directive-release` in `project.scripts`)
- GitHub Actions workflows (new file under `.github/workflows/release.yml`)
- Optional helper module in `src/directive/` to implement version bump logic

## Contracts to update (APIs, events, schemas, migrations)
- CLI surface: new console script `directive-release` with arg `major|minor|patch`
- No public Python APIs changed; no schema/migration updates

## Risks
- Security:
  - Exposure of `PYPI_API_TOKEN` if misconfigured logs or echo occur in CI
  - Ensure `actions/checkout` fetch-depth and token scoping are minimal
- Performance/Availability:
  - CI runner time for building and publishing; negligible impact on repo users
- Data integrity:
  - Incorrect version bump leading to duplicate or skipped versions
  - Accidental publish if branch detection is incorrect

## Observability needs
- Logs:
  - Script: print planned next version, target branch, and guard on dirty tree
  - CI: log branch detection, build steps, `twine check` output, publish success
- Metrics:
  - Optional: count releases per period; CI duration for build/publish
- Alerts:
  - Optional: notify on CI failure for `release/*` merges (GitHub notifications sufficient for now)
