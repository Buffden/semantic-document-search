# RDE-3 | Phase 3: RAG Pipeline

**Status:** Complete
**Type:** Feature
**Priority:** High
**Depends on:** RDE-2

---

## Goal

Close the loop -- add LLM generation on top of retrieval so the system answers questions, not just returns chunks. Retrieved chunks become context, the LLM generates a grounded answer, and every claim is tied back to a source chunk.

---

## What Changes from Phase 2

- `search.py` already returns chunks + metadata -- no changes needed
- New `generate.py` takes a query + top-K chunks, builds a prompt, calls the chat completions API, returns answer + citations
- New `rag.py` orchestrates the full pipeline: query in, answer + sources out

---

## Tasks

- [x] Create `generate.py` with function `generate_answer(question: str, chunks: list[dict]) -> dict`
  - Builds a prompt: system instruction + retrieved chunks as context + user question
  - System prompt must instruct the model to answer ONLY from the provided context
  - System prompt must instruct the model to respond with exactly `"I don't know based on the provided documents."` when the answer is not in the context
  - Calls `gpt-4o-mini` via the OpenAI chat completions API
  - Returns `{ "answer": "...", "sources": [...] }`
- [x] Add token budget logic to `generate.py`
  - Use `tiktoken` to count tokens in each chunk before building the prompt
  - Set a max context token budget (2000 tokens)
  - Walk chunks in order of relevance and add each until the budget is reached -- skip any chunk that would exceed it
- [x] Create `rag.py` as the end-to-end pipeline entry point
  - Accept a question via `input()` or a command-line argument
  - Embed the question using OpenAI
  - Query Chroma for top-5 most similar chunks
  - Pass the question and chunks to `generate_answer()`
  - Detect the fixed "I don't know" phrase -- if matched, print `"No answer found in the documents."` instead of passing the raw model response
  - Otherwise, print the answer and source citations
- [x] Test with at least 3 questions
  - One where the answer is clearly in the documents
  - One where the answer spans multiple chunks
  - One where the answer is NOT in the documents -- verify the no-answer path prints cleanly
- [x] Debug retrieval vs generation separately for one question -- print raw chunks before generation to confirm the right context is being retrieved
- [x] Tune K: run the same question with K=3 and K=7, compare answers

---

## Acceptance Criteria

- `python rag.py` accepts a question and returns a grounded answer with source citations
- The answer is generated only from retrieved chunks -- the prompt enforces this
- When context is insufficient, the output is `"No answer found in the documents."` -- not raw model text
- The prompt never silently truncates: the token budget trims the chunk list before the prompt is built
- Source citations show the chunk text and the source filename

---

## Example Output

```
Answer:
The main dietary sources of omega-3 fatty acids include fatty fish such as salmon,
mackerel, and sardines, as well as walnuts and flaxseed.

Sources:
[1] nutrition.txt (chunk 4): "Omega-3 fatty acids are found in high concentrations in..."
[2] nutrition.txt (chunk 6): "Walnuts and flaxseed are among the best plant-based sources..."
```

---

## Stack Additions

- OpenAI `gpt-4o-mini` via chat completions API
- `tiktoken` -- OpenAI tokenizer for counting tokens before sending to the API

---

## Questions to Answer Before Closing

- What is in the context prompt you send to the LLM -- exactly?
- Why use a fixed "I don't know" phrase instead of letting the model respond however it wants?
- How do you decide how many chunks to include when each one has a different token count?
- What happens if K=1 and the single retrieved chunk doesn't contain the answer?
- How would you test whether the model is using the context or its training memory?
- What would you change in the prompt if the model keeps ignoring the grounding instruction?
- Why is `tiktoken` needed -- why not just count words or characters?
