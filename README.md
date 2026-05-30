# AI Personalized Learning Assistant

An intelligent recommendation system that adapts **personalized learning paths** based on student performance, learning behavior, assessment scores, and engagement metrics.

Built with **FastAPI** (backend), **Streamlit** (dashboard), **scikit-learn** (ML), and **SQLite/PostgreSQL** (database). The architecture is modular, role-based (student vs. educator), and container-ready.

---

## Features

### Student
- Personalized **student dashboard** with progress tracking
- **Personalized course recommendations** with explainable scoring
- **Performance prediction** (pass probability and projected score)
- **Adaptive learning engine** that re-orders the learning path
- **Quiz performance analysis** and weak-topic detection

### Educator
- **Educator analytics dashboard** (cohort view)
- **Intervention recommendations** for at-risk students
- **Statistical scoring model** for engagement and mastery
- Exportable **student analytics reports**

### Platform
- **Role-based authentication** (JWT) for students and educators
- **Learning path optimization**
- Modular, scalable service architecture
- Auto-generated **API documentation** (Swagger / ReDoc)

---

## Architecture

```
+-----------------+      REST / JSON       +----------------------+
|  Streamlit UI   | <-------------------->  |   FastAPI Backend    |
|  student /      |       JWT auth          |   routers / services |
|  educator views |                         |   ML models          |
+-----------------+                         |   analytics          |
                                            +----------+-----------+
                                                       |
                                                       v
                                            +----------------------+
                                            |  SQLite / PostgreSQL |
                                            +----------------------+
```

The ML layer is decoupled into independent modules: a **recommendation engine**, a **performance prediction model**, an **adaptive learning engine**, and an **intervention predictor**, coordinated by service classes.

---

## Project Structure

```
ai-personalized-learning-assistant/
|-- backend/app/
|   |-- main.py                 # FastAPI entrypoint
|   |-- config.py               # Settings
|   |-- database.py             # DB engine/session
|   |-- models.py               # SQLAlchemy ORM models
|   |-- schemas.py              # Pydantic schemas
|   |-- auth.py                 # JWT auth + roles
|   |-- seed.py                 # Load sample data
|   |-- routers/                # students, courses, recommendations, analytics
|   `-- ml/                     # recommendation, performance, adaptive, intervention, scoring, evaluation
|-- frontend/streamlit_app.py   # Role-based dashboard
|-- data/                       # schema.sql + sample CSV datasets
|-- docs/screenshots/           # Screenshot placeholders
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- .gitignore
`-- README.md
```

---

## Tech Stack

| Layer        | Technology                              |
|--------------|-----------------------------------------|
| Backend API  | FastAPI, Uvicorn                        |
| ML / Stats   | scikit-learn, NumPy, pandas, SciPy      |
| Database     | SQLAlchemy + SQLite (PostgreSQL ready)  |
| Auth         | JWT (python-jose), passlib              |
| Frontend     | Streamlit, Plotly                       |
| Deployment   | Docker, docker-compose                  |

---

## Quickstart

```bash
# 1. Clone
git clone https://github.com/sbandi22/ai-personalized-learning-assistant.git
cd ai-personalized-learning-assistant

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed the database with sample data
python -m backend.app.seed

# 5. Run the API (http://localhost:8000, docs at /docs)
uvicorn backend.app.main:app --reload

# 6. In a second terminal, run the dashboard (http://localhost:8501)
streamlit run frontend/streamlit_app.py
```

---

## Running with Docker

```bash
docker-compose up --build
```

- API: http://localhost:8000/docs
- Dashboard: http://localhost:8501

---

## API Documentation

FastAPI auto-generates interactive docs at `/docs` (Swagger) and `/redoc` (ReDoc).

| Method | Endpoint                              | Description                          |
|--------|---------------------------------------|--------------------------------------|
| POST   | `/auth/login`                         | Obtain JWT token                     |
| GET    | `/students/{id}`                      | Student profile                      |
| GET    | `/students/{id}/progress`             | Progress tracking                    |
| GET    | `/recommendations/{student_id}`       | Personalized recommendations         |
| GET    | `/recommendations/{student_id}/path`  | Optimized learning path              |
| GET    | `/analytics/predict/{student_id}`     | Performance prediction               |
| GET    | `/analytics/interventions`            | At-risk students (educator only)     |
| GET    | `/analytics/cohort`                   | Cohort analytics (educator only)     |

---

## Machine Learning Models

- **Recommendation Engine** - content-based + collaborative scoring blended with a personalization weight from mastery and engagement.
- **Performance Prediction** - RandomForest classifier and GradientBoosting regressor predicting pass probability and projected score.
- **Adaptive Engine** - reorders modules by predicted difficulty vs. current mastery.
- **Intervention Predictor** - flags at-risk students using engagement and trend features.
- **Statistical Scoring** - z-score normalization and weighted composite mastery score.

---

## Evaluation Metrics

- Classification: Accuracy, Precision, Recall, F1, ROC-AUC
- Regression: MAE, RMSE, R-squared
- Recommendation: Precision@K, Recall@K, NDCG

See `backend/app/ml/evaluation.py`.

---

## Sample Datasets

Located in `data/`: `students.csv`, `courses.csv`, `quiz_results.csv`. Synthetic and safe for demos.

---

## Screenshots

> Placeholders - add real screenshots to `docs/screenshots/`.

| Student Dashboard | Educator Analytics |
|-------------------|--------------------|
| `docs/screenshots/student_dashboard.png` | `docs/screenshots/educator_analytics.png` |

---

## Roadmap

- Real-time engagement streaming
- Deep-learning sequence models for path prediction
- Multi-tenant institution support

---

## License

MIT
