# Lab 1 — Your First Agno Agent

> **Time:** 10 minutes (instructor-led)
> **Format:** Type along with the speaker

## Goal

Run a streaming Agno agent on your laptop. Prove your environment works end-to-end.

## What you'll learn

- Creating an `Agent` with `OpenAIChat`
- Setting `instructions` (system prompt)
- The difference between `print_response()` and `run()`
- Streaming output with `stream=True`

## Prerequisites

- Completed [setup-guide.md](../../../handouts/setup-guide.md)
- `OPENAI_API_KEY` set in your `.env`
- Activated venv with `pip install -r requirements.txt`

## Run

```bash
python labs/day1/lab1_first_agent/starter.py
```

You should see streaming text appear character-by-character. If you do, your environment is ready for the rest of Day 1. 🎉

## Try this

Once it works, change one line at a time and re-run:

1. Swap the model: `id="gpt-4o-mini"` → `id="gpt-4o"`. Notice quality difference.
2. Remove `stream=True`. Notice how it now waits then dumps.
3. Change the instructions to "Reply only in haiku." See what happens.
4. Change the prompt entirely.

## Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: agno` | Activate your venv (`.venv\Scripts\activate`), then `pip install -r requirements.txt` |
| `AuthenticationError` | Bad `OPENAI_API_KEY` in `.env`. Re-paste it. |
| Nothing happens | Check you ran from the repo root, not from inside the lab folder. |
