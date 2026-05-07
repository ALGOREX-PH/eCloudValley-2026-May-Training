"""
Lab 6 — Reference solution.

Personal Finance Team — FinEd Coach (RAG over the Financial Wellness Journal)
+ Web Researcher (DuckDuckGo for current rates / news), with a coordinator.
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
        vector_db=ChromaDb(collection="fined_journal", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)
    return knowledge


def build_fined_coach(knowledge: Knowledge) -> Agent:
    return Agent(
        name="FinEd Coach",
        role="Answer personal-finance questions from the Financial Wellness Journal with citations.",
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "Always search the knowledge base before answering.",
            "Cite every factual claim with [source: financial-wellness-journal-english.pdf] "
            "and add the chapter or topic when you can infer it.",
            "If the journal doesn't cover it, say exactly: \"I don't see that in the journal.\"",
            "Stay focused on personal finance from the journal — defer current rates, "
            "news, and BSP announcements to the Web Researcher.",
        ],
        markdown=True,
    )


def build_web_researcher() -> Agent:
    return Agent(
        name="Web Researcher",
        role="Search the public web for current rates, news, BSP announcements, and market data.",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools()],
        tool_call_limit=4,
        instructions=[
            "Search the web 1–3 times with focused queries, then stop.",
            "Keep replies under 6 sentences.",
            "Always include the URL for every claim you make.",
            "If asked about general personal-finance concepts, reply: "
            "\"Defer to FinEd Coach for grounded personal-finance guidance.\"",
        ],
        markdown=True,
    )


def build_team(fined: Agent, web: Agent) -> Team:
    return Team(
        name="Personal Finance Team",
        mode="coordinate",
        model=OpenAIChat(id="gpt-4o-mini"),
        members=[fined, web],
        show_members_responses=True,
        markdown=True,
        instructions=[
            "Read the question and decide which member(s) should answer.",
            "Personal-finance concepts / case studies / journal content → FinEd Coach.",
            "Current rates, BSP announcements, market data, news → Web Researcher.",
            "If the question needs both (e.g., 'what does the journal say about insurance "
            "AND what are current rates?'), dispatch both and merge their replies into ONE "
            "coherent answer.",
            "Refuse off-topic questions politely (weather, sports, personal advice "
            "outside finance).",
            "Always preserve the citations and URLs the members produced — "
            "don't drop sources when synthesizing.",
        ],
    )


def repl(team: Team) -> None:
    print("Personal Finance Team 💸🤝🌐  (Ctrl+C to exit)\n")
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
    fined = build_fined_coach(knowledge)
    web = build_web_researcher()

    print("🤝 Composing the team...\n")
    team = build_team(fined, web)

    repl(team)
