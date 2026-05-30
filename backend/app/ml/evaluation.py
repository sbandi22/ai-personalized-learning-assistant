"""Evaluation metrics for the prediction and recommendation models."""
from typing import Dict, List, Sequence
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, mean_absolute_error,
                             mean_squared_error, r2_score)


def classification_metrics(y_true: Sequence[int], y_pred: Sequence[int],
                           y_prob: Sequence[float] = None) -> Dict[str, float]:
    out = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
    }
    if y_prob is not None and len(set(y_true)) > 1:
        out["roc_auc"] = round(float(roc_auc_score(y_true, y_prob)), 4)
    return out


def regression_metrics(y_true: Sequence[float], y_pred: Sequence[float]) -> Dict[str, float]:
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
    }


def precision_at_k(recommended: List[int], relevant: List[int], k: int) -> float:
    if k == 0:
        return 0.0
    topk = recommended[:k]
    hits = len(set(topk) & set(relevant))
    return round(hits / k, 4)


def recall_at_k(recommended: List[int], relevant: List[int], k: int) -> float:
    if not relevant:
        return 0.0
    topk = recommended[:k]
    hits = len(set(topk) & set(relevant))
    return round(hits / len(relevant), 4)


def ndcg_at_k(recommended: List[int], relevant: List[int], k: int) -> float:
    """Normalized Discounted Cumulative Gain (binary relevance)."""
    rel_set = set(relevant)
    dcg = 0.0
    for i, item in enumerate(recommended[:k]):
        if item in rel_set:
            dcg += 1.0 / np.log2(i + 2)
    ideal_hits = min(len(rel_set), k)
    idcg = sum(1.0 / np.log2(i + 2) for i in range(ideal_hits))
    return round(float(dcg / idcg), 4) if idcg > 0 else 0.0
