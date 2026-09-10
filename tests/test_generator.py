"""Tests for SyntheticCohortGenerator."""

import pytest
from src.domain.generator import SyntheticCohortGenerator
from src.domain.models import BenchmarkScenario


def test_generate_biased_tech_ats():
    """Verify synthetic generation of biased ATS scenario."""
    cohort = SyntheticCohortGenerator.generate_scenario(BenchmarkScenario.BIASED_TECH_ATS, n_candidates=200)
    assert len(cohort) == 200
    assert all(len(c.test_items) == 6 for c in cohort)
    assert all(15.0 <= c.merit_score <= 100.0 for c in cohort)


def test_generate_age_penalized_exec():
    """Verify generation of age penalized executive scenario."""
    cohort = SyntheticCohortGenerator.generate_scenario(BenchmarkScenario.AGE_PENALIZED_EXEC, n_candidates=150)
    assert len(cohort) == 150
    assert all(len(c.test_items) == 5 for c in cohort)


def test_generate_compliant_pipeline():
    """Verify generation of fully compliant talent pipeline."""
    cohort = SyntheticCohortGenerator.generate_scenario(BenchmarkScenario.COMPLIANT_FAIR_PIPELINE, n_candidates=100)
    assert len(cohort) == 100
    assert all(len(c.test_items) == 8 for c in cohort)


def test_invalid_scenario():
    """Verify error on invalid scenario."""
    with pytest.raises(ValueError):
        SyntheticCohortGenerator.generate_scenario("invalid_scenario_name", n_candidates=50)
