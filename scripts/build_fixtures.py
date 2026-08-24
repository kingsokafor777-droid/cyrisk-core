"""Write the deterministic synthetic fixture from an embedded canonical payload."""

from __future__ import annotations

import json
from pathlib import Path

from cyrisk_core.models import RiskScenario

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "synthetic_ransomware_scenario.json"

PAYLOAD = {
    "scenario_id": "scn-ransomware-payments",
    "title": "Synthetic ransomware event against payments API",
    "asset_id": "asset-payments-api",
    "threat_event": "Synthetic ransomware execution",
    "loss_unit": "synthetic-usd",
    "source_class": "synthetic",
    "factors": [
        {
            "factor_id": "frequency-range",
            "metric": "annual event frequency",
            "unit": "events-per-year",
            "distribution": "triangular",
            "lower": "0.1",
            "central": "0.3",
            "upper": "0.8",
            "source_class": "synthetic",
            "confidence": "low",
            "rationale": "Sealed fixture assumption; not a threat-frequency estimate.",
        },
        {
            "factor_id": "recovery-range",
            "metric": "recovery loss component",
            "unit": "synthetic-usd",
            "distribution": "pert",
            "lower": "10000",
            "central": "25000",
            "upper": "50000",
            "source_class": "synthetic",
            "confidence": "low",
            "rationale": "Sealed fixture assumption; not an operating cost estimate.",
        },
    ],
    "loss_components": [
        {
            "component_id": "loss-recovery",
            "label": "Synthetic recovery component",
            "unit": "synthetic-usd",
            "factor_ids": ["recovery-range"],
            "rationale": "Exercises factor linkage only; no real loss is represented.",
        }
    ],
    "evidence_references": [
        {
            "evidence_id": "evidence-synthetic-control-gap",
            "source_class": "synthetic",
            "integrity_hash": "7f9b8c2b4b452be484fe4ecf7f8d08ed6a9ca2f80d29c1238ccce47f4e2343a4",
            "description": "Synthetic payload-blind evidence reference for fixture validation.",
            "expires_on": "2099-12-31",
        }
    ],
    "completeness_note": "Synthetic fixture; no input is a real-world observation or forecast.",
}


def main() -> None:
    """Validate and write a stable fixture used by tests and release gates."""
    scenario = RiskScenario.model_validate(PAYLOAD)
    FIXTURE.write_text(
        json.dumps(scenario.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
