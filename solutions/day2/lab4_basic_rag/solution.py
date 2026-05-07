"""
Lab 4 — Reference solution.

Ingest CloudKaiju docs into Chroma, then run similarity queries.
"""

from pathlib import Path

from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv()

# Re-use Lab 4's docs (same path the starter uses)
LAB_DIR = Path(__file__).parent
DOCS_DIR = LAB_DIR.parent.parent.parent / "labs" / "day2" / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"


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


def main() -> None:
    print(f"📚 Building knowledge base from: {DOCS_DIR}\n")
    knowledge = build_knowledge()

    for q in QUERIES:
        print(f"❓ {q}")
        results = knowledge.search(q, max_results=3)
        for i, r in enumerate(results, 1):
            preview = r.content[:160].replace("\n", " ")
            score = getattr(r, "score", None)
            print(f"  [{i}] (score={score})  {preview}…")
        print()


if __name__ == "__main__":
    main()
