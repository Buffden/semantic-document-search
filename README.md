# Semantic Document Search

A Python implementation of semantic search using OpenAI embeddings.

No vector database. No frameworks. Just embeddings, cosine similarity, and plain Python.

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
- python-dotenv

---

## Project Structure

```
semantic-document-search/
├── documents/              # Sample .txt files to embed
│   ├── ancient-rome.txt
│   ├── climate-change.txt
│   ├── music-and-the-brain.txt
│   ├── nutrition-and-health.txt
│   └── space-exploration.txt
├── embed.py                # Load, chunk, embed documents → embeddings.json
├── search.py               # Embed query + retrieve top-K chunks
├── utils.py                # chunk_text helper
├── pyproject.toml          # Project dependencies
└── .env                    # API keys (not committed)
```

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Create a `.env` file:

```
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
```

---

## Usage

```bash
# Step 1 — Embed all documents (generates embeddings.json)
python3 embed.py

# Step 2 — Search
python3 search.py "your query here"
```

---

## Sample Output

`embeddings.json` is generated locally and not committed. Each entry looks like:

```json
[
  {
    "text": "Climate change refers to long-term shifts in global temperatures and weather patterns...",
    "embedding": [0.0021, -0.0342, 0.0187, "...1536 values total"]
  },
  {
    "text": "The primary cause is the burning of fossil fuels such as coal, oil, and natural gas...",
    "embedding": [0.0019, -0.0311, 0.0204, "...1536 values total"]
  }
]
```

Each embedding is a 1536-dimensional vector produced by `text-embedding-3-small`. Chunks from the same document on the same topic will have vectors that point in similar directions — chunks from different topics will not.

---

## Key Concepts

- **Embeddings** — fixed-length vectors that encode the meaning of text, not just the words
- **Cosine similarity** — measures the angle between vectors; direction encodes meaning, magnitude does not
- **Chunking** — splits documents into overlapping windows so meaning isn't diluted or cut at boundaries
- **Model consistency** — the same embedding model must be used for both documents and queries
