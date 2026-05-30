"""Course catalog endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=List[schemas.CourseOut])
def list_courses(subject: str = None, db: Session = Depends(get_db),
                 user: models.User = Depends(get_current_user)):
    query = db.query(models.Course)
    if subject:
        query = query.filter(models.Course.subject == subject)
    return query.all()


@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db),
               user: models.User = Depends(get_current_user)):
    course = db.query(models.Course).get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
