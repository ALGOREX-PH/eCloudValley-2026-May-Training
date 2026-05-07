"""
Lab 6 — Multi-Agent Team (20 min, paired)

Build a Team that has two specialists:
  - FinEd Coach     — RAG over the Financial Wellness Journal (reuses Lab 4/5)
  - Web Researcher  — DuckDuckGo for current rates / news / market info

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
        vector_db=ChromaDb(collection="fined_journal", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)
    return knowledge


# ---------------------------------------------------------------------------
# TODO 1 — Build the FinEd Coach (Lab 5 agent, tightened for team use)
# ---------------------------------------------------------------------------
# Requirements:
#   - name="FinEd Coach"
#   - role="Answer personal-finance questions from the Financial Wellness Journal with citations"
#   - model=OpenAIChat(id="gpt-4o-mini")
#   - knowledge=<the knowledge object passed in>
#   - search_knowledge=True
#   - instructions:
#       * Always search the knowledge base before answering.
#       * Cite every factual claim with [source: financial-wellness-journal-english.pdf].
#       * If the journal doesn't cover it, say "I don't see that in the journal."
#       * Stay focused on personal finance — defer current rates / news to the Web Researcher.
#   - markdown=True
def build_fined_coach(knowledge: Knowledge) -> Agent:
    ...


# ---------------------------------------------------------------------------
# TODO 2 — Build the Web Researcher
# ---------------------------------------------------------------------------
# Requirements:
#   - name="Web Researcher"
#   - role="Search the public web for current rates, news, market data, BSP announcements"
#   - model=OpenAIChat(id="gpt-4o-mini")
#   - tools=[DuckDuckGoTools()]
#   - tool_call_limit=4   # cap searches to keep latency / cost bounded
#   - instructions:
#       * Search the web 1–3 times with focused queries.
#       * Keep replies under 6 sentences.
#       * Always include the URL for every claim you make.
#       * If asked about general personal-finance concepts, say
#         "Defer to FinEd Coach for grounded personal-finance guidance."
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
#   - name="Personal Finance Team"
#   - mode="coordinate"
#   - model=OpenAIChat(id="gpt-4o-mini")   # this is the coordinator
#   - members=[fined, web]
#   - show_members_responses=True
#   - markdown=True
#   - instructions:
#       * Read the question and decide which member(s) should answer.
#       * Personal-finance concepts / case studies / journal content → FinEd Coach.
#       * Current rates, BSP announcements, market data, news → Web Researcher.
#       * If the question needs both (e.g., "what does the journal say about
#         insurance and what are current rates?"), dispatch both and merge.
#       * Refuse off-topic questions politely (weather, sports, personal advice
#         outside finance).
#       * Always preserve the citations / URLs from members in the final answer.
def build_team(fined: Agent, web: Agent) -> Team:
    ...


def repl(team: Team) -> None:
    print("Personal Finance Team 💸🤝🌐  (Ctrl+C to exit)\n")
    print("Try mixing journal questions with current-rates questions.\n")
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
