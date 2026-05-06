"""
Lab 6 — Reference solution.

A two-specialist team — Docs (RAG) + Web Researcher (DuckDuckGo) — with
a coordinator that routes questions and merges answers.
"""

from pathlib import Path

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
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


def build_docs_specialist(knowledge: Knowledge) -> Agent:
    return Agent(
        name="Docs Specialist",
        role="Answer CloudKaiju product / docs questions with citations.",
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "Always search the knowledge base before answering.",
            "Cite every factual claim with [source: filename].",
            "If the docs don't cover it, say exactly: 'I don't see that in the docs.'",
            "Stay focused on CloudKaiju — don't speculate about other tools.",
        ],
        markdown=True,
    )


def build_web_researcher() -> Agent:
    return Agent(
        name="Web Researcher",
        role="Search the public web for general / industry questions.",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools()],
        tool_call_limit=4,
        instructions=[
            "Search the web 1–3 times with focused queries, then stop.",
            "Keep replies under 6 sentences.",
            "Always include the URL for every claim you make.",
            "If asked about CloudKaiju specifically, reply: "
            "'Defer to the Docs Specialist for product questions.'",
        ],
        markdown=True,
    )


def build_team(docs: Agent, web: Agent) -> Team:
    return Team(
        name="CloudKaiju Support Team",
        mode="coordinate",
        model=OpenAIChat(id="gpt-4o-mini"),
        members=[docs, web],
        show_members_responses=True,
        markdown=True,
        instructions=[
            "Read the question and decide which member(s) should answer.",
            "CloudKaiju product / docs questions → Docs Specialist.",
            "General / industry / 'what's a good X' questions → Web Researcher.",
            "If the question needs both (e.g., a comparison), dispatch both "
            "and merge their replies into ONE coherent answer.",
            "Refuse off-topic questions politely (weather, sports, personal advice).",
            "Always preserve the citations and URLs the members produced — "
            "don't drop sources when synthesizing.",
        ],
    )


def repl(team: Team) -> None:
    print("CloudKaiju Support Team 🦖🤝🌐  (Ctrl+C to exit)\n")
    try:
        while True:
            q = input("you ▸ ").strip()
            if not q:
                continue
            print()
            team.print_response(q, stream=True)
            print()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    print("📚 Loading knowledge base...")
    knowledge = build_knowledge()

    print("🤖 Wiring up specialists...")
    docs = build_docs_specialist(knowledge)
    web = build_web_researcher()

    print("🤝 Composing the team...\n")
    team = build_team(docs, web)

    repl(team)
