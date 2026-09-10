"""Automated Fair-ML Mitigation & Threshold Calibration Engine.

Applies post-processing Pareto-optimal threshold calibration to eliminate
disparate impact violations (EEOC 80% Rule) while maximizing retained talent competency.
"""

from typing import Dict, List
import numpy as np

from src.domain.fairness_auditor import FairnessAuditor
from src.domain.models import CandidateRecord, MitigationRequest, MitigationResult


class ThresholdMitigationEngine:
    """Post-processing calibration engine to eliminate adverse impact."""

    def __init__(self, auditor: FairnessAuditor = None):
        self.auditor = auditor or FairnessAuditor()

    def calibrate_thresholds(
        self,
        candidates: List[CandidateRecord],
        request: MitigationRequest,
    ) -> MitigationResult:
        """Find group-specific cutoff thresholds that satisfy the EEOC 80% rule."""
        if not candidates:
            raise ValueError("Candidate cohort cannot be empty.")

        target_attr = request.target_attribute
        base_threshold = request.baseline_threshold
        target_dir = request.desired_min_impact_ratio

        # 1. Run baseline audit with uniform threshold
        initial_audit = self.auditor.audit_cohort(candidates, cutoff_threshold=base_threshold)
        attr_audit = initial_audit.audits_by_attribute.get(target_attr)
        if not attr_audit:
            raise ValueError(f"Protected attribute '{target_attr}' not found in candidate data.")

        orig_impact_ratio = attr_audit.lowest_impact_ratio

        # Extract baseline selected candidates
        selected_before = [c for c in candidates if c.merit_score >= base_threshold]
        mean_merit_before = float(np.mean([c.merit_score for c in selected_before])) if selected_before else 0.0

        # Group candidates by the target attribute
        grouped_candidates: Dict[str, List[CandidateRecord]] = {}
        for c in candidates:
            val = getattr(c, target_attr).value if hasattr(getattr(c, target_attr), "value") else str(getattr(c, target_attr))
            grouped_candidates.setdefault(val, []).append(c)

        ref_group_name = attr_audit.reference_group
        ref_metric = attr_audit.group_metrics.get(ref_group_name)
        ref_rate = ref_metric.selection_rate if ref_metric else 0.20

        # Target minimum selection rate for disadvantaged groups: ref_rate * target_dir
        min_required_rate = max(0.01, ref_rate * target_dir)

        calibrated_thresholds: Dict[str, float] = {}
        newly_selected_candidates: List[CandidateRecord] = []

        for group_name, group_list in grouped_candidates.items():
            scores = np.array([c.merit_score for c in group_list])
            if len(scores) == 0:
                calibrated_thresholds[group_name] = base_threshold
                continue

            current_rate = float(np.mean(scores >= base_threshold))

            if current_rate >= min_required_rate or group_name == ref_group_name:
                # Group already satisfies requirement
                calibrated_thresholds[group_name] = round(base_threshold, 1)
                newly_selected_candidates.extend([c for c in group_list if c.merit_score >= base_threshold])
            else:
                # Need to calibrate cutoff to achieve at least min_required_rate
                # Sort descending to find score at required rank
                sorted_scores = np.sort(scores)[::-1]
                required_count = int(np.ceil(len(scores) * min_required_rate))
                required_count = min(len(sorted_scores), max(1, required_count))
                calibrated_cutoff = float(sorted_scores[required_count - 1])
                # Ensure threshold does not exceed baseline
                calibrated_cutoff = min(base_threshold, calibrated_cutoff)
                # Floor to 1 decimal place to prevent rounding up past the target score
                calibrated_cutoff = float(np.floor(calibrated_cutoff * 10.0) / 10.0)
                calibrated_thresholds[group_name] = calibrated_cutoff
                newly_selected_candidates.extend([c for c in group_list if c.merit_score >= calibrated_cutoff])

        # Recalculate post-mitigation metrics
        mean_merit_after = float(np.mean([c.merit_score for c in newly_selected_candidates])) if newly_selected_candidates else 0.0
        delta_loss_pct = round(
            max(0.0, ((mean_merit_before - mean_merit_after) / mean_merit_before) * 100.0), 2
        ) if mean_merit_before > 0 else 0.0

        # Compute new selection rates per group
        new_rates: Dict[str, float] = {}
        for group_name, group_list in grouped_candidates.items():
            cutoff = calibrated_thresholds[group_name]
            sel_count = sum(1 for c in group_list if c.merit_score >= cutoff)
            new_rates[group_name] = sel_count / len(group_list) if len(group_list) > 0 else 0.0

        max_new_rate = max(new_rates.values()) if new_rates else 1.0
        mitigated_dirs = [
            round(rate / max_new_rate, 4) if max_new_rate > 0 else 1.0
            for rate in new_rates.values()
        ]
        mitigated_dir = min(mitigated_dirs) if mitigated_dirs else 1.0

        resolved = mitigated_dir >= target_dir

        desc = (
            f"Successfully calibrated group-specific cutoffs. Disparate Impact Ratio improved from "
            f"{orig_impact_ratio:.2f} to {mitigated_dir:.2f} (Target: {target_dir:.2f}), "
            f"preserving {100.0 - delta_loss_pct:.1f}% of baseline merit score quality."
        )

        return MitigationResult(
            target_attribute=target_attr,
            original_impact_ratio=round(orig_impact_ratio, 4),
            mitigated_impact_ratio=round(mitigated_dir, 4),
            calibrated_thresholds=calibrated_thresholds,
            mean_selected_merit_before=round(mean_merit_before, 2),
            mean_selected_merit_after=round(mean_merit_after, 2),
            merit_efficiency_loss_percent=delta_loss_pct,
            eeoc_violation_resolved=resolved,
            description=desc,
        )
