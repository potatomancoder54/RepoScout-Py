import os
from typing import List

# Configurable weights for ranking
WEIGHTS = {
    "semantic": 0.6,
    "stars": 0.25,
    "recency": 0.15,
}

# Known languages and frameworks (used for lightweight detection)
LANGUAGES: List[str] = [
    "python", "javascript", "typescript", "go", "java", "ruby", "c", "c++", "c#", "php", "rust",
]

FRAMEWORKS: List[str] = [
    "django", "flask", "fastapi", "react", "vue", "angular", "spring", "express", "rails", "laravel",
]

# GitHub API settings
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Search defaults
DEFAULT_PER_PAGE = 30
MAX_RESULTS = 50
