# Research branch additions

The research branch restores the missing `src.pipeline` imported by `app.py`, adds deterministic synthetic generation, a chronological 70/30 evaluation, a simple-rule comparator, tests, experiment scripts, and a paper outline.

Run from the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 -m experiments.run_experiments --n 5000 --seeds 42 123 2026 --out results
python3 -m streamlit run app.py
```

The metrics in `experiments/RESULTS.md` were generated locally on 2026-11-03 with seven tests passing. Re-run them in your environment. **Do not interpret synthetic label prediction as detecting real EHR misuse.** The dashboard's `risk_factors` explains constructed scenario signals, not Random Forest decisions.

The existing README on `main` contains a clone-path typo (`careshild-ai`); use `careshield-ai` instead.
