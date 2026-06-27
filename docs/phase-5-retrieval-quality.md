# RDE-5 | Phase 5: Retrieval Quality

**Status:** Complete
**Type:** Enhancement
**Priority:** High
**Depends on:** RDE-4

---

## Goal

Make retrieval measurably better -- not just faster, but more accurate. Cosine similarity over embeddings is a good first pass but misses cases where exact terms matter (product codes, names, IDs). It also returns top-K closest vectors without any sense of whether they actually answer the question. Build a baseline evaluation first, then improve chunk tuning, add hybrid search, add a cross-encoder re-ranker, and measure whether each change actually helped.

---

## What Changed from Phase 4

- Built a labeled evaluation set before changing anything -- so improvements can be measured
- Experimented with chunk size and overlap across three settings (300/50, 150/25, 600/100)
- Extended `search.py` with an optional metadata filter passed to Chroma's `where` argument, with a fallback when filtered results are too few
- Created `hybrid_search.py` -- runs BM25 keyword search alongside vector search and merges both ranked lists using reciprocal rank fusion (RRF, k=60)
- Created `rerank.py` -- cross-encoder model (`cross-encoder/ms-marco-MiniLM-L-6-v2`) re-scores the hybrid search candidates before passing to generation
- Updated `rag.py` to use hybrid search + reranker instead of plain vector search
- Created `config.py` to centralise all tuneable constants (chunk size, reranker K, RRF K)
- Evaluation results and observations recorded in `eval/results.md`

---

## Tasks

- [x] Create `eval/golden_dataset.json` -- 20 manually written question + expected answer pairs (15 answerable, 3 multi-chunk, 2 unanswerable)
- [x] Create `eval/eval.py` -- runs each query through the full RAG pipeline, scores retrieval recall and answer correctness via LLM-as-judge, prints a summary
- [x] Run baseline evaluation and record scores before making any changes
- [x] Experiment with chunk size and overlap -- re-ran ingestion with 3 settings, compared eval scores, settled on chunk_size=150, overlap=25
- [x] Create `hybrid_search.py` -- BM25 + vector search merged via RRF
- [x] Create `rerank.py` -- cross-encoder re-scores hybrid search candidates
- [x] Add metadata filter interface to `search.py` -- optional `filters` dict passed to Chroma `where`, fallback to unfiltered if results < 2
- [x] Re-ran evaluation after each change and recorded results in `eval/results.md`

---

## Acceptance Criteria

- [x] `python3 eval/eval.py` reports retrieval recall and answer correctness for the current setup
- [x] Hybrid search is wired into `rag.py` as the retrieval stage
- [x] Reranker re-scores hybrid candidates before generation
- [x] Metadata filtering works -- querying with `source="nutrition-and-health.txt"` returns only chunks from that file; falls back to unfiltered if too few results
- [x] All changes are accompanied by eval score comparisons in `eval/results.md`

---

## Stack Additions

- `rank_bm25` -- BM25 keyword scoring
- `sentence-transformers` -- cross-encoder re-ranking (`cross-encoder/ms-marco-MiniLM-L-6-v2`)

---

## Eval Summary

| Configuration | Retrieval recall | Answer correctness |
| ------------- | :--------------: | :----------------: |
| Baseline (chunk_size=300) | 18/20 (90%) | 4.3 / 5.0 |
| Small chunks (chunk_size=150) | 18/20 (90%) | 4.5 / 5.0 |
| Large chunks (chunk_size=600) | 18/20 (90%) | 4.4 / 5.0 |
| Small chunks + reranking | 18/20 (90%) | 4.3 / 5.0 |
| Small chunks + hybrid + reranking | 18/20 (90%) | 4.3 / 5.0 |

Full raw results and observations in `eval/results.md`.

---

## Questions to Answer Before Closing

- How do you know if a smaller chunk size improved or hurt retrieval without a test set?
- What is overlap doing -- what breaks if you set it to zero?
- When does hybrid search outperform pure vector search? When does it not?
- What is reciprocal rank fusion and why is it used to merge scores instead of just averaging?
- What is the difference between a bi-encoder (embeddings) and a cross-encoder (re-ranker)?
