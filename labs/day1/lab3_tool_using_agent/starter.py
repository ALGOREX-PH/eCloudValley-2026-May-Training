"""
Lab 3 — Personal Research Assistant (30 min, paired)

A tool-using agent that researches a topic and saves a markdown brief.

Run:
    python labs/day1/lab3_tool_using_agent/starter.py "latest agentic AI papers"
"""

import sys
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------------------------------------------
# TODO 1 — Implement the save_note tool.
#   - Decorate with @tool
#   - Accept (filename: str, content: str) -> str
#   - Write a STRONG docstring: when to use, arg formats, return value
#   - Save to a notes/ folder at the repo root, creating it if needed
#   - Slug-safe filenames: lowercase, hyphens, no extension required
#   - Return the absolute path of the saved file
# ----------------------------------------------------------------------

# @tool
# def save_note(...) -> str:
#     """..."""
#     ...


# ----------------------------------------------------------------------
# TODO 2 — Build the agent.
#   - model: OpenAIChat(id="gpt-4o-mini")
#   - tools: [DuckDuckGoTools(), save_note]
#   - markdown: True
#   - instructions should:
#       (a) define the agent's role (research assistant)
#       (b) describe the brief structure: # Title, ## Summary, ## Key Findings, ## Sources
#       (c) require URL citations for every fact
#       (d) tell it to STOP after at most 3 searches, then save and finish
# ----------------------------------------------------------------------

def build_agent() -> Agent:
    raise NotImplementedError("Build me!")


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python starter.py "your research topic"')
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    agent = build_agent()
    agent.print_response(
        f"Research the topic: '{topic}'. Synthesize a brief and save it.",
        stream=True,
    )


if __name__ == "__main__":
    main()
