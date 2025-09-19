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
    (tmp_path / "directive" / "reference" / "templates").mkdir(parents=True)
    (tmp_path / "directive" / "reference" / "agent_operating_procedure.md").write_text("Do not write code until the TDR is produced and approved.")
    (tmp_path / "directive" / "reference" / "agent_context.md").write_text("CTX")
    (tmp_path / "directive" / "reference" / "templates" / "spec_template.md").write_text("SPEC TMPL")

    resp = _run_server_once(tmp_path, {"method": "spec.template", "params": {}})
    assert resp.get("id") == 1
    result = resp.get("result")
    assert result
    assert result["template"]["content"] == "SPEC TMPL"
    assert result["agentContext"]["path"] == "directive/reference/agent_context.md"


def test_tools_list_and_call_spec_template(tmp_path: Path):
    # Prepare directive files
    (tmp_path / "directive" / "reference" / "templates").mkdir(parents=True)
    (tmp_path / "directive" / "reference" / "agent_operating_procedure.md").write_text("Do not write code before TDR approval.")
    (tmp_path / "directive" / "reference" / "agent_context.md").write_text("CTX")
    (tmp_path / "directive" / "reference" / "templates" / "spec_template.md").write_text("SPEC TMPL")

    # tools/list
    list_resp = _run_server_once(tmp_path, {"method": "tools/list", "params": {}})
    assert list_resp.get("id") == 1
    tools = list_resp.get("result", {}).get("tools", [])
    names = {t.get("name") for t in tools}
    assert {
        "directive/files.list",
        "directive/file.get",
        "directive/spec.template",
        "directive/impact.template",
        "directive/tdr.template",
    }.issubset(names)

    # tools/call spec.template
    call_resp = _run_server_once(
        tmp_path,
        {"method": "tools/call", "params": {"name": "directive/spec.template", "arguments": {}}},
    )
    assert call_resp.get("id") == 1
    content = call_resp.get("result", {}).get("content")
    assert isinstance(content, list) and content and content[0].get("type") == "text"
    # Parse embedded JSON
    payload = json.loads(content[0]["text"])
    assert payload["template"]["content"] == "SPEC TMPL"


def test_tools_call_file_get_and_list(tmp_path: Path):
    (tmp_path / "directive").mkdir(parents=True)
    (tmp_path / "directive" / "reference").mkdir(parents=True)
    (tmp_path / "directive" / "reference" / "agent_context.md").write_text("CTX")

    # tools/call file.get
    get_resp = _run_server_once(
        tmp_path,
        {
            "method": "tools/call",
            "params": {"name": "directive/file.get", "arguments": {"path": "directive/reference/agent_context.md"}},
        },
    )
    assert get_resp.get("id") == 1
    payload = json.loads(get_resp.get("result", {}).get("content")[0]["text"])
    assert payload["content"] == "CTX"

    # tools/call files.list
    list_resp = _run_server_once(
        tmp_path,
        {"method": "tools/call", "params": {"name": "directive/files.list", "arguments": {}}},
    )
    assert list_resp.get("id") == 1
    payload2 = json.loads(list_resp.get("result", {}).get("content")[0]["text"])
    assert "directive/reference/agent_context.md" in payload2.get("files", [])


