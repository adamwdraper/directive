import argparse
import re
import subprocess
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def run_git_command(*args: str, capture_output: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", *args],
            check=True,
            text=True,
            capture_output=capture_output,
        )
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            print(exc.stdout)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        fail(f"git {' '.join(args)} failed with exit code {exc.returncode}")


def ensure_clean_working_tree() -> None:
    proc = run_git_command("status", "--porcelain", capture_output=True)
    if proc.stdout.strip():
        fail("Working tree is dirty. Commit or stash changes before running release.")


def parse_version(version_str: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version_str.strip())
    if not match:
        fail(f"Malformed version: '{version_str}'. Expected format X.Y.Z")
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def bump_version(current: str, bump_type: str) -> str:
    major, minor, patch = parse_version(current)
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        fail("bump_type must be one of: major, minor, patch")
    return f"{major}.{minor}.{patch}"


def read_current_version(pyproject_path: Path) -> str:
    if not pyproject_path.exists():
        fail(f"pyproject.toml not found at {pyproject_path}")
    in_project = False
    version_value: str | None = None
    for line in pyproject_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
            continue
        if in_project:
            m = re.match(r"version\s*=\s*\"([^\"]+)\"", stripped)
            if m:
                version_value = m.group(1)
                break
    if not version_value:
        fail("Could not find project.version in pyproject.toml")
    return version_value


def write_new_version(pyproject_path: Path, new_version: str) -> None:
    lines = pyproject_path.read_text(encoding="utf-8").splitlines()
    in_project = False
    replaced = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
        elif in_project:
            if re.match(r"version\s*=\s*\"([^\"]+)\"", stripped):
                indent = line[: len(line) - len(line.lstrip())]
                lines[i] = f"{indent}version = \"{new_version}\""
                replaced = True
                break
    if not replaced:
        fail("project.version not found for update in pyproject.toml")
    pyproject_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def create_and_push_release_branch(new_version: str) -> None:
    branch_name = f"release/v{new_version}"
    run_git_command("add", "pyproject.toml")
    run_git_command("commit", "-m", f"chore(release): v{new_version}")
    # Create and switch to new branch
    run_git_command("checkout", "-b", branch_name)
    # Push and set upstream
    run_git_command("push", "-u", "origin", branch_name)
    print(f"Pushed {branch_name} to origin")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Bump version and create a release branch")
    parser.add_argument("bump", choices=["major", "minor", "patch"], help="Type of version bump")
    args = parser.parse_args(argv)

    # Ensure inside a git repo
    try:
        run_git_command("rev-parse", "--is-inside-work-tree")
    except SystemExit:
        raise

    ensure_clean_working_tree()

    pyproject_path = Path("pyproject.toml")
    current_version = read_current_version(pyproject_path)
    next_version = bump_version(current_version, args.bump)

    if next_version == current_version:
        fail("Next version equals current version; nothing to do.")

    print(f"Current version: {current_version}\nNext version: {next_version}")
    write_new_version(pyproject_path, next_version)

    create_and_push_release_branch(next_version)


if __name__ == "__main__":
    main()


