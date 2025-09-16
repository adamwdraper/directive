import argparse
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Dict, List, Optional, Tuple

from .bundles import build_template_bundle, list_directive_files, read_directive_file


def _print(msg: str) -> None:
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def _err(msg: str) -> None:
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def _package_data_root() -> Path:
    try:
        import importlib.resources as resources
    except Exception:  # pragma: no cover
        import importlib_resources as resources  # type: ignore

    # Resolve the path to packaged defaults under directive/data/
    return Path(resources.files("directive")).joinpath("data", "directive")  # type: ignore[attr-defined]


def _copy_tree(src: Path, dst: Path, overwrite: bool = False) -> Tuple[int, int, List[str]]:
    copied = 0
    skipped = 0
    notes: List[str] = []
    for root, dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        target_dir = dst.joinpath(rel)
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in files:
            s = Path(root).joinpath(name)
            d = target_dir.joinpath(name)
            if d.exists() and not overwrite:
                skipped += 1
                notes.append(f"skip existing: {d}")
                continue
            shutil.copy2(s, d)
            copied += 1
            notes.append(f"wrote: {d}")
    return copied, skipped, notes


def cmd_init(args: argparse.Namespace) -> int:
    repo_root = Path.cwd()
    target = repo_root.joinpath("directive")
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    defaults = _package_data_root()
    copied, skipped, notes = _copy_tree(defaults, target, overwrite=False)
    _print(f"Initialized directive/ (copied {copied}, skipped {skipped})")
    if args.verbose:
        for n in notes:
            _print(n)
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    repo_root = Path.cwd()
    target = repo_root.joinpath("directive")
    if not target.exists():
        _err("No directive/ found. Run 'directive init' first.")
        return 1
    defaults = _package_data_root()
    copied, skipped, notes = _copy_tree(defaults, target, overwrite=False)
    _print(f"Updated directive/ (copied {copied} new files, left {skipped} unchanged)")
    if args.verbose:
        for n in notes:
            _print(n)
    return 0


def cmd_mcp_serve(args: argparse.Namespace) -> int:
    try:
        from .server import serve_stdio
    except Exception as exc:  # ImportError or others
        _err("MCP server dependencies not available. Install the 'mcp' package.")
        _err("Try: uv add mcp")
        _err(f"Details: {exc}")
        return 1

    return serve_stdio(root=Path.cwd().joinpath("directive"))


def cmd_bundle(args: argparse.Namespace) -> int:
    template_name = args.template
    try:
        bundle = build_template_bundle(template_name=template_name, repo_root=Path.cwd())
    except FileNotFoundError as e:
        _err(str(e))
        # Helpful list of available templates
        try:
            files = list_directive_files(Path.cwd())
            available = [f for f in files if "/templates/" in f or "\\templates\\" in f]
        except Exception:
            available = []
        _err("Available templates:")
        for p in available:
            _err(f" - {p}")
        _err("Suggestion: run 'directive update' to restore defaults.")
        return 1

    _print(json.dumps(bundle, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="directive", description="Directive CLI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize directive/ with defaults (non-destructive)")
    p_init.set_defaults(func=cmd_init)

    p_update = sub.add_parser("update", help="Update directive/ with any missing defaults")
    p_update.set_defaults(func=cmd_update)

    p_serve = sub.add_parser("mcp", help="MCP related commands")
    sub_mcp = p_serve.add_subparsers(dest="mcp_command", required=True)
    p_serve_stdio = sub_mcp.add_parser("serve", help="Start MCP server over stdio in current repo")
    p_serve_stdio.set_defaults(func=cmd_mcp_serve)

    p_bundle = sub.add_parser("bundle", help="Print a template bundle (for testing)")
    p_bundle.add_argument("template", choices=["spec_template.md", "impact_template.md", "tdr_template.md"], help="Template file name")
    p_bundle.set_defaults(func=cmd_bundle)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    return int(ns.func(ns) or 0)


if __name__ == "__main__":
    raise SystemExit(main())


