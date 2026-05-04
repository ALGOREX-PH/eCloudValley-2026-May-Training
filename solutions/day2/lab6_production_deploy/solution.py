"""
Lab 6 — Reference solution.

FastAPI wrapper around the agentic RAG service from Lab 5.
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
DOCS_DIR = LAB_DIR.parent.parent.parent / "labs" / "day2" / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"


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


api = FastAPI(title="CloudKaiju Docs Agent", version="1.0.0")


class AskRequest(BaseModel):
    question: str
    session_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    session_id: str


@api.get("/health")
def health() -> dict:
    return {"status": "ok"}


@api.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    result = agent.run(req.question, session_id=req.session_id)
    return AskResponse(
        answer=result.content,
        session_id=result.session_id,
    )
