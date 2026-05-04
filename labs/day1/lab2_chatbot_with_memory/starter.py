"""
Lab 2 — Customer Support Chatbot with Persistent Memory (20 min, paired)

Build a CloudKaiju support chatbot that remembers users across process restarts.

Fill in the TODOs. The reference solution is in solutions/day1/lab2_chatbot_with_memory/
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv

load_dotenv()


def build_agent(session_id: str) -> Agent:
    """Build the CloudKaiju support agent.

    TODO 1 — Create a SqliteStorage that writes to agent_storage/chat.db
             with a table named "chat_sessions".
    """
    storage = ...  # TODO 1

    """TODO 2 — Create the Agent with:
                  - model: OpenAIChat(id="gpt-4o-mini")
                  - storage: the storage you created above
                  - session_id: the function arg
                  - add_history_to_messages: True
                  - num_history_runs: 10
                  - instructions: a clear persona for CloudKaiju support
                  - markdown: True
    """
    agent = ...  # TODO 2

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
