"""
Lab 6 — Multi-Agent Team (20 min, paired)

Build a Team that has two specialists:
  - Docs Specialist  — RAG over the CloudKaiju docs (reuses Lab 4/5)
  - Web Researcher   — DuckDuckGo for general-web questions

A coordinator routes the question, dispatches to one or both members,
and synthesizes the final answer.

Run:
    python labs/day2/lab6_multi_agent_team/starter.py
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
DOCS_DIR = LAB_DIR.parent / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"


# ---------------------------------------------------------------------------
# Knowledge base — same Chroma setup as Lab 4 / 5
# ---------------------------------------------------------------------------

def build_knowledge() -> Knowledge:
    knowledge = Knowledge(
        vector_db=ChromaDb(collection="cloudkaiju", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)
    return knowledge


# ---------------------------------------------------------------------------
# TODO 1 — Build the Docs Specialist
# ---------------------------------------------------------------------------
# This is the Lab 5 agent, slightly tightened for team use.
# Requirements:
#   - name="Docs Specialist"
#   - role="Answer CloudKaiju product / docs questions with citations"
#   - model=OpenAIChat(id="gpt-4o-mini")
#   - knowledge=<the knowledge object passed in>
#   - search_knowledge=True
#   - instructions:
#       * Always search the knowledge base before answering.
#       * Cite every factual claim with [source: filename].
#       * If the docs don't cover it, say "I don't see that in the docs."
#       * Stay focused on CloudKaiju — don't speculate about other tools.
#   - markdown=True
def build_docs_specialist(knowledge: Knowledge) -> Agent:
    ...


# ---------------------------------------------------------------------------
# TODO 2 — Build the Web Researcher
# ---------------------------------------------------------------------------
# Requirements:
#   - name="Web Researcher"
#   - role="Search the public web for general / industry questions"
#   - model=OpenAIChat(id="gpt-4o-mini")
#   - tools=[DuckDuckGoTools()]
#   - tool_call_limit=4   # cap searches to keep latency / cost bounded
#   - instructions:
#       * Search the web 1–3 times with focused queries.
#       * Keep replies under 6 sentences.
#       * Always include the URL for every claim you make.
#       * If asked about CloudKaiju specifically, say
#         "Defer to the Docs Specialist for product questions."
#   - markdown=True
def build_web_researcher() -> Agent:
    ...


# ---------------------------------------------------------------------------
# TODO 3 — Compose the Team
# ---------------------------------------------------------------------------
# Use Agno's Team with mode="coordinate" so the coordinator can dispatch
# to one or both members and merge the results.
#
# Requirements:
#   - name="CloudKaiju Support Team"
#   - mode="coordinate"
#   - model=OpenAIChat(id="gpt-4o-mini")   # this is the coordinator
#   - members=[docs, web]
#   - show_members_responses=True
#   - markdown=True
#   - instructions:
#       * Read the question and decide which member(s) should answer.
#       * For CloudKaiju product/docs questions → Docs Specialist.
#       * For general / industry / "what's a good X" questions → Web Researcher.
#       * If the question needs both (e.g., comparison), dispatch both
#         and merge their replies into ONE coherent answer.
#       * Refuse off-topic questions politely (weather, sports, personal advice).
#       * Always preserve the citations / URLs from members in the final answer.
def build_team(docs: Agent, web: Agent) -> Team:
    ...


def repl(team: Team) -> None:
    print("CloudKaiju Support Team 🦖🤝🌐  (Ctrl+C to exit)\n")
    print("Try mixing docs questions with general-web questions.\n")
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
