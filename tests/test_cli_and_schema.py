from __future__ import annotations

import json
from pathlib import Path

import pytest

from cyrisk_core.cli import main

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "synthetic_ransomware_scenario.json"


def test_hash_cli_emits_digest(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["hash", str(FIXTURE)]) == 0
    assert len(capsys.readouterr().out.strip()) == 64


def test_canonical_cli_emits_valid_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["canonical", str(FIXTURE)]) == 0
    assert json.loads(capsys.readouterr().out)["scenario_id"] == "scn-ransomware-payments"


def test_cli_rejects_invalid_json(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text("not-json", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["hash", str(invalid)])


def test_schema_export_artifacts_exist() -> None:
    schemas = list((ROOT / "schemas").glob("*.schema.json"))
    assert len(schemas) == 7
