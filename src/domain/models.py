"""Pydantic v2 data models for FairTalent-Engine.

Strict validation contracts for applicants, psychometric properties,
fairness audits, EEOC compliance, and mitigation outcomes.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class Gender(str, Enum):
    """Demographic gender category."""
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"


class AgeGroup(str, Enum):
    """Age bracket aligned with ADEA (Age Discrimination in Employment Act)."""
    UNDER_40 = "UNDER_40"
    OVER_40 = "OVER_40"


class Ethnicity(str, Enum):
    """Demographic ethnicity category."""
    MAJORITY = "MAJORITY"
    MINORITY_A = "MINORITY_A"
    MINORITY_B = "MINORITY_B"


class BenchmarkScenario(str, Enum):
    """Preconfigured benchmark datasets for demonstration and stress testing."""
    BIASED_TECH_ATS = "biased_tech_ats"
    AGE_PENALIZED_EXEC = "age_penalized_exec"
    COMPLIANT_FAIR_PIPELINE = "compliant_fair_pipeline"


class CandidateRecord(BaseModel):
    """Individual candidate record containing demographic data and test telemetry."""
    candidate_id: str = Field(..., description="Unique applicant identifier")
    gender: Gender = Field(..., description="Gender identifier for parity tracking")
    age_group: AgeGroup = Field(..., description="Age category (<40 vs >=40)")
    ethnicity: Ethnicity = Field(..., description="Demographic ethnicity slice")
    test_items: List[float] = Field(..., description="Individual psychometric item scores (0-5 or 0-1)")
    merit_score: float = Field(..., ge=0.0, le=100.0, description="Overall evaluated competency/merit score (0-100)")
    selected: Optional[bool] = Field(None, description="Binary selection outcome based on cutoff threshold")

    @field_validator("test_items")
    @classmethod
    def validate_test_items(cls, items: List[float]) -> List[float]:
        if not items:
            raise ValueError("Candidate must have at least one test item response.")
        return items


class PsychometricMetrics(BaseModel):
    """Classical Test Theory (CTT) psychometric reliability audit."""
    num_items: int = Field(..., description="Number of psychometric assessment items evaluated")
    num_candidates: int = Field(..., description="Sample size of evaluated test takers")
    cronbach_alpha: float = Field(..., description="Cronbach's alpha internal consistency coefficient")
    internal_consistency: str = Field(..., description="Qualitative rating (EXCELLENT, GOOD, ACCEPTABLE, POOR)")
    standard_error_measurement: float = Field(..., description="Standard Error of Measurement (SEM)")
    item_discriminations: Dict[str, float] = Field(..., description="Corrected item-total correlation per item")
    is_valid_construct: bool = Field(..., description="Whether Cronbach's Alpha meets regulatory baseline (>= 0.70)")


class GroupSelectionMetric(BaseModel):
    """Statistical selection indicators for a demographic subgroup."""
    group_name: str
    total_applicants: int
    total_selected: int
    selection_rate: float = Field(..., ge=0.0, le=1.0, description="Selection rate (Selected / Total)")
    impact_ratio: float = Field(..., ge=0.0, description="Selection rate relative to highest-performing group")
    eeoc_compliant: bool = Field(..., description="True if impact_ratio >= 0.80 (Four-Fifths Rule)")


class DisparateImpactAudit(BaseModel):
    """EEOC Four-Fifths & Disparate Impact audit for a specific protected attribute."""
    attribute_name: str = Field(..., description="Protected attribute evaluated (e.g., gender, age_group)")
    reference_group: str = Field(..., description="Baseline group with highest selection rate")
    group_metrics: Dict[str, GroupSelectionMetric]
    lowest_impact_ratio: float = Field(..., description="Lowest Disparate Impact Ratio observed in cohort")
    has_adverse_impact: bool = Field(..., description="True if any group violates the Four-Fifths (80%) rule")
    legal_risk_level: str = Field(..., description="COMPLIANT, MARGINAL_RISK, or CRITICAL_VIOLATION")


class FairnessAuditReport(BaseModel):
    """Master executive audit certificate for NYC LL144, EEOC, and EU AI Act compliance."""
    audit_id: str
    timestamp: float
    total_evaluated: int
    selection_threshold: float
    overall_selection_rate: float
    psychometrics: PsychometricMetrics
    audits_by_attribute: Dict[str, DisparateImpactAudit]
    demographic_parity_diff: float = Field(..., description="Max difference in selection rates across subgroups")
    overall_compliance: bool = Field(..., description="True only if all attributes satisfy EEOC 80% Rule and CTT validity")
    regulatory_summary: str
    nyc_local_law_144_certified: bool
    eu_ai_act_annex_iii_status: str


class MitigationRequest(BaseModel):
    """Parameters for threshold tuning and adverse impact elimination."""
    target_attribute: str = Field("gender", description="Attribute to optimize (gender, age_group, ethnicity)")
    desired_min_impact_ratio: float = Field(0.80, ge=0.50, le=1.0, description="Target minimum DIR (default 0.80)")
    baseline_threshold: float = Field(75.0, ge=0.0, le=100.0, description="Initial naive global threshold")


class MitigationResult(BaseModel):
    """Outcome of Pareto-optimal threshold calibration."""
    target_attribute: str
    original_impact_ratio: float
    mitigated_impact_ratio: float
    calibrated_thresholds: Dict[str, float]
    mean_selected_merit_before: float
    mean_selected_merit_after: float
    merit_efficiency_loss_percent: float
    eeoc_violation_resolved: bool
    description: str
