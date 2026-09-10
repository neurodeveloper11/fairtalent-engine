"""Tests for FairnessAuditor (EEOC 80% Rule & Regulatory Checks)."""

import pytest
from src.domain.fairness_auditor import FairnessAuditor
from src.domain.models import AgeGroup, CandidateRecord, Ethnicity, Gender


def test_audit_cohort_detects_adverse_impact():
    """Verify that an artificial cohort with unequal selection triggers an EEOC violation."""
    candidates = []

    # 100 Males: 80 score high (85.0), 20 score low (50.0) -> Selection rate ~80%
    for i in range(100):
        score = 85.0 if i < 80 else 50.0
        candidates.append(
            CandidateRecord(
                candidate_id=f"MALE-{i}",
                gender=Gender.MALE,
                age_group=AgeGroup.UNDER_40,
                ethnicity=Ethnicity.MAJORITY,
                test_items=[4.0, 4.0, 3.5, 4.5],
                merit_score=score,
            )
        )

    # 100 Females: 30 score high (85.0), 70 score low (50.0) -> Selection rate ~30%
    # DIR = 30% / 80% = 0.375 < 0.80 -> Severe EEOC Violation
    for i in range(100):
        score = 85.0 if i < 30 else 50.0
        candidates.append(
            CandidateRecord(
                candidate_id=f"FEMALE-{i}",
                gender=Gender.FEMALE,
                age_group=AgeGroup.UNDER_40,
                ethnicity=Ethnicity.MAJORITY,
                test_items=[4.0, 3.8, 3.7, 4.1],
                merit_score=score,
            )
        )

    auditor = FairnessAuditor(eoc_threshold=0.80)
    report = auditor.audit_cohort(candidates, cutoff_threshold=75.0)

    gender_audit = report.audits_by_attribute["gender"]
    assert gender_audit.has_adverse_impact is True
    assert gender_audit.lowest_impact_ratio < 0.80
    assert gender_audit.reference_group == "MALE"
    assert gender_audit.legal_risk_level == "CRITICAL_VIOLATION"
    assert report.overall_compliance is False
    assert report.nyc_local_law_144_certified is False
    assert "NON-CONFORMANT" in report.eu_ai_act_annex_iii_status


def test_audit_cohort_compliant_fairness():
    """Verify that an evenly balanced cohort passes EEOC standards."""
    candidates = []
    # Both groups have 50% selection rate
    for i in range(50):
        candidates.append(
            CandidateRecord(
                candidate_id=f"C1-{i}",
                gender=Gender.MALE,
                age_group=AgeGroup.UNDER_40,
                ethnicity=Ethnicity.MAJORITY,
                test_items=[3.5, 4.0, 4.0, 3.5],
                merit_score=80.0 if i < 25 else 60.0,
            )
        )
        candidates.append(
            CandidateRecord(
                candidate_id=f"C2-{i}",
                gender=Gender.FEMALE,
                age_group=AgeGroup.UNDER_40,
                ethnicity=Ethnicity.MAJORITY,
                test_items=[3.5, 4.0, 4.0, 3.5],
                merit_score=80.0 if i < 25 else 60.0,
            )
        )

    auditor = FairnessAuditor()
    report = auditor.audit_cohort(candidates, cutoff_threshold=70.0)

    gender_audit = report.audits_by_attribute["gender"]
    assert gender_audit.has_adverse_impact is False
    assert gender_audit.lowest_impact_ratio >= 0.80
    assert gender_audit.legal_risk_level == "COMPLIANT"
    assert report.nyc_local_law_144_certified is True


def test_audit_empty_cohort_raises_error():
    """Verify empty candidate cohort triggers ValueError."""
    auditor = FairnessAuditor()
    with pytest.raises(ValueError):
        auditor.audit_cohort([])
