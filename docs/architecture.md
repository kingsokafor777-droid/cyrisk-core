# Architecture

`cyrisk-core` is a serialization and integrity boundary. It holds no state, starts no background
work, and has no provider or database client. All timestamps, numbers, and identifiers that enter
a record are supplied explicitly by a caller.

## Runtime flow

1. A caller constructs a typed record using the versioned models.
2. The model enforces units, IDs, non-empty rationale, bounded input ranges, and explicit source
   class/confidence labels.
3. `canonical_json` emits a stable representation; `content_hash` emits a SHA-256 digest.
4. A downstream component persists, evaluates, compares, or displays the record under its own
   authorization and retention boundary.

## Failure rules

The package rejects invalid identifiers, non-positive factor bounds, an out-of-range central value,
unlabeled source/confidence, blank rationale, malformed integrity hashes, and missing review
references. It does not infer values, silently choose units, fill an unknown input, or downgrade a
validation failure to a default.

## Non-negotiable rules

- A factor range is an assumption record, not a probability or an observed statistic.
- `synthetic-usd` means a deliberately fictional unit; it must not be presented as a real currency estimate.
- A review observation is evidence that an observation was recorded, not proof of authority.
- A control comparison binds supplied manifests. Causality and savings are not determined here.
