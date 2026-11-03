"""Reproducible synthetic EHR access experiment. Not a real-world threat detector."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score, confusion_matrix, precision_score, recall_score, f1_score

FEATURES = ['hour', 'outside_shift', 'unassigned', 'failed_logins', 'access_count', 'emergency', 'role_code']
ROLES = ['Nurse', 'Doctor', 'Care Assistant', 'Administrator']

def generate_events(n=5000, seed=42):
    if n < 20:
        raise ValueError('At least 20 events required')
    rng = np.random.default_rng(int(seed))
    timestamps = pd.date_range('2026-01-01', periods=n, freq='15min')
    hour = timestamps.hour.to_numpy()
    roles = rng.choice(ROLES, n)
    outside = ((hour < 7) | (hour >= 20)).astype(int)
    unassigned = rng.binomial(1, .15, n)
    failed = rng.poisson(.35, n)
    count = rng.poisson(3, n) + 1
    emergency = rng.binomial(1, .09, n)
    # Labels deliberately derive from features; metrics only assess rule imitation.
    alert = (((unassigned == 1) & (emergency == 0) & ((outside == 1) | (count >= 6))) |
             ((failed >= 3) & (emergency == 0))).astype(int)
    return pd.DataFrame({'timestamp': timestamps, 'event_id': [f'E{i:06d}' for i in range(n)],
       'staff_id': [f'S{x:03d}' for x in rng.integers(0, 120, n)],
       'patient_token': [f'P{x:04d}' for x in rng.integers(0, 600, n)],
       'role': roles, 'hour': hour, 'outside_shift': outside, 'unassigned': unassigned,
       'failed_logins': failed, 'access_count': count, 'emergency': emergency,
       'role_code': pd.Categorical(roles, categories=ROLES).codes,
       'synthetic_alert': alert})

def explain_rules(row):
    factors = []
    if row['outside_shift']: factors.append('outside typical hours')
    if row['unassigned']: factors.append('not assigned to patient')
    if row['failed_logins'] >= 3: factors.append('multiple failed logins')
    if row['access_count'] >= 6: factors.append('high access count')
    if row['emergency']: factors.append('emergency context')
    return ', '.join(factors) if factors else 'no constructed risk factors'

def rule_baseline(df):
    # Deliberately simpler rule for a transparent comparator.
    return ((df['unassigned'] == 1) & (df['outside_shift'] == 1)).astype(int).to_numpy()

def train_and_evaluate(df):
    required = FEATURES + ['timestamp', 'synthetic_alert']
    if any(col not in df for col in required):
        raise ValueError('Missing required columns')
    data = df.sort_values('timestamp').copy()
    split = int(len(data) * .7)
    train, test = data.iloc[:split], data.iloc[split:].copy()
    if train.synthetic_alert.nunique() < 2 or test.synthetic_alert.nunique() < 2:
        raise ValueError('Both partitions must contain both classes')
    model = RandomForestClassifier(n_estimators=150, min_samples_leaf=3, random_state=42, n_jobs=1)
    model.fit(train[FEATURES], train['synthetic_alert'])
    probabilities = model.predict_proba(test[FEATURES])[:, 1]
    predictions = (probabilities >= .5).astype(int)
    test['predicted_risk'] = probabilities
    test['predicted_alert'] = predictions
    y = test['synthetic_alert'].to_numpy()
    tn, fp, fn, tp = confusion_matrix(y, predictions, labels=[0, 1]).ravel()
    metrics = {'sample_size': len(data), 'train_size': len(train), 'test_size': len(test),
       'train_positive_rate': float(train.synthetic_alert.mean()), 'test_positive_rate': float(test.synthetic_alert.mean()),
       'average_precision': float(average_precision_score(y, probabilities)),
       'roc_auc': float(roc_auc_score(y, probabilities)), 'precision': float(precision_score(y, predictions, zero_division=0)),
       'recall': float(recall_score(y, predictions, zero_division=0)),
       'f1': float(f1_score(y, predictions, zero_division=0)),
       'true_negatives': int(tn), 'false_positives': int(fp), 'false_negatives': int(fn), 'true_positives': int(tp)}
    return model, metrics, test
