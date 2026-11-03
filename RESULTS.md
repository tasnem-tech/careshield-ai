# Verified local synthetic benchmark (2026-11-03)

Executed locally with `python -m experiments.run_experiments --n 5000 --seeds 42 123 2026 --out results` and seven passing pytest tests. This is **not** external validation or evidence of detecting real threats.

| Seed | Model | Precision | Recall | F1 | False positives | False negatives |
|---|---|---:|---:|---:|---:|---:|
| 42 | Random Forest | 0.9915 | 1.0000 | 0.9957 | 1 | 0 |
| 42 | Simple contextual rule | 0.8900 | 0.7672 | 0.8241 | 11 | 27 |
| 123 | Random Forest | 1.0000 | 1.0000 | 1.0000 | 0 | 0 |
| 123 | Simple contextual rule | 0.9111 | 0.7130 | 0.8000 | 8 | 33 |
| 2026 | Random Forest | 1.0000 | 0.9923 | 0.9961 | 0 | 1 |
| 2026 | Simple contextual rule | 0.9138 | 0.8154 | 0.8618 | 10 | 24 |

**Interpretation:** The model closely learns labels constructed directly from the same input features. This expected result cannot establish clinical/security effectiveness, novelty, or superiority on independent real incidents. The rule baseline intentionally omits some labelling rules, so this is a limited comparison rather than a fair test against optimized production rules.

**Next research step:** design independent scenario labels, multiple simulation environments and staff-group holdouts, and evaluate calibration and explanations.
