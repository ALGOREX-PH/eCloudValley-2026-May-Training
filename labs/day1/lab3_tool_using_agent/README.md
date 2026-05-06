# Lab 3 — Personal Research Assistant (Tools)

> **Time:** 30 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Build an agent that takes a research topic from the command line, searches the web, synthesizes findings into a structured markdown brief, and saves it to disk via your own custom tool.

## What you'll learn

- Built-in toolkit: `DuckDuckGoTools`
- Writing your own tool with the `@tool` decorator
- The ReAct trace shown live via `print_response(stream=True)`
- Multi-step reasoning over multiple tool calls
- Why docstrings ARE the API for LLMs

## Run

```bash
python labs/day1/lab3_tool_using_agent/starter.py "latest agentic AI papers"
```

Watch the trace appear. When it finishes, check the `notes/` folder — your brief should be there.

```bash
ls notes/
cat notes/latest-agentic-ai-papers.md
```

## What "good" looks like

- The agent searches with focused queries (not just the user's raw input)
- It synthesizes — doesn't just dump search results
- The markdown has clear sections: Summary, Key Findings, Sources
- Every claim has a URL citation
- File is saved with a sensible slug (lowercase, hyphens, no spaces)

## Stretch goals

- Add a 2nd custom tool: `read_note(filename)` that reads a previously-saved brief, so the agent can build on past research
- Add a "skim mode" that limits to 3 search queries (use `tool_call_limit`)
- Print the final brief to stdout in addition to saving

## Common bugs

| Symptom | Likely cause |
|---|---|
| Tool never called | Vague docstring; rewrite "Use this when…" |
| Wrong filename (spaces, caps) | Add explicit examples + format rules to the docstring |
| Agent loops calling search forever | Add a sentence to instructions: "Stop after 3 searches and write the brief" |
| Empty notes file | Tool was called with empty content — check the trace |
