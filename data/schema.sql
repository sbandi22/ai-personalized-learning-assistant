-- Database schema for the AI Personalized Learning Assistant
-- Compatible with SQLite and PostgreSQL (minor type tweaks for PG).

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY,
    username        TEXT UNIQUE NOT NULL,
    email           TEXT UNIQUE,
    hashed_password TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'student',  -- 'student' | 'educator'
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    id               INTEGER PRIMARY KEY,
    user_id          INTEGER REFERENCES users(id),
    name             TEXT NOT NULL,
    grade_level      TEXT,
    avg_score        REAL DEFAULT 0,
    engagement_score REAL DEFAULT 0,
    study_hours_week REAL DEFAULT 0,
    login_count      INTEGER DEFAULT 0,
    completion_rate  REAL DEFAULT 0,
    last_active      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    subject     TEXT,
    difficulty  REAL DEFAULT 0.5,
    tags        TEXT DEFAULT '',
    description TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS enrollments (
    id          INTEGER PRIMARY KEY,
    student_id  INTEGER REFERENCES students(id),
    course_id   INTEGER REFERENCES courses(id),
    progress    REAL DEFAULT 0,
    completed   BOOLEAN DEFAULT 0,
    score       REAL DEFAULT 0,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quiz_results (
    id             INTEGER PRIMARY KEY,
    student_id     INTEGER REFERENCES students(id),
    course_id      INTEGER REFERENCES courses(id),
    topic          TEXT,
    score          REAL DEFAULT 0,
    max_score      REAL DEFAULT 100,
    attempts       INTEGER DEFAULT 1,
    time_spent_min REAL DEFAULT 0,
    taken_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quiz_student ON quiz_results(student_id);
CREATE INDEX IF NOT EXISTS idx_enroll_student ON enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_course_subject ON courses(subject);
