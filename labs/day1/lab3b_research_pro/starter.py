"""
Lab 3B — Research Assistant Pro (OPTIONAL — bonus after Lab 3)

Same agent shape as Lab 3, with two new knobs:
  --format md|docx|pdf       choose the output format
  --sources <domain>...      preferred source domains (DuckDuckGo `site:` operator)

Run:
    pip install python-docx fpdf2
    python labs/day1/lab3b_research_pro/starter.py "agentic AI patterns 2026" --format pdf
"""

import argparse
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

DEFAULT_PREFERRED_SOURCES = [
    "arxiv.org",
    "anthropic.com",
    "openai.com",
    "docs.agno.com",
    "research.google",
    "deepmind.google",
    "huggingface.co",
]


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    return value[:60] or "untitled"


def _to_latin1(text: str) -> str:
    """fpdf2's default Helvetica is latin-1; strip what it can't render."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


# ---------------------------------------------------------------------------
# TODO 1 — Implement multi-format save
# ---------------------------------------------------------------------------
# This is a single tool that branches on `format`. The agent calls it once at the end.
# Behaviors:
#   - "md":    write `content` straight to disk as UTF-8
#   - "docx":  use python-docx; map "# X" → Heading 1, "## X" → Heading 2,
#              lines starting with "- " → bullet, blank lines → spacer, else paragraph
#   - "pdf":   use fpdf2 (FPDF); map "# X" → bold 16pt, "## X" → bold 13pt,
#              other lines → 11pt body via multi_cell. Pass text through _to_latin1().
#
# Always call NOTES_DIR.mkdir(exist_ok=True) first. Always slugify the filename.
# Return the absolute path of the saved file.
@tool
def save_note(filename: str, content: str, format: str = "md") -> str:
    """Save a research brief to disk in the chosen format.

    Use this tool ONCE at the end of your research, after you have synthesized
    findings into a final markdown brief.

    Args:
        filename: A short, descriptive slug. Lowercase, hyphenated, no
            extension. Example: "agentic-ai-papers-may-2026".
        content: The full markdown content of the brief. Must include
            `# Title`, `## Summary`, `## Key Findings`, `## Sources`.
        format: One of "md", "docx", "pdf". Default "md".

    Returns:
        The absolute path of the file that was written.
    """
    ...   # TODO 1


# ---------------------------------------------------------------------------
# TODO 2 — Build the agent with preferred-source steering
# ---------------------------------------------------------------------------
# Take the list of preferred_sites and stitch them into a `site:` clause that
# the agent should APPEND to each search query. Example clause:
#     "site:arxiv.org OR site:anthropic.com OR site:openai.com"
#
# Then pass that clause into the agent's instructions so the model knows to
# include it in its queries. Also tell the model in instructions which `format`
# to call save_note with at the end.
def build_agent(format: str, preferred_sites: list[str]) -> Agent:
    sites_clause = " OR ".join(f"site:{d}" for d in preferred_sites)

    return Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools(), save_note],
        markdown=True,
        tool_call_limit=8,
        instructions=[
            "You are a thorough research assistant.",
            "When given a topic, search the web 2–3 times with focused queries.",
            # TODO 2 — uncomment and adapt:
            # f"Append this site filter to EACH search query so results come from preferred domains:",
            # f"  ({sites_clause})",
            # "Spread your queries across at least 3 of those domains when possible.",
            "After at most 3 searches, STOP searching and write the brief.",
            "The brief must follow this exact structure:",
            "  # <Title>",
            "  ## Summary  (2–3 sentences)",
            "  ## Key Findings  (bullet list, each with a URL)",
            "  ## Sources  (numbered list of URLs)",
            "Every factual claim must include a URL.",
            f"At the end, call save_note exactly once with format={format!r}.",
            "Then reply with a one-line confirmation including the file path.",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Research assistant with preferred sources + multi-format output",
    )
    parser.add_argument("topic", nargs="+", help="Research topic")
    parser.add_argument(
        "--format",
        choices=["md", "docx", "pdf"],
        default="md",
        help="Output format (default: md)",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        default=DEFAULT_PREFERRED_SOURCES,
        help="Preferred source domains (default: arxiv, anthropic, openai, ...)",
    )
    args = parser.parse_args()

    topic = " ".join(args.topic)
    print(f"📚 Researching: {topic}")
    print(f"📄 Format:      {args.format}")
    print(f"🌐 Preferring:  {', '.join(args.sources)}\n")

    agent = build_agent(args.format, args.sources)
    agent.print_response(
        f"Research the topic: '{topic}'. Synthesize a brief and save it.",
        stream=True,
    )


if __name__ == "__main__":
    main()
