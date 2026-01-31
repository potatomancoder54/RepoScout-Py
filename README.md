# RepoSearch — Terminal GitHub repository discovery

RepoSearch is a small, beginner-friendly terminal application that helps you find relevant GitHub repositories by describing what you need in plain English. It performs a lightweight natural-language analysis, queries the GitHub Search API, ranks results, and shows the top matches in a readable terminal UI.

Why use this
- Quickly discover repositories related to an idea or use case without crafting search queries.
- Lightweight and easy to run locally.
- Supports authenticated GitHub API requests via an environment variable to avoid strict rate limits.

Prerequisites
- Python 3.8+ installed
- Git (optional, for cloning)

Quick start (recommended)

1. Clone the repo:

```powershell
git clone <your-repo-url>
cd RepoSearch
```

2. Create and activate a virtual environment:

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. (Optional but recommended) Set your GitHub token to increase rate limits:

Windows (PowerShell):
```powershell
$env:GITHUB_TOKEN = 'ghp_xxx'
```

macOS / Linux:
```bash
export GITHUB_TOKEN='ghp_xxx'
```

5. Run the tool:

```bash
python main.py
```

How to use
- When prompted, type a natural-language description such as:
	- "REST API example in FastAPI for user auth"
	- "image classification PyTorch example"

- The tool will show a compact, colorized table of results and a "Full URLs" panel with copyable links.

Troubleshooting
- If you see an error that `rich` or `requests` is missing, ensure you installed `requirements.txt` into the same Python interpreter used to run `python main.py`.
- If VS Code warns about missing types or shows yellow squiggles, select the correct Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter") and consider enabling library types in `.vscode/settings.json`.

Project layout

- `main.py` — CLI entrypoint and Rich UI
- `nlp.py` — lightweight NLP helpers (keyword extraction, language/framework detection)
- `github_search.py` — GitHub Search API calls, auth support
- `ranking.py` — scoring and ranking repositories
- `config.py` — configuration and defaults
- `requirements.txt` — Python dependencies
- `README.md`, `LICENSE` — project docs and license

Contribution & development
- Open an issue or a pull request with proposed changes.
- Keep changes focused and add tests where applicable.

Future enhancements
- Add embeddings-based semantic search for better relevance.
- Interactive browsing and pagination of results.
- Caching and query history.

License

This project is licensed under the MIT License. See `LICENSE` for details.
