from pathlib import Path
import json
import re
import subprocess
import sys


def _read_pyproject(root: Path) -> str:
    return root.joinpath("pyproject.toml").read_text(encoding="utf-8")


def test_pyproject_scripts_and_sdist_include(tmp_path: Path):
    """Validate console_scripts and that sdist includes Python sources.

    This guards against publishing a package without directive/cli.py present.
    """
    repo_root = Path(__file__).resolve().parents[1]
    pyproject = _read_pyproject(repo_root)

    # Ensure console script points to directive.cli:main
    assert 'directive = "directive.cli:main"' in pyproject

    # Ensure sdist includes src/** so Python sources are shipped
    assert "[tool.hatch.build.targets.sdist]" in pyproject
    assert '"src/**"' in pyproject


def test_built_wheel_and_sdist_expose_cli(tmp_path: Path):
    """Build artifacts and verify directive.cli import and entrypoint works in venvs."""
    repo_root = Path(__file__).resolve().parents[1]

    # Build artifacts
    subprocess.run(["uv", "build"], cwd=str(repo_root), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    dist_dir = repo_root.joinpath("dist")
    wheels = sorted(dist_dir.glob("directive-*-py3-none-any.whl"))
    sdists = sorted(dist_dir.glob("directive-*.tar.gz"))
    assert wheels, "wheel not built"
    assert sdists, "sdist not built"

    wheel = wheels[-1]
    sdist = sdists[-1]

    # Test wheel
    venv_wheel = tmp_path / "venv-wheel"
    subprocess.run([sys.executable, "-m", "venv", str(venv_wheel)], check=True)
    pip_wheel = venv_wheel / "bin" / "pip"
    py_wheel = venv_wheel / "bin" / "python"
    cli_wheel = venv_wheel / "bin" / "directive"
    subprocess.run([str(pip_wheel), "install", "-q", str(wheel)], check=True)
    # import directive.cli and run --help
    subprocess.run([str(py_wheel), "-c", "import directive, directive.cli; print('ok')"], check=True)
    help_out = subprocess.run([str(cli_wheel), "--help"], check=True, stdout=subprocess.PIPE, text=True).stdout
    assert "Directive CLI" in help_out

    # Test sdist
    venv_sdist = tmp_path / "venv-sdist"
    subprocess.run([sys.executable, "-m", "venv", str(venv_sdist)], check=True)
    pip_sdist = venv_sdist / "bin" / "pip"
    py_sdist = venv_sdist / "bin" / "python"
    cli_sdist = venv_sdist / "bin" / "directive"
    subprocess.run([str(pip_sdist), "install", "-q", str(sdist)], check=True)
    subprocess.run([str(py_sdist), "-c", "import directive, directive.cli; print('ok')"], check=True)
    help_out2 = subprocess.run([str(cli_sdist), "--help"], check=True, stdout=subprocess.PIPE, text=True).stdout
    assert "Directive CLI" in help_out2


