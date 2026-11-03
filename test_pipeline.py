import pandas as pd
import pytest
from src.pipeline import generate_events, train_and_evaluate, explain_rules, rule_baseline

def test_reproducible():
    pd.testing.assert_frame_equal(generate_events(1000, 42), generate_events(1000, 42))

def test_different_seeds():
    assert not generate_events(1000, 42).equals(generate_events(1000, 43))

def test_schema_and_privacy():
    df = generate_events(1000)
    assert df.event_id.is_unique
    assert df.synthetic_alert.isin([0, 1]).all()
    assert not {'name', 'date_of_birth', 'nhs_number'}.intersection(df.columns)

def test_training_and_chronology():
    df = generate_events(5000)
    model, metrics, test = train_and_evaluate(df)
    assert len(test) == 1500
    assert df.iloc[3499].timestamp < test.iloc[0].timestamp
    assert 0 <= metrics['average_precision'] <= 1
    assert metrics['true_positives'] + metrics['false_positives'] + metrics['false_negatives'] + metrics['true_negatives'] == len(test)
    assert test.predicted_risk.between(0, 1).all()

def test_explanations_are_rule_factors_not_shap():
    row = generate_events(100).iloc[0]
    assert isinstance(explain_rules(row), str)

def test_baseline():
    df = generate_events(100)
    assert len(rule_baseline(df)) == len(df)

def test_too_few_events():
    with pytest.raises(ValueError): generate_events(10)
