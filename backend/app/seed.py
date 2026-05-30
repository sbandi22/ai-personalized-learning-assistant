"""Seed the database from the sample CSV datasets in ./data.

Usage:  python -m backend.app.seed
Creates demo users:  educator/educator123  and  alice/student123
"""
import csv
import os
from datetime import datetime

from .database import SessionLocal, init_db
from . import models
from .auth import hash_password

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _read_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seed():
    init_db()
    db = SessionLocal()
    if db.query(models.Student).first():
        print("Database already seeded; skipping.")
        db.close()
        return

    # --- Demo users (role-based) ---
    educator = models.User(username="educator", email="educator@example.com",
                           hashed_password=hash_password("educator123"),
                           role="educator")
    db.add(educator)

    # --- Courses ---
    course_map = {}
    for row in _read_csv("courses.csv"):
        c = models.Course(title=row["title"], subject=row["subject"],
                          difficulty=float(row["difficulty"]), tags=row["tags"],
                          description=row.get("description", ""))
        db.add(c); db.flush()
        course_map[int(row["id"])] = c.id

    # --- Students (each gets a login) ---
    student_map = {}
    for row in _read_csv("students.csv"):
        uname = row["name"].split()[0].lower()
        user = models.User(username=uname, email=f"{uname}@example.com",
                           hashed_password=hash_password("student123"),
                           role="student")
        db.add(user); db.flush()
        s = models.Student(
            user_id=user.id, name=row["name"], grade_level=row["grade_level"],
            avg_score=float(row["avg_score"]),
            engagement_score=float(row["engagement_score"]),
            study_hours_week=float(row["study_hours_week"]),
            login_count=int(row["login_count"]),
            completion_rate=float(row["completion_rate"]),
            last_active=datetime.utcnow(),
        )
        db.add(s); db.flush()
        student_map[int(row["id"])] = s.id

    # --- Quiz results ---
    for row in _read_csv("quiz_results.csv"):
        db.add(models.QuizResult(
            student_id=student_map[int(row["student_id"])],
            course_id=course_map.get(int(row["course_id"])),
            topic=row["topic"], score=float(row["score"]),
            max_score=float(row["max_score"]),
            attempts=int(row["attempts"]),
            time_spent_min=float(row["time_spent_min"]),
        ))

    db.commit()
    db.close()
    print("Seeded database with sample students, courses, and quiz results.")
    print("Logins -> educator/educator123 | <firstname>/student123")


if __name__ == "__main__":
    seed()
