"""Tests for ThresholdMitigationEngine (Post-processing Pareto tuning)."""

import pytest
from src.domain.generator import SyntheticCohortGenerator
from src.domain.mitigation import ThresholdMitigationEngine
from src.domain.models import BenchmarkScenario, MitigationRequest


def test_calibrate_thresholds_resolves_gender_bias():
    """Verify mitigation engine tunes cutoffs to satisfy EEOC 80% rule."""
    cohort = SyntheticCohortGenerator.generate_scenario(BenchmarkScenario.BIASED_TECH_ATS, n_candidates=400)
    mitigator = ThresholdMitigationEngine()

    request = MitigationRequest(
        target_attribute="gender",
        desired_min_impact_ratio=0.80,
        baseline_threshold=75.0,
    )

    result = mitigator.calibrate_thresholds(cohort, request)

    assert result.original_impact_ratio < 0.80
    assert result.mitigated_impact_ratio >= 0.80
    assert result.eeoc_violation_resolved is True
    assert result.mean_selected_merit_after > 0.0
    # Merit efficiency loss should be small (< 10%)
    assert result.merit_efficiency_loss_percent < 10.0
    assert "FEMALE" in result.calibrated_thresholds
    assert "MALE" in result.calibrated_thresholds


def test_calibrate_thresholds_invalid_attribute():
    """Verify error on nonexistent protected attribute."""
    cohort = SyntheticCohortGenerator.generate_scenario(BenchmarkScenario.COMPLIANT_FAIR_PIPELINE, n_candidates=50)
    mitigator = ThresholdMitigationEngine()

    request = MitigationRequest(
        target_attribute="nonexistent_attr",
        desired_min_impact_ratio=0.80,
        baseline_threshold=75.0,
    )

    with pytest.raises(ValueError):
        mitigator.calibrate_thresholds(cohort, request)
