"""Student performance prediction model.

Trains a classifier (pass / not pass) and a regressor (projected final
score) on engagement + assessment features. Falls back to a heuristic
when the model has not yet been trained.
"""
from typing import Dict, List
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

FEATURES = ["avg_score", "engagement_score", "study_hours_week",
            "completion_rate", "login_count"]
PASS_THRESHOLD = 60.0


class PerformanceModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.clf = RandomForestClassifier(n_estimators=200, random_state=42)
        self.reg = GradientBoostingRegressor(random_state=42)
        self.trained = False

    def _matrix(self, rows: List[Dict]) -> np.ndarray:
        return np.array([[r.get(f, 0.0) for f in FEATURES] for r in rows], dtype=float)

    def train(self, rows: List[Dict]) -> Dict[str, float]:
        X = self._matrix(rows)
        y_score = np.array([r.get("final_score", r.get("avg_score", 0.0)) for r in rows])
        y_pass = (y_score >= PASS_THRESHOLD).astype(int)
        Xs = self.scaler.fit_transform(X)
        # Guard against a single-class target in tiny demo datasets.
        if len(np.unique(y_pass)) > 1:
            self.clf.fit(Xs, y_pass)
        self.reg.fit(Xs, y_score)
        self.trained = True
        return {"n_samples": len(rows), "pass_rate": float(y_pass.mean())}

    def predict(self, student: Dict) -> Dict:
        if not self.trained:
            return self._heuristic(student)
        Xs = self.scaler.transform(self._matrix([student]))
        try:
            prob = float(self.clf.predict_proba(Xs)[0][1])
        except Exception:
            prob = 1.0 if student.get("avg_score", 0) >= PASS_THRESHOLD else 0.0
        projected = float(np.clip(self.reg.predict(Xs)[0], 0, 100))
        return self._package(student, prob, projected)

    def _heuristic(self, student: Dict) -> Dict:
        base = student.get("avg_score", 0.0)
        adj = base + 0.1 * student.get("engagement_score", 0.0)
        projected = float(np.clip(adj, 0, 100))
        prob = float(np.clip(projected / 100.0, 0, 1))
        return self._package(student, prob, projected)

    @staticmethod
    def _package(student: Dict, prob: float, projected: float) -> Dict:
        if prob >= 0.7:
            risk = "low"
        elif prob >= 0.45:
            risk = "medium"
        else:
            risk = "high"
        return {
            "student_id": student.get("id"),
            "pass_probability": round(prob, 3),
            "projected_score": round(projected, 1),
            "risk_level": risk,
        }
