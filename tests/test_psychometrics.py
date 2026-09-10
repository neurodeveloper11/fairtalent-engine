"""Tests for PsychometricEngine (Classical Test Theory)."""

import pytest
from src.domain.models import AgeGroup, CandidateRecord, Ethnicity, Gender
from src.domain.psychometrics import PsychometricEngine


def test_evaluate_reliability_consistent_items():
    """Verify Cronbach's alpha calculation on strongly correlated test items."""
    candidates = []
    for i in range(100):
        val = (i % 5) + 1.0
        candidates.append(
            CandidateRecord(
                candidate_id=f"TEST-{i}",
                gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                age_group=AgeGroup.UNDER_40,
                ethnicity=Ethnicity.MAJORITY,
                test_items=[val, val, val + 0.1, val - 0.1, val],
                merit_score=75.0,
            )
        )

    metrics = PsychometricEngine.evaluate_reliability(candidates)
    assert metrics.num_items == 5
    assert metrics.num_candidates == 100
    assert metrics.cronbach_alpha >= 0.90
    assert metrics.internal_consistency == "EXCELLENT"
    assert metrics.is_valid_construct is True
    assert metrics.standard_error_measurement >= 0.0
    assert len(metrics.item_discriminations) == 5


def test_evaluate_reliability_empty_cohort():
    """Verify ValueError is raised on empty cohort."""
    with pytest.raises(ValueError):
        PsychometricEngine.evaluate_reliability([])


def test_evaluate_reliability_zero_variance():
    """Verify edge case where all candidate scores are identical."""
    candidates = [
        CandidateRecord(
            candidate_id=f"TEST-{i}",
            gender=Gender.MALE,
            age_group=AgeGroup.UNDER_40,
            ethnicity=Ethnicity.MAJORITY,
            test_items=[3.0, 3.0, 3.0],
            merit_score=50.0,
        )
        for i in range(10)
    ]
    metrics = PsychometricEngine.evaluate_reliability(candidates)
    assert metrics.cronbach_alpha == 0.0
    assert metrics.internal_consistency == "POOR"
    assert metrics.is_valid_construct is False


def test_calculate_sten_scores():
    """Verify Sten scores are properly mapped to integers between 1 and 10."""
    scores = [20.0, 40.0, 50.0, 60.0, 80.0, 95.0]
    stens = PsychometricEngine.calculate_sten_scores(scores)
    assert len(stens) == len(scores)
    assert all(1 <= s <= 10 for s in stens)
    assert stens[0] < stens[-1]  # Lowest score gets lower Sten than highest
