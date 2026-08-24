# ADR 0001: Record analysis context, do not decide risk

**Status:** Accepted

## Decision

`cyrisk-core` records a supplied scenario, uncertainty-bearing factors, evidence references,
calculation manifest, and review observation. It does not calculate a decision, establish reviewer
authority, set tolerance, accept risk, authorize spend, or execute remediation.

## Rationale

Risk calculation and risk decision have different authorization, evidence, and accountability
requirements. Combining them would create an unsupported claim that a deterministic package can
make an organizational decision from incomplete inputs.

## Consequences

Downstream applications must add authenticated workflows, authorizer validation, retention,
auditability, and organization-specific policy before presenting a decision action.
