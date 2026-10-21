# 🛡️ CareShield AI
### Context-Aware Healthcare Record Access Risk Lab

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io) ![Research prototype](https://img.shields.io/badge/status-research%20prototype-38D9C5) ![Data](https://img.shields.io/badge/data-100%25%20synthetic-6B7280)

**A reproducible security analytics prototype exploring whether contextual access signals can distinguish suspicious-looking electronic health record (EHR) access from routine care activity.**

> **Scope:** This is a portfolio research demonstration using simulated access logs and constructed alert labels. It has not been tested against real hospital security incidents and must not be used for clinical, employment or operational security decisions.

## Why this matters

In healthcare, access outside standard hours is not automatically malicious: emergency and night-shift care are routine. Simple alert rules can overwhelm security teams. CareShield explores context such as scheduled shifts, assigned patients, access bursts, device changes, failed logins and emergency overrides.

## Features

- Reproducible generator of **5,000 synthetic EHR access events** (adjustable in app)
- Interactive dashboard: event trends, role-level alerts and investigation queue
- Random Forest baseline with chronological 70/30 holdout and training-only preprocessing
- Holdout average precision, ROC-AUC, false-positive and false-negative counts
- Explicit scenario-level risk factors for analyst review (not model explanations)
- CSV export, automated tests, configurable experiment seed

## Quick start (macOS / Windows / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

To run tests:

```bash
python -m pytest -q
```

## Method

1. Simulate event timestamps, pseudonymous staff and patient tokens, roles, shift and assignment context, and access behaviour.
2. Generate **synthetic scenario alerts** with an openly specified rule in `src/pipeline.py`. This is a constructed target, **not independent ground truth**.
3. Sort events chronologically; fit preprocessing and Random Forest on the earliest 70%; evaluate on the latest 30%.
4. Review predicted probabilities alongside the scenario risk factors. Export selected events for investigation exercises.

**Interpretation warning:** Because the labels are generated from the same behavioural features, high scores mainly demonstrate how well the model learns the simulation's rules. They are **not evidence of real-world insider-threat detection performance**. A chronological split does not prevent the same simulated staff ID from appearing in both partitions.

## Repository map

```text
careshield-ai/
├── app.py                  # Streamlit analyst interface
├── src/pipeline.py         # Synthetic data + baseline evaluation
├── tests/test_pipeline.py  # Automated reproducibility tests
├── .streamlit/config.toml  # Dashboard theme
├── requirements.txt
├── LICENSE
└── README.md
```

## Research roadmap

- [ ] Independently label threat scenarios and add benign edge cases
- [ ] Compare against transparent rule-based baselines and isolation forest
- [ ] Grouped evaluation by staff member and simulated hospital
- [ ] Add calibration, precision-recall curves and threshold-cost analysis
- [ ] Explain model predictions with validated local explanation methods
- [ ] Model emergency-access workflows and fairness across clinical roles
- [ ] Security review, audit trail and privacy impact assessment

## Ethical use

No real patient information is required. All identifiers are synthetic. This is not a medical device, an EHR integration, a validated security detector or a replacement for human investigation.

## Author

**Tasnem Islam Prome** · Applied Computing | Data Analytics | Machine Learning & Research  
GitHub: [@tasnem-tech](https://github.com/tasnem-tech)

## License
MIT.
