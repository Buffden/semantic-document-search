# RAG Document Engine

A progressive RAG system built from first principles -- from raw embeddings and cosine similarity all the way to a full retrieval-augmented generation pipeline with document ingestion, reranking, and cited answers.

Each phase extends the previous one. No framework magic -- just Python, OpenAI, and deliberate tooling choices at each layer.

---

## What It Does (Current State)

<table>
<tr>
<td valign="top" width="55%">

1. **Chunks** text documents into overlapping word windows so meaning is preserved at boundaries
2. **Embeds** each chunk using the OpenAI `text-embedding-3-small` API, producing a 1536-dimensional vector per chunk
3. **Stores** vectors alongside the original text in a local `embeddings.json` file
4. **Searches** by embedding a natural language query using the same model, then ranking all chunks by cosine similarity and returning the top-K matches

</td>
<td valign="top" width="45%">

![Pipeline](./diagrams/pipeline.svg)

</td>
</tr>
</table>

---

## Stack

- Python 3.12
- OpenAI SDK (`text-embedding-3-small`)
- NumPy (cosine similarity)
- Plain JSON (storage -- current phase)
- python-dotenv

---

## Project Structure

```text
rag-document-engine/
├── documents/              # Sample .txt files to embed
│   ├── ancient-rome.txt
│   ├── climate-change.txt
│   ├── music-and-the-brain.txt
│   ├── nutrition-and-health.txt
│   └── space-exploration.txt
├── embed.py                # Load, chunk, embed documents -> embeddings.json
├── search.py               # Embed query + retrieve top-K chunks by cosine similarity
├── utils.py                # chunk_text and cosine_similarity helpers
├── docs/
│   └── implementation-plan.md  # Phase-by-phase build plan
├── pyproject.toml
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

```env
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
```

---

## Usage

```bash
# Step 1 -- Embed all documents (generates embeddings.json)
python3 embed.py

# Step 2 -- Search
python3 search.py
```

The query is set in `search.py` main. Change it to anything you want to search for.

---

## Sample Output

Query: `"what foods are good for the heart"`

```text
Result 1 (score: 0.3571)
Nutrition is the science of how food affects the body. The food we eat provides energy and
the raw materials needed to build and repair tissues... Unsaturated fats found in olive oil,
nuts, avocados, and fatty fish are associated with reduced risk of heart disease...

Result 2 (score: 0.3143)
The Mediterranean diet -- rich in vegetables, fruit, whole grains, fish, and olive oil -- is
consistently associated with lower rates of heart disease, diabetes, and cognitive decline...

Result 3 (score: 0.1786)
Music also affects mood and stress. Slow, quiet music activates the parasympathetic nervous
system, lowering heart rate and cortisol levels...
```

The top two results come from the nutrition document. Result 3 surfaces from the music document because it mentions "heart rate" -- semantic search catches conceptual overlap, not just keyword matches.

---

## Progress

| Phase | Title | Status |
| ----: | ----- | ------ |
| 1 | Semantic Foundation | Complete |
| 2 | Vector Store | In Progress |
| 3 | RAG Pipeline | Planned |
| 4 | Document Ingestion | Planned |
| 5 | Retrieval Quality | Planned |

See [docs/implementation-plan.md](./docs/implementation-plan.md) for full phase details, tasks, and build notes.

---

## Key Concepts

- **Embeddings** -- fixed-length vectors that encode the meaning of text, not just the words
- **Cosine similarity** -- measures the angle between vectors; direction encodes meaning, magnitude does not
- **Chunking** -- splits documents into overlapping windows so meaning is not diluted or cut at boundaries
- **Model consistency** -- the same embedding model must be used for both documents and queries
- **RAG** -- Retrieval-Augmented Generation: retrieve relevant context, then generate a grounded answer

---

## Diagrams

The pipeline diagram is maintained as a PlantUML source file (`pipeline.puml`) and auto-exported to SVG on every push to main using [diagram-sync](https://www.npmjs.com/package/diagram-sync).
