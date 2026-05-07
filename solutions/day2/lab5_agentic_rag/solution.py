"""
Lab 5 — Reference solution.

FinEd Coach — agentic RAG over the Financial Wellness Journal.
Searches knowledge base, cites sources, refuses off-topic, admits gaps.
"""

from pathlib import Path

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv()

LAB_DIR = Path(__file__).parent
DOCS_DIR = LAB_DIR.parent.parent.parent / "labs" / "day2" / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"


def build_knowledge() -> Knowledge:
    knowledge = Knowledge(
        vector_db=ChromaDb(collection="fined_journal", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)
    return knowledge


def build_agent(knowledge: Knowledge) -> Agent:
    return Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=knowledge,
        search_knowledge=True,
        markdown=True,
        tool_call_limit=6,
        instructions=[
            "You are FinEd Coach — a personal-finance coach grounded in the "
            "Financial Wellness Journal (BPI Foundation FinEd program).",
            "Always search the knowledge base before answering any factual question.",
            "Cite EVERY factual claim with [source: financial-wellness-journal-english.pdf] "
            "and add the chapter or topic when you can infer it from the chunk.",
            "If the journal does not contain an answer, say exactly: "
            "\"I don't see that in the journal.\" — do NOT make things up.",
            "Refuse politely if the question is not about personal finance: "
            "\"I only answer personal-finance questions from the Financial Wellness Journal.\"",
            "Keep replies under 6 sentences unless walking through a procedure or case study.",
        ],
    )


def repl(agent: Agent) -> None:
    print("FinEd Coach 💸  (Ctrl+C to exit)\n")
    try:
        while True:
            q = input("you ▸ ").strip()
            if not q:
                continue
            print()
            agent.print_response(q, stream=True)
            print()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    print("📚 Loading knowledge base...")
    knowledge = build_knowledge()
    print("🤖 Starting agent...\n")
    agent = build_agent(knowledge)
    repl(agent)
