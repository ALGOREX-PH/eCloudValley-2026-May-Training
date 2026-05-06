# Agentic AI Systems — eCloudValley Training

<p align="center">
  <img src="public/byc-logo.avif" alt="eCloudValley" height="60">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="public/algorex-logo-black.png" alt="Algorex Technologies" height="60">
</p>

A 6-hour hands-on training on building production-grade agentic AI systems with Python.

> **Speaker:** Danielle Bagaforo Meer
> **Client:** eCloudValley Philippines
> **Venue:** AWS Office, Arthaland Century Pacific Tower, BGC, Taguig
> **Format:** 2 evening sessions × 3 hours (5:00 PM – 8:00 PM)

---

## What you'll build

By the end of Day 2 you will have built — from scratch, on your own laptop — a stateful AI agent that:

- Holds a conversation with persistent memory
- Calls external tools (web search, custom functions)
- Retrieves answers from your own documents (RAG)
- Cites its sources and refuses out-of-scope questions
- Works as part of a multi-agent team that routes questions between specialists

All code is in **Python**, all agents use the **[Agno](https://docs.agno.com)** framework, and all model calls go through your **OpenAI** API key.

---

## Agenda

### Day 1 — Foundations + Chatbots

| Time        | Module                                                       |
| ----------- | ------------------------------------------------------------ |
| 5:00 – 5:15 | Welcome & setup verification                                 |
| 5:15 – 5:50 | Module 1 — Fundamentals of Agentic AI                        |
| 5:50 – 6:00 | Break                                                        |
| 6:00 – 6:45 | Module 2 — Building AI-Powered Chatbots *(Lab 1, Lab 2)*     |
| 6:45 – 6:55 | Break                                                        |
| 6:55 – 7:50 | Module 3 — Tools & Reasoning *(Lab 3)*                       |
| 7:50 – 8:00 | Wrap-up                                                      |

### Day 2 — RAG + Cloud Integration

| Time        | Module                                                          |
| ----------- | --------------------------------------------------------------- |
| 5:00 – 5:10 | Welcome back                                                    |
| 5:10 – 5:55 | Module 4 — RAG Fundamentals *(Lab 4)*                           |
| 5:55 – 6:05 | Break                                                           |
| 6:05 – 6:55 | Module 5 — Agentic RAG *(Lab 5)*                                |
| 6:55 – 7:05 | Break                                                           |
| 7:05 – 7:45 | Module 6 — Cloud & Data Platform Integration *(Lab 6)*          |
| 7:45 – 8:00 | Capstone demos & close                                          |

---

## Prerequisites

- A laptop (Windows / macOS / Linux)
- Python **3.11 or newer** (`python --version`)
- Git
- A code editor (VS Code recommended)
- Docker Desktop *(only required for Lab 6)*
- The OpenAI API key sent to you by the speaker before Day 1

Full step-by-step setup is in **[handouts/setup-guide.md](handouts/setup-guide.md)**.

---

## Repository layout

```
.
├── slides/        # Reveal.js decks (open day1.html / day2.html in a browser)
├── labs/          # Hands-on starter code (you will fill these in)
│   ├── day1/
│   └── day2/
├── solutions/     # Reference solutions (don't peek until you've tried!)
├── handouts/      # Setup guide, cheat sheet, further reading
└── public/        # Brand assets used by the slides
```

---

## Quick start

```bash
git clone <repo-url> eCloudValley-Training-May-2026
cd eCloudValley-Training-May-2026

python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Open .env and paste in the OPENAI_API_KEY shared with you

python labs/day1/lab1_first_agent/starter.py
```

If you see streaming text from the agent, you're ready. See you in class.

---

## During the workshop

- **Slides:** open `slides/day1.html` in Chrome. Press `S` for speaker view, `?` for keyboard help, `ESC` for slide overview.
- **Labs:** every lab has a `README.md` with goals, concepts, and step-by-step tasks. Work through `labs/dayN/labX/starter.py`.
- **Stuck?** Reference solutions live in `solutions/dayN/labX/solution.py`. Try yours first.
- **Cheat sheet:** `handouts/cheat-sheet.md` for the Agno API at a glance.

---

## License

Training materials © 2026 Algorex Technologies. Course materials may be used by attendees for personal learning. Redistribution without permission is not permitted.
