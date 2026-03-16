---
name: api-bootstrapper-staff-review
description: Perform staff-level technical review focused on architecture, risk, tradeoffs, and long-term maintainability. Use before high-impact changes or design decisions.
---
# API Bootstrapper Staff Review

Use this skill for rigorous technical review with decision-quality feedback.

## Inputs

- `target`: Design, diff, or implementation to review.
- `focus`: Optional emphasis (`architecture`, `risk`, `tests`, `all`). Default to `all`.

## Execution Contract

1. Evaluate in this order:
- Behavioral correctness and regression risk.
- Architectural boundaries and cohesion.
- Tradeoffs and alternative options.
- Test adequacy and operational impact.

2. Classify findings by severity with file references when code is involved.

3. State assumptions explicitly and separate facts from inferences.

4. Before applying structural or behavior changes from this review, require explicit confirmation. Show:
- Proposed direction.
- Risk and mitigation summary.
- Prompt: `Proceed? (yes/no)`.

5. Report:
- `Critical findings`
- `Tradeoffs`
- `Recommended path`
- `Validation strategy`
