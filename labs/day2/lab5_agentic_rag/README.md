# Lab 5 — Agentic Documentation Assistant

> **Time:** 30 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Build an agent that answers questions about CloudKaiju using the docs from Lab 4. The agent must:

- **Cite** every factual claim with the source filename
- **Refuse** out-of-scope questions ("What's the weather?")
- **Honestly say** "not in the docs" when stumped, instead of hallucinating
- **Decide** when to search and when it already knows

## What you'll learn

- The "knowledge as a tool" pattern (`search_knowledge=True`)
- Writing instructions for citations + guardrails
- Multi-step retrieval (the agent searches, thinks, searches again)
- The difference between a chatbot with RAG and an *agentic* RAG system

## Run

```bash
python labs/day2/lab5_agentic_rag/starter.py
```

You'll get an interactive prompt. Try these:

```
> How do I rotate API keys?
> Does CloudKaiju support OIDC on the Free tier?
> What's the SLA for Enterprise?
> What's the weather in Manila?     # should refuse
> Who is the CEO?                   # should say "not in docs"
```

## What "good" looks like

| Question | Expected behavior |
|---|---|
| "How do I rotate API keys?" | Step-by-step from `02-security.md`, cited |
| "Does CloudKaiju support OIDC on Free?" | "No, OIDC is Pro and Enterprise only" — cited |
| "What's the SLA for Enterprise?" | "99.95% uptime, ..." cited from `03-pricing-and-sla.md` |
| "What's the weather?" | Polite refusal: "I only answer questions about CloudKaiju" |
| "What color is the logo?" | "I don't see that in the docs" |

## Stretch goals

- Add a `--debug` flag that prints the full tool-call trace
- Add a custom tool `report_gap(question)` that logs questions the agent couldn't answer (so PMs can prioritize doc updates)
- Try lowering the LLM temperature to 0 — see if hallucinations drop

## Tips

- The first time it runs, it ingests the docs (~5 sec). Subsequent runs reuse the index.
- If it ever hallucinates a fact, watch the streamed tool-call output — did it actually search? Did the search return relevant chunks?
- The instructions string is doing 80% of the work here. Iterate on it.
