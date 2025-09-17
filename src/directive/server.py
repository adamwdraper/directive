from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .bundles import build_template_bundle, list_directive_files, read_directive_file, get_directive_root


# Minimal stdio JSON-RPC server shape tailored for MCP-like usage.
# This is a lightweight scaffold; if the official MCP Python library is available
# later, this module can be adapted to use it without changing higher-level logic.


@dataclass
class Request:
    id: Any
    method: str
    params: Dict[str, Any]


def _read_message() -> Optional[Dict[str, Any]]:
    import sys

    header = sys.stdin.readline()
    if not header:
        return None
    header = header.strip()
    if not header.lower().startswith("content-length:"):
        return None
    try:
        length = int(header.split(":", 1)[1].strip())
    except Exception:
        return None
    # Read empty line
    sys.stdin.readline()
    raw = sys.stdin.read(length)
    if not raw:
        return None
    return json.loads(raw)


def _write_message(payload: Dict[str, Any]) -> None:
    import sys

    data = json.dumps(payload)
    sys.stdout.write(f"Content-Length: {len(data)}\r\n\r\n{data}")
    sys.stdout.flush()


def _error(id_value: Any, code: int, message: str, data: Any = None) -> None:
    err: Dict[str, Any] = {"jsonrpc": "2.0", "id": id_value, "error": {"code": code, "message": message}}
    if data is not None:
        err["error"]["data"] = data
    _write_message(err)


def _result(id_value: Any, result: Any) -> None:
    _write_message({"jsonrpc": "2.0", "id": id_value, "result": result})


# ---- MCP helpers ----

def _tool_descriptors() -> List[Dict[str, Any]]:
    return [
        {
            "name": "directive/files.list",
            "title": "List Directive Files",
            "description": "List all files under the repository’s directive/ directory (context and templates).",
            "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
        },
        {
            "name": "directive/file.get",
            "title": "Read Directive File",
            "description": "Read a file under directive/ by path and return its full contents verbatim.",
            "inputSchema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path under directive/ (e.g., directive/agent_context.md)",
                    }
                },
                "required": ["path"],
            },
        },
        {
            "name": "directive/spec.template",
            "title": "Spec Template Bundle",
            "description": "Return Agent Operating Procedure, Agent Context, and the Spec template, plus a concise Primer for drafting a new Spec.",
            "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
        },
        {
            "name": "directive/impact.template",
            "title": "Impact Template Bundle",
            "description": "Return Agent Operating Procedure, Agent Context, and the Impact template, plus a concise Primer for drafting an Impact analysis.",
            "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
        },
        {
            "name": "directive/tdr.template",
            "title": "TDR Template Bundle",
            "description": "Return Agent Operating Procedure, Agent Context, and the TDR template, plus a concise Primer for drafting a Technical Design Review.",
            "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
        },
    ]


def _wrap_text_content(text: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


def serve_stdio(root: Path) -> int:
    # Ensure we consistently resolve the repo root and directive root once.
    repo_root = root.parent
    try:
        directive_root = get_directive_root(repo_root)
    except Exception:
        directive_root = root

    while True:
        msg = _read_message()
        if msg is None:
            break
        id_value = msg.get("id")
        method = msg.get("method")
        params = msg.get("params") or {}

        try:
            # MCP tool discovery
            if method == "tools/list":
                _result(id_value, {"tools": _tool_descriptors()})

            # MCP tool execution
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments") or {}
                if not isinstance(name, str):
                    raise ValueError("name must be a string")

                # Dispatch based on tool name
                if name == "directive/files.list":
                    files = list_directive_files(repo_root)
                    _result(id_value, _wrap_text_content(json.dumps({"files": files})))

                elif name == "directive/file.get":
                    path = arguments.get("path")
                    if not isinstance(path, str):
                        raise ValueError("path must be a string")
                    content = read_directive_file(repo_root, path)
                    _result(id_value, _wrap_text_content(json.dumps({"path": path, "content": content})))

                elif name == "directive/spec.template":
                    bundle = build_template_bundle("spec_template.md", repo_root)
                    _result(id_value, _wrap_text_content(json.dumps(bundle)))

                elif name == "directive/impact.template":
                    bundle = build_template_bundle("impact_template.md", repo_root)
                    _result(id_value, _wrap_text_content(json.dumps(bundle)))

                elif name == "directive/tdr.template":
                    bundle = build_template_bundle("tdr_template.md", repo_root)
                    _result(id_value, _wrap_text_content(json.dumps(bundle)))

                else:
                    _error(id_value, -32601, f"Tool not found: {name}")

            # Back-compat custom methods
            elif method == "directive.files.list":
                files = list_directive_files(repo_root)
                _result(id_value, {"files": files})
            elif method == "directive.file.get":
                path = params.get("path")
                if not isinstance(path, str):
                    raise ValueError("path must be a string")
                content = read_directive_file(repo_root, path)
                _result(id_value, {"path": path, "content": content})
            elif method == "spec.template":
                _result(id_value, build_template_bundle("spec_template.md", repo_root))
            elif method == "impact.template":
                _result(id_value, build_template_bundle("impact_template.md", repo_root))
            elif method == "tdr.template":
                _result(id_value, build_template_bundle("tdr_template.md", repo_root))
            else:
                _error(id_value, -32601, f"Method not found: {method}")
        except FileNotFoundError as e:
            _error(id_value, 1001, str(e))
        except Exception as e:  # pragma: no cover
            _error(id_value, -32000, "Server error", {"details": str(e)})

    return 0


