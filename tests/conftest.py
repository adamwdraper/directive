from pathlib import Path
import sys


def _ensure_src_on_path():
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    if src_dir.exists():
        src_str = str(src_dir)
        if src_str not in sys.path:
            sys.path.insert(0, src_str)


_ensure_src_on_path()


