from pathlib import Path
import json
import subprocess
import sys
import os


def _run_cli(args, cwd: Path):
    cmd = [sys.executable, "-m", "directive.cli"] + args
    # Ensure child process can import from src/
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (str(src_dir) + (os.pathsep + existing if existing else ""))
    return subprocess.run(cmd, cwd=str(cwd), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_cli_init_and_bundle_outputs_json(tmp_path: Path, monkeypatch):
    # Create an empty repo dir and run init
    res = _run_cli(["init"], tmp_path)
    assert res.returncode == 0
    # Ensure files created
    assert (tmp_path / "directive" / "reference" / "agent_operating_procedure.md").exists()
    assert (tmp_path / "directive" / "reference" / "agent_context.md").exists()
    assert (tmp_path / "directive" / "reference" / "templates" / "spec_template.md").exists()
    # Ensure Cursor launcher and mcp.json created
    assert (tmp_path / ".cursor" / "servers" / "directive.sh").exists()
    assert (tmp_path / ".cursor" / "mcp.json").exists()

    # Now run bundle and parse JSON
    res2 = _run_cli(["bundle", "spec_template.md"], tmp_path)
    assert res2.returncode == 0
    data = json.loads(res2.stdout)
    assert data["template"]["path"].endswith("spec_template.md")


def test_cli_init_creates_rule_noninteractive(tmp_path: Path):
    # Non-interactive default is Yes; should create the core rule
    res = _run_cli(["init"], tmp_path)
    assert res.returncode == 0
    assert (tmp_path / ".cursor" / "rules" / "directive-core-protocol.mdc").exists()


def test_cli_init_decline_skips_cursor_setup(tmp_path: Path, monkeypatch):
    # Call cmd_init directly with a TTY and input('n') to decline
    from directive import cli as dcli  # type: ignore

    class Args:
        verbose = False

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    rc = dcli.cmd_init(Args())
    assert rc == 0
    # .cursor directory should not be created when declined
    assert not (tmp_path / ".cursor").exists()


def test_cli_init_second_run_verbose_skips(tmp_path: Path):
    # First run creates files
    res1 = _run_cli(["init"], tmp_path)
    assert res1.returncode == 0
    # Second run with --verbose should print skip messages
    res2 = _run_cli(["--verbose", "init"], tmp_path)
    assert res2.returncode == 0
    out = res2.stdout
    assert "skip existing:" in out


