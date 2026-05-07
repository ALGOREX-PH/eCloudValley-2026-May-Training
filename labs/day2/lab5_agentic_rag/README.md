# Lab 5 — Agentic Documentation Assistant (FinEd Coach)

> **Time:** 30 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Build **FinEd Coach** — an agent that answers personal-finance questions using the Financial Wellness Journal from Lab 4. The agent must:

- **Cite** every factual claim with the source file (and chapter where possible)
- **Refuse** off-topic questions ("What's the weather?")
- **Honestly say** "not in the journal" when stumped, instead of hallucinating
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
> What is financial wellness?
> What kinds of insurance should I consider?
> What is a debt trap and how do I avoid it?
> Tell me about Mang Rafael's saving problem.
> What's the difference between saving, insurance, and investment?
> What's the weather in Manila?               # should refuse
> Who is the CEO of BPI?                      # should say "not in the journal"
```

## What "good" looks like

| Question | Expected behavior |
|---|---|
| "What is financial wellness?" | Concise definition pulled from Chapter 1, cited |
| "What kinds of insurance should I consider?" | List from Chapter 3, cited |
| "How do I avoid a debt trap?" | Tips from Chapter 4, cited |
| "Tell me about Mang Rafael's saving problem" | Summary of the case study from Chapter 2, cited |
| "What's the weather?" | Polite refusal: "I only answer personal-finance questions from the Financial Wellness Journal." |
| "Who is the CEO of BPI?" | "I don't see that in the journal." |

## Stretch goals

- Add a `--debug` flag that prints the full tool-call trace
- Add a custom tool `report_gap(question)` that logs questions the agent couldn't answer (so the FinEd team can prioritize new content)
- Try lowering the LLM temperature to 0 — see if hallucinations drop
- Add a "give me a savings tip in Tagalog" path that translates the journal's advice

## Tips

- The first time it runs, it ingests the PDF (~10–20 sec for 55 pages). Subsequent runs reuse the index.
- If it ever hallucinates a fact, watch the streamed tool-call output — did it actually search? Did the search return relevant chunks?
- The instructions string is doing 80% of the work here. Iterate on it.
