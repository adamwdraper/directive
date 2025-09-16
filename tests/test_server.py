from pathlib import Path
import json
import subprocess
import sys


def _run_server_once(cwd: Path, request: dict) -> dict:
    # Launch the server and send a single JSON-RPC request over stdio
    proc = subprocess.Popen(
        [sys.executable, "-c", "from directive.server import serve_stdio; import sys, json; serve_stdio(__import__('pathlib').Path.cwd().joinpath('directive'))"],
        cwd=str(cwd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, **request})
    message = f"Content-Length: {len(payload)}\r\n\r\n{payload}"
    out, err = proc.communicate(input=message, timeout=5)
    assert err == "" or err is not None
    # Parse response frame
    assert out.startswith("Content-Length:")
    if "\r\n\r\n" in out:
        header, body = out.split("\r\n\r\n", 1)
    else:
        # Fallback for environments that normalize newlines
        header, body = out.split("\n\n", 1)
    return json.loads(body)


def test_server_spec_template_bundle(tmp_path: Path):
    # Prepare directive files
    (tmp_path / "directive" / "templates").mkdir(parents=True)
    (tmp_path / "directive" / "agent_operating_procedure.md").write_text("Do not write code until the TDR is produced and approved.")
    (tmp_path / "directive" / "agent_context.md").write_text("CTX")
    (tmp_path / "directive" / "templates" / "spec_template.md").write_text("SPEC TMPL")

    resp = _run_server_once(tmp_path, {"method": "spec.template", "params": {}})
    assert resp.get("id") == 1
    result = resp.get("result")
    assert result
    assert result["template"]["content"] == "SPEC TMPL"
    assert result["agentContext"]["path"] == "directive/agent_context.md"


