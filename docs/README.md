# Docs

This folder contains the implementation plan, phase-by-phase notes, and sequence diagrams for the RAG Document Engine.

---

## Implementation Plan

| File | Description |
| ---- | ----------- |
| `implementation-plan.md` | Full build plan across all 7 phases — goals, what gets built, stack additions, and questions to answer per phase |

---

## Phase Notes

One file per phase. Each covers the goal, design decisions, and key concepts for that phase.

| File | Phase |
| ---- | ----- |
| `phase-1-semantic-foundation.md` | Semantic search from scratch — chunking, embeddings, cosine similarity over flat JSON |
| `phase-2-vector-store.md` | Replace JSON with ChromaDB — persistent collection, metadata, `collection.query()` |
| `phase-3-rag-pipeline.md` | Close the loop — retrieval + LLM generation, grounded answers, citations, token budget |
| `phase-4-document-ingestion.md` | Multi-format ingestion — PDF, DOCX, Markdown parsers, CLI trigger, deduplication |
| `phase-5-retrieval-quality.md` | Improve retrieval — evaluation set, hybrid search (BM25 + vector), re-ranker, metadata filters |
| `phase-6-search-and-chat-mode.md` | Two interaction modes — document search and multi-turn chat with conversation history |
| `phase-7-role-based-document-access.md` | Access control — owner metadata at ingestion, per-user query filters, no bypass path |

---

## Sequence Diagrams

PlantUML sequence diagrams for each pipeline. Open with any PlantUML-compatible renderer.

### Document Ingestion Pipeline

Covers Phase 4. Split into 4 focused diagrams — read in this order to follow the full flow:

| Order | File | Covers |
| ----- | ---- | ------- |
| 1 | [pipeline-document-ingestion-entry-routing.svg](../diagrams/docs/pipeline-document-ingestion-entry-routing.svg) | CLI entry, arg validation, `get_or_create_collection`, file vs directory routing |
| 2 | [pipeline-document-ingestion-parsing.svg](../diagrams/docs/pipeline-document-ingestion-parsing.svg) | Router extension resolution, all 4 parsers (PDF / DOCX / MD / TXT), flatten to plain text |
| 3 | [pipeline-document-ingestion-chunk-embed.svg](../diagrams/docs/pipeline-document-ingestion-chunk-embed.svg) | Sliding window chunking, OpenAI embeddings API call |
| 4 | [pipeline-document-ingestion-upsert.svg](../diagrams/docs/pipeline-document-ingestion-upsert.svg) | Deduplication check, ChromaDB upsert with full payload |

### Other Pipelines

| File | Covers |
| ---- | ------- |
| [pipeline-semantic-search.svg](../diagrams/docs/pipeline-semantic-search.svg) | Phase 1 — query embedding, cosine similarity, top-K retrieval over flat JSON |
| [pipeline-vector-store.svg](../diagrams/docs/pipeline-vector-store.svg) | Phase 2 — ingest and query flow using ChromaDB |
| [pipeline-rag.svg](../diagrams/docs/pipeline-rag.svg) | Phase 3 — end-to-end RAG: retrieval, token budget, prompt construction, LLM generation, citations |
