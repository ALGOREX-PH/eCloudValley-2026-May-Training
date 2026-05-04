"""
Lab 1 — Reference solution.

Identical to the starter — Lab 1 is a "type along" lab, no TODOs to fill in.
The point is to verify the environment.
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
