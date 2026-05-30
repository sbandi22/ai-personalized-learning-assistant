"""SQLAlchemy ORM models defining the database schema."""
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Float, Boolean, DateTime,
                        ForeignKey, Text)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")  # 'student' or 'educator'
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    grade_level = Column(String)
    # Behaviour / engagement features used by the ML models
    avg_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)   # 0-100
    study_hours_week = Column(Float, default=0.0)
    login_count = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)    # 0-1
    last_active = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")
    quiz_results = relationship("QuizResult", back_populates="student")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, index=True)
    difficulty = Column(Float, default=0.5)   # 0 (easy) - 1 (hard)
    tags = Column(String, default="")          # comma separated topics
    description = Column(Text, default="")

    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    progress = Column(Float, default=0.0)     # 0-1
    completed = Column(Boolean, default=False)
    score = Column(Float, default=0.0)        # final score 0-100
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    topic = Column(String, index=True)
    score = Column(Float, default=0.0)        # 0-100
    max_score = Column(Float, default=100.0)
    attempts = Column(Integer, default=1)
    time_spent_min = Column(Float, default=0.0)
    taken_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="quiz_results")
