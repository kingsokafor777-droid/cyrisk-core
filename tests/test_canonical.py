from __future__ import annotations

from cyrisk_core.canonical import canonical_json, content_hash
from cyrisk_core.models import FactorRange


def test_canonical_json_sorts_mapping_keys() -> None:
    assert canonical_json({"b": 2, "a": 1}) == '{"a":1,"b":2}'


def test_content_hash_is_stable_for_validated_model() -> None:
    factor = FactorRange(
        factor_id="factor-one",
        metric="synthetic metric",
        unit="synthetic-unit",
        distribution="uniform",
        lower="1",
        central="2",
        upper="3",
        source_class="synthetic",
        confidence="low",
        rationale="A sealed test value.",
    )
    assert content_hash(factor) == content_hash(factor)
