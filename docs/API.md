# API Documentation

Base URL: `http://localhost:8000`  ·  Interactive docs: `/docs` (Swagger), `/redoc` (ReDoc)

All endpoints except `/auth/login`, `/` and `/health` require a Bearer JWT.

## Authentication

### POST /auth/login
Form-encoded body: `username`, `password`. Returns a JWT.

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=educator&password=educator123"
```

Response:
```json
{ "access_token": "<jwt>", "token_type": "bearer", "role": "educator" }
```

Use the token on subsequent calls:
```bash
curl http://localhost:8000/students/1 \
  -H "Authorization: Bearer <jwt>"
```

## Students

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /students | any | List all students |
| GET | /students/{id} | any | Single student profile |
| GET | /students/{id}/progress | any | Progress, mastery, weak topics |

## Courses

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /courses | any | List courses (optional ?subject=) |
| GET | /courses/{id} | any | Single course |

## Recommendations

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /recommendations/{student_id} | any | Top-K personalized course recommendations |
| GET | /recommendations/{student_id}/path | any | Optimized adaptive learning path |

## Analytics

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /analytics/predict/{student_id} | any | Pass probability + projected score |
| GET | /analytics/interventions | educator | At-risk students ranked by urgency |
| GET | /analytics/cohort | educator | Aggregate cohort statistics |

## Roles

Two roles are issued at login: `student` and `educator`. Educator-only routes
return HTTP 403 for student tokens.
