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


def serve_stdio(root: Path) -> int:
    try:
        directive_root = get_directive_root(root.parent)
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
            if method == "directive.files.list":
                files = list_directive_files(directive_root.parent)
                _result(id_value, {"files": files})
            elif method == "directive.file.get":
                path = params.get("path")
                if not isinstance(path, str):
                    raise ValueError("path must be a string")
                content = read_directive_file(directive_root.parent, path)
                _result(id_value, {"path": path, "content": content})
            elif method == "spec.template":
                _result(id_value, build_template_bundle("spec_template.md", directive_root.parent))
            elif method == "impact.template":
                _result(id_value, build_template_bundle("impact_template.md", directive_root.parent))
            elif method == "tdr.template":
                _result(id_value, build_template_bundle("tdr_template.md", directive_root.parent))
            else:
                _error(id_value, -32601, f"Method not found: {method}")
        except FileNotFoundError as e:
            _error(id_value, 1001, str(e))
        except Exception as e:  # pragma: no cover
            _error(id_value, -32000, "Server error", {"details": str(e)})

    return 0


