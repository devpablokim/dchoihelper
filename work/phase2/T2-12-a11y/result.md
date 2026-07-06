# T2-12-a11y Result

## Commands

`cd incubator && node packages/deck-grader/tests/run-a11y.mjs && node packages/deck-grader/tests/run.mjs`

```text
PASS deck-grader accessibility rules (4 rules, 6 fixtures, golden snapshots matched)
PASS deck-grader skeleton (6 hard-fail rules, reports in tests/out)
```

Additional regression checks:

`cd incubator && node packages/deck-grader/tests/run-typo.mjs && node packages/deck-grader/tests/run-color.mjs && node packages/deck-grader/tests/run-align.mjs`

```text
PASS deck-grader typography rules (5 rules, 6 fixtures, snapshots in tests/fixtures/typo/golden)
PASS deck-grader color rules (5 fixtures, 4 rules, golden snapshots matched)
PASS deck-grader alignment rules (4 rules, 5 golden reports matched)
```

## Summary

- Added `src/rules/a11y.mjs` with deterministic accessibility checks for media text alternatives, non-text contrast, DOM/visual reading order, and decorative aria handling.
- Added `rules-a11y.yaml` thresholds and rule settings; numeric thresholds are loaded from YAML while base constants are loaded through existing grader config.
- Added positive and negative fixtures plus golden grade-report snapshots under `tests/fixtures/a11y/`.
- Added `tests/run-a11y.mjs` with slide-html contract checks, grade-report schema validation, exact failing-rule assertions, and golden snapshot comparison.
