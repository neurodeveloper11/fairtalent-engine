"""Psychometric Reliability & Classical Test Theory (CTT) Engine.

Engineered to validate the construct reliability, internal consistency,
item discrimination, and Standard Error of Measurement (SEM) of talent assessments.
"""

from typing import Dict, List
import numpy as np

from src.domain.models import CandidateRecord, PsychometricMetrics


class PsychometricEngine:
    """Vectorized Classical Test Theory (CTT) validation engine."""

    @staticmethod
    def evaluate_reliability(candidates: List[CandidateRecord]) -> PsychometricMetrics:
        """Compute Cronbach's Alpha, Item-Total correlations, and SEM across candidates."""
        if not candidates:
            raise ValueError("Candidate cohort cannot be empty.")

        # Convert candidate item matrices to 2D numpy array [N, K]
        item_matrix = np.array([c.test_items for c in candidates], dtype=np.float64)
        n_candidates, k_items = item_matrix.shape

        if k_items < 2:
            return PsychometricMetrics(
                num_items=k_items,
                num_candidates=n_candidates,
                cronbach_alpha=1.0 if k_items == 1 else 0.0,
                internal_consistency="INSUFFICIENT_ITEMS",
                standard_error_measurement=0.0,
                item_discriminations={"item_0": 1.0} if k_items == 1 else {},
                is_valid_construct=k_items == 1,
            )

        # 1. Variance of each individual item: var(Y_j) with ddof=1
        item_variances = np.var(item_matrix, axis=0, ddof=1)
        sum_item_variances = np.sum(item_variances)

        # 2. Total test score per candidate and its variance
        total_scores = np.sum(item_matrix, axis=1)
        total_score_var = float(np.var(total_scores, ddof=1))
        total_score_std = float(np.std(total_scores, ddof=1))

        # 3. Cronbach's Alpha: (K / (K - 1)) * (1 - sum(var_items) / var_total)
        if total_score_var > 1e-9:
            alpha = (k_items / (k_items - 1)) * (1.0 - (sum_item_variances / total_score_var))
            # Alpha mathematically can be negative in aberrant adversarial tests, bounded to [-1.0, 1.0]
            alpha = float(np.clip(alpha, -1.0, 1.0))
        else:
            alpha = 0.0

        # Qualitative categorization according to psychometric standards (Nunnally & Bernstein)
        if alpha >= 0.90:
            consistency = "EXCELLENT"
        elif alpha >= 0.80:
            consistency = "GOOD"
        elif alpha >= 0.70:
            consistency = "ACCEPTABLE"
        elif alpha >= 0.60:
            consistency = "QUESTIONABLE"
        else:
            consistency = "POOR"

        # 4. Standard Error of Measurement (SEM = SD_total * sqrt(1 - alpha))
        if alpha >= 0.0 and total_score_std > 0:
            sem = float(total_score_std * np.sqrt(max(0.0, 1.0 - alpha)))
        else:
            sem = float(total_score_std)

        # 5. Corrected Item-Total Discrimination (Pearson r between item and total minus item)
        discriminations: Dict[str, float] = {}
        for j in range(k_items):
            item_col = item_matrix[:, j]
            rest_total = total_scores - item_col
            std_item = np.std(item_col)
            std_rest = np.std(rest_total)

            if std_item > 1e-9 and std_rest > 1e-9:
                r_corr = float(np.corrcoef(item_col, rest_total)[0, 1])
                # Filter NaNs
                discriminations[f"item_{j+1}"] = round(float(np.nan_to_num(r_corr, nan=0.0)), 3)
            else:
                discriminations[f"item_{j+1}"] = 0.0

        is_valid = alpha >= 0.70

        return PsychometricMetrics(
            num_items=k_items,
            num_candidates=n_candidates,
            cronbach_alpha=round(alpha, 4),
            internal_consistency=consistency,
            standard_error_measurement=round(sem, 3),
            item_discriminations=discriminations,
            is_valid_construct=is_valid,
        )

    @staticmethod
    def calculate_sten_scores(raw_scores: List[float]) -> List[int]:
        """Convert continuous raw scores into standard 10-point Sten scale (Mean 5.5, SD 2.0)."""
        if not raw_scores:
            return []
        arr = np.array(raw_scores, dtype=np.float64)
        mean = np.mean(arr)
        std = np.std(arr)

        if std < 1e-9:
            return [5] * len(raw_scores)

        z_scores = (arr - mean) / std
        sten = np.round(5.5 + 2.0 * z_scores).astype(int)
        sten_clipped = np.clip(sten, 1, 10).tolist()
        return sten_clipped
