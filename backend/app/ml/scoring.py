"""Statistical scoring model.

Combines several normalized student signals into a single composite
*mastery score* using z-score normalization and configurable weights.
"""
from dataclasses import dataclass, field
from typing import Dict, List
import numpy as np


@dataclass
class ScoringWeights:
    avg_score: float = 0.40
    completion_rate: float = 0.25
    engagement_score: float = 0.20
    study_hours_week: float = 0.15

    def as_dict(self) -> Dict[str, float]:
        return {
            "avg_score": self.avg_score,
            "completion_rate": self.completion_rate,
            "engagement_score": self.engagement_score,
            "study_hours_week": self.study_hours_week,
        }


def zscore(value: float, mean: float, std: float) -> float:
    if std == 0:
        return 0.0
    return (value - mean) / std


def normalize_0_1(z: float) -> float:
    """Map a z-score onto (0, 1) using the logistic function."""
    return float(1.0 / (1.0 + np.exp(-z)))


class MasteryScorer:
    """Fit population statistics, then score individual students."""

    def __init__(self, weights: ScoringWeights = None):
        self.weights = weights or ScoringWeights()
        self.stats: Dict[str, Dict[str, float]] = {}

    def fit(self, population: List[Dict[str, float]]):
        for feature in self.weights.as_dict():
            vals = np.array([row.get(feature, 0.0) for row in population], dtype=float)
            self.stats[feature] = {"mean": float(vals.mean()), "std": float(vals.std())}
        return self

    def score(self, student: Dict[str, float]) -> float:
        """Return a composite mastery score in [0, 100]."""
        if not self.stats:
            raise RuntimeError("MasteryScorer must be fit before scoring")
        total = 0.0
        for feature, w in self.weights.as_dict().items():
            s = self.stats[feature]
            z = zscore(student.get(feature, 0.0), s["mean"], s["std"])
            total += w * normalize_0_1(z)
        return round(total * 100, 2)

    def percentile(self, student_score: float, all_scores: List[float]) -> float:
        arr = np.array(all_scores, dtype=float)
        if arr.size == 0:
            return 0.0
        return round(float((arr < student_score).mean() * 100), 1)
