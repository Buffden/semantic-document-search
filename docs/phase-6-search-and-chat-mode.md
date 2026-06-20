# RDE-6 | Phase 6: Search and Chat Mode

**Status:** Todo
**Type:** Feature
**Priority:** Medium
**Depends on:** RDE-5

---

## Goal

Give the engine two distinct interaction modes -- find a document, or have a conversation over one. Right now the engine only does one-shot retrieval: one query in, top-K chunks out. This phase adds document-level search (which files are relevant to a topic?) and multi-turn chat (ask follow-up questions with the system remembering prior context).

---

## What Changes from Phase 5

- New `chat.py` wraps `rag.py` with conversation history management
- New `search_mode.py` returns document-level relevance, not chunk-level, for finding what to read
- Conversation history is passed as context on every LLM call so follow-up questions make sense

---

## Tasks

- [ ] Create `chat.py` -- multi-turn conversation loop
  - Maintains a conversation history list (list of `{"role": ..., "content": ...}` dicts)
  - Appends each user question and model answer to the history
  - Passes the full history as context on every call
  - Truncation: count tokens in the history using `tiktoken` before each call; if it exceeds the limit, drop the oldest turns until it fits (sliding window)
- [ ] Create `search_mode.py` -- document-level relevance mode
  - Retrieves top-K chunks as usual
  - Aggregates chunk scores by source document
  - Returns a ranked list of documents with a summary of why each is relevant
- [ ] Keep clear CLI separation:
  - `python rag.py` -- one-shot QA
  - `python chat.py` -- multi-turn conversation
  - `python search_mode.py` -- find relevant documents

---

## Acceptance Criteria

- `python chat.py` starts an interactive loop where follow-up questions reference prior answers correctly
- History truncation activates when history exceeds the token limit -- older turns are dropped, newer turns are kept
- `python search_mode.py "<query>"` returns a ranked list of relevant documents with a reason for each
- All three modes use the same underlying retrieval and generation pipeline

---

## Stack Additions

None -- uses existing `tiktoken`, OpenAI, and Chroma dependencies.

---

## Questions to Answer Before Closing

- How much conversation history can you pass before hitting the context window limit?
- How do you handle follow-up questions that reference something said two turns ago?
- What is the difference between document-level and chunk-level retrieval -- when does each matter?
- How do you summarize why a document is relevant without reading it fully each time?
