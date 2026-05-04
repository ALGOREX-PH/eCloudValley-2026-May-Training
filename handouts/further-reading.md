# Further Reading & Where to Go Next

You just spent 6 hours building agentic systems. Here's where to keep learning.

---

## Foundational papers

These are the papers behind everything we built today. Read them in order; each is short.

1. **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al., 2022)
   <https://arxiv.org/abs/2210.03629>
   *The think-act-observe loop your agent uses every time it picks a tool.*

2. **Toolformer: Language Models Can Teach Themselves to Use Tools** (Schick et al., 2023)
   <https://arxiv.org/abs/2302.04761>
   *Why function calling works at all.*

3. **Reflexion: Language Agents with Verbal Reinforcement Learning** (Shinn et al., 2023)
   <https://arxiv.org/abs/2303.11366>
   *How agents can learn from their own mistakes within a single session.*

4. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (Lewis et al., 2020)
   <https://arxiv.org/abs/2005.11401>
   *The original RAG paper. Five years old, still the foundation.*

5. **Lost in the Middle: How Language Models Use Long Contexts** (Liu et al., 2023)
   <https://arxiv.org/abs/2307.03172>
   *Why retrieval quality matters more than context window size.*

6. **The Rise and Potential of Large Language Model Based Agents: A Survey** (Xi et al., 2023)
   <https://arxiv.org/abs/2309.07864>
   *A 100-page map of the field. Skim the table of contents and dive where curious.*

---

## Production & engineering resources

- **Anthropic — Building Effective Agents** — <https://www.anthropic.com/research/building-effective-agents>
  *The single best practitioner guide. Bookmark it.*
- **OpenAI — A Practical Guide to Building Agents** (PDF whitepaper)
  *Search for "OpenAI practical guide to building agents".*
- **Agno docs** — <https://docs.agno.com>
- **LangChain docs** — <https://python.langchain.com>
  *The other major framework. Worth knowing even if you stick with Agno.*
- **LlamaIndex docs** — <https://docs.llamaindex.ai>
  *Best resource on the RAG side specifically.*

---

## Evaluation & observability

- **Phoenix (Arize)** — <https://docs.arize.com/phoenix>
  *Open-source LLM tracing. Drop-in for any agent.*
- **Langfuse** — <https://langfuse.com>
  *Open-source observability + evals. Self-hostable.*
- **Ragas** — <https://docs.ragas.io>
  *Specialized eval harness for RAG pipelines.*
- **OpenAI Evals** — <https://github.com/openai/evals>

---

## Vector DBs worth knowing

| Tool | Best for |
|---|---|
| **Chroma** (we used today) | Local development, single-machine apps |
| **LanceDB** | Embedded production, fast columnar queries |
| **pgvector** | You already run Postgres |
| **OpenSearch / Elasticsearch** | Hybrid search at scale, AWS-native |
| **Pinecone / Weaviate / Qdrant** | Managed vector DB SaaS |

---

## Cloud deployment paths

You finished Lab 6 with a Dockerized FastAPI agent. Here's where to deploy it:

- **AWS:** ECS Fargate (containers), Lambda (with Mangum for FastAPI), Bedrock Agents (managed runtime)
- **GCP:** Cloud Run (containers), Vertex AI Agent Builder
- **Azure:** Container Apps, Azure AI Foundry
- **Vercel / Railway / Fly.io:** Fastest path to a public URL for prototypes

For any of these: check the response time of your first prod request — agents can be slow on cold start. Add a warmup endpoint or use provisioned concurrency.

---

## Stay in touch

- Speaker LinkedIn: search **Danielle Bagaforo Meer**
- Course feedback / questions: reply to the email thread that brought you here
- Want a follow-up workshop on a specific topic? Let eCloudValley know.

Build something this week. Even something small. The fastest path to fluency is shipping a real agent that solves a real problem.

— Danielle
