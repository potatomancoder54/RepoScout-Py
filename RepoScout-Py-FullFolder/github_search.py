"""Module to query GitHub Search API and return repository results."""
import math
import time
from typing import Dict, List, Optional

import requests

from config import GITHUB_API_URL, GITHUB_TOKEN, DEFAULT_PER_PAGE, MAX_RESULTS


class GitHubSearchError(Exception):
    pass


def build_query(keywords: List[str], language: Optional[str] = None) -> str:
    q = " ".join(keywords) if keywords else ""
    if language:
        # exact match language token
        q = f"{q} language:{language}"
    return q.strip() or ""


def _headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers


def search_repositories(query: str, per_page: int = DEFAULT_PER_PAGE) -> Dict:
    if not query:
        raise GitHubSearchError("Empty search query")

    url = f"{GITHUB_API_URL}/search/repositories"
    params = {"q": query, "per_page": min(per_page, MAX_RESULTS)}
    try:
        resp = requests.get(url, headers=_headers(), params=params, timeout=15)
    except requests.RequestException as e:
        raise GitHubSearchError(f"Network error: {e}")

    if resp.status_code == 403:
        # possibly rate limit
        raise GitHubSearchError(f"GitHub API error 403: {resp.text}")

    if not resp.ok:
        raise GitHubSearchError(f"GitHub API error {resp.status_code}: {resp.text}")

    return {"items": resp.json().get("items", []), "rate_limit": _parse_rate_limit(resp.headers)}


def _parse_rate_limit(headers: Dict) -> Dict:
    try:
        remaining = int(headers.get("X-RateLimit-Remaining", -1))
        reset = int(headers.get("X-RateLimit-Reset", 0))
        limit = int(headers.get("X-RateLimit-Limit", -1))
    except Exception:
        remaining = -1
        reset = 0
        limit = -1
    return {"remaining": remaining, "reset": reset, "limit": limit}


def fetch_combined(keywords: List[str], language: Optional[str] = None, per_page: int = DEFAULT_PER_PAGE) -> Dict:
    """Perform one optimized search and return items and rate limit info."""
    q = build_query(keywords, language)
    if not q:
        raise GitHubSearchError("No query to run")
    return search_repositories(q, per_page=per_page)
