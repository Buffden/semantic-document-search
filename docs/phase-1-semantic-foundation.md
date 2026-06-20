# RDE-1 | Phase 1: Semantic Foundation

**Status:** Done
**Type:** Feature
**Priority:** High
**Depends on:** None

---

## Goal

Understand how meaning-based search works under the hood before reaching for any infrastructure. Build a working semantic search pipeline using only Python primitives -- no vector database, no framework. Storage is a flat JSON file. Similarity is brute-force cosine over NumPy. The point is to understand the mechanics at every step.

---

## Tasks

- [x] Create `utils.py` with `chunk_text(text, chunk_size, overlap)` -- splits a document into overlapping word windows
- [x] Create `embed.py` -- loads `.txt` files from `documents/`, chunks them, calls OpenAI embeddings API, saves results to `embeddings.json`
- [x] Create `search.py` -- embeds a query using the same model, computes cosine similarity against all stored chunks, returns top-K results

---

## Acceptance Criteria

- `embed.py` processes all `.txt` files in `documents/` and writes `embeddings.json` with chunk text, source filename, and embedding vector
- `search.py` accepts a query string, returns the top-K most semantically similar chunks with their source
- Chunking produces overlapping windows so context is not split at chunk boundaries
- No vector database or similarity library is used -- cosine similarity is implemented manually using NumPy

---

## Stack

- Python 3.12
- OpenAI `text-embedding-3-small`
- NumPy for cosine similarity
- Plain JSON for storage

---

## Questions to Answer Before Closing

- Why do you embed the query with the same model as the documents?
- What happens if chunks are too large? Too small?
- Why does cosine similarity work better than Euclidean distance for text?
- What breaks if you use different embedding models for queries vs documents?
