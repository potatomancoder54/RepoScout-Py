"""Ranking utilities to score and sort GitHub repositories."""
from datetime import datetime, timezone
from math import log1p
from typing import Dict, List

from difflib import SequenceMatcher

from config import WEIGHTS


def semantic_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def stars_score(stars: int) -> float:
    # log scale normalization
    return log1p(stars)


def recency_score(updated_at: str) -> float:
    # updated_at expected in ISO 8601
    try:
        dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    except Exception:
        return 0.0
    now = datetime.now(timezone.utc)
    delta_days = (now - dt).days
    # More recent -> higher score; clamp
    return 1.0 / (1 + delta_days)


def score_repo(repo: Dict, description: str) -> float:
    # Compose a text for semantic comparison
    text = " ".join(filter(None, [repo.get("name"), repo.get("description") or ""]))
    sem = semantic_similarity(description, text)
    stars = stars_score(repo.get("stargazers_count", 0))
    rec = recency_score(repo.get("updated_at", ""))

    w = WEIGHTS
    total = w.get("semantic", 0.6) * sem + w.get("stars", 0.25) * _normalize(stars) + w.get("recency", 0.15) * _normalize(rec)
    return total


def _normalize(x: float, min_v: float = 0.0, max_v: float = 1.0) -> float:
    # For our usage, ensure value in [0,1]. For values already in (0,1), clamp.
    if x <= 0:
        return 0.0
    # If x already in range (0,1] return min(1,x)
    if 0 < x <= 1:
        return min(1.0, x)
    # for larger values, use log scaling to squash
    return min(1.0, (log1p(x) / (1 + log1p(x))))


def rank_repositories(items: List[Dict], description: str, top_n: int = 10) -> List[Dict]:
    scored = []
    for r in items:
        try:
            s = score_repo(r, description)
        except Exception:
            s = 0.0
        r_copy = dict(r)
        r_copy["_score"] = s
        scored.append(r_copy)

    scored.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return scored[:top_n]
