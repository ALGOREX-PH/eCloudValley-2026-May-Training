# Lab 4 — Build a Vector DB from Documents

> **Time:** 20 minutes (instructor-led)
> **Format:** Type along

## Goal

Ingest a real-world PDF into a Chroma vector DB, then run similarity queries against it. Inspect what comes back and tune the retrieval.

## What you'll learn

- Agno's `Knowledge` abstraction
- `ChromaDb` as a vector store
- Document loading & chunking (Agno does this for you, but tunable)
- Similarity search with `max_results`
- The effect of chunk size on retrieval quality

## The data

A 55-page **Financial Wellness Journal** from BPI Foundation's FinEd program — covers saving, insurance, credit, and investing with case studies (Mang Rafael, Aling Yolanda, Teacher Mary, Corporal Star). You'll re-use this dataset in Lab 5 and Lab 6.

```
labs/day2/lab4_basic_rag/docs/
└── financial-wellness-journal-english.pdf
```

> Drop your own PDFs / Markdown into `docs/` if you want — the lab works with anything Agno can read.

## Run

```bash
python labs/day2/lab4_basic_rag/starter.py
```

The script will:

1. Create a `chroma_db/` folder for the vector store
2. Ingest the docs (only the first run — subsequent runs reuse the index)
3. Run a few sample queries and print the top results with similarity scores

## Things to try

After it works, change one knob at a time:

1. **Query different things.** Edit `QUERIES` in the script and re-run.
2. **Bigger / smaller chunks.** Pass `chunk_size=1500` (or `200`) to the chunking strategy. Re-index. Compare.
3. **Bigger `max_results`.** Ask for top 10 instead of top 3 — see how relevance falls off.
4. **Delete `chroma_db/`** to force re-indexing from scratch.

## Common bugs

| Symptom | Cause | Fix |
|---|---|---|
| Empty results | Forgot to ingest | Delete `chroma_db/` and re-run |
| Same results for every query | Embeddings broken | Check `OPENAI_API_KEY` works |
| Slow first run | Embedding API calls | Normal — ~5s for these 3 docs |
| `chroma_db is locked` | Another process running | Kill it |
