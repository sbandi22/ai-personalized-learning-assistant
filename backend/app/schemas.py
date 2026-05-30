"""Pydantic request/response schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


class StudentBase(BaseModel):
    name: str
    grade_level: Optional[str] = None


class StudentOut(StudentBase):
    id: int
    avg_score: float
    engagement_score: float
    study_hours_week: float
    completion_rate: float
    last_active: datetime

    class Config:
        from_attributes = True


class CourseOut(BaseModel):
    id: int
    title: str
    subject: str
    difficulty: float
    tags: str

    class Config:
        from_attributes = True


class RecommendationItem(BaseModel):
    course_id: int
    title: str
    subject: str
    score: float          # personalized recommendation score 0-1
    reason: str           # human readable explanation


class LearningPathStep(BaseModel):
    order: int
    course_id: int
    title: str
    predicted_difficulty: float
    rationale: str


class PerformancePrediction(BaseModel):
    student_id: int
    pass_probability: float
    projected_score: float
    risk_level: str       # 'low' | 'medium' | 'high'


class InterventionItem(BaseModel):
    student_id: int
    name: str
    risk_level: str
    risk_score: float
    recommended_action: str


class ProgressOut(BaseModel):
    student_id: int
    overall_progress: float
    courses_completed: int
    courses_in_progress: int
    mastery_score: float
    weak_topics: List[str]
