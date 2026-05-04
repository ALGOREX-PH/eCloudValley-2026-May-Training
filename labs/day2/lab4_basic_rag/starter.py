"""
Lab 4 — Build a Vector DB from Documents (20 min, instructor-led)

Ingest a folder of markdown docs into Chroma, then run similarity queries.

Run:
    python labs/day2/lab4_basic_rag/starter.py
"""

from pathlib import Path

from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv()

LAB_DIR = Path(__file__).parent
DOCS_DIR = LAB_DIR / "docs"
DB_PATH = LAB_DIR / "chroma_db"


def build_knowledge() -> Knowledge:
    """Build (and ingest, on first run) the Chroma-backed knowledge base."""
    # TODO 1 — Create a ChromaDb pointed at DB_PATH, collection name "cloudkaiju".
    vector_db = ...  # TODO 1

    # TODO 2 — Wrap it in a Knowledge object.
    knowledge = ...  # TODO 2

    # TODO 3 — Ingest DOCS_DIR (Agno re-uses an existing index automatically).
    #          Hint: knowledge.add_content(path=DOCS_DIR)
    ...  # TODO 3

    return knowledge


QUERIES = [
    "How do I rotate API keys?",
    "What's the SLA for the Pro tier?",
    "Does CloudKaiju support OIDC?",
    "What's the pricing for the Free plan?",
]


def main() -> None:
    print(f"📚 Building knowledge base from: {DOCS_DIR}\n")
    knowledge = build_knowledge()

    for q in QUERIES:
        print(f"❓ {q}")
        results = knowledge.search(q, num_documents=3)
        for i, r in enumerate(results, 1):
            preview = r.content[:160].replace("\n", " ")
            score = getattr(r, "score", None)
            print(f"  [{i}] (score={score})  {preview}…")
        print()


if __name__ == "__main__":
    main()
