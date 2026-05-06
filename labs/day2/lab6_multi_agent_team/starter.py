"""
Lab 6 — Ship It: FastAPI + Docker (20 min, paired)

Wrap the Lab 5 agentic RAG service in a FastAPI HTTP endpoint.

Run locally (without Docker, for fast iteration):
    uvicorn labs.day2.lab6_production_deploy.starter:api --reload --port 8000

Run with Docker:
    cd labs/day2/lab6_production_deploy
    docker compose up --build
"""

from pathlib import Path

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

LAB_DIR = Path(__file__).parent
DOCS_DIR = LAB_DIR.parent / "lab4_basic_rag" / "docs"
# In Docker, this folder is a mounted volume so the index persists.
DB_PATH = LAB_DIR / "chroma_db"


# ---------------------------------------------------------------------------
# Build the agent ONCE at startup (don't re-build on every request)
# ---------------------------------------------------------------------------

def _build_agent() -> Agent:
    knowledge = Knowledge(
        vector_db=ChromaDb(collection="cloudkaiju", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)

    return Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "You are the CloudKaiju documentation assistant.",
            "Always search the knowledge base before answering factual questions.",
            "Cite every factual claim with [source: filename].",
            "If something isn't in the docs, say so — don't make things up.",
            "Refuse non-CloudKaiju questions politely.",
        ],
        markdown=True,
    )


agent: Agent = _build_agent()


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

api = FastAPI(title="CloudKaiju Docs Agent", version="1.0.0")


class AskRequest(BaseModel):
    question: str
    session_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    session_id: str


@api.get("/health")
def health() -> dict:
    """TODO 1 — Return {"status": "ok"}."""
    ...


@api.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    """TODO 2 — Run the agent against req.question.

    Use req.session_id if provided so multi-turn conversations work.

    Return AskResponse with:
      - answer: result.content
      - session_id: result.session_id (Agno generates one if not provided)
    """
    ...
