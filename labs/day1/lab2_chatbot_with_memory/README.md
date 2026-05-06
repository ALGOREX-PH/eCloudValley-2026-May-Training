# Lab 2 — Customer Support Chatbot with Persistent Memory

> **Time:** 20 minutes (paired)
> **Format:** Work with a partner, fill in the TODOs

## Goal

Build a chatbot for a fictional SaaS called **CloudKaiju** that:

1. Has a defined persona (helpful, slightly cheeky, escalates politely)
2. Remembers the user's name and last issue across turns
3. **Persists** to SQLite so a process restart doesn't lose context

## What you'll learn

- `add_history_to_context` — in-session memory
- `SqliteDb` — durable memory across processes
- `session_id` — how to resume the same conversation
- Writing personality into `instructions`

## Run

```bash
python labs/day1/lab2_chatbot_with_memory/starter.py
```

Type messages. After a couple of turns, **press `Ctrl+C`**, then run the script again. The bot should remember your name.

## Stretch goals

If you finish early:

- Add a `/reset` command that starts a fresh session
- Add a 2nd persona (`--persona terse`) and switch via CLI flag
- Inspect `agent_storage/chat.db` with [DB Browser for SQLite](https://sqlitebrowser.org) — see what's stored

## Tips

- The first few interactions teach the agent context — try saying your name and what you need help with.
- If memory feels broken, check that you're passing the **same `session_id`** every run.
- `num_history_runs=10` keeps the last 10 turns in context. Increase if memory feels too short.

## Common bugs

| Symptom | Cause | Fix |
|---|---|---|
| Bot doesn't remember after restart | New `session_id` each run | Hardcode or read from CLI |
| Bot remembers TOO much (off-topic) | `num_history_runs` too high | Lower it |
| `sqlite3.OperationalError: database is locked` | Two processes hitting same db | Stop the other one |
