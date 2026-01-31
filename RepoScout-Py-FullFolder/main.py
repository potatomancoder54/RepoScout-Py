"""CLI entrypoint for reposearch: interactive terminal tool to find GitHub repos."""
import os
import sys
from datetime import datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config import GITHUB_TOKEN
from nlp import analyze
from github_search import fetch_combined, GitHubSearchError
from ranking import rank_repositories

console = Console()


def format_repo_row(repo: dict):
    name = f"[bold cyan]{repo.get('full_name')}[/]"
    desc = repo.get("description") or ""
    lang = repo.get("language") or "-"
    stars = repo.get("stargazers_count", 0)
    updated = repo.get("updated_at", "")
    url = repo.get("html_url")
    return name, desc, lang, str(stars), updated, url


def display_results(analysis, ranked, rate_limit):
    header = f"Found {len(ranked)} repositories"
    keywords = ', '.join(analysis.get('keywords') or [])
    langs = ', '.join(analysis.get('languages') or [])
    frs = ', '.join(analysis.get('frameworks') or [])
    header_content = f"[b]Keywords:[/] {keywords}    [b]Languages:[/] {langs}    [b]Frameworks:[/] {frs}"
    header_panel = Panel(header_content, title=header, border_style="green", padding=(0,1), expand=True)

    console.print(header_panel)

    table = Table(box=box.MINIMAL, show_lines=False, expand=True)
    table.add_column("Repository", style="cyan", no_wrap=True, overflow="ellipsis", max_width=40)
    table.add_column("Description", style="white", overflow="ellipsis", max_width=60)
    table.add_column("Lang", style="magenta", width=10, no_wrap=True)
    table.add_column("Stars", justify="right", style="yellow", no_wrap=True)
    table.add_column("Updated", style="green", no_wrap=True)
    table.add_column("URL", style="blue", overflow="ellipsis", max_width=60)

    for r in ranked:
        name, desc, lang, stars, updated, url = format_repo_row(r)
        # pretty updated date
        updated_display = updated
        try:
            updated_display = datetime.fromisoformat(updated.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except Exception:
            pass

        table.add_row(name, desc or "-", lang, stars, updated_display, url)

    console.print(table)

    # also print full URLs below so users can copy them easily
    url_lines = []
    for idx, r in enumerate(ranked, start=1):
        href = r.get("html_url") or ""
        url_lines.append(f"{idx}. {href}")
    if url_lines:
        console.print(Panel("\n".join(url_lines), title="Full URLs", border_style="blue"))

    # footer
    rl = rate_limit or {}
    rem = rl.get("remaining")
    if rem is not None:
        msg = f"GitHub rate limit remaining: {rem}"
        if rem == 0:
            msg += " (exhausted; wait until reset)"
        console.print(Panel(msg, border_style="red" if rem == 0 else "blue"))


def main():
    console.print(Panel("GitHub repository discovery — describe what you need", style="bold white on dark_green", padding=(0,1), expand=True))

    try:
        query = Prompt.ask("What kind of GitHub repository are you looking for?")
    except KeyboardInterrupt:
        console.print("\nAborted.")
        sys.exit(0)

    if not query or not query.strip():
        console.print("[red]Empty input received. Please describe the repository you're looking for.[/]")
        sys.exit(1)

    analysis = analyze(query)

    # prefer detected language if any
    language = (analysis.get("languages") or [None])[0]

    with console.status("Searching GitHub..."):
        try:
            res = fetch_combined(analysis.get("keywords"), language=language)
        except GitHubSearchError as e:
            console.print(Panel(f"Error: {e}", style="red"))
            sys.exit(1)

    items = res.get("items", [])
    rate_limit = res.get("rate_limit")

    if not items:
        console.print(Panel("No repositories found. Try another description or broaden keywords.", style="yellow"))
        if rate_limit:
            console.print(f"Rate info: {rate_limit}")
        sys.exit(0)

    ranked = rank_repositories(items, query, top_n=10)

    display_results(analysis, ranked, rate_limit)


if __name__ == "__main__":
    if not GITHUB_TOKEN:
        console.print(Panel("Warning: No GITHUB_TOKEN set — unauthenticated requests are rate-limited.", style="yellow"))
    main()
