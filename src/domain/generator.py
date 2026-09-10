"""Synthetic Applicant & Telemetry Cohort Generator.

Generates realistic candidate cohorts with psychometric test items,
merit scores, and protected demographic attributes under controlled experimental conditions.
"""

from typing import List
import numpy as np

from src.domain.models import (
    AgeGroup,
    BenchmarkScenario,
    CandidateRecord,
    Ethnicity,
    Gender,
)

ETHNICITY_LIST = [Ethnicity.MAJORITY, Ethnicity.MINORITY_A, Ethnicity.MINORITY_B]
GENDER_LIST = [Gender.MALE, Gender.FEMALE, Gender.NON_BINARY]
AGE_LIST = [AgeGroup.UNDER_40, AgeGroup.OVER_40]


class SyntheticCohortGenerator:
    """Vectorized generator of realistic candidate hiring pools."""

    @classmethod
    def generate_scenario(
        cls,
        scenario: BenchmarkScenario,
        n_candidates: int = 500,
        random_seed: int = 42,
    ) -> List[CandidateRecord]:
        """Generate a complete candidate cohort based on a predefined hiring scenario."""
        np.random.seed(random_seed)

        if scenario == BenchmarkScenario.BIASED_TECH_ATS:
            return cls._generate_biased_tech_ats(n_candidates)
        elif scenario == BenchmarkScenario.AGE_PENALIZED_EXEC:
            return cls._generate_age_penalized_exec(n_candidates)
        elif scenario == BenchmarkScenario.COMPLIANT_FAIR_PIPELINE:
            return cls._generate_compliant_pipeline(n_candidates)
        else:
            raise ValueError(f"Unknown scenario: {scenario}")

    @classmethod
    def _generate_biased_tech_ats(cls, n: int) -> List[CandidateRecord]:
        """Simulates automated screening with latent gender bias (common in uncalibrated resume parsers)."""
        candidates: List[CandidateRecord] = []
        n_male = int(n * 0.60)
        n_nb = int(n * 0.05)
        n_female = n - n_male - n_nb
        genders = [Gender.MALE] * n_male + [Gender.FEMALE] * n_female + [Gender.NON_BINARY] * n_nb
        np.random.shuffle(genders)

        for i, gender in enumerate(genders):
            true_ability = np.random.normal(70, 10)

            if gender == Gender.FEMALE:
                bias_offset = -8.0
            elif gender == Gender.NON_BINARY:
                bias_offset = -6.0
            else:
                bias_offset = +2.0

            merit_score = float(np.clip(true_ability + bias_offset + np.random.normal(0, 3), 15.0, 99.0))

            latent_trait = (true_ability - 50.0) / 25.0
            items = []
            for _ in range(6):
                val = 3.0 + 1.2 * latent_trait + np.random.normal(0, 0.6)
                items.append(round(float(np.clip(val, 1.0, 5.0)), 2))

            age = AgeGroup.UNDER_40 if np.random.rand() > 0.3 else AgeGroup.OVER_40
            eth_idx = np.random.choice(len(ETHNICITY_LIST), p=[0.7, 0.2, 0.1])
            eth = ETHNICITY_LIST[eth_idx]

            candidates.append(
                CandidateRecord(
                    candidate_id=f"CAND-BATS-{i+1:04d}",
                    gender=gender,
                    age_group=age,
                    ethnicity=eth,
                    test_items=items,
                    merit_score=round(merit_score, 1),
                )
            )
        return candidates

    @classmethod
    def _generate_age_penalized_exec(cls, n: int) -> List[CandidateRecord]:
        """Simulates executive leadership screening penalizing candidates >40 years old (ADEA violation)."""
        candidates: List[CandidateRecord] = []
        n_under = int(n * 0.55)
        n_over = n - n_under
        ages = [AgeGroup.UNDER_40] * n_under + [AgeGroup.OVER_40] * n_over
        np.random.shuffle(ages)

        for i, age in enumerate(ages):
            true_ability = np.random.normal(72, 9)

            if age == AgeGroup.OVER_40:
                merit_offset = -9.0
            else:
                merit_offset = +3.0

            merit_score = float(np.clip(true_ability + merit_offset + np.random.normal(0, 3), 20.0, 98.0))

            latent_trait = (true_ability - 50.0) / 25.0
            items = []
            for _ in range(5):
                val = 3.2 + 1.1 * latent_trait + np.random.normal(0, 0.7)
                items.append(round(float(np.clip(val, 1.0, 5.0)), 2))

            g_idx = np.random.choice(len(GENDER_LIST), p=[0.55, 0.40, 0.05])
            gender = GENDER_LIST[g_idx]

            e_idx = np.random.choice(len(ETHNICITY_LIST), p=[0.65, 0.25, 0.10])
            eth = ETHNICITY_LIST[e_idx]

            candidates.append(
                CandidateRecord(
                    candidate_id=f"CAND-EXEC-{i+1:04d}",
                    gender=gender,
                    age_group=age,
                    ethnicity=eth,
                    test_items=items,
                    merit_score=round(merit_score, 1),
                )
            )
        return candidates

    @classmethod
    def _generate_compliant_pipeline(cls, n: int) -> List[CandidateRecord]:
        """Simulates a fully calibrated, psychometrically audited talent acquisition funnel."""
        candidates: List[CandidateRecord] = []

        for i in range(n):
            true_ability = np.random.normal(73, 11)
            merit_score = float(np.clip(true_ability + np.random.normal(0, 2), 20.0, 99.5))

            latent_trait = (true_ability - 50.0) / 25.0
            items = []
            for _ in range(8):
                val = 3.0 + 1.3 * latent_trait + np.random.normal(0, 0.5)
                items.append(round(float(np.clip(val, 1.0, 5.0)), 2))

            g_idx = np.random.choice(len(GENDER_LIST), p=[0.48, 0.48, 0.04])
            gender = GENDER_LIST[g_idx]

            a_idx = np.random.choice(len(AGE_LIST), p=[0.6, 0.4])
            age = AGE_LIST[a_idx]

            e_idx = np.random.choice(len(ETHNICITY_LIST), p=[0.55, 0.30, 0.15])
            eth = ETHNICITY_LIST[e_idx]

            candidates.append(
                CandidateRecord(
                    candidate_id=f"CAND-FAIR-{i+1:04d}",
                    gender=gender,
                    age_group=age,
                    ethnicity=eth,
                    test_items=items,
                    merit_score=round(merit_score, 1),
                )
            )
        return candidates
