# Lab 3B — Research Assistant Pro *(Optional)*

> **Time:** Open-ended (15–25 min if you finished Lab 3 early)
> **Format:** Solo or paired. Builds on Lab 3.

## Why this exists

Lab 3 gave you a research agent that searches the open web and saves a markdown brief. In real life you usually want **two more knobs**:

1. **Preferred sources** — "Don't quote random blogs. Use arxiv, anthropic, openai, agno docs."
2. **Output format** — Your boss wants a `.docx`. Your CTO wants a `.pdf`. You want `.md`.

This lab adds both — same agent shape, two new constraints.

## Goal

Run:

```bash
python labs/day1/lab3b_research_pro/starter.py "agentic AI patterns 2026" --format pdf
```

…and end up with a polished `notes/agentic-ai-patterns-2026.pdf` whose sources are mostly from your preferred-domain list.

## What you'll learn

- **Steering search with `site:`** — DuckDuckGo's domain operator, and how to teach the agent to use it
- **Tools that branch on input** — one `save_note` tool, three output formats
- **Composing pure-Python output libraries** — `python-docx` + `fpdf2`, no system deps
- **CLI flags that change agent behavior** — `argparse` → instruction text → search queries

## Prerequisites

```bash
pip install python-docx fpdf2
```

(Already in `requirements.txt` from this commit, so a fresh install picks them up.)

## Run

```bash
# Markdown (default)
python starter.py "best practices for prompt caching"

# DOCX
python starter.py "best practices for prompt caching" --format docx

# PDF
python starter.py "best practices for prompt caching" --format pdf

# Override the preferred sources
python starter.py "philippine fintech AI 2026" --format md \
  --sources bsp.gov.ph rappler.com inquirer.net manilatimes.net
```

## Default preferred sources

If you don't pass `--sources`, the agent prefers:

```
arxiv.org   anthropic.com   openai.com   docs.agno.com
research.google   deepmind.google   huggingface.co
```

The agent will still occasionally hit other domains if a preferred source has nothing — that's intentional. The list is a *preference*, not a hard filter.

## TODOs in the starter

1. Implement `save_note` to handle `md`, `docx`, and `pdf` (the format param picks the branch)
2. Build the agent with a `site:` clause stitched into its instructions from the `preferred_sites` list

## What "good" looks like

| File | Heading rendering | Bullet rendering | URLs preserved |
|---|---|---|---|
| `.md` | `# / ##` | `- ` | yes |
| `.docx` | Word native heading styles | "List Bullet" style | yes |
| `.pdf` | Larger bold | one bullet line per item | yes (clickable depends on your PDF reader) |

## Stretch goals

- Add `--format html` using Python's `markdown` package
- Re-rank sources after search: drop any URL whose domain isn't in the preferred list (hard filter mode, `--strict-sources`)
- Add a `--depth N` flag that controls `tool_call_limit`
- Pipe two agents: a researcher → an editor that proofreads the brief before save

## Common bugs

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: docx` | `pip install python-docx` (note: package name is `python-docx`, import is `docx`) |
| `ModuleNotFoundError: fpdf` | `pip install fpdf2` (import is still `fpdf`) |
| PDF chokes on emoji / curly quotes | fpdf2's default Helvetica is latin-1 only. The starter handles this by stripping non-ASCII; for true Unicode add a TTF font with `pdf.add_font(..., uni=True)` |
| Agent ignores `--sources` | Make sure your instructions string actually interpolates the site list — print it once before passing to the Agent |
| All results from one domain | DuckDuckGo's `site:` operator is OR'd — the model still picks per-query. Add to instructions: *"Spread queries across at least 3 of the preferred domains."* |
