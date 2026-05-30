"""Unit tests for the ML and statistical modules.

Run with:  pytest -q
"""
from backend.app.ml.recommendation_engine import RecommendationEngine
from backend.app.ml.performance_model import PerformanceModel
from backend.app.ml.adaptive_engine import AdaptiveEngine
from backend.app.ml.scoring import MasteryScorer
from backend.app.ml import intervention, evaluation

COURSES = [
    {"id": 1, "title": "Algebra", "subject": "Math", "tags": "equations", "difficulty": 0.3},
    {"id": 2, "title": "Calculus", "subject": "Math", "tags": "derivatives", "difficulty": 0.8},
    {"id": 3, "title": "Python", "subject": "CS", "tags": "programming", "difficulty": 0.4},
]


def test_recommendation_scores_in_range():
    eng = RecommendationEngine().fit(COURSES)
    recs = eng.recommend({"interests": "math", "weak_topics": ["equations"],
                          "mastery": 0.4, "engagement": 0.6}, top_k=3)
    assert len(recs) == 3
    assert all(0.0 <= r["score"] <= 1.0 for r in recs)


def test_performance_heuristic_without_training():
    model = PerformanceModel()
    out = model.predict({"id": 1, "avg_score": 85, "engagement_score": 80})
    assert 0.0 <= out["pass_probability"] <= 1.0
    assert out["risk_level"] in {"low", "medium", "high"}


def test_adaptive_path_orders_all_candidates():
    cands = [{"course_id": c["id"], "title": c["title"],
              "difficulty": c["difficulty"]} for c in COURSES]
    path = AdaptiveEngine().optimize_path(cands, mastery=0.3)
    assert len(path) == len(COURSES)
    assert [s["order"] for s in path] == [1, 2, 3]


def test_mastery_scorer_bounds():
    pop = [{"avg_score": 50, "completion_rate": 0.5, "engagement_score": 50,
            "study_hours_week": 5},
           {"avg_score": 90, "completion_rate": 0.9, "engagement_score": 90,
            "study_hours_week": 10}]
    scorer = MasteryScorer().fit(pop)
    score = scorer.score(pop[1])
    assert 0.0 <= score <= 100.0


def test_intervention_levels():
    high = intervention.compute_risk({"id": 1, "name": "X", "avg_score": 30,
        "engagement_score": 20, "completion_rate": 0.2, "days_since_active": 20})
    assert high["risk_level"] == "high"


def test_evaluation_metrics():
    m = evaluation.classification_metrics([1, 0, 1], [1, 0, 0])
    assert 0.0 <= m["accuracy"] <= 1.0
    assert evaluation.precision_at_k([1, 2, 3], [1, 3], 2) >= 0.0
