"""
Lab 6 — Reference solution.

Personal Finance Team — FinEd Coach (RAG over the Financial Wellness Journal)
+ Web Researcher (DuckDuckGo for current rates / news), with a coordinator.

This solution adds a custom collaboration visualizer (Rich-based, same console
library Agno uses internally) so attendees can SEE the multi-agent interaction:

  • A team-topology tree printed once at startup.
  • A per-query call trace after every run: routing decision, each member's
    panel (with tool count, tokens, duration), and the coordinator's final
    merged answer.
"""

import sys
from pathlib import Path

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.tree import Tree

load_dotenv()

# Windows PowerShell legacy console can't encode emojis through Rich's legacy
# renderer — force UTF-8 stdout so the panels render cleanly.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LAB_DIR = Path(__file__).parent
DOCS_DIR = LAB_DIR.parent.parent.parent / "labs" / "day2" / "lab4_basic_rag" / "docs"
DB_PATH = LAB_DIR / "chroma_db"

console = Console()

# Per-member styling — used by both the topology tree and the per-run panels.
MEMBER_STYLES = {
    "FinEd Coach": {"emoji": "💸", "color": "magenta"},
    "Web Researcher": {"emoji": "🌐", "color": "blue"},
}
DEFAULT_STYLE = {"emoji": "🤖", "color": "white"}


def _style_for(name: str) -> dict:
    return MEMBER_STYLES.get(name, DEFAULT_STYLE)


def build_knowledge() -> Knowledge:
    knowledge = Knowledge(
        vector_db=ChromaDb(collection="fined_journal", path=str(DB_PATH)),
    )
    knowledge.add_content(path=DOCS_DIR)
    return knowledge


def build_fined_coach(knowledge: Knowledge) -> Agent:
    return Agent(
        name="FinEd Coach",
        role="Answer personal-finance questions from the Financial Wellness Journal with citations.",
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "Always search the knowledge base before answering.",
            "Cite every factual claim with [source: financial-wellness-journal-english.pdf, p. <page>] "
            "using the page number from the search result's meta_data.page.",
            "If the journal doesn't cover it, say exactly: \"I don't see that in the journal.\"",
            "Stay focused on personal finance from the journal — defer current rates, "
            "news, and BSP announcements to the Web Researcher.",
        ],
        markdown=True,
    )


def build_web_researcher() -> Agent:
    return Agent(
        name="Web Researcher",
        role="Search the public web for current rates, news, BSP announcements, and market data.",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGoTools()],
        tool_call_limit=4,
        instructions=[
            "Search the web 1–3 times with focused queries, then stop.",
            "Keep replies under 6 sentences.",
            "Always include the URL for every claim you make.",
            "If asked about general personal-finance concepts, reply: "
            "\"Defer to FinEd Coach for grounded personal-finance guidance.\"",
        ],
        markdown=True,
    )


def build_team(fined: Agent, web: Agent) -> Team:
    return Team(
        name="Personal Finance Team",
        mode="coordinate",
        model=OpenAIChat(id="gpt-4o-mini"),
        members=[fined, web],
        show_members_responses=True,
        markdown=True,
        instructions=[
            "Read the question and decide which member(s) should answer.",
            "Personal-finance concepts / case studies / journal content → FinEd Coach.",
            "Current rates, BSP announcements, market data, news → Web Researcher.",
            "If the question needs both (e.g., 'what does the journal say about insurance "
            "AND what are current rates?'), dispatch both and merge their replies into ONE "
            "coherent answer.",
            "Refuse off-topic questions politely (weather, sports, personal advice "
            "outside finance).",
            "Always preserve the citations and URLs the members produced — "
            "don't drop sources when synthesizing.",
        ],
    )


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def render_topology(team: Team) -> None:
    """Print a Rich Tree showing the team graph (coordinator + members + tools)."""
    model_id = getattr(team.model, "id", "?") if team.model else "?"
    root = Tree(
        Text.assemble(
            ("🤝 ", "bold cyan"),
            (team.name or "Team", "bold cyan"),
            ("  ·  ", "dim"),
            (f"mode={team.mode}", "yellow"),
            ("  ·  ", "dim"),
            (model_id, "green"),
        ),
        guide_style="cyan",
    )
    members = team.members if isinstance(team.members, list) else []
    for m in members:
        style = _style_for(m.name or "")
        node = root.add(
            Text.assemble(
                (f"{style['emoji']} ", style["color"]),
                (m.name or "(unnamed)", f"bold {style['color']}"),
                ("  —  ", "dim"),
                (m.role or "", "italic"),
            )
        )
        has_knowledge = getattr(m, "knowledge", None) is not None
        if has_knowledge:
            vdb = getattr(m.knowledge, "vector_db", None)
            collection = getattr(vdb, "collection_name", None) or getattr(
                vdb, "name", "?"
            )
            vdb_kind = vdb.__class__.__name__ if vdb else "?"
            node.add(Text(f"🧠 knowledge: {collection} ({vdb_kind})", style="magenta"))
            if getattr(m, "search_knowledge", False):
                node.add(Text("🔧 tool: search_knowledge_base", style="yellow"))
        for t in getattr(m, "tools", None) or []:
            node.add(Text(f"🔧 tool: {t.__class__.__name__}", style="yellow"))

    console.print(
        Panel(root, title="Team Topology", border_style="cyan", padding=(1, 2))
    )


