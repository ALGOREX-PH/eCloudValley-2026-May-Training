"""
Lab 5 — Agentic Documentation Assistant (30 min, paired)

The agent (FinEd Coach) answers personal-finance questions using the
Financial Wellness Journal PDF from Lab 4.

Run:
    python labs/day2/lab5_agentic_rag/starter.py
"""

from pathlib import Path

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv()

LAB_DIR = Path(__file__).parent
# Re-use Lab 4's docs to keep things simple
DOCS_DIR = LAB_DIR.parent / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"


def build_knowledge() -> Knowledge:
    knowledge = Knowledge(
        vector_db=ChromaDb(collection="fined_journal", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)
    return knowledge


def build_agent(knowledge: Knowledge) -> Agent:
    """Build the agentic RAG documentation assistant.

    TODO — Construct the Agent with:
      - model: OpenAIChat(id="gpt-4o-mini")
      - knowledge: the knowledge object passed in
      - search_knowledge: True   (this is the agentic switch)
      - markdown: True
      - instructions: a list that ENFORCES:
          1. Role: "FinEd Coach" — a personal-finance coach grounded in the
             Financial Wellness Journal
          2. CITE every factual claim with [source: financial-wellness-journal-english.pdf]
             (mention the chapter or page if you can infer it from the chunk)
          3. REFUSE off-topic questions politely (weather, sports, politics) with
             "I only answer personal-finance questions from the Financial Wellness Journal."
          4. ADMIT when an answer isn't in the journal — DO NOT make things up
          5. SEARCH the knowledge base before answering anything factual
          6. Keep replies under 6 sentences unless walking through a procedure
    """
    agent = ...  # TODO

    return agent


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
