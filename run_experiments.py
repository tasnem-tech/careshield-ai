"""Run reproducible synthetic benchmarks. No operational validity claims."""
import argparse
import json
from pathlib import Path
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from src.pipeline import generate_events, train_and_evaluate, rule_baseline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=5000)
    parser.add_argument('--seeds', type=int, nargs='+', default=[42, 123, 2026])
    parser.add_argument('--out', default='results')
    args = parser.parse_args()
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in args.seeds:
        df = generate_events(args.n, seed)
        _, metrics, test = train_and_evaluate(df)
        baseline = rule_baseline(test)
        y = test.synthetic_alert
        rows.append({'seed': seed, 'model': 'Random Forest', **metrics})
        rows.append({'seed': seed, 'model': 'Simple contextual rule', 'sample_size': len(df),
                     'train_size': metrics['train_size'], 'test_size': len(test),
                     'precision': precision_score(y, baseline, zero_division=0),
                     'recall': recall_score(y, baseline, zero_division=0),
                     'f1': f1_score(y, baseline, zero_division=0),
                     'false_positives': int(((baseline == 1) & (y == 0)).sum()),
                     'false_negatives': int(((baseline == 0) & (y == 1)).sum())})
    result = pd.DataFrame(rows)
    result.to_csv(output / 'benchmark.csv', index=False)
    (output / 'run_config.json').write_text(json.dumps({'n': args.n, 'seeds': args.seeds,
       'data': 'synthetic', 'label_warning': 'Constructed labels are not independently validated incidents'}, indent=2))
    print(result.to_string(index=False))
if __name__ == '__main__':
    main()
