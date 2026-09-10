# FairTalent-Engine ⚖️⚡

[![CI](https://github.com/neurodeveloper11/fairtalent-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/neurodeveloper11/fairtalent-engine/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Async_REST-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2_Strict-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://pydantic.dev)
[![Polars](https://img.shields.io/badge/Polars-Vectorized_OLAP-CD792C?style=flat-square&logo=polars&logoColor=white)](https://pola.rs)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/PyTest-100%25_PASS-brightgreen?style=flat-square&logo=pytest&logoColor=white)](tests/)
[![Compliance](https://img.shields.io/badge/Compliance-EEOC_%E2%80%A2_NYC_LL144_%E2%80%A2_EU_AI_Act-blue?style=flat-square)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

An enterprise-grade, high-throughput **Fair Machine Learning (Fair ML)** auditing pipeline and psychometric integrity engine designed for AI-assisted talent acquisition. 

Audits automated recruitment systems against the **EEOC Four-Fifths Rule (29 CFR § 1607.4(D))**, **NYC Local Law 144 (AEDT Bias Audits)**, and **EU AI Act Annex III (High-Risk AI in Employment)**, coupling Classical Test Theory construct validation ($\alpha \ge 0.70$) with automated Pareto threshold mitigation.

Designed and engineered by **[Fabio Torres](https://github.com/neurodeveloper11)** (M.Sc. in Data Engineering & Cloud Infrastructure • 10+ Years Behavioral & Cognitive Psychology Leadership).

---

## 🧠 The Domain Moat: "Del Diván al Dato"

In automated recruitment and talent acquisition (HRTech), large-scale machine learning filters and ATS screening models routinely introduce latent discrimination against protected demographic groups (gender, age, ethnicity). Traditional algorithmic solutions fail because:

1. **Software Engineers and Data Scientists** know how to deploy XGBoost or vector databases, but **do not understand psychometric construct validity, Classical Test Theory (CTT), item discrimination ($r_{bis}$), or federal employment law standards**.
2. **HR Practitioners and Industrial Psychologists** understand Title VII and test administration, but **cannot engineer distributed Polars pipelines, write vectorized async APIs, or automate post-processing mitigation algorithms**.

**FairTalent-Engine** bridges this chasm:

```mermaid
graph TD
    subgraph BehavioralDomain ["Behavioral & Cognitive Science (10+ Years)"]
        B1["Classical Test Theory (Cronbach's α, SEM)"]
        B2["Item Discrimination & Construct Reliability"]
        B3["Title VII & EEOC Selection Protocol Standards"]
    end

    subgraph DataEngineering ["High-Performance Data Engineering"]
        D1["Pydantic v2 Contract Validation"]
        D2["Vectorized Polars Cohort Ingestion"]
        D3["Async High-Throughput FastAPI Microservices"]
    end

    subgraph FairnessDelivery ["Fairness ML & Regulatory Compliance"]
        F1["EEOC 80% Rule & Disparate Impact Ratio (DIR)"]
        F2["Pareto Optimal Post-Processing Threshold Calibration"]
        F3["Automated NYC LL144 & EU AI Act Audit Certificates"]
    end

    BehavioralDomain --> FairnessDelivery
    DataEngineering --> FairnessDelivery

    style BehavioralDomain fill:#0f172a,stroke:#34d399,stroke-width:1px,color:#f8fafc
    style DataEngineering fill:#0f172a,stroke:#38bdf8,stroke-width:1px,color:#f8fafc
    style FairnessDelivery fill:#1e293b,stroke:#a855f7,stroke-width:2px,color:#f8fafc
```

---

## 🏗️ System Architecture & Event Flow

```mermaid
flowchart LR
    subgraph Ingestion ["1. Applicant Ingestion"]
        AP["Applicant Records<br>• Demographics (Gender, Age, Race)<br>• Psychometric Test Items<br>• Candidate Merit Score"]
        VAL["Pydantic v2 Contracts<br><code>CandidateRecord</code>"]
        AP --> VAL
    end

    subgraph AuditCore ["2. Dual Audit Engine"]
        CTT["Psychometric Engine<br>• Cronbach's Alpha (α)<br>• Item-Total Correlation<br>• Standard Error (SEM)"]
        FAIR["Fair ML Auditor (Polars)<br>• Group Selection Rates<br>• Disparate Impact Ratio (DIR)<br>• Four-Fifths 80% Gate"]
        VAL --> CTT
        VAL --> FAIR
    end

    subgraph MitigationEngine ["3. Post-Processing Mitigation"]
        MIT["Threshold Calibrator<br>• Group Cutoff Tuning<br>• DIR ≥ 0.80 Resolution<br>• &gt;95% Merit Preservation"]
        FAIR -->|Adverse Impact Detected| MIT
    end

    subgraph Serving ["4. Serving & Compliance"]
        API["FastAPI Async REST API<br><code>/api/v1/audit/cohort</code><br><code>/api/v1/simulate/{scenario}</code>"]
        DASH["Interactive Off-White Web UI<br>1-Click Scenario Simulation & Telemetry"]
        CERT["Regulatory Audit Certificate<br>NYC LL144 & EU AI Act JSON"]
        
        FAIR --> API
        MIT --> API
        API --> DASH
        API --> CERT
    end

    style Ingestion fill:#0f172a,stroke:#38bdf8,stroke-width:1px,color:#f8fafc
    style AuditCore fill:#0f172a,stroke:#34d399,stroke-width:1px,color:#f8fafc
    style MitigationEngine fill:#0f172a,stroke:#f59e0b,stroke-width:1px,color:#f8fafc
    style Serving fill:#1e293b,stroke:#10b981,stroke-width:2px,color:#f8fafc
```

---

## 📐 Mathematical & Regulatory Foundations

### 1. EEOC Four-Fifths Rule (Disparate Impact Ratio)
Under **29 CFR § 1607.4(D)**, if the selection rate of a protected demographic group is less than 80% (4/5ths) of the highest selecting group, the selection tool possesses **Adverse Impact**:

$$\text{DIR} = \frac{\text{Selection Rate}_{\text{Minority Group}}}{\text{Selection Rate}_{\text{Reference Group}}} \ge 0.80$$

If $\text{DIR} < 0.80$, the system generates a **Critical Legal Violation** warning.

### 2. Psychometric Construct Reliability (Cronbach's Alpha)
Under Title VII employment litigation, an employer cannot defend a selection test unless it demonstrates proven construct validity:

$$\alpha = \frac{K}{K - 1} \left( 1 - \frac{\sum_{i=1}^K \sigma_i^2}{\sigma_X^2} \right)$$

Where $K$ is the item count, $\sigma_i^2$ is individual item variance, and $\sigma_X^2$ is aggregate test score variance. Baseline regulatory validity requires $\alpha \ge 0.70$.

### 3. Standard Error of Measurement ($SEM$)
Quantifies score uncertainty around decision cutoffs:

$$SEM = \sigma_X \sqrt{1 - \alpha}$$

---

## 🚀 Live Interactive Dashboard

The engine includes a zero-dependency, executive **Off-White / Dark Mode Dashboard** served directly at `GET /`:

* **1-Click Benchmark Cohort Simulation:**
  * `Biased Tech ATS`: Simulates uncalibrated resume parsers penalizing female technical candidates ($\text{DIR} \approx 0.46$).
  * `Executive Leadership Screening`: Simulates automated tests penalizing candidates $\ge 40$ years old (ADEA violation).
  * `Calibrated Pipeline`: Demonstrates full compliance across all demographic categories.
* **Interactive Cutoff Slider:** Adjust selection cutoffs in real time ($50.0$ to $92.0$) and watch adverse impact ratios and selection rates update dynamically.
* **Automated Fair-ML Mitigation Button:** Automatically computes group-specific cutoffs to resolve the EEOC violation while retaining over $95\%$ of original talent merit.
* **Audit Certificate Exporter:** Generates an official, structured compliance certificate aligned with NYC Local Law 144 and EU AI Act Annex III standards.

---

## 🔌 API Reference & Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the interactive executive web dashboard |
| `GET` | `/health` | System health check and regulatory framework status |
| `GET` | `/api/v1/simulate/{scenario}` | Simulates and audits a synthetic cohort (`biased_tech_ats`, `age_penalized_exec`, `compliant_fair_pipeline`) |
| `POST` | `/api/v1/audit/cohort` | Audits an uploaded batch of candidate records |
| `POST` | `/api/v1/mitigate` | Executes Pareto threshold calibration to eliminate adverse impact |
| `GET` | `/api/v1/compliance/certificate` | Generates a certified audit trail payload for legal compliance officers |

Interactive OpenAPI documentation is available at `/docs` (Swagger) and `/redoc`.

---

## 🛠️ Quickstart Guide

### 1. Local Setup
```bash
# Clone repository
git clone https://github.com/neurodeveloper11/fairtalent-engine.git
cd fairtalent-engine

# Install dependencies
pip install -r requirements.txt

# Run test suite (100% pass)
python -m pytest -v tests/

# Launch development server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Visit `http://localhost:8000` for the dashboard and `http://localhost:8000/docs` for the interactive API explorer.

### 2. Docker Deployment
```bash
# Build and launch with Docker Compose
docker-compose up --build -d

# Check health status
curl http://localhost:8000/health
```

---

## 🧪 Testing & Validation Suite

The test suite covers psychometric accuracy, boundary edge cases, regulatory thresholds, and API handlers:

```bash
python -m pytest -v tests/
```

Test coverage includes:
* `test_psychometrics.py`: Verification of Cronbach's alpha, item discrimination, zero-variance handling, and Sten conversions.
* `test_fairness_auditor.py`: EEOC 80% rule validation, adverse impact detection, and regulatory synthesis.
* `test_mitigation.py`: Post-processing Pareto threshold tuning, merit score retention, and DIR resolution.
* `test_generator.py`: Deterministic synthetic cohort generation across standard hiring scenarios.
* `test_api.py`: FastAPI endpoints, error handling, contract validation, and certificate generation.

---

## 📄 License & Intellectual Property

Distributed under the **MIT License**. See `LICENSE` for details.

*All applicant cohorts, candidate names, and simulation figures are 100% synthetic, generated for algorithmic demonstration and benchmark testing.*
