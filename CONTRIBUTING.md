# Contributing

Contributions must preserve deterministic behavior and the contract boundary. Do not add real
incident evidence, customer data, cloud credentials, market data feeds, real loss figures,
current timestamps, or a default network dependency to fixtures or tests.

Run `make check` before opening a pull request. Contract changes require a schema-version review,
canonical-hash compatibility analysis, fixture regeneration, and tests for both acceptance and
rejection behavior. Never weaken the coverage threshold to make a change pass.
