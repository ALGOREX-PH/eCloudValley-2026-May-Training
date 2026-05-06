"""
Lab 5 — Reference solution.

Agentic documentation assistant — searches knowledge base, cites sources,
refuses out-of-scope questions, admits gaps.
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
        vector_db=ChromaDb(collection="cloudkaiju", path=str(DB_PATH)),
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
            "You are the CloudKaiju documentation assistant.",
            "Always search the knowledge base before answering any factual question.",
            "Cite EVERY factual claim with [source: filename] using the chunk's source filename.",
            "If the knowledge base does not contain an answer, say exactly: "
            "'I don't see that in the docs.' — do NOT make things up.",
            "Refuse politely if the question is not about CloudKaiju: "
            "'I only answer questions about CloudKaiju.'",
            "Keep replies under 6 sentences unless walking through a procedure.",
        ],
    )


def repl(agent: Agent) -> None:
    print("CloudKaiju Docs Bot 📚  (Ctrl+C to exit)\n")
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
