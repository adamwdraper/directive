## TDR — Package includes `src/directive` (CLI import fix)

### Design
Use Hatchling configuration to ensure Python modules under `src/directive` are included in the wheel while retaining packaged data. Keep console scripts unchanged.

Key configuration:
- `[tool.hatch.build.targets.wheel].packages = ["src/directive"]`
- `[tool.hatch.build].include = ["src/directive/**"]`

### Implementation Steps
1. Update `pyproject.toml` with the include settings above.
2. `uv build` to produce wheel/sdist.
3. Inspect wheel contents to verify `directive/cli.py` and peers are present.
4. Install into a clean env and validate runtime.

### Verification Steps
- Wheel inspection:
  - `python -c "import zipfile as z; f=z.ZipFile('dist/directive-*.whl'); print([n for n in f.namelist() if n.startswith('directive/')])"`
- Import check in fresh env:
  - `python -c "import importlib.util as iu; assert iu.find_spec('directive.cli')"`
- CLI smoke test in fresh repo:
  - `uv run directive init` → exit 0 and creates `directive/` and `.cursor/` artifacts.

### Spec → Test Mapping
- Spec: wheel contains `directive/cli.py` → Test: wheel listing includes `directive/cli.py`.
- Spec: `directive init` works in fresh env → Test: run command and assert files and exit code.
- Spec: no CLI behavior change → Sanity: existing tests still pass.

### Rollout / Versioning
- Patch release on merge (e.g., `0.0.6`).

### Backout
- Revert `pyproject.toml` changes; rebuild and republish.


