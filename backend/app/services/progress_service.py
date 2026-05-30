"""Progress-tracking service: aggregates enrollment + quiz data."""
from collections import defaultdict
from typing import List
from sqlalchemy.orm import Session

from .. import models
from ..ml.scoring import MasteryScorer

WEAK_TOPIC_THRESHOLD = 60.0


def _population(db: Session) -> List[dict]:
    rows = []
    for s in db.query(models.Student).all():
        rows.append({
            "avg_score": s.avg_score,
            "completion_rate": s.completion_rate,
            "engagement_score": s.engagement_score,
            "study_hours_week": s.study_hours_week,
        })
    return rows


def weak_topics(db: Session, student_id: int) -> List[str]:
    """Topics where the student's average quiz score is below threshold."""
    agg = defaultdict(list)
    results = db.query(models.QuizResult).filter(
        models.QuizResult.student_id == student_id).all()
    for q in results:
        pct = (q.score / q.max_score) * 100 if q.max_score else 0
        agg[q.topic].append(pct)
    return [t for t, scores in agg.items()
            if sum(scores) / len(scores) < WEAK_TOPIC_THRESHOLD]


def build_progress(db: Session, student: models.Student) -> dict:
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student.id).all()
    completed = sum(1 for e in enrollments if e.completed)
    in_progress = sum(1 for e in enrollments if not e.completed and e.progress > 0)
    overall = (sum(e.progress for e in enrollments) / len(enrollments)
               if enrollments else 0.0)

    scorer = MasteryScorer().fit(_population(db))
    mastery = scorer.score({
        "avg_score": student.avg_score,
        "completion_rate": student.completion_rate,
        "engagement_score": student.engagement_score,
        "study_hours_week": student.study_hours_week,
    })

    return {
        "student_id": student.id,
        "overall_progress": round(overall, 3),
        "courses_completed": completed,
        "courses_in_progress": in_progress,
        "mastery_score": mastery,
        "weak_topics": weak_topics(db, student.id),
    }
