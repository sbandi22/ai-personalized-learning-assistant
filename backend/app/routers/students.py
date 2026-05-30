"""Student profile and progress-tracking endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas
from ..services import progress_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=List[schemas.StudentOut])
def list_students(db: Session = Depends(get_db),
                  user: models.User = Depends(get_current_user)):
    return db.query(models.Student).all()


@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/{student_id}/progress", response_model=schemas.ProgressOut)
def get_progress(student_id: int, db: Session = Depends(get_db),
                 user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return progress_service.build_progress(db, student)
