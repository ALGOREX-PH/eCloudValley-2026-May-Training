# Lab 6 — Ship It: FastAPI + Docker

> **Time:** 20 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Wrap your Lab 5 agentic RAG service in a FastAPI HTTP endpoint, containerize it with Docker, and run the whole thing locally with `docker compose up`. The same image will run on ECS, Cloud Run, or any Kubernetes cluster.

## What you'll learn

- Wrapping an Agno agent in a FastAPI route
- Pydantic request/response models
- Containerizing a Python app with `Dockerfile`
- Persisting the vector store across container restarts via a Docker volume
- Passing API keys safely via env vars

## Prerequisites

- **Docker Desktop installed and running** (`docker --version` works)
- Lab 5 working — the same `chroma_db` and docs are reused

## Run

```bash
cd labs/day2/lab6_production_deploy
docker compose up --build
```

In another terminal:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I rotate API keys?"}'
```

You should get JSON back:

```json
{
  "answer": "To rotate an API key in CloudKaiju...",
  "session_id": "..."
}
```

## What's in this folder

```
.
├── README.md
├── starter.py            # FastAPI app — fill in the TODOs
├── Dockerfile            # Multi-stage build, runs uvicorn
├── docker-compose.yml    # One-command local run with persistent volume
└── (chroma_db/)          # Created on first run; shared with Lab 4/5 via volume mount
```

## Endpoints to implement

| Method | Path | Body | Returns |
|---|---|---|---|
| `GET` | `/health` | — | `{"status": "ok"}` |
| `POST` | `/ask` | `{question: str, session_id?: str}` | `{answer: str, session_id: str}` |

## Stretch goals

- Add `/sessions/{id}/history` to inspect a conversation
- Add streaming via `text/event-stream` (FastAPI's `StreamingResponse`)
- Push the image to GHCR or ECR and deploy to your cloud of choice

## Common bugs

| Symptom | Fix |
|---|---|
| `Cannot connect to Docker daemon` | Start Docker Desktop |
| `OPENAI_API_KEY not set` inside container | Make sure your `.env` is at repo root and `env_file:` in compose points to it |
| Vector DB re-ingests on every restart | Volume mount missing or wrong path |
| `Address already in use` on 8000 | Another process; change the host port in compose: `"8001:8000"` |
