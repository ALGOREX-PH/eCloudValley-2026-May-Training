"""
Lab 2 — Customer Support Chatbot with Persistent Memory (20 min, paired)

Build a CloudKaiju support chatbot that remembers users across process restarts.

Fill in the TODOs. The reference solution is in solutions/day1/lab2_chatbot_with_memory/
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
    """Build the CloudKaiju support agent.

    TODO 1 — Create a SqliteDb that writes to agent_storage/chat.db
             with a session_table named "chat_sessions".
             SqliteDb(db_file="agent_storage/chat.db", session_table="chat_sessions")
    """
    db = SqliteDb(
        db_file=str(STORAGE_DIR/ "chat.db"), 
        session_table="chat_sessions",
        ) # TODO 1

    """TODO 2 — Create the Agent with:
                  - model: OpenAIChat(id="gpt-4o-mini")
                  - db: the SqliteDb you created above
                  - session_id: the function arg
                  - add_history_to_context: True
                  - num_history_runs: 10
                  - instructions: a clear persona for CloudKaiju support
                  - markdown: True
    """
    agent = agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        db = db,
        session_id = session_id,
        add_history_to_context = True,
        num_history_runs= 10,
        instructions=[
            "You are CloudKaiju Support 🦖 — a helpful, slightly cheeky support agent.",
            "Always greet the user by name once you know it.",
            "Keep replies under 4 sentences unless walking through steps.",
        ],
        markdown=True,
        )  # TODO 2

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
    # Reuse the same session_id every run so memory persists.
    SESSION_ID = "workshop-attendee"

    agent = build_agent(session_id=SESSION_ID)
    chat_loop(agent)
