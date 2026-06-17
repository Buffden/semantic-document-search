# Implementation Plan

This document tracks the full build plan for the RAG Document Engine. Each phase extends the previous one -- the storage layer, retrieval strategy, and generation capabilities evolve incrementally.

---

## Phase 1: Semantic Foundation

**Goal:** Understand how meaning-based search works under the hood before reaching for any infrastructure.

Build a working semantic search pipeline using only Python primitives -- no vector database, no framework. The storage is a flat JSON file. The similarity is brute-force cosine over NumPy. The point is to understand the mechanics at every step.

**What gets built:**
- `utils.py` -- `chunk_text(text, chunk_size, overlap)` splits documents into overlapping word windows
- `embed.py` -- loads `.txt` files, chunks them, calls OpenAI embeddings API, saves to `embeddings.json`
- `search.py` -- embeds a query, computes cosine similarity against all stored chunks, returns top-K

**Stack:**
- OpenAI `text-embedding-3-small`
- NumPy for cosine similarity
- Plain JSON for storage

**Status:** Complete

**Questions answered:**
- Why do you embed the query with the same model as the documents?
- What happens if chunks are too large? Too small?
- Why does cosine similarity work better than Euclidean distance for text?
- What breaks if you use different embedding models for queries vs documents?

---

## Phase 2: Vector Store

**Goal:** Replace the flat JSON file and brute-force cosine loop with a real vector database.

The chunking and embedding logic from Phase 1 carries over unchanged. The only thing being swapped is the storage and retrieval layer -- `embeddings.json` becomes a Chroma persistent collection, and the manual cosine loop becomes `collection.query()`.

**What changes vs Phase 1:**

| Phase 1 | Phase 2 Replacement |
| ------- | ------------------- |
| `embeddings.json` | Chroma persistent collection |
| `json.dump` / `json.load` | `collection.add()` / `collection.query()` |
| Brute-force cosine loop in `search.py` | Chroma's built-in similarity search |
| No metadata | `source` filename + `chunk_index` stored as metadata |

**What gets built:**
- `ingest.py` -- replaces `embed.py`: chunks, embeds, and stores in Chroma with metadata
- `search.py` -- rewritten to query Chroma instead of scanning JSON
- `utils.py` -- carried over from Phase 1, no changes needed

**Stack additions:**
- `chromadb` -- local persistent vector database

**Status:** In Progress

**Questions to answer:**
- What does Chroma store that the JSON file didn't?
- What does `collection.query()` return -- how is it structured?
- What would you need to change to switch from Chroma to pgvector?
- Why is `persist_directory` important for a local vector database?

---

## Phase 3: RAG Pipeline

**Goal:** Close the loop -- add LLM generation on top of retrieval so the system answers questions, not just returns chunks.

Phase 1 and 2 return raw text chunks. A user still has to read them and synthesize the answer themselves. This phase adds the generation step: retrieved chunks become context, the LLM generates a grounded answer, and every claim is tied back to a source chunk.

**What changes vs Phase 2:**
- `search.py` returns chunks + metadata (already works)
- New `generate.py` -- takes query + top-K chunks, builds a prompt, calls the chat completions API, returns answer + citations
- New `rag.py` -- orchestrates the full pipeline: query in, answer + sources out

**What gets built:**
- `generate.py` -- prompt construction, LLM call, citation extraction
- `rag.py` -- end-to-end pipeline entry point
- Prompt template for grounded generation with source attribution

**Stack additions:**
- OpenAI chat completions API (`gpt-4o-mini` or `gpt-4o`)

**Questions to answer:**
- How do you prevent the LLM from answering beyond what the retrieved context contains?
- What does a good citation look like in the response -- chunk ID, source file, or both?
- What happens when the retrieved chunks don't contain the answer?
- How do you structure the prompt so the model stays grounded?

---

## Phase 4: Document Ingestion

**Goal:** Support real document formats beyond plain `.txt` files.

The engine can only process `.txt` files right now. Real use cases involve PDFs, Word documents, and Markdown. This phase adds a document parsing layer that sits in front of the chunking pipeline -- any format in, plain text out, same embedding and storage flow after.

**What changes vs Phase 3:**
- New `ingest/` module with format-specific parsers
- `ingest.py` updated to route files by extension before chunking

**What gets built:**
- `ingest/pdf_parser.py` -- extract text from PDF using `pymupdf` or `pdfplumber`
- `ingest/docx_parser.py` -- extract text from DOCX using `python-docx`
- `ingest/markdown_parser.py` -- strip Markdown syntax, extract clean text
- `ingest/router.py` -- detect file type, call the right parser, return plain text

**Stack additions:**
- `pymupdf` or `pdfplumber` for PDF parsing
- `python-docx` for DOCX parsing

**Questions to answer:**
- How do you handle PDFs with tables or images -- what gets lost?
- What metadata is worth extracting at parse time (title, author, page number)?
- How do you handle multi-page PDFs where a chunk might span a page boundary?

---

## Phase 5: Retrieval Quality

**Goal:** Make retrieval measurably better -- not just faster or more scalable, but more accurate.

Cosine similarity over embeddings is a good first pass but it misses cases where exact terms matter (product codes, names, IDs). It also returns the top-K closest vectors without any sense of whether they actually answer the question. This phase adds hybrid search (vector + keyword), a reranker to re-score retrieved results, and metadata filters to narrow the search space before retrieval runs.

**What changes vs Phase 4:**
- Retrieval in `search.py` extended with BM25 keyword scoring
- Results merged using reciprocal rank fusion before passing to the generator
- Cross-encoder reranker added as a second pass on the merged top-K
- Metadata filter support added to `collection.query()` calls

**What gets built:**
- `retrieval/hybrid.py` -- combine vector similarity scores with BM25 scores via reciprocal rank fusion
- `retrieval/reranker.py` -- cross-encoder model re-scores top-K results before generation
- Metadata filter interface in `search.py` -- filter by source file or document type before query

**Stack additions:**
- `rank_bm25` for keyword scoring
- `sentence-transformers` for cross-encoder reranking

**Questions to answer:**
- When does hybrid search outperform pure vector search? When does it not?
- What is reciprocal rank fusion and why is it used to merge scores instead of just averaging?
- What is the difference between a bi-encoder (embeddings) and a cross-encoder (reranker)?
- How do you build a labeled test set to measure whether retrieval actually improved?
