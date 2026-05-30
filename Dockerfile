# Base image shared by the API and dashboard services.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source.
COPY . .

# Seed the SQLite database at build time (safe / idempotent).
RUN python -m backend.app.seed || true

EXPOSE 8000 8501

# Default command runs the API; docker-compose overrides for the dashboard.
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
