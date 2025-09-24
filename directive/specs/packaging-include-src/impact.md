## Impact Analysis — Package includes `src/directive`

### Summary
Adjust packaging so wheels include Python modules from `src/directive` in addition to existing data files. This resolves `ModuleNotFoundError: No module named 'directive.cli'` when installed.

### Code/Files Touched
- `pyproject.toml`
  - `[tool.hatch.build.targets.wheel].packages` → include `src/directive`
  - `[tool.hatch.build].include` → include `src/directive/**`

### Public Interfaces and Contracts
- CLI entry points remain the same (`directive = directive.cli:main`).
- No API or behavior changes; packaging/distribution only.

### Risks
- Over-inclusion: risk of bundling unintended files. Mitigation: limit include to `src/directive/**`.
- Build variation across environments. Mitigation: verify with `uv build` and inspect wheel contents.

### Observability / Verification
- CI step (local for now):
  - `uv build` and inspect wheel content for `directive/cli.py`.
  - Install into a fresh env via `uv pip install` and assert `find_spec('directive.cli')` is not `None`.
  - Smoke-run `uv run directive init` in a temp directory; expect exit code 0 and created files.

### Rollout
- Merge to `release/v0.0.5` and publish a patch release (e.g., `0.0.6`).

### Backout Plan
- Revert `pyproject.toml` changes and rebuild if any unexpected packaging fallout occurs.


