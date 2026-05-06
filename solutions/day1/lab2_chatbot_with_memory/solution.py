"""
Lab 2 — Reference solution.

Customer-support chatbot with persistent SQLite memory.
"""

from pathlib import Path

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

STORAGE_DIR = Path("agent_storage")
STORAGE_DIR.mkdir(exist_ok=True)


def build_agent(session_id: str) -> Agent:
    db = SqliteDb(
        db_file=str(STORAGE_DIR / "chat.db"),
        session_table="chat_sessions",
    )

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        db=db,
        session_id=session_id,
        add_history_to_context=True,
        num_history_runs=10,
        instructions=[
            "You are CloudKaiju Support 🦖 — a helpful, slightly cheeky support agent.",
            "Always greet the user by name once you know it.",
            "Ask one clarifying question if the user's issue is vague.",
            "If the user is frustrated, drop the cheek and be straightforward.",
            "If you can't help, escalate politely: 'Let me hand you to a human teammate.'",
            "Keep replies under 4 sentences unless walking through steps.",
        ],
        markdown=True,
    )

    return agent


def chat_loop(agent: Agent) -> None:
    print("CloudKaiju Support 🦖  (Ctrl+C to exit)\n")
    try:
        while True:
            user_input = input("you ▸ ").strip()
            if not user_input:
                continue
            print("kaiju ▸ ", end="", flush=True)
            agent.print_response(user_input, stream=True)
            print()
    except KeyboardInterrupt:
        print("\n\nSee you next time! Your session was saved.")


if __name__ == "__main__":
    SESSION_ID = "workshop-attendee"

    agent = build_agent(session_id=SESSION_ID)
    chat_loop(agent)
