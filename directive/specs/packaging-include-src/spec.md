## Package wheel must include src modules (expose `directive.cli`)

### Problem
Installing the project as a package produced a wheel that contained only `directive/data/**` and omitted Python modules under `src/directive`. As a result, environments could install the package but fail to import `directive.cli`, causing `ModuleNotFoundError` when running `uv run directive init` or the console script.

### Goals
- Ensure built wheels include the full `directive` Python package: `__init__.py`, `cli.py`, `bundles.py`, `server.py`, `release.py`, plus packaged data under `directive/data/**`.
- Make `directive.cli` importable in fresh environments and runnable via both `uv run directive init` and `python -m directive.cli ...`.
- Keep entry points unchanged.

### Acceptance Criteria
- After `uv build`, the wheel contains at minimum:
  - `directive/__init__.py`
  - `directive/cli.py`
  - `directive/bundles.py`
  - `directive/server.py`
  - `directive/release.py`
  - `directive/data/directive/reference/**`
- In a clean project with `uv`:
  - `uv add directive` installs the package.
  - `uv run directive init` exits 0 and creates:
    - `directive/reference/agent_operating_procedure.md`
    - `directive/reference/agent_context.md`
    - `directive/reference/templates/{spec,impact,tdr}_template.md`
    - `.cursor/servers/directive.sh` and `.cursor/mcp.json`
- `python -c "import importlib.util as iu; assert iu.find_spec('directive.cli')"` succeeds in the target environment.
- No functional CLI behavior changes beyond successful import/run.

### Non-Goals
- Changing command names, arguments, or CLI behavior.
- Refactoring module contents beyond packaging configuration.


