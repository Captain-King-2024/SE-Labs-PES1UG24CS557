# Lab 7 — Property-Based Testing for Ski Resort Passes

This lab uses Hypothesis to test how three ski resort pass functions handle arbitrary strings and `None`. Each property test runs up to 200 generated examples and checks that its function returns the expected type without raising an exception.

## Run the program and tests

From the `Lab 7` directory, run:

```sh
python processor.py
python -m pip install pytest hypothesis
python -m pytest test_processor.py -v
```

## Bugs fixed

| Function | Fix |
| --- | --- |
| `parse_season_pass_validity` | Validates the `YYYY/MM/DD` format and calendar date. Invalid input returns `Invalid date`. Valid dates from 2026 onward are marked `VALID`, and earlier dates are marked `EXPIRED`. |
| `compute_trail_gradient` | Parses `drop:distance` and rounds the percentage to two decimals. Malformed input, zero distance, or non-finite values return `0.0`. |
| `calculate_lift_access_tier` | Trims whitespace, ignores case, and looks up the first three characters. Unknown zones and non-string inputs return `0.0`. |

## Evidence

The captured pytest runs show three failures before the fixes and three passing tests afterward.

- [Before the fixes, the CLI crashed on a gradient input without a separator](before-cli-gradient-missing-separator.png)
- [Before the fixes, pytest reported three failures and showed the date parsing traceback](before-pytest-failures-and-date-traceback.png)
- [Before the fixes, Hypothesis reported gradient parsing failures](before-pytest-gradient-tracebacks.png)
- [Duplicate upload of the gradient failure screenshot](before-pytest-gradient-tracebacks-duplicate-upload.png)
- [Before the fixes, Hypothesis reported lift tier failures](before-pytest-lift-tier-tracebacks.png)
- [After the fixes, the CLI produced results for the sample runs](after-cli-sample-runs.png)
- [After the fixes, all three pytest tests passed](after-pytest-three-passing-tests.png)
