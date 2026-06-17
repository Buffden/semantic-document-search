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

**Vector DB tradeoffs to understand:**

| | Chroma | pgvector | Pinecone | Weaviate |
| --- | --- | --- | --- | --- |
| Setup | Local, zero config | Requires PostgreSQL | Managed cloud | Self-hosted or cloud |
| Best for | Local dev, prototyping | Production, existing Postgres stack | Fully managed at scale | Hybrid search out of the box |
| Metadata filtering | Basic | Full SQL expressiveness | Moderate | Strong |
| Scaling | Limited | Scales with Postgres | Scales automatically | Scales with deployment |
| Cost | Free | Free (infra cost) | Paid above free tier | Free self-hosted |

Chroma is used here because it requires no infrastructure. The flagship project uses pgvector. Pinecone is the go-to when you want zero ops at scale. Weaviate is worth knowing because hybrid search is built in -- no extra wiring needed.

**Questions to answer:**

- What does Chroma store that the JSON file didn't?
- What does `collection.query()` return -- how is it structured?
- What would you need to change to switch from Chroma to pgvector?
- Why is `persist_directory` important for a local vector database?
- When would you pick Pinecone over pgvector, and vice versa?

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
- Token budget logic in `generate.py` -- count tokens per chunk using `tiktoken`, set a max context budget, trim the chunk list to fit before building the prompt
- Graceful no-answer handling -- prompt instructs the model to respond with a fixed phrase when context is insufficient; `rag.py` detects this response and surfaces it cleanly instead of passing it through as a regular answer

**Stack additions:**

- OpenAI chat completions API (`gpt-4o-mini` or `gpt-4o`)
- `tiktoken` -- OpenAI's tokenizer, used to count tokens before sending to the API

**Questions to answer:**

- How do you prevent the LLM from answering beyond what the retrieved context contains?
- What does a good citation look like in the response -- chunk ID, source file, or both?
- What happens when the retrieved chunks don't contain the answer?
- How do you structure the prompt so the model stays grounded?
- How do you decide how many chunks to include when each one has a different token count?

---

## Phase 4: Document Ingestion

**Goal:** Support real document formats and a proper ingestion trigger, not just static `.txt` files in a folder.

The engine currently processes a hardcoded `documents/` directory of `.txt` files. Real use cases involve PDFs, Word documents, and Markdown -- and users need a way to drop in a new file and have it ingested without editing code. This phase adds format-specific parsers and a CLI ingestion command.

**What changes vs Phase 3:**

- New `ingest/` module with format-specific parsers
- `ingest.py` updated to accept a file path or directory as a CLI argument and route by extension
- Any format in, plain text out -- same embedding and storage flow after

**What gets built:**

- `ingest/pdf_parser.py` -- extract text from PDF using `pymupdf` or `pdfplumber`
- `ingest/docx_parser.py` -- extract text from DOCX using `python-docx`
- `ingest/markdown_parser.py` -- strip Markdown syntax, extract clean text
- `ingest/router.py` -- detect file type, call the right parser, return plain text
- CLI interface in `ingest.py` -- `python ingest.py <file_or_directory>` triggers ingestion for any supported format
- Deduplication in `ingest.py` -- before adding chunks for a file, delete any existing chunks in Chroma with the same `source` metadata value so re-ingesting a file replaces rather than duplicates

**Stack additions:**

- `pymupdf` or `pdfplumber` for PDF parsing
- `python-docx` for DOCX parsing

**Questions to answer:**

- How do you handle PDFs with tables or images -- what gets lost?
- What metadata is worth extracting at parse time (title, author, page number)?
- How do you handle multi-page PDFs where a chunk might span a page boundary?
- What happens if the same file is ingested twice -- how do you avoid duplicate vectors?

---

## Phase 5: Retrieval Quality

**Goal:** Make retrieval measurably better -- not just faster or more scalable, but more accurate.

Cosine similarity over embeddings is a good first pass but it misses cases where exact terms matter (product codes, names, IDs). It also returns the top-K closest vectors without any sense of whether they actually answer the question. This phase starts with a baseline evaluation, then improves chunk tuning, adds hybrid search and a cross-encoder re-ranker, and measures whether each change actually helped.

**What changes vs Phase 4:**

