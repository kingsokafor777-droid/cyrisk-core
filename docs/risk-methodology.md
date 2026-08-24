# Risk Methodology Boundary

Cyrisk uses a FAIR-inspired vocabulary only as a planning influence. It does not copy an external
standard, implement a certification program, or claim conformance. The core package only preserves
the information needed for an explainable downstream model: scenario identity, units, factor
ranges, loss components, evidence references, and model-manifest metadata.

Every numerical input must provide a `lower`, `central`, and `upper` bound, a declared unit, a
distribution family, confidence, source class, and rationale. A downstream model may use those
inputs only when its own documented policy allows it. It must report uncertainty and sensitivity
instead of converting incomplete inputs into a single precise result.

NIST positions cybersecurity risk information as an input to enterprise risk-management processes,
with scenario documentation, likelihood, and impact supporting later prioritization and response.
[1] [2]

[1]: https://csrc.nist.gov/pubs/ir/8286/r1/final "NISTIR 8286 Rev. 1"
[2]: https://csrc.nist.gov/pubs/ir/8286/a/r1/final "NISTIR 8286A Rev. 1"
