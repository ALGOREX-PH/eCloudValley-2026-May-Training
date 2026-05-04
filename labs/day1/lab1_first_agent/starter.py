"""
Lab 1 — Your First Agno Agent (10 min, instructor-led)

Run this from the repo root:
    python labs/day1/lab1_first_agent/starter.py

If you see streaming text from the agent, your environment is ready.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        instructions=[
            "You are a friendly Filipino tech mentor.",
            "Be concise. Use code examples when helpful.",
            "Use a warm, encouraging tone.",
        ],
        markdown=True,
    )

    agent.print_response(
        "Explain agentic AI to a junior engineer in 3 sentences.",
        stream=True,
    )


if __name__ == "__main__":
    main()
