# Lab 6 — Multi-Agent Team

> **Time:** 20 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Build a two-agent **team** that decides on its own which specialist should answer:

- **Docs Specialist** — reuses the Lab 5 RAG agent over the CloudKaiju docs
- **Web Researcher** — searches the public web with DuckDuckGo

A **coordinator** routes each question to the right member, runs them in parallel when both are needed, and synthesizes the final answer.

```
                ┌──────────────────────────────┐
   user  ─────► │  Coordinator (Team)          │
                │  — reads the question        │
                │  — decides who to dispatch   │
                └──┬──────────────────┬─────────┘
                   ▼                  ▼
       ┌────────────────────┐   ┌────────────────────┐
       │ Docs Specialist    │   │ Web Researcher     │
       │ (RAG, citations)   │   │ (DuckDuckGo)       │
       └────────────────────┘   └────────────────────┘
                   │                  │
                   └────────┬─────────┘
                            ▼
                       Final answer
```

## What you'll learn

- **Specialist agents** with focused instructions and tools
- Agno's **`Team`** primitive and the `coordinate` / `route` / `collaborate` modes
- Routing decisions made by the model, not by your code
- When multi-agent helps — and when it just adds latency and cost

## Prerequisites

- Lab 4 + Lab 5 working (we reuse the same `chroma_db` and CloudKaiju docs)
- `OPENAI_API_KEY` in your `.env`

## Run

```bash
python labs/day2/lab6_multi_agent_team/starter.py
```

You'll get an interactive prompt. Try a mix:

| Question                                            | Who should answer            |
| --------------------------------------------------- | ---------------------------- |
| `How do I rotate API keys in CloudKaiju?`           | Docs Specialist              |
| `What's the SLA on the Pro tier?`                   | Docs Specialist              |
| `What's a good open-source LLM observability tool in 2026?` | Web Researcher       |
| `Compare CloudKaiju Pro to similar managed services` | Both — coordinator merges   |
| `What's the weather in Manila?`                     | Coordinator should refuse    |

Watch the printed member calls — you'll see the coordinator decide.

## What's in this folder

```
.
├── README.md
└── starter.py     # The team — fill in the TODOs
```

## TODOs in the starter

1. Build the **Docs Specialist** agent (RAG + citations)
2. Build the **Web Researcher** agent (DuckDuckGo, brief replies, source URLs)
3. Compose them into a `Team` with a clear coordinator prompt

## Stretch goals

- Add a third member: a **Pricing Calculator** with a custom `@tool` that computes monthly cost from tier + usage
- Try `mode="route"` — the coordinator picks exactly one specialist instead of merging
- Cap the team's total tool calls to bound cost
- Add a refusal guardrail at the team level for off-topic questions

## When NOT to use multi-agent

| Symptom                                                | Better answer            |
| ------------------------------------------------------ | ------------------------ |
| Latency matters and one agent could already do this    | One agent + more tools   |
| You only have one knowledge source                     | One agent + RAG          |
| Two agents keep contradicting each other               | Tighten the single agent's prompt |
| Cost is going up faster than answer quality            | Drop a member            |

Multi-agent shines when **specialists genuinely disagree on what 'good' looks like** — e.g., a docs-grounded specialist that refuses to speculate vs. a web researcher that's expected to. If both members have the same goals and tools, you've built a slower single agent.

## Common bugs

| Symptom                                                   | Fix                                                                     |
| --------------------------------------------------------- | ----------------------------------------------------------------------- |
| Coordinator answers without calling any member            | Tighten its instructions: *"Always dispatch to a specialist for facts"* |
| Both members run on every question                        | Add explicit routing rules in the coordinator's instructions            |
| Web Researcher cites no sources                           | Tell it explicitly: *"Always include the URL for each claim"*           |
| Docs Specialist makes things up                           | It needs `search_knowledge=True` + citation rules from Lab 5            |
