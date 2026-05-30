"""Analytics service: prediction, interventions, and cohort summaries."""
from datetime import datetime
from typing import List
import numpy as np
from sqlalchemy.orm import Session

from .. import models
from ..ml.performance_model import PerformanceModel, FEATURES
from ..ml import intervention


def _student_row(s: models.Student) -> dict:
    return {
        "id": s.id, "name": s.name,
        "avg_score": s.avg_score, "engagement_score": s.engagement_score,
        "study_hours_week": s.study_hours_week,
        "completion_rate": s.completion_rate, "login_count": s.login_count,
        "final_score": s.avg_score,
    }


def _trained_model(db: Session) -> PerformanceModel:
    rows = [_student_row(s) for s in db.query(models.Student).all()]
    model = PerformanceModel()
    if len(rows) >= 5:
        model.train(rows)
    return model


def predict_student(db: Session, student: models.Student) -> dict:
    model = _trained_model(db)
    return model.predict(_student_row(student))


def _days_since(dt: datetime) -> float:
    if not dt:
        return 0.0
    return (datetime.utcnow() - dt).days


def intervention_report(db: Session) -> List[dict]:
    students = []
    for s in db.query(models.Student).all():
        students.append({
            "id": s.id, "name": s.name, "avg_score": s.avg_score,
            "engagement_score": s.engagement_score,
            "completion_rate": s.completion_rate,
            "days_since_active": _days_since(s.last_active),
        })
    return intervention.rank_interventions(students)


def cohort_summary(db: Session) -> dict:
    students = db.query(models.Student).all()
    if not students:
        return {"count": 0}
    scores = np.array([s.avg_score for s in students])
    engagement = np.array([s.engagement_score for s in students])
    completion = np.array([s.completion_rate for s in students])
    risk = intervention_report(db)
    risk_buckets = {"low": 0, "medium": 0, "high": 0}
    for r in risk:
        risk_buckets[r["risk_level"]] += 1
    return {
        "count": len(students),
        "avg_score_mean": round(float(scores.mean()), 2),
        "avg_score_std": round(float(scores.std()), 2),
        "engagement_mean": round(float(engagement.mean()), 2),
        "completion_mean": round(float(completion.mean()), 3),
        "risk_distribution": risk_buckets,
        "at_risk_count": risk_buckets["high"] + risk_buckets["medium"],
    }
