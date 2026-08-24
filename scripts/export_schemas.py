"""Export deterministic JSON Schema for public Cyrisk contract types."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from cyrisk_core.models import (
    CalculationManifest,
    ControlComparison,
    EvidenceReference,
    FactorRange,
    ReviewObservation,
    RiskRegisterRecord,
    RiskScenario,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
MODELS: tuple[type[BaseModel], ...] = (
    EvidenceReference,
    FactorRange,
    RiskScenario,
    CalculationManifest,
    ControlComparison,
    RiskRegisterRecord,
    ReviewObservation,
)


def main() -> None:
    """Write sorted JSON Schema documents for all public record contracts."""
    SCHEMAS.mkdir(exist_ok=True)
    for model in MODELS:
        target = SCHEMAS / f"{model.__name__}.schema.json"
        target.write_text(
            json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
