# RDE-2 | Phase 2: Vector Store

**Status:** Done
**Type:** Enhancement
**Priority:** High
**Depends on:** RDE-1

---

## Goal

Replace the flat JSON file and brute-force cosine loop with a real vector database. The chunking and embedding logic from Phase 1 carries over unchanged. The only thing being swapped is the storage and retrieval layer.

---

## What Changes from Phase 1

| Phase 1 | Phase 2 Replacement |
| ------- | ------------------- |
| `embeddings.json` | Chroma persistent collection |
| `json.dump` / `json.load` | `collection.add()` / `collection.query()` |
| Brute-force cosine loop in `search.py` | Chroma's built-in similarity search |
| No metadata | `source` filename + `chunk_index` stored as metadata |

---

## Tasks

- [x] Create `ingest.py` -- replaces `embed.py`: chunks documents, generates embeddings, stores in Chroma with `source` and `chunk_index` metadata
- [x] Rewrite `search.py` -- query Chroma instead of scanning the JSON file
- [x] Keep `utils.py` from Phase 1 unchanged

---

## Acceptance Criteria

- Running `python ingest.py` loads all `.txt` files, chunks them, embeds them, and stores results in a persistent Chroma collection under `chroma_db/`
- Running `python search.py "<query>"` returns the top-K most relevant chunks from Chroma with their source filename and chunk index
- Re-running `ingest.py` on the same files does not create duplicate entries
- `chroma_db/` persists between runs -- data survives process restarts

---

## Stack

- `chromadb` -- local persistent vector database

---

## Vector DB Tradeoff Reference

| | Chroma | pgvector | Pinecone | Weaviate |
| --- | --- | --- | --- | --- |
| Setup | Local, zero config | Requires PostgreSQL | Managed cloud | Self-hosted or cloud |
| Best for | Local dev, prototyping | Production, existing Postgres stack | Fully managed at scale | Hybrid search out of the box |
| Metadata filtering | Basic | Full SQL expressiveness | Moderate | Strong |
| Scaling | Limited | Scales with Postgres | Scales automatically | Scales with deployment |
| Cost | Free | Free (infra cost) | Paid above free tier | Free self-hosted |

---

## Questions to Answer Before Closing

- What does Chroma store that the JSON file didn't?
- What does `collection.query()` return -- how is it structured?
- What would you need to change to switch from Chroma to pgvector?
- Why is `persist_directory` important for a local vector database?
- When would you pick Pinecone over pgvector, and vice versa?
