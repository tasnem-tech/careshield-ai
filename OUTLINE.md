# CareShield AI: Context-Aware Detection of Constructed Anomalous Electronic Health Record Access Events

**Status:** Research outline, not a completed paper. No empirical results are asserted here.

## Abstract (write after running experiments)
State the synthetic-data setting, research question, comparison, actual measured outcomes, and limits. Do not claim detection of real-world attacks.

## 1. Introduction
EHR access monitoring; why emergency care and off-hours work complicate security rules; scope of a simulation-based proof of concept.

## 2. Related work
Literature search required: EHR audit-log anomaly detection, insider threats, contextual access control, explainability, synthetic data validation. Verify each citation before publication.

## 3. Research questions
RQ1: Can a Random Forest reproduce constructed contextual alert rules on chronologically held-out synthetic events?
RQ2: How does it compare with a deliberately simpler contextual rule baseline?
RQ3: Which scenario types create false positives and false negatives?

## 4. Methods
Deterministic synthetic generator with explicit rule-derived labels; role, hour, assignment, authentication, frequency and emergency signals; chronological 70/30 split; Random Forest and simple-rule baseline; fixed seeds; precision, recall, F1, average precision, ROC-AUC, confusion matrix. Describe all scenario construction choices.

## 5. Results (pending execution)
Insert the actual CSV from `python -m experiments.run_experiments`. Report per-seed values and variability. Do not fabricate figures, p-values or conclusions. Include a confusion matrix and error analysis.

## 6. Threats to validity
Rule-derived labels create circularity; synthetic distributions may be unrealistic; repeated staff IDs across splits; no independent incident labels; no clinical deployment; explanation strings describe input scenario factors, not model attributions; potential class imbalance and temporal artefacts.

## 7. Discussion
Interpret results only as simulation behaviour. Propose independent scenario validation, group splits, calibration, shift-sensitive controls, clinician/security expert review, and external audit logs under appropriate governance.

## 8. Ethics and reproducibility
Synthetic records only; no actual patient or employee data; release generator, scripts, dependencies, seed configuration, and results with versioned code.

## 9. Conclusion
Write only after validating and analysing results.
