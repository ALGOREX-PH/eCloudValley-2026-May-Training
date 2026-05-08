"""
Lab 4 — Reference solution.

Ingest the Financial Wellness Journal PDF into Chroma, then run similarity
queries and render the matched chunks (with source file + page number) using
Agno's bundled Rich console.
"""

import sys
from pathlib import Path

from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

load_dotenv()

# Windows PowerShell legacy console can't encode emojis through Rich's
# legacy renderer — force UTF-8 stdout so the panels render cleanly.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LAB_DIR = Path(__file__).parent
DOCS_DIR = LAB_DIR.parent.parent.parent / "labs" / "day2" / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"

console = Console()


def build_knowledge() -> Knowledge:
    vector_db = ChromaDb(
        collection="fined_journal",
        path=str(DB_PATH),
    )

    knowledge = Knowledge(vector_db=vector_db)

    # Idempotent — Agno detects already-ingested content
    knowledge.add_content(path=DOCS_DIR)

    return knowledge


QUERIES = [
    "What is financial wellness?",
    "What kinds of insurance should I consider?",
    "How do I avoid a debt trap?",
    "What's the difference between saving, insurance, and investment?",
]


def _preview(text: str, width: int = 220) -> str:
    cleaned = " ".join(text.split())
    return cleaned if len(cleaned) <= width else cleaned[: width - 1] + "…"


def render_results(query: str, results) -> None:
    if not results:
        console.print(Panel(f"No matches for: {query}", style="yellow"))
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        expand=True,
        pad_edge=False,
    )
    table.add_column("#", justify="right", width=3, style="bold")
    table.add_column("Source", style="green", no_wrap=True)
    table.add_column("Page", justify="right", style="magenta", width=5)
    table.add_column("Distance", justify="right", style="yellow", width=9)
    table.add_column("Preview", overflow="fold", ratio=1)

    for i, r in enumerate(results, 1):
        meta = r.meta_data or {}
        page = meta.get("page", "—")
        distance = meta.get("distances")
        distance_str = f"{distance:.4f}" if isinstance(distance, (int, float)) else "—"

        table.add_row(
            str(i),
            r.name or "(unknown)",
            str(page),
            distance_str,
            _preview(r.content),
        )

    console.print(
        Panel(
            table,
            title=Text(f"❓ {query}", style="bold white"),
            border_style="cyan",
            padding=(1, 1),
        )
    )


def main() -> None:
    console.print(
        Panel.fit(
            f"📚 Building knowledge base\n[dim]{DOCS_DIR}[/dim]",
            border_style="green",
        )
    )
    knowledge = build_knowledge()

    for q in QUERIES:
        results = knowledge.search(q, max_results=3)
        render_results(q, results)
        console.print()


if __name__ == "__main__":
    main()
