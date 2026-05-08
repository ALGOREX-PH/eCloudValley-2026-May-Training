"""
Lab 4 — Reference solution.

Ingest the Financial Wellness Journal PDF into Chroma, then run similarity
queries and render each matched chunk (source filename + page number +
similarity distance + content preview) as a Rich panel.

Rich is bundled with Agno's dependencies — same console primitives Agno's own
agents use under the hood.
"""

import sys
from pathlib import Path

from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
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


def _preview(text: str, width: int = 320) -> str:
    cleaned = " ".join(text.split())
    return cleaned if len(cleaned) <= width else cleaned[: width - 1] + "…"


def render_results(query: str, results) -> None:
    console.print(Rule(Text(f"❓ {query}", style="bold cyan"), style="cyan"))

    if not results:
        console.print("[yellow]  No matches.[/yellow]\n")
        return

    for i, r in enumerate(results, 1):
        meta = r.meta_data or {}
        page = meta.get("page", "—")
        distance = meta.get("distances")
        distance_str = f"{distance:.4f}" if isinstance(distance, (int, float)) else "—"
        source = r.name or "(unknown)"

        header = Text.assemble(
            ("#", "bold white"), (f"{i}", "bold white"),
            ("  ·  ", "dim"),
            ("page ", "magenta"), (str(page), "bold magenta"),
            ("  ·  ", "dim"),
            ("distance ", "yellow"), (distance_str, "bold yellow"),
            ("  ·  ", "dim"),
            (source, "green"),
        )

        body = Text(_preview(r.content), style="white")

        console.print(
            Panel(
                Group(header, Text(""), body),
                border_style="cyan",
                padding=(0, 1),
            )
        )

    console.print()


def main() -> None:
    console.print(
        Panel.fit(
            f"📚 Building knowledge base\n[dim]{DOCS_DIR}[/dim]",
            border_style="green",
        )
    )
    knowledge = build_knowledge()
    console.print()

    for q in QUERIES:
        results = knowledge.search(q, max_results=3)
        render_results(q, results)


if __name__ == "__main__":
    main()