def _fmt_metrics(metrics) -> str:
    if metrics is None:
        return ""
    parts = []
    if getattr(metrics, "total_tokens", None):
        parts.append(f"tokens: {metrics.total_tokens}")
    duration = getattr(metrics, "duration", None)
    if duration:
        parts.append(f"duration: {duration:.1f}s")
    return "  ·  ".join(parts)


def _render_member(mr) -> Panel:
    name = getattr(mr, "agent_name", None) or getattr(mr, "team_name", None) or "(member)"
    style = _style_for(name)
    tools = getattr(mr, "tools", None) or []
    tool_names = [t.tool_name for t in tools if getattr(t, "tool_name", None)]

    header_parts = [
        (f"{style['emoji']} ", style["color"]),
        (name, f"bold {style['color']}"),
    ]
    if tool_names:
        header_parts += [
            ("  ·  ", "dim"),
            (f"tools fired: {len(tool_names)} ({', '.join(tool_names)})", "yellow"),
        ]
    metrics_str = _fmt_metrics(getattr(mr, "metrics", None))
    if metrics_str:
        header_parts += [("  ·  ", "dim"), (metrics_str, "dim")]

    body = Text(getattr(mr, "content", "") or "(empty response)")
    citations = getattr(mr, "citations", None)
    if citations:
        urls = getattr(citations, "urls", None) or []
        if urls:
            body.append("\n\nCitations:\n", style="bold")
            for u in urls:
                url = getattr(u, "url", None) or str(u)
                body.append(f"  • {url}\n", style="cyan")

    return Panel(
        Group(Text.assemble(*header_parts), Text(""), body),
        border_style=style["color"],
        padding=(0, 1),
    )


def render_run(question: str, result) -> None:
    """Render the full collaboration trace for one team run."""
    console.print(Rule(Text(f"❓ {question}", style="bold cyan"), style="cyan"))

    members = list(getattr(result, "member_responses", None) or [])

    # Routing decision
    if members:
        names = [
            getattr(m, "agent_name", None) or getattr(m, "team_name", None) or "?"
            for m in members
        ]
        joined = "  +  ".join(
            f"{_style_for(n)['emoji']} {n}" for n in names
        )
        routing_text = Text.assemble(
            ("Coordinator dispatched → ", "bold"),
            (joined, "bold cyan"),
        )
    else:
        routing_text = Text(
            "Coordinator answered directly (no member dispatched)", style="bold yellow"
        )
    console.print(Panel(routing_text, border_style="yellow", padding=(0, 1)))

    # Per-member panels
    for mr in members:
        console.print(_render_member(mr))

    # Final synthesized answer
    final_body = Text(getattr(result, "content", "") or "(no content)")
    metrics_str = _fmt_metrics(getattr(result, "metrics", None))
    footer_parts = [(f"members called: {len(members)}", "dim")]
    if metrics_str:
        footer_parts += [("  ·  ", "dim"), (metrics_str, "dim")]
    final_body.append("\n\n")
    final_body.append(Text.assemble(*footer_parts))
    console.print(
        Panel(
            final_body,
            title=Text("🤝 Coordinator (final)", style="bold green"),
            border_style="green",
            padding=(1, 1),
        )
    )
    console.print()


# ---------------------------------------------------------------------------
# REPL
# ---------------------------------------------------------------------------

def repl(team: Team) -> None:
    render_topology(team)
    console.print()
    console.print("[bold]Personal Finance Team[/] 💸🤝🌐  (Ctrl+C to exit)\n")
    try:
        while True:
            q = input("you ▸ ").strip()
            if not q:
                continue
            console.print()
            result = team.run(q)
            render_run(q, result)
    except (KeyboardInterrupt, EOFError):
        console.print("\nBye!")


if __name__ == "__main__":
    console.print("📚 Loading knowledge base...")
    knowledge = build_knowledge()

    console.print("🤖 Wiring up specialists...")
    fined = build_fined_coach(knowledge)
    web = build_web_researcher()

    console.print("🤝 Composing the team...\n")
    team = build_team(fined, web)

    repl(team)
