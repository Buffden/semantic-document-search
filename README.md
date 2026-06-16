# Semantic Document Search

A Python implementation of semantic search using OpenAI embeddings — built as part of Week 6 of the AI Application Engineering roadmap (Phase 2: RAG and Document Intelligence).

No vector database. No frameworks. Just embeddings, cosine similarity, and plain Python — so the mechanics are clear before adding infrastructure.

---

## What It Does

1. **Chunks** text documents into overlapping windows
2. **Embeds** each chunk using OpenAI `text-embedding-3-small`
3. **Stores** the vectors locally as JSON
4. **Searches** by embedding a natural language query and returning the most semantically similar chunks

---

## Stack

- Python 3.12
- OpenAI SDK (`text-embedding-3-small`)
- NumPy (cosine similarity)
- Plain JSON (storage)

---

## Project Structure

```
semantic-document-search/
├── documents/          # Sample .txt files to embed
├── embeddings.json     # Stored chunk embeddings (generated)
├── embed.py            # Chunk + embed documents
├── search.py           # Embed query + retrieve top-K chunks
└── utils.py            # Chunking and cosine similarity helpers
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install openai numpy python-dotenv
```

Create a `.env` file:

```
OPENAI_API_KEY=sk-...
```

---

## Usage

```bash
# Embed all documents
python embed.py

# Search
python search.py "your query here"
```

---

## Key Concepts

- **Embeddings** — fixed-length vectors that encode the meaning of text, not just the words
- **Cosine similarity** — measures the angle between vectors; direction encodes meaning, magnitude does not
- **Chunking** — splits documents into overlapping windows so meaning isn't diluted or cut at boundaries
- **Model consistency** — the same embedding model must be used for both documents and queries

---

## Part of

[AI Application Engineering Roadmap](https://github.com/Buffden/ai-application-engineering) — Phase 2: RAG and Document Intelligence
