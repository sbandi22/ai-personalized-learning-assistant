"""Personalized course recommendation engine.

Blends content-based similarity (course tags vs. a student's weak topics
and interests) with a personalization weight derived from mastery and
engagement. Produces an explainable score in [0, 1] per candidate course.
"""
from typing import Dict, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.course_matrix = None
        self.courses: List[Dict] = []

    def fit(self, courses: List[Dict]):
        """courses: list of dicts with id, title, subject, tags, difficulty."""
        self.courses = courses
        corpus = [f"{c['subject']} {c['tags']}" for c in courses]
        self.course_matrix = self.vectorizer.fit_transform(corpus)
        return self

    def _difficulty_fit(self, course_difficulty: float, mastery: float) -> float:
        """Reward courses whose difficulty is just above current mastery."""
        target = min(1.0, mastery + 0.15)
        return float(1.0 - abs(course_difficulty - target))

    def recommend(self, student_profile: Dict, top_k: int = 5,
                  exclude_ids: List[int] = None) -> List[Dict]:
        """Return ranked, explainable recommendations.

        student_profile expects: interests (str), weak_topics (list[str]),
        mastery (0-1), engagement (0-1).
        """
        exclude_ids = set(exclude_ids or [])
        interest_text = student_profile.get("interests", "")
        weak = " ".join(student_profile.get("weak_topics", []))
        query = f"{interest_text} {weak}".strip() or "general"
        q_vec = self.vectorizer.transform([query])
        content_sim = cosine_similarity(q_vec, self.course_matrix)[0]

        mastery = float(student_profile.get("mastery", 0.5))
        engagement = float(student_profile.get("engagement", 0.5))
        personalization = 0.5 * mastery + 0.5 * engagement

        results = []
        for idx, course in enumerate(self.courses):
            if course["id"] in exclude_ids:
                continue
            content = float(content_sim[idx])
            fit = self._difficulty_fit(course.get("difficulty", 0.5), mastery)
            score = 0.55 * content + 0.30 * fit + 0.15 * personalization
            reason = self._explain(content, fit, course)
            results.append({
                "course_id": course["id"],
                "title": course["title"],
                "subject": course["subject"],
                "score": round(float(np.clip(score, 0, 1)), 3),
                "reason": reason,
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    @staticmethod
    def _explain(content: float, fit: float, course: Dict) -> str:
        if content > 0.4:
            return f"Closely matches your interests and weak topics in {course['subject']}."
        if fit > 0.7:
            return "Difficulty is well matched to your current mastery level."
        return f"Broadens your skills in {course['subject']}."
