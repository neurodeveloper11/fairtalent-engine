"""Fairness ML & Regulatory Compliance Auditor.

Implements the EEOC Four-Fifths Rule (80% Rule - 29 CFR § 1607.4(D)),
NYC Local Law 144 AEDT bias audit standards, and EU AI Act Annex III
High-Risk AI System compliance verification.
"""

import time
import uuid
from typing import Dict, List, Optional
import polars as pl

from src.domain.models import (
    CandidateRecord,
    DisparateImpactAudit,
    FairnessAuditReport,
    GroupSelectionMetric,
)
from src.domain.psychometrics import PsychometricEngine


class FairnessAuditor:
    """Enterprise Algorithmic Bias & Regulatory Compliance Auditor."""

    def __init__(self, eoc_threshold: float = 0.80):
        self.eeoc_threshold = eoc_threshold

    def audit_cohort(
        self,
        candidates: List[CandidateRecord],
        cutoff_threshold: float = 75.0,
        custom_audit_id: Optional[str] = None,
    ) -> FairnessAuditReport:
        """Execute comprehensive audit across protected classes and psychometric validity."""
        if not candidates:
            raise ValueError("Cannot audit an empty candidate cohort.")

        # 1. Classify selection decisions based on cutoff threshold
        evaluated_candidates = []
        for c in candidates:
            c_copy = c.model_copy()
            c_copy.selected = c.merit_score >= cutoff_threshold
            evaluated_candidates.append(c_copy)

        # 2. Build Polars DataFrame for high-performance vectorized grouping
        df = pl.DataFrame([
            {
                "candidate_id": c.candidate_id,
                "gender": c.gender.value,
                "age_group": c.age_group.value,
                "ethnicity": c.ethnicity.value,
                "merit_score": c.merit_score,
                "selected": 1 if c.selected else 0,
            }
            for c in evaluated_candidates
        ])

        total_evaluated = len(df)
        total_selected = int(df["selected"].sum())
        overall_selection_rate = round(total_selected / total_evaluated, 4) if total_evaluated > 0 else 0.0

        # 3. Audit each protected demographic attribute
        audits_by_attribute: Dict[str, DisparateImpactAudit] = {}
        all_selection_rates: List[float] = []

        for attr in ["gender", "age_group", "ethnicity"]:
            audit = self._audit_attribute(df, attr)
            audits_by_attribute[attr] = audit
            for m in audit.group_metrics.values():
                all_selection_rates.append(m.selection_rate)

        # 4. Demographic Parity Difference (DPD = max(rate) - min(rate))
        dpd = round(max(all_selection_rates) - min(all_selection_rates), 4) if all_selection_rates else 0.0

        # 5. Evaluate psychometric validity (Classical Test Theory)
        psychometrics = PsychometricEngine.evaluate_reliability(evaluated_candidates)

        # 6. Synthesize regulatory certifications
        has_any_adverse_impact = any(a.has_adverse_impact for a in audits_by_attribute.values())
        is_psychometrically_valid = psychometrics.is_valid_construct
        overall_compliance = (not has_any_adverse_impact) and is_psychometrically_valid

        # Regulatory checks
        nyc_certified = not has_any_adverse_impact
        if overall_compliance:
            eu_ai_act_status = "COMPLIANT: High-Risk AI Conformity requirements met (Annex III)."
            risk_summary = (
                "PASSED: The selection procedure satisfies the EEOC Four-Fifths rule across all demographic groups "
                f"and demonstrates solid psychometric reliability (Cronbach's α = {psychometrics.cronbach_alpha})."
            )
        elif has_any_adverse_impact and not is_psychometrically_valid:
            eu_ai_act_status = "NON-CONFORMANT: Multiple critical deficiencies in fairness and construct validity."
            risk_summary = (
                "CRITICAL VIOLATION: Disparate impact detected under 29 CFR § 1607.4(D) AND assessment instrument "
                f"lacks psychometric reliability (α = {psychometrics.cronbach_alpha} < 0.70)."
            )
        elif has_any_adverse_impact:
            eu_ai_act_status = "NON-CONFORMANT: Disparate impact detected under NYC LL144 / EU AI Act standards."
            risk_summary = (
                "ADVERSE IMPACT VIOLATION: Selection rates for at least one protected group fall below 80% "
                "of the reference group rate. Mitigation is legally required prior to deployment."
            )
        else:
            eu_ai_act_status = "CONDITIONAL: Fair selection rates, but psychometric construct validity is questionable."
            risk_summary = (
                f"PSYCHOMETRIC RISK: While selection rates are balanced, assessment reliability is low "
                f"(α = {psychometrics.cronbach_alpha} < 0.70), risking test invalidity under Title VII standards."
            )

        audit_id = custom_audit_id or f"AUDIT-{uuid.uuid4().hex[:8].upper()}"

        return FairnessAuditReport(
            audit_id=audit_id,
            timestamp=time.time(),
            total_evaluated=total_evaluated,
            selection_threshold=cutoff_threshold,
            overall_selection_rate=overall_selection_rate,
            psychometrics=psychometrics,
            audits_by_attribute=audits_by_attribute,
            demographic_parity_diff=dpd,
            overall_compliance=overall_compliance,
            regulatory_summary=risk_summary,
            nyc_local_law_144_certified=nyc_certified,
            eu_ai_act_annex_iii_status=eu_ai_act_status,
        )

    def _audit_attribute(self, df: pl.DataFrame, attribute: str) -> DisparateImpactAudit:
        """Calculate selection rates and adverse impact ratios for sub-categories of an attribute."""
        grouped = (
            df.group_by(attribute)
            .agg([
                pl.len().alias("total"),
                pl.col("selected").sum().alias("selected_count"),
            ])
            .with_columns(
                (pl.col("selected_count") / pl.col("total")).round(4).alias("rate")
            )
        )

        rows = grouped.to_dicts()
        if not rows:
            return DisparateImpactAudit(
                attribute_name=attribute,
                reference_group="NONE",
                group_metrics={},
                lowest_impact_ratio=1.0,
                has_adverse_impact=False,
                legal_risk_level="COMPLIANT",
            )

        # Baseline is group with highest selection rate
        max_rate = max(r["rate"] for r in rows)
        ref_row = max(rows, key=lambda r: r["rate"])
        reference_group = ref_row[attribute]

        group_metrics: Dict[str, GroupSelectionMetric] = {}
        lowest_impact_ratio = 1.0

        for r in rows:
            g_name = str(r[attribute])
            rate = float(r["rate"])
            if max_rate > 1e-9:
                impact_ratio = round(rate / max_rate, 4)
            else:
                impact_ratio = 1.0  # If nobody selected anywhere, ratio is 1.0

            if impact_ratio < lowest_impact_ratio:
                lowest_impact_ratio = impact_ratio

            eeoc_ok = impact_ratio >= self.eeoc_threshold

            group_metrics[g_name] = GroupSelectionMetric(
                group_name=g_name,
                total_applicants=int(r["total"]),
                total_selected=int(r["selected_count"]),
                selection_rate=rate,
                impact_ratio=impact_ratio,
                eeoc_compliant=eeoc_ok,
            )

        has_adverse_impact = lowest_impact_ratio < self.eeoc_threshold
        if lowest_impact_ratio >= 0.80:
            legal_risk = "COMPLIANT"
        elif lowest_impact_ratio >= 0.70:
            legal_risk = "MARGINAL_RISK"
        else:
            legal_risk = "CRITICAL_VIOLATION"

        return DisparateImpactAudit(
            attribute_name=attribute,
            reference_group=reference_group,
            group_metrics=group_metrics,
            lowest_impact_ratio=round(lowest_impact_ratio, 4),
            has_adverse_impact=has_adverse_impact,
            legal_risk_level=legal_risk,
        )
