# RDE-5 | Phase 5: Retrieval Quality

**Status:** Todo
**Type:** Enhancement
**Priority:** High
**Depends on:** RDE-4

---

## Goal

Make retrieval measurably better -- not just faster, but more accurate. Cosine similarity over embeddings is a good first pass but misses cases where exact terms matter (product codes, names, IDs). It also returns top-K closest vectors without any sense of whether they actually answer the question. Build a baseline evaluation first, then improve chunk tuning, add hybrid search, add a cross-encoder re-ranker, and measure whether each change actually helped.

---

## What Changes from Phase 4

- Build a labeled test set before changing anything -- so improvements can be measured
- Experiment with chunk size and overlap to find what works best for the document set
- Extend `search.py` with BM25 keyword scoring alongside vector similarity
- Merge vector and BM25 results using reciprocal rank fusion before passing to the generator
- Add a cross-encoder re-ranker as a second pass on the merged top-K
- Add metadata filter support to all `collection.query()` calls

---

## Tasks

- [ ] Create `eval/test_set.json` -- at least 10 manually written question + expected source chunk pairs
- [ ] Create `eval/evaluate.py` -- runs each query, checks if the expected chunk appears in top-K results, reports recall@K
- [ ] Run baseline evaluation against Phase 4 retrieval and record the score
- [ ] Experiment with chunk size and overlap -- re-run ingestion with at least 2 different settings, compare eval scores
- [ ] Create `retrieval/hybrid.py` -- combine vector similarity scores with BM25 scores via reciprocal rank fusion
- [ ] Create `retrieval/reranker.py` -- cross-encoder model re-scores top-K results before they are passed to generation
- [ ] Add metadata filter interface to `search.py` -- allow filtering by source file or document type before running the query
- [ ] Re-run evaluation after each change and record the delta

---

## Acceptance Criteria

- `python eval/evaluate.py` reports recall@K for the current retrieval setup against the test set
- Hybrid search recall@K is higher than pure vector search recall@K on the test set
- Re-ranker changes the order of at least some results -- verify with a debug print before and after
- Metadata filtering works: querying with `source="nutrition.txt"` returns only chunks from that file
- All changes are accompanied by eval score comparisons showing the impact

---

## Stack Additions

- `rank_bm25` for keyword scoring
- `sentence-transformers` for cross-encoder re-ranking

---

## Questions to Answer Before Closing

- How do you know if a smaller chunk size improved or hurt retrieval without a test set?
- What is overlap doing -- what breaks if you set it to zero?
- When does hybrid search outperform pure vector search? When does it not?
- What is reciprocal rank fusion and why is it used to merge scores instead of just averaging?
- What is the difference between a bi-encoder (embeddings) and a cross-encoder (re-ranker)?
