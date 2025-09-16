from pathlib import Path
import json
import subprocess
import sys


def _run_cli(args, cwd: Path):
    cmd = [sys.executable, "-m", "directive.cli"] + args
    return subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_cli_init_and_bundle_outputs_json(tmp_path: Path, monkeypatch):
    # Create an empty repo dir and run init
    res = _run_cli(["init"], tmp_path)
    assert res.returncode == 0
    # Ensure files created
    assert (tmp_path / "directive" / "agent_operating_procedure.md").exists()
    assert (tmp_path / "directive" / "agent_context.md").exists()
    assert (tmp_path / "directive" / "templates" / "spec_template.md").exists()

    # Now run bundle and parse JSON
    res2 = _run_cli(["bundle", "spec_template.md"], tmp_path)
    assert res2.returncode == 0
    data = json.loads(res2.stdout)
    assert "primer" in data
    assert data["template"]["path"].endswith("spec_template.md")


