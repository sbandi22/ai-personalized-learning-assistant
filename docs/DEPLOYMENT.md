# Deployment Guide

## 1. Local (development)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then edit SECRET_KEY
python -m backend.app.seed    # load sample data
uvicorn backend.app.main:app --reload          # terminal 1
streamlit run frontend/streamlit_app.py        # terminal 2
```

## 2. Docker Compose (recommended)

```bash
docker-compose up --build
```

Services:
- API -> http://localhost:8000 (docs at /docs)
- Dashboard -> http://localhost:8501

## 3. Production notes

- Set a strong `SECRET_KEY` and use PostgreSQL via `DATABASE_URL`.
- Run the API behind a reverse proxy (nginx / Caddy) with TLS.
- Use `gunicorn -k uvicorn.workers.UvicornWorker backend.app.main:app` for multiple workers.
- Restrict CORS `allow_origins` in `main.py` to your dashboard domain.
- Persist the database with a Docker volume or a managed PostgreSQL instance.

## 4. Cloud options

- **Render / Railway / Fly.io**: deploy the Docker image; add a managed Postgres add-on.
- **Streamlit Community Cloud**: host the dashboard, pointing `API_URL` at the deployed API.
- **AWS / GCP / Azure**: containers on ECS / Cloud Run / Container Apps.
