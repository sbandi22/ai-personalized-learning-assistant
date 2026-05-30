"""Recommendation and learning-path endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas
from ..services import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/{student_id}", response_model=List[schemas.RecommendationItem])
def get_recommendations(student_id: int, top_k: int = 5,
                        db: Session = Depends(get_db),
                        user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return recommendation_service.recommend_courses(db, student, top_k=top_k)


@router.get("/{student_id}/path", response_model=List[schemas.LearningPathStep])
def get_learning_path(student_id: int, db: Session = Depends(get_db),
                      user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return recommendation_service.optimized_path(db, student)
