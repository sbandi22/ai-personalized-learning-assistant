"""Intervention prediction logic.

Computes a weighted risk score from engagement, performance and recency
signals, then maps it to a recommended action for educators.
"""
from typing import Dict, List


def _recency_penalty(days_since_active: float) -> float:
    """More days inactive => higher risk contribution (0-1)."""
    if days_since_active <= 2:
        return 0.0
    if days_since_active >= 14:
        return 1.0
    return (days_since_active - 2) / 12.0


def compute_risk(student: Dict) -> Dict:
    """Return risk score (0-1), level, and a recommended action."""
    perf = 1.0 - min(student.get("avg_score", 0.0), 100.0) / 100.0
    engagement = 1.0 - min(student.get("engagement_score", 0.0), 100.0) / 100.0
    completion = 1.0 - min(student.get("completion_rate", 0.0), 1.0)
    recency = _recency_penalty(student.get("days_since_active", 0.0))

    risk = (0.35 * perf + 0.30 * engagement +
            0.20 * completion + 0.15 * recency)
    risk = round(float(min(max(risk, 0.0), 1.0)), 3)

    if risk >= 0.6:
        level, action = "high", "Schedule a 1:1 mentoring session and assign remedial modules."
    elif risk >= 0.35:
        level, action = "medium", "Send a check-in nudge and recommend practice quizzes."
    else:
        level, action = "low", "On track - continue current learning path."

    return {
        "student_id": student.get("id"),
        "name": student.get("name", "Unknown"),
        "risk_level": level,
        "risk_score": risk,
        "recommended_action": action,
    }


def rank_interventions(students: List[Dict]) -> List[Dict]:
    """Return students sorted by descending risk (most urgent first)."""
    items = [compute_risk(s) for s in students]
    items.sort(key=lambda x: x["risk_score"], reverse=True)
    return items
