# Threat Model

| Threat | Example | Control boundary |
|---|---|---|
| Input substitution | A caller swaps an assumption after review. | Canonical hashes bind emitted records; downstream stores must bind review evidence to the same hash. |
| False precision | A UI displays a central value as a certain loss. | Ranges, confidence, source class, and rationale are mandatory; the core provides no single exposure calculation. |
| Evidence disclosure | Raw sensitive evidence is embedded in a scenario. | `EvidenceReference` accepts IDs, descriptions, and integrity hashes only; raw evidence has no field. |
| Authority confusion | A review record is treated as risk acceptance. | `ReviewObservation` records supplied status and declares that authority is not validated. |
| Version confusion | A downstream model uses a changed contract/model. | Schema version, model version, canonical JSON, and content hashes are explicit. |
| Secret leakage | A fixture embeds credentials or a production URL. | Fixtures are sealed synthetic data; `.env.example` contains no secret; CI scans only source contracts. |

Residual risks such as unauthorized downstream storage access, reviewer impersonation, and real
evidence retention are owned by the deployer of a downstream service and are outside this offline
package.
