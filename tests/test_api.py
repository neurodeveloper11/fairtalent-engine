"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_dashboard_html():
    """Verify root / serves HTML dashboard."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FairTalent-Engine" in response.text
    assert "EEOC 4/5ths" in response.text


def test_health_check():
    """Verify /health returns 200 healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "FairTalent-Engine"


def test_simulate_scenario():
    """Verify /api/v1/simulate returns a full audit report."""
    response = client.get("/api/v1/simulate/biased_tech_ats?threshold=75&candidates_count=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total_evaluated"] == 100
    assert "psychometrics" in data
    assert "audits_by_attribute" in data
    assert "gender" in data["audits_by_attribute"]


def test_audit_custom_cohort_endpoint():
    """Verify /api/v1/audit/cohort accepts candidate list and returns report."""
    candidates_payload = [
        {
            "candidate_id": "C-1",
            "gender": "MALE",
            "age_group": "UNDER_40",
            "ethnicity": "MAJORITY",
            "test_items": [4.0, 4.0, 3.5],
            "merit_score": 85.0,
        },
        {
            "candidate_id": "C-2",
            "gender": "FEMALE",
            "age_group": "UNDER_40",
            "ethnicity": "MAJORITY",
            "test_items": [4.0, 4.0, 4.0],
            "merit_score": 88.0,
        },
    ]
    response = client.post("/api/v1/audit/cohort?cutoff_threshold=80", json=candidates_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_evaluated"] == 2
    assert data["overall_selection_rate"] == 1.0


def test_mitigate_endpoint():
    """Verify /api/v1/mitigate triggers threshold tuning."""
    payload = {
        "target_attribute": "gender",
        "desired_min_impact_ratio": 0.80,
        "baseline_threshold": 75.0,
    }
    response = client.post("/api/v1/mitigate?scenario=biased_tech_ats", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_attribute"] == "gender"
    assert data["mitigated_impact_ratio"] >= 0.80


def test_compliance_certificate_endpoint():
    """Verify /api/v1/compliance/certificate exports compliance audit trail."""
    response = client.get("/api/v1/compliance/certificate?scenario=compliant_fair_pipeline&threshold=70")
    assert response.status_code == 200
    data = response.json()
    assert "audit_metadata" in data
    assert "psychometric_validation" in data
    assert "certification_status" in data
