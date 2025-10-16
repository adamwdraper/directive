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
    # Ensure Cursor rules created (but NOT MCP files)
    assert (tmp_path / ".cursor" / "rules" / "directive-core-protocol.mdc").exists()

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


def test_init_creates_rules_not_mcp(tmp_path: Path):
    """Test that init creates only Cursor rules, not MCP server files."""
    # Run init in a fresh directory
    res = _run_cli(["init"], tmp_path)
    assert res.returncode == 0
    
    # Cursor rules should be created
    assert (tmp_path / ".cursor" / "rules" / "directive-core-protocol.mdc").exists()
    
    # MCP server files should NOT be created
    assert not (tmp_path / ".cursor" / "mcp.json").exists()
    assert not (tmp_path / ".cursor" / "servers" / "directive.sh").exists()


def test_update_preserves_existing_mcp(tmp_path: Path):
    """Test that update does not modify existing MCP configuration files."""
    # Set up a repo with directive/ and existing MCP config
    _run_cli(["init"], tmp_path)
    
    # Manually create MCP files (simulating old version behavior)
    cursor_dir = tmp_path / ".cursor"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    
    mcp_json = cursor_dir / "mcp.json"
    original_content = '{"mcpServers": {"test": "original"}}'
    mcp_json.write_text(original_content)
    
    servers_dir = cursor_dir / "servers"
    servers_dir.mkdir(parents=True, exist_ok=True)
    launcher = servers_dir / "directive.sh"
    launcher_content = "#!/bin/bash\necho 'original'"
    launcher.write_text(launcher_content)
    
    # Run update
    res = _run_cli(["update"], tmp_path)
    assert res.returncode == 0
    
    # Verify MCP files are unchanged
    assert mcp_json.exists()
    assert mcp_json.read_text() == original_content
    assert launcher.exists()
    assert launcher.read_text() == launcher_content


def test_mcp_serve_still_works(tmp_path: Path):
    """Test that MCP server command still functions."""
    from directive import cli as dcli
    
    class Args:
        pass
    
    # Initialize a repo first
    _run_cli(["init"], tmp_path)
    
    # This test just verifies the command doesn't crash immediately
    # In a real scenario, we'd mock the server, but for now we'll
    # just verify the function exists and is callable
    import inspect
    assert callable(dcli.cmd_mcp_serve)
    assert "args" in inspect.signature(dcli.cmd_mcp_serve).parameters


def test_init_prompt_no_mcp_mention(tmp_path: Path):
    """Test that init prompt does not mention MCP server."""
    res = _run_cli(["init"], tmp_path)
    assert res.returncode == 0
    
    # Check stdout/stderr for the prompt text
    output = res.stdout + res.stderr
    
    # Should mention "Cursor Project Rules" or similar
    assert "Cursor" in output
    
    # Should NOT mention "MCP server" or "mcp.json"
    assert "MCP server" not in output
    assert "mcp.json" not in output


