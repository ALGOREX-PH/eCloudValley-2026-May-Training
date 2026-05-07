# Lab 6 — Multi-Agent Team

> **Time:** 20 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Build a two-agent **team** that decides on its own which specialist should answer:

- **FinEd Coach** — reuses the Lab 5 RAG agent over the Financial Wellness Journal
- **Web Researcher** — searches the public web with DuckDuckGo (current rates, BSP news, etc.)

A **coordinator** routes each question to the right member, runs them in parallel when both are needed, and synthesizes the final answer.

```
                ┌──────────────────────────────┐
   user  ─────► │  Coordinator (Team)          │
                │  — reads the question        │
                │  — decides who to dispatch   │
                └──┬──────────────────┬─────────┘
                   ▼                  ▼
       ┌────────────────────┐   ┌────────────────────┐
       │ FinEd Coach        │   │ Web Researcher     │
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

- Lab 4 + Lab 5 working (we reuse the same `chroma_db` and Financial Wellness Journal)
- `OPENAI_API_KEY` in your `.env`

## Run

```bash
python labs/day2/lab6_multi_agent_team/starter.py
```

You'll get an interactive prompt. Try a mix:

| Question                                                       | Who should answer            |
| -------------------------------------------------------------- | ---------------------------- |
| `What's a debt trap and how do I avoid it?`                    | FinEd Coach                  |
| `Tell me about Mang Rafael's saving problem`                   | FinEd Coach                  |
| `What is BSP's current overnight reverse repo rate?`           | Web Researcher               |
| `What does the journal say about insurance, and what are typical premiums in PH right now?` | Both — coordinator merges |
| `What's the weather in Manila?`                                | Coordinator should refuse    |

Watch the printed member calls — you'll see the coordinator decide.

## What's in this folder

```
.
├── README.md
└── starter.py     # The team — fill in the TODOs
```

## TODOs in the starter

1. Build the **FinEd Coach** agent (RAG + citations)
2. Build the **Web Researcher** agent (DuckDuckGo, brief replies, source URLs)
3. Compose them into a `Team` with a clear coordinator prompt

## Stretch goals

- Add a third member: a **Loan Calculator** with a custom `@tool` that computes monthly amortization from principal, rate, and term
- Try `mode="route"` — the coordinator picks exactly one specialist instead of merging
- Cap the team's total tool calls to bound cost
- Add a refusal guardrail at the team level for non-finance questions

## When NOT to use multi-agent

| Symptom                                                | Better answer            |
| ------------------------------------------------------ | ------------------------ |
| Latency matters and one agent could already do this    | One agent + more tools   |
| You only have one knowledge source                     | One agent + RAG          |
| Two agents keep contradicting each other               | Tighten the single agent's prompt |
| Cost is going up faster than answer quality            | Drop a member            |

Multi-agent shines when **specialists genuinely disagree on what 'good' looks like** — e.g., a journal-grounded coach that refuses to speculate vs. a web researcher that's expected to fetch live data. If both members have the same goals and tools, you've built a slower single agent.

## Common bugs

| Symptom                                                   | Fix                                                                     |
| --------------------------------------------------------- | ----------------------------------------------------------------------- |
| Coordinator answers without calling any member            | Tighten its instructions: *"Always dispatch to a specialist for facts"* |
| Both members run on every question                        | Add explicit routing rules in the coordinator's instructions            |
| Web Researcher cites no sources                           | Tell it explicitly: *"Always include the URL for each claim"*           |
| FinEd Coach makes things up                               | It needs `search_knowledge=True` + citation rules from Lab 5            |
| DuckDuckGo errors out                                     | Rate-limited; rerun in 30s or switch to BraveSearchTools (paid key)     |
