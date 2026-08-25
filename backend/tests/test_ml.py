import pytest
from app.ml.synthetic_generator import SyntheticPatternGenerator
from app.ml.eval_pipeline import PatternEvaluator

def test_synthetic_generator_amigurumi():
    sample = SyntheticPatternGenerator.generate_amigurumi_sphere(start_count=6, max_rounds=6)
    assert "written_pattern" in sample
    assert "structured_ast" in sample
    assert "expected_chart" in sample
    assert len(sample["structured_ast"]["units"]) > 0

def test_synthetic_generator_batch():
    batch = SyntheticPatternGenerator.generate_batch(5)
    assert len(batch) == 5

def test_ml_eval_pipeline():
    batch = SyntheticPatternGenerator.generate_batch(6)
    metrics = PatternEvaluator.evaluate_dataset(batch)
    assert metrics["total_samples"] == 6
    assert metrics["overall_score"] > 0
    assert "ast_accuracy" in metrics
