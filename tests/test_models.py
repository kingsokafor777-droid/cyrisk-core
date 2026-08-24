from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from cyrisk_core.models import (
    ControlComparison,
    FactorRange,
    LossComponent,
    ReviewObservation,
    RiskScenario,
)

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_ransomware_scenario.json"


def load_payload() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_synthetic_scenario_is_valid() -> None:
    scenario = RiskScenario.model_validate(load_payload())
    assert scenario.loss_unit == "synthetic-usd"
    assert scenario.factors[0].central == Decimal("0.3")


def test_factor_range_rejects_reversed_bounds() -> None:
    with pytest.raises(ValidationError, match="lower <= central <= upper"):
        FactorRange(
            factor_id="factor-one",
            metric="synthetic metric",
            unit="synthetic-unit",
            distribution="uniform",
            lower="3",
            central="2",
            upper="1",
            source_class="synthetic",
            confidence="low",
            rationale="A sealed test value.",
        )


def test_loss_component_rejects_duplicate_factor_ids() -> None:
    with pytest.raises(ValidationError, match="must be unique"):
        LossComponent(
            component_id="loss-one",
            label="Synthetic loss",
            unit="synthetic-unit",
            factor_ids=("factor-one", "factor-one"),
            rationale="A sealed test value.",
        )


def test_scenario_rejects_unknown_loss_factor() -> None:
    payload = load_payload()
    payload["loss_components"][0]["factor_ids"] = ["not-present"]  # type: ignore[index]
    with pytest.raises(ValidationError, match="unknown factor_ids"):
        RiskScenario.model_validate(payload)


def test_scenario_rejects_duplicate_evidence_reference() -> None:
    payload = load_payload()
    payload["evidence_references"].append(payload["evidence_references"][0])  # type: ignore[index]
    with pytest.raises(ValidationError, match="evidence_ids must be unique"):
        RiskScenario.model_validate(payload)


def test_scenario_rejects_duplicate_factor_id() -> None:
    payload = load_payload()
    payload["factors"].append(payload["factors"][0])  # type: ignore[index]
    with pytest.raises(ValidationError, match="factor_ids must be unique"):
        RiskScenario.model_validate(payload)


def test_control_comparison_rejects_causal_claim() -> None:
    with pytest.raises(ValidationError, match="causal"):
        ControlComparison(
            comparison_id="comparison-one",
            scenario_id="scenario-one",
            baseline_manifest_id="manifest-baseline",
            candidate_manifest_id="manifest-candidate",
            assumption_note="Synthetic comparison only.",
            causal_claim=True,
        )


def test_control_comparison_rejects_same_manifest() -> None:
    with pytest.raises(ValidationError, match="must differ"):
        ControlComparison(
            comparison_id="comparison-one",
            scenario_id="scenario-one",
            baseline_manifest_id="manifest-same",
            candidate_manifest_id="manifest-same",
            assumption_note="Synthetic comparison only.",
        )


def test_control_comparison_accepts_non_causal_distinct_manifests() -> None:
    comparison = ControlComparison(
        comparison_id="comparison-one",
        scenario_id="scenario-one",
        baseline_manifest_id="manifest-baseline",
        candidate_manifest_id="manifest-candidate",
        assumption_note="Synthetic comparison only.",
    )
    assert comparison.causal_claim is False


def test_review_rejects_authority_assertion() -> None:
    with pytest.raises(ValidationError, match="authority"):
        ReviewObservation(
            review_id="review-one",
            risk_id="risk-one",
            observed_status="reviewed",
            reviewer_ref="synthetic-reviewer",
            observation_note="A supplied observation.",
            authority_validated=True,
        )


def test_review_accepts_non_authoritative_observation() -> None:
    observation = ReviewObservation(
        review_id="review-one",
        risk_id="risk-one",
        observed_status="reviewed",
        reviewer_ref="synthetic-reviewer",
        observation_note="A supplied observation.",
    )
    assert observation.authority_validated is False
