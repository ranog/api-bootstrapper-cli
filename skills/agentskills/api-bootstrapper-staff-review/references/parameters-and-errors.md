# Parameters and Errors

## Parameters

- `target` (required): Scope under review (files, branch, or design).
- `focus` (optional): `architecture`, `risk`, `tests`, or `all`.

## Validation Rules

- Findings should prioritize risk and behavior over style.
- Recommendations should include rationale and tradeoffs.
- High-severity findings require concrete impact description.

## Common Errors

- Overly generic advice:
  - Cause: no tie to concrete code or design.
  - Action: ground feedback in observable artifacts.

- Missing risk prioritization:
  - Cause: findings listed without severity.
  - Action: classify and order by impact.
