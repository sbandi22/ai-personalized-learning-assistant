"""Adaptive learning engine.

Builds an optimized, ordered learning path for a student by sequencing
recommended courses so that difficulty rises gradually from the student's
current mastery level (the 'zone of proximal development').
"""
from typing import Dict, List


class AdaptiveEngine:
    def __init__(self, step: float = 0.12):
        # target difficulty increment between consecutive steps
        self.step = step

    def optimize_path(self, candidates: List[Dict], mastery: float) -> List[Dict]:
        """candidates: list of dicts with course_id, title, difficulty.

        Returns an ordered path where each step's difficulty is the closest
        available course to the rising target difficulty.
        """
        remaining = list(candidates)
        path = []
        target = mastery
        order = 1
        while remaining:
            target = min(1.0, target + self.step)
            # pick the course closest to the current target difficulty
            choice = min(remaining, key=lambda c: abs(c.get("difficulty", 0.5) - target))
            remaining.remove(choice)
            path.append({
                "order": order,
                "course_id": choice["course_id"],
                "title": choice["title"],
                "predicted_difficulty": round(float(choice.get("difficulty", 0.5)), 2),
                "rationale": self._rationale(choice.get("difficulty", 0.5), target),
            })
            order += 1
        return path

    @staticmethod
    def _rationale(difficulty: float, target: float) -> str:
        if difficulty < target - 0.1:
            return "Reinforces fundamentals before advancing."
        if difficulty > target + 0.1:
            return "A stretch challenge to accelerate growth."
        return "Optimally matched to your current readiness."
