"""Analytics endpoints: performance prediction, interventions, cohort view."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user, require_educator
from .. import models, schemas
from ..services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/predict/{student_id}", response_model=schemas.PerformancePrediction)
def predict_performance(student_id: int, db: Session = Depends(get_db),
                        user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return analytics_service.predict_student(db, student)


@router.get("/interventions", response_model=List[schemas.InterventionItem])
def interventions(db: Session = Depends(get_db),
                  educator: models.User = Depends(require_educator)):
    """Educator-only: students ranked by intervention urgency."""
    return analytics_service.intervention_report(db)


@router.get("/cohort")
def cohort_analytics(db: Session = Depends(get_db),
                     educator: models.User = Depends(require_educator)):
    """Educator-only: aggregate cohort statistics for the dashboard."""
    return analytics_service.cohort_summary(db)
