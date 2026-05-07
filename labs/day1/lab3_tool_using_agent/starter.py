"""
Lab 3 — Personal Research Assistant (30 min, paired)

A tool-using agent that researches a topic and saves a markdown brief.

Run:
    python labs/day1/lab3_tool_using_agent/starter.py "latest agentic AI papers"
"""
import re
import sys
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()

NOTES_DIR = Path("notes")

def _slugify(value: str) -> str:
    """Lowercase, hyphenate, strip non-safe characters."""
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    return value[:60] or "untitled"


@tool
def save_note(filename: str, content : str) -> str :
    """
    Save a markdown note to disk in the local `notes/` folder.

    Use this tool ONCE at the end of your research, after you have synthesized
    findings into a final markdown brief. Do not call it with empty content.

    Args:
        filename: A short, descriptive slug. Lowercase, hyphenated, no
            extension. Example: "agentic-ai-papers-may-2026".
            If you pass a phrase or filename with spaces or extension,
            it will be normalized.
        content: The full markdown content of the brief. Must include:
            - A `# Title` heading
            - A `## Summary` (2–3 sentences)
            - A `## Key Findings` bullet list
            - A `## Sources` list with URLs

    Returns:
        The absolute path of the file that was written.
    """
    NOTES_DIR.mkdir(exist_ok=True)
    safe_name = _slugify(filename)
    path = NOTES_DIR / f"{safe_name}.md"
    path.write_text(content, encoding = "utf-8")
    return str(path.resolve())
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

def build_agent() -> Agent :
    return Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools(), save_note],
        markdown = True,
        tool_call_limit = 8,
        instructions=[
            "You are a thorough research assistant.",
            "When given a topic, search the web 2–3 times with focused queries.",
            "After at most 3 searches, STOP searching and write the brief.",
            # — Anti-hallucination guardrails (critical) —
            "CRITICAL: every URL in the brief MUST come from a successful web_search result. "
            "Do NOT invent URLs from memory, do NOT reconstruct URLs from training data, do NOT guess.",
            "If ALL of your searches return errors or empty results, write a brief whose Summary "
            "states honestly: 'Web search returned no results for this topic.' Leave Key Findings "
            "and Sources empty. Then save and stop.",
            "Only cite a URL if it appeared verbatim in a tool result you received this run.",
            # — Output structure —
            "The brief must follow this exact structure:",
            "  # <Title>",
            "  ## Summary  (2–3 sentences)",
            "  ## Key Findings  (bullet list, each with a URL)",
            "  ## Sources  (numbered list of URLs)",
            "Save the brief by calling save_note exactly once at the end.",
            "Then reply with a one-line confirmation including the file path.",
        ],
    )
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
