"""Pydantic contracts for Cyrisk records; values are supplied, never inferred."""

from __future__ import annotations

from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = "1.0"
HASH_PATTERN = r"^[a-f0-9]{64}$"
ID_PATTERN = r"^[a-z][a-z0-9_-]{2,63}$"


class SourceClass(str, Enum):
    """How a supplied input was obtained; no class implies truth."""

    SYNTHETIC = "synthetic"
    PUBLIC = "public"
    SUPPLIED = "supplied"
    UNKNOWN = "unknown"


class Confidence(str, Enum):
    """A declared assessment of input quality."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class ReviewStatus(str, Enum):
    """Observed workflow state; this is not an authorization decision."""

    DRAFT = "draft"
    REVIEWED = "reviewed"
    RECORDED = "recorded"
    DECLINED = "declined"


class CoreModel(BaseModel):
    """Strict base model for versioned contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)
    schema_version: str = Field(default=SCHEMA_VERSION, pattern=r"^1\.0$")


class EvidenceReference(CoreModel):
    """Payload-blind reference to a supplied evidence item."""

    evidence_id: str = Field(pattern=ID_PATTERN)
    source_class: SourceClass
    integrity_hash: str = Field(pattern=HASH_PATTERN)
    description: str = Field(min_length=1, max_length=240)
    expires_on: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")


class FactorRange(CoreModel):
    """A bounded, explainable factor input for a downstream model."""

    factor_id: str = Field(pattern=ID_PATTERN)
    metric: str = Field(min_length=1, max_length=120)
    unit: str = Field(min_length=1, max_length=64)
    distribution: str = Field(pattern=r"^(triangular|pert|uniform)$")
    lower: Decimal = Field(gt=0)
    central: Decimal = Field(gt=0)
    upper: Decimal = Field(gt=0)
    source_class: SourceClass
    confidence: Confidence
    rationale: str = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def validate_bounds(self) -> FactorRange:
        if not self.lower <= self.central <= self.upper:
            raise ValueError("factor bounds must satisfy lower <= central <= upper")
        return self


class LossComponent(CoreModel):
    """Named loss component with an explicit synthetic or supplied unit."""

    component_id: str = Field(pattern=ID_PATTERN)
    label: str = Field(min_length=1, max_length=120)
    unit: str = Field(min_length=1, max_length=64)
    factor_ids: tuple[str, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1, max_length=500)

    @field_validator("factor_ids")
    @classmethod
    def factor_ids_are_unique(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("loss component factor_ids must be unique")
        return value


class RiskScenario(CoreModel):
    """Versioned scenario context, supplied factors, and evidence references."""

    scenario_id: str = Field(pattern=ID_PATTERN)
    title: str = Field(min_length=1, max_length=160)
    asset_id: str = Field(pattern=ID_PATTERN)
    threat_event: str = Field(min_length=1, max_length=160)
    loss_unit: str = Field(min_length=1, max_length=64)
    source_class: SourceClass
    factors: tuple[FactorRange, ...] = Field(min_length=1)
    loss_components: tuple[LossComponent, ...] = Field(min_length=1)
    evidence_references: tuple[EvidenceReference, ...] = Field(min_length=1)
    completeness_note: str = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def validate_references(self) -> RiskScenario:
        factor_ids = {factor.factor_id for factor in self.factors}
        evidence_ids = [reference.evidence_id for reference in self.evidence_references]
        if len(factor_ids) != len(self.factors):
            raise ValueError("scenario factor_ids must be unique")
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("scenario evidence_ids must be unique")
        missing = {
            factor_id
            for component in self.loss_components
            for factor_id in component.factor_ids
            if factor_id not in factor_ids
        }
        if missing:
            raise ValueError(f"loss component references unknown factor_ids: {sorted(missing)}")
        return self


class CalculationManifest(CoreModel):
    """Integrity-bound metadata for a deterministic downstream calculation."""

    manifest_id: str = Field(pattern=ID_PATTERN)
    scenario_id: str = Field(pattern=ID_PATTERN)
    model_version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    deterministic_seed: int = Field(ge=0, le=2_147_483_647)
    simulation_count: int = Field(ge=1, le=1_000_000)
    input_hash: str = Field(pattern=HASH_PATTERN)
    output_hash: str = Field(pattern=HASH_PATTERN)
    completeness_status: str = Field(pattern=r"^(complete|partial|insufficient)$")
    limitation_note: str = Field(min_length=1, max_length=500)


class ControlComparison(CoreModel):
    """A supplied-assumption comparison, intentionally not a causal claim."""

    comparison_id: str = Field(pattern=ID_PATTERN)
    scenario_id: str = Field(pattern=ID_PATTERN)
    baseline_manifest_id: str = Field(pattern=ID_PATTERN)
    candidate_manifest_id: str = Field(pattern=ID_PATTERN)
    assumption_note: str = Field(min_length=1, max_length=500)
    causal_claim: bool = False

    @model_validator(mode="after")
    def forbid_causal_claim(self) -> ControlComparison:
        if self.causal_claim:
            raise ValueError("cyrisk-core does not permit causal control-effect claims")
        if self.baseline_manifest_id == self.candidate_manifest_id:
            raise ValueError("comparison manifests must differ")
        return self


class RiskRegisterRecord(CoreModel):
    """Risk-register context that does not establish tolerance or authority."""

    risk_id: str = Field(pattern=ID_PATTERN)
    scenario_id: str = Field(pattern=ID_PATTERN)
    owner_ref: str = Field(min_length=1, max_length=120)
    appetite_context: str = Field(min_length=1, max_length=500)
    tolerance_context: str = Field(min_length=1, max_length=500)
    manifest_id: str = Field(pattern=ID_PATTERN)
    review_status: ReviewStatus


class ReviewObservation(CoreModel):
    """A supplied review observation; external authority validation is out of scope."""

    review_id: str = Field(pattern=ID_PATTERN)
    risk_id: str = Field(pattern=ID_PATTERN)
    observed_status: ReviewStatus
    reviewer_ref: str = Field(min_length=1, max_length=120)
    observation_note: str = Field(min_length=1, max_length=500)
    authority_validated: bool = False

    @model_validator(mode="after")
    def authority_is_not_asserted(self) -> ReviewObservation:
        if self.authority_validated:
            raise ValueError("authority validation belongs to an authenticated downstream workflow")
        return self
