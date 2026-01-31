"""Lightweight NLP helpers for extracting keywords and detecting languages/frameworks."""
import re
from collections import Counter
from typing import Dict, List

from config import LANGUAGES, FRAMEWORKS

STOPWORDS = {
    "the",
    "a",
    "an",
    "for",
    "to",
    "of",
    "in",
    "on",
    "with",
    "and",
    "or",
    "that",
    "is",
    "as",
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(text: str, top_n: int = 8) -> List[str]:
    if not text:
        return []
    text = normalize(text)
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 1]
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_n)]


def detect_language_and_frameworks(text: str) -> Dict[str, List[str]]:
    text_norm = normalize(text)
    found_langs = [l for l in LANGUAGES if l in text_norm]
    found_frameworks = [f for f in FRAMEWORKS if f in text_norm]
    return {"languages": found_langs, "frameworks": found_frameworks}


def analyze(text: str) -> Dict:
    """Return structured analysis: keywords, languages, frameworks."""
    return {
        "keywords": extract_keywords(text),
        **detect_language_and_frameworks(text),
    }
