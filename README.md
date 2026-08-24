# Cyrisk Core

> **Deterministic contracts for evidence-governed cyber-risk scenario analysis.**

`cyrisk-core` is the canonical vocabulary for the Cyrisk program. It models **supplied** risk
scenarios, bounded factor ranges, loss components, evidence references, calculation manifests,
control-comparison records, risk-register records, and review observations. It provides JSON
Schema, canonical JSON, and SHA-256 content hashes so downstream components can exchange and
verify records deterministically.

## Scope

The package deliberately models **analysis inputs and records**, not an operating risk service.
It does not call cloud APIs, collect customer data, connect to a database, run a loss simulation,
estimate a real organization's exposure, set risk appetite, authorize spending, accept risk, or
execute a control change. Those actions require organizational authority and belong outside this
package.

> A Cyrisk output is a versioned analysis of supplied assumptions and evidence references. It is
> not a forecast, insurance estimate, audit opinion, investment recommendation, or risk decision.

## Data flow

```text
sealed synthetic scenario + supplied assumptions + evidence references
                              |
                              v
                    cyrisk-core contracts
                              |
              +---------------+----------------+
              |                                |
              v                                v
       canonical JSON + hash              JSON Schema
              |                                |
              +---------------+----------------+
                              v
         cyrisk-model / evidence / controls / register
```

## Contract inventory

| Contract | Purpose | Important boundary |
|---|---|---|
| `RiskScenario` | Identifies a synthetic or supplied threat scenario, asset, loss unit, factors, and evidence references. | No real-world loss assertion is made. |
| `FactorRange` | Captures a bounded numeric input, unit, distribution family, confidence, rationale, and source class. | Unknown inputs are explicit; a range is not an observation. |
| `EvidenceReference` | Records a payload-blind evidence ID, source class, integrity hash, and expiry metadata. | No raw evidence is stored. |
| `CalculationManifest` | Binds scenario, model version, seed, input hash, output hash, and simulation count. | A manifest records a run; it does not calculate an exposure. |
| `ControlComparison` | Binds two manifests and labels a supplied comparison assumption. | It cannot establish that a control caused savings. |
| `RiskRegisterRecord` | Records scenario linkage, owner, appetite/tolerance context, and review state. | It does not accept or transfer risk. |
| `ReviewObservation` | Records a human review observation and supplied decision status. | The package cannot validate authority. |

## Quick start

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e .
make check
cyrisk-core hash fixtures/synthetic_ransomware_scenario.json
```

The only committed fixture is synthetic. It uses an arbitrary `synthetic-usd` unit to prevent an
example from being mistaken for a company loss estimate.

## Engineering controls

The release gate regenerates schemas and the deterministic fixture, runs Ruff, strict mypy,
branch-aware tests with a 95% minimum, and verifies wheel contents. GitHub Actions uses immutable
action SHAs for the Python matrix, quality gate, package check, and CodeQL.

## Documentation

| Document | Purpose |
|---|---|
| [Architecture](docs/architecture.md) | Component boundaries and downstream integration contract. |
| [Risk methodology](docs/risk-methodology.md) | Scenario/range conventions and anti-false-precision rules. |
| [Threat model](docs/threat-model.md) | Integrity, provenance, and misuse threats. |
| [Decision boundary ADR](docs/adr/0001-record-not-decide.md) | Why records and decisions are separate. |
| [Synthetic example](docs/examples/synthetic-ransomware.md) | How the sealed fixture should be interpreted. |

## License

Licensed under the [Apache License 2.0](LICENSE).
