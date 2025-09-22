from pathlib import Path

from directive.bundles import build_template_bundle, list_directive_files, get_directive_root


def test_list_directive_files_lists_known_paths(tmp_path: Path, monkeypatch):
    # Create a temporary directive structure
    root = tmp_path / "directive"
    (root / "reference" / "templates").mkdir(parents=True)
    (root / "reference" / "agent_operating_procedure.md").write_text("AOP line: Do not write code before TDR approval.")
    (root / "reference" / "agent_context.md").write_text("Context")
    (root / "reference" / "templates" / "spec_template.md").write_text("Tmpl")

    monkeypatch.chdir(tmp_path)

    files = list_directive_files()
    assert "directive/reference/agent_operating_procedure.md" in files
    assert "directive/reference/agent_context.md" in files
    assert "directive/reference/templates/spec_template.md" in files


def test_build_template_bundle_happy_path(tmp_path: Path, monkeypatch):
    root = tmp_path / "directive"
    (root / "reference" / "templates").mkdir(parents=True)
    (root / "reference" / "agent_operating_procedure.md").write_text("Do not write code until the TDR is produced and approved.")
    (root / "reference" / "agent_context.md").write_text("Context body")
    (root / "reference" / "templates" / "spec_template.md").write_text("Spec template body")

    monkeypatch.chdir(tmp_path)

    bundle = build_template_bundle("spec_template.md")
    assert bundle["agentOperatingProcedure"]["path"] == "directive/reference/agent_operating_procedure.md"
    assert bundle["agentContext"]["path"] == "directive/reference/agent_context.md"
    assert bundle["template"]["path"].endswith("spec_template.md")
    # Verbatim content check
    assert bundle["template"]["content"] == "Spec template body"


def test_build_template_bundle_missing_template(tmp_path: Path, monkeypatch):
    root = tmp_path / "directive"
    root.mkdir()
    (root / "reference").mkdir(parents=True, exist_ok=True)
    (root / "reference" / "agent_operating_procedure.md").write_text("AOP")
    (root / "reference" / "agent_context.md").write_text("CTX")

    monkeypatch.chdir(tmp_path)

    try:
        build_template_bundle("spec_template.md")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as e:
        assert "Missing template" in str(e)


