"""Recommendation service: wires DB data into the ML engines."""
from typing import List
from sqlalchemy.orm import Session

from .. import models
from ..ml.recommendation_engine import RecommendationEngine
from ..ml.adaptive_engine import AdaptiveEngine
from .progress_service import weak_topics


def _all_courses(db: Session) -> List[dict]:
    return [{
        "id": c.id, "title": c.title, "subject": c.subject,
        "tags": c.tags or "", "difficulty": c.difficulty,
    } for c in db.query(models.Course).all()]


def _student_profile(db: Session, student: models.Student) -> dict:
    return {
        "interests": "",
        "weak_topics": weak_topics(db, student.id),
        "mastery": min(student.avg_score / 100.0, 1.0),
        "engagement": min(student.engagement_score / 100.0, 1.0),
    }


def _enrolled_ids(db: Session, student_id: int) -> List[int]:
    return [e.course_id for e in db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id,
        models.Enrollment.completed.is_(True)).all()]


def recommend_courses(db: Session, student: models.Student, top_k: int = 5) -> List[dict]:
    engine = RecommendationEngine().fit(_all_courses(db))
    profile = _student_profile(db, student)
    return engine.recommend(profile, top_k=top_k,
                            exclude_ids=_enrolled_ids(db, student.id))


def optimized_path(db: Session, student: models.Student) -> List[dict]:
    recs = recommend_courses(db, student, top_k=6)
    candidates = []
    for r in recs:
        course = db.query(models.Course).get(r["course_id"])
        candidates.append({
            "course_id": r["course_id"], "title": r["title"],
            "difficulty": course.difficulty if course else 0.5,
        })
    mastery = min(student.avg_score / 100.0, 1.0)
    return AdaptiveEngine().optimize_path(candidates, mastery)