- Build a labeled test set first so improvements can be measured
- Experiment with chunk size and overlap to find what works best for the document set
- Retrieval in `search.py` extended with BM25 keyword scoring
- Results merged using reciprocal rank fusion before passing to the generator
- Cross-encoder re-ranker added as a second pass on the merged top-K
- Metadata filter support added to `collection.query()` calls

**What gets built:**

- `eval/test_set.json` -- at least 10 question + expected source chunk pairs, written by hand
- `eval/evaluate.py` -- runs each query, checks if the expected chunk appears in top-K results, reports recall@K
- Chunk size and overlap experiments -- re-run ingestion with different settings, compare eval scores
- `retrieval/hybrid.py` -- combine vector similarity scores with BM25 scores via reciprocal rank fusion
- `retrieval/reranker.py` -- cross-encoder model re-scores top-K results before generation
- Metadata filter interface in `search.py` -- filter by source file or document type before query

**Stack additions:**

- `rank_bm25` for keyword scoring
- `sentence-transformers` for cross-encoder re-ranking

**Questions to answer:**

- How do you know if a smaller chunk size improved or hurt retrieval without a test set?
- What is overlap doing -- what breaks if you set it to zero?
- When does hybrid search outperform pure vector search? When does it not?
- What is reciprocal rank fusion and why is it used to merge scores instead of just averaging?
- What is the difference between a bi-encoder (embeddings) and a cross-encoder (re-ranker)?

---

## Phase 6: Search and Chat Mode

**Goal:** Give the engine two distinct interaction modes -- find a document, or have a conversation over one.

Right now the engine only does retrieval: one query in, top-K chunks out. This phase adds two higher-level modes. Search mode lets a user find which documents are most relevant to a topic. Chat mode lets a user ask follow-up questions over a document, with the system remembering what was asked before and building on prior answers.

**What changes vs Phase 5:**

- New `chat.py` -- wraps `rag.py` with conversation history management
- New `search_mode.py` -- returns document-level relevance, not chunk-level, useful for finding what to read
- Conversation history passed as context in each LLM call so follow-up questions make sense

**What gets built:**

- `chat.py` -- maintains a conversation history list, appends each query and answer, passes the full history as context on every turn
- History truncation in `chat.py` -- count tokens in the history using `tiktoken` before each call; if it exceeds a set limit, drop the oldest turns until it fits (sliding window)
- `search_mode.py` -- aggregates chunk scores by source document, returns ranked list of documents with a summary of why each is relevant
- Clear CLI separation: `python rag.py` for one-shot QA, `python chat.py` for multi-turn conversation, `python search_mode.py` to find documents

**Questions to answer:**

- How much conversation history can you pass before hitting the context window limit?
- How do you handle follow-up questions that reference something said two turns ago?
- What is the difference between document-level and chunk-level retrieval -- when does each matter?
- How do you summarize why a document is relevant without reading it fully each time?

---

## Phase 7: Role-Based Document Access

**Goal:** Control which documents a user can search and chat over -- not every user should see every document.

Right now any query searches the entire vector collection. In a real product, documents belong to teams, projects, or individuals. This phase adds an access control layer: documents are tagged with ownership metadata at ingestion time, and all search and retrieval is filtered by the current user's permissions before results are returned.

**What changes vs Phase 6:**

- Ingestion extended to accept an `--owner` or `--access` flag, stored as metadata on every chunk
- Search and RAG pipeline wrapped with an access filter that injects a metadata constraint before querying Chroma
- A simple `users.json` config defines users and their allowed document groups
- All modes (search, chat, QA) go through the access layer -- no bypass path

**What gets built:**

- `users.json` -- defines users, their roles, and which document groups they can access
- `access.py` -- given a user, returns the set of allowed sources as a metadata filter
- Updated `ingest.py` -- accepts `--owner <group>` flag, tags all chunks with the group on ingestion
- Updated `search.py`, `rag.py`, `chat.py` -- all pass the access filter from `access.py` into `collection.query()`

**Questions to answer:**

- Why is enforcing access at the vector DB query level safer than filtering results after retrieval?
- What happens if a document is re-ingested with a different owner -- which chunks win?
- How would you model group-based access vs user-based access in metadata?
- What does this pattern look like in production when the user identity comes from a JWT instead of a config file?
