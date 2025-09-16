from pathlib import Path

from directive.bundles import build_template_bundle, list_directive_files, get_directive_root


def test_list_directive_files_lists_known_paths(tmp_path: Path, monkeypatch):
    # Create a temporary directive structure
    root = tmp_path / "directive"
    (root / "templates").mkdir(parents=True)
    (root / "agent_operating_procedure.md").write_text("AOP line: Do not write code before TDR approval.")
    (root / "agent_context.md").write_text("Context")
    (root / "templates" / "spec_template.md").write_text("Tmpl")

    monkeypatch.chdir(tmp_path)

    files = list_directive_files()
    assert "directive/agent_operating_procedure.md" in files
    assert "directive/agent_context.md" in files
    assert "directive/templates/spec_template.md" in files


def test_build_template_bundle_happy_path(tmp_path: Path, monkeypatch):
    root = tmp_path / "directive"
    (root / "templates").mkdir(parents=True)
    (root / "agent_operating_procedure.md").write_text("Do not write code until the TDR is produced and approved.")
    (root / "agent_context.md").write_text("Context body")
    (root / "templates" / "spec_template.md").write_text("Spec template body")

    monkeypatch.chdir(tmp_path)

    bundle = build_template_bundle("spec_template.md")
    assert bundle["primer"].lower().startswith("do not write code")
    assert bundle["agentOperatingProcedure"]["path"] == "directive/agent_operating_procedure.md"
    assert bundle["agentContext"]["path"] == "directive/agent_context.md"
    assert bundle["template"]["path"].endswith("spec_template.md")
    # Verbatim content check
    assert bundle["template"]["content"] == "Spec template body"


def test_build_template_bundle_missing_template(tmp_path: Path, monkeypatch):
    root = tmp_path / "directive"
    root.mkdir()
    (root / "agent_operating_procedure.md").write_text("AOP")
    (root / "agent_context.md").write_text("CTX")

    monkeypatch.chdir(tmp_path)

    try:
        build_template_bundle("spec_template.md")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as e:
        assert "Missing template" in str(e)


