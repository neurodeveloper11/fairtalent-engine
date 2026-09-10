"""FastAPI Route Handlers for FairTalent-Engine.

Provides interactive dashboard serving, real-time cohort audits,
benchmark simulations, automated threshold mitigation, and compliance exports.
"""

import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import HTMLResponse

from src.domain.fairness_auditor import FairnessAuditor
from src.domain.generator import SyntheticCohortGenerator
from src.domain.mitigation import ThresholdMitigationEngine
from src.domain.models import (
    BenchmarkScenario,
    CandidateRecord,
    FairnessAuditReport,
    MitigationRequest,
    MitigationResult,
)
from src.ui import render_fairness_dashboard

router = APIRouter()
_AUDITOR = FairnessAuditor()
_MITIGATOR = ThresholdMitigationEngine(_AUDITOR)


@router.get("/", response_class=HTMLResponse, tags=["Dashboard"])
async def get_interactive_dashboard():
    """Serve the interactive executive dashboard and educational simulator."""
    return HTMLResponse(content=render_fairness_dashboard())


@router.get("/health", tags=["System"])
async def health_check():
    """Service health and telemetry status endpoint."""
    return {
        "status": "healthy",
        "service": "FairTalent-Engine",
        "version": "1.0.0",
        "regulations_supported": ["EEOC 29 CFR § 1607", "NYC Local Law 144", "EU AI Act Annex III"],
        "timestamp": time.time(),
    }


@router.get("/api/v1/simulate/{scenario}", response_model=FairnessAuditReport, tags=["Simulation"])
async def simulate_benchmark_cohort(
    scenario: BenchmarkScenario,
    threshold: float = Query(75.0, ge=40.0, le=95.0, description="Selection score cutoff"),
    candidates_count: int = Query(500, ge=50, le=5000, description="Number of synthetic applicants"),
):
    """Generate and immediately audit a realistic hiring cohort under standard scenarios."""
    try:
        cohort = SyntheticCohortGenerator.generate_scenario(scenario, n_candidates=candidates_count)
        report = _AUDITOR.audit_cohort(cohort, cutoff_threshold=threshold)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation error: {str(e)}",
        )


@router.post("/api/v1/audit/cohort", response_model=FairnessAuditReport, tags=["Auditing"])
async def audit_custom_cohort(
    candidates: List[CandidateRecord],
    cutoff_threshold: float = Query(75.0, ge=0.0, le=100.0),
    audit_id: Optional[str] = Query(None),
):
    """Audit a custom list of candidate records for EEOC 4/5ths compliance and CTT validity."""
    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate cohort cannot be empty.",
        )
    try:
        report = _AUDITOR.audit_cohort(
            candidates,
            cutoff_threshold=cutoff_threshold,
            custom_audit_id=audit_id,
        )
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit execution failure: {str(e)}",
        )


@router.post("/api/v1/mitigate", response_model=MitigationResult, tags=["Mitigation"])
async def calibrate_thresholds_for_fairness(
    request: MitigationRequest,
    scenario: BenchmarkScenario = Query(BenchmarkScenario.BIASED_TECH_ATS),
):
    """Perform post-processing Pareto threshold tuning to eliminate adverse impact."""
    try:
        cohort = SyntheticCohortGenerator.generate_scenario(scenario, n_candidates=500)
        result = _MITIGATOR.calibrate_thresholds(cohort, request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Mitigation failure: {str(e)}",
        )


@router.get("/api/v1/compliance/certificate", tags=["Compliance"])
async def export_compliance_certificate(
    scenario: BenchmarkScenario = Query(BenchmarkScenario.BIASED_TECH_ATS),
    threshold: float = Query(75.0),
):
    """Export formal audit certification for legal/compliance review."""
    cohort = SyntheticCohortGenerator.generate_scenario(scenario, n_candidates=500)
    report = _AUDITOR.audit_cohort(cohort, cutoff_threshold=threshold)

    return {
        "certificate_type": "AEDT Independent Bias Audit & Psychometric Integrity Certification",
        "standards": {
            "us_federal": "EEOC Uniform Guidelines on Employee Selection Procedures (29 CFR § 1607.4(D))",
            "nyc_municipal": "NYC Administrative Code Title 20, Chapter 5 (NYC Local Law 144)",
            "european_union": "Regulation (EU) 2024/1689 (EU AI Act - Annex III High-Risk Classification)",
            "psychometrics": "Standards for Educational and Psychological Testing (AERA, APA, NCME)",
        },
        "audit_metadata": {
            "audit_id": report.audit_id,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(report.timestamp)),
            "audited_sample_size": report.total_evaluated,
            "cutoff_threshold": report.selection_threshold,
            "overall_selection_rate": f"{report.overall_selection_rate * 100:.2f}%",
        },
        "psychometric_validation": {
            "cronbach_alpha": report.psychometrics.cronbach_alpha,
            "construct_status": report.psychometrics.internal_consistency,
            "standard_error_measurement": report.psychometrics.standard_error_measurement,
            "is_valid_construct": report.psychometrics.is_valid_construct,
        },
        "adverse_impact_summary": {
            attr: {
                "reference_group": audit.reference_group,
                "lowest_impact_ratio": audit.lowest_impact_ratio,
                "adverse_impact_detected": audit.has_adverse_impact,
                "legal_risk": audit.legal_risk_level,
                "group_rates": {
                    g: f"{m.selection_rate * 100:.1f}% (DIR: {m.impact_ratio:.2f})"
                    for g, m in audit.group_metrics.items()
                },
            }
            for attr, audit in report.audits_by_attribute.items()
        },
        "certification_status": {
            "overall_compliant": report.overall_compliance,
            "nyc_local_law_144_certified": report.nyc_local_law_144_certified,
            "eu_ai_act_annex_iii_status": report.eu_ai_act_annex_iii_status,
            "auditor_authority": "Fabio Torres (Licensed Psychologist • M.Sc. Data Engineering & Cloud Infrastructure)",
        },
    }
