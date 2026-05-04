# Agno Cheat Sheet

Quick reference for the Agno API patterns we use across the 6 labs. Keep this open in a tab during class.

> Full docs: <https://docs.agno.com>

---

## 1. The simplest possible agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="You are a helpful assistant.",
    markdown=True,
)

agent.print_response("Hello, world!", stream=True)
```

---

## 2. Common Agent parameters

| Parameter | What it does |
|---|---|
| `model=` | The LLM. `OpenAIChat`, `Claude`, `Gemini`, etc. |
| `instructions=` | System prompt. String or list of strings. |
| `tools=[...]` | List of tool functions or built-in toolkits. |
| `add_history_to_messages=True` | Include previous turns of the conversation. |
| `num_history_runs=5` | How many previous turns to include. |
| `storage=...` | Persistent storage for memory across processes. |
| `markdown=True` | Render output as Markdown. |
| `show_tool_calls=True` | Print each tool call & result (great for debugging). |
| `debug_mode=True` | Verbose internal logging. |

---

## 3. Calling the agent

```python
# Synchronous, prints to stdout (great for demos)
agent.print_response("What's 2+2?", stream=True)

# Get the result back as an object
result = agent.run("What's 2+2?")
print(result.content)

# Continue a conversation
result = agent.run("What's 2+2?")
result = agent.run("Multiply that by 10")  # Agent remembers if memory is on
```

---

## 4. Persistent memory

```python
from agno.storage.sqlite import SqliteStorage

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=SqliteStorage(table_name="sessions", db_file="agent.db"),
    add_history_to_messages=True,
    num_history_runs=10,
    session_id="user-42",  # The same session_id resumes the same chat
)
```

---

## 5. Built-in tools

```python
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools(), CalculatorTools(), YFinanceTools(stock_price=True)],
    show_tool_calls=True,
)
```

---

## 6. Custom tools

```python
from agno.tools import tool

@tool
def save_note(filename: str, content: str) -> str:
    """Save a markdown note to disk.

    Args:
        filename: Name of the file (without extension).
        content: The markdown content to write.

    Returns:
        The full path to the saved file.
    """
    path = f"notes/{filename}.md"
    with open(path, "w") as f:
        f.write(content)
    return path

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[save_note],
    show_tool_calls=True,
)
```

> The docstring is what the LLM reads to decide whether/how to call the tool. Make it good.

---

## 7. Knowledge / RAG (Day 2)

```python
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

knowledge = Knowledge(
    vector_db=ChromaDb(collection="docs", path="chroma_db"),
)

# One-time: ingest documents
knowledge.add_content(path="labs/day2/lab4_basic_rag/docs/")

# Use as an agent tool
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge,
    search_knowledge=True,  # The agent decides when to search
    instructions=[
        "Always cite the source document and page when answering.",
        "If the answer isn't in the knowledge base, say so.",
    ],
)
```

---

## 8. Streaming

```python
# Print streaming output
agent.print_response("Explain RAG", stream=True)

# Iterate over chunks yourself
for chunk in agent.run("Explain RAG", stream=True):
    print(chunk.content, end="", flush=True)
```

---

## 9. Models we use

| ID | When to use |
|---|---|
| `gpt-4o-mini` | Default for labs — cheap & fast |
| `gpt-4o` | When you need stronger reasoning |
| `text-embedding-3-small` | Default embeddings for RAG |

---

## 10. Common errors & fixes

| Error | Likely cause | Fix |
|---|---|---|
| `AuthenticationError` | Bad `OPENAI_API_KEY` | Re-paste from the speaker's email |
| `RateLimitError` | Workshop key throttling | Wait 30s, retry |
| Tool not called | Docstring too vague | Rewrite the tool's docstring with explicit "use this when..." |
| Hallucinated tool args | Schema unclear | Add type hints; describe each arg in the docstring |
| Vector DB returns nothing | Forgot to ingest | Run `knowledge.add_content(...)` once |
| Memory doesn't persist | Same `session_id` not reused | Pass the same `session_id=` to every run |
