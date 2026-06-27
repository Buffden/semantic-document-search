# RAG Quality Evaluation Results

## Setup

- Dataset: `golden_dataset.json` -- 20 questions (15 single-chunk, 3 multi-chunk, 2 unanswerable)
- top_k: 5
- Embedding model: `text-embedding-3-small`
- Generation model: `gpt-4o-mini`
- Scoring: retrieval recall (pass/miss per question) + LLM-as-judge answer correctness (1-5 per question)

---

## Experiment 1 -- Chunk Size

### Baseline -- chunk_size=300, overlap=50

```
[1/20] When was the city of Rome traditionally founded?
  Retrieval: pass  |  Answer score: 5/5
[2/20] Who founded Rome according to tradition?
  Retrieval: pass  |  Answer score: 4/5
[3/20] What government system replaced the Roman Kingdom around 509 BC?
  Retrieval: pass  |  Answer score: 4/5
[4/20] What were the Punic Wars?
  Retrieval: pass  |  Answer score: 5/5
[5/20] What did Julius Caesar do after conquering Gaul?
  Retrieval: pass  |  Answer score: 5/5
[6/20] What is the primary cause of modern climate change described in the document?
  Retrieval: pass  |  Answer score: 4/5
[7/20] How much have average global temperatures risen since the Industrial Revolution?
  Retrieval: pass  |  Answer score: 5/5
[8/20] How fast is the Arctic warming compared with the rest of the planet?
  Retrieval: pass  |  Answer score: 5/5
[9/20] What brain areas activate when someone listens to music?
  Retrieval: pass  |  Answer score: 4/5
[10/20] Why can music be intensely pleasurable?
  Retrieval: pass  |  Answer score: 4/5
[11/20] Why is music therapy useful for dementia and Alzheimer's disease?
  Retrieval: pass  |  Answer score: 5/5
[12/20] What are macronutrients and what do they provide?
  Retrieval: pass  |  Answer score: 5/5
[13/20] Which plant proteins can be combined to provide all essential amino acids?
  Retrieval: pass  |  Answer score: 5/5
[14/20] Why is hydration important for the body?
  Retrieval: pass  |  Answer score: 4/5
[15/20] Who became the first human in space and when?
  Retrieval: pass  |  Answer score: 4/5
[16/20] How did the Roman Republic become the Roman Empire, and who became the first emperor?
  Retrieval: pass  |  Answer score: 5/5
[17/20] How does climate change threaten both coastal cities and marine biodiversity?
  Retrieval: pass  |  Answer score: 4/5
[18/20] What are two examples of human efforts to explore or live beyond Earth after the Apollo era?
  Retrieval: pass  |  Answer score: 4/5
[19/20] What is the capital city of France?
  Retrieval: MISS  |  Answer score: 4/5
[20/20] Who won the 2022 FIFA World Cup?
  Retrieval: MISS  |  Answer score: 2/5

--- Evaluation Results ---
Retrieval recall:   18/20 (90%)
Answer correctness: 4.3 / 5.0 average
```

### Small chunks -- chunk_size=150, overlap=25

```
[1/20] When was the city of Rome traditionally founded?
  Retrieval: pass  |  Answer score: 5/5
[2/20] Who founded Rome according to tradition?
  Retrieval: pass  |  Answer score: 4/5
[3/20] What government system replaced the Roman Kingdom around 509 BC?
  Retrieval: pass  |  Answer score: 4/5
[4/20] What were the Punic Wars?
  Retrieval: pass  |  Answer score: 5/5
[5/20] What did Julius Caesar do after conquering Gaul?
  Retrieval: pass  |  Answer score: 5/5
[6/20] What is the primary cause of modern climate change described in the document?
  Retrieval: pass  |  Answer score: 4/5
[7/20] How much have average global temperatures risen since the Industrial Revolution?
  Retrieval: pass  |  Answer score: 5/5
[8/20] How fast is the Arctic warming compared with the rest of the planet?
  Retrieval: pass  |  Answer score: 5/5
[9/20] What brain areas activate when someone listens to music?
  Retrieval: pass  |  Answer score: 4/5
[10/20] Why can music be intensely pleasurable?
  Retrieval: pass  |  Answer score: 4/5
[11/20] Why is music therapy useful for dementia and Alzheimer's disease?
  Retrieval: pass  |  Answer score: 5/5
[12/20] What are macronutrients and what do they provide?
  Retrieval: pass  |  Answer score: 5/5
[13/20] Which plant proteins can be combined to provide all essential amino acids?
  Retrieval: pass  |  Answer score: 5/5
[14/20] Why is hydration important for the body?
  Retrieval: pass  |  Answer score: 4/5
[15/20] Who became the first human in space and when?
  Retrieval: pass  |  Answer score: 4/5
[16/20] How did the Roman Republic become the Roman Empire, and who became the first emperor?
  Retrieval: pass  |  Answer score: 4/5
[17/20] How does climate change threaten both coastal cities and marine biodiversity?
  Retrieval: pass  |  Answer score: 5/5
[18/20] What are two examples of human efforts to explore or live beyond Earth after the Apollo era?
  Retrieval: pass  |  Answer score: 4/5
[19/20] What is the capital city of France?
  Retrieval: MISS  |  Answer score: 4/5
[20/20] Who won the 2022 FIFA World Cup?
  Retrieval: MISS  |  Answer score: 4/5

--- Evaluation Results ---
Retrieval recall:   18/20 (90%)
Answer correctness: 4.5 / 5.0 average
```

### Large chunks -- chunk_size=600, overlap=100

```
[1/20] When was the city of Rome traditionally founded?
  Retrieval: pass  |  Answer score: 5/5
[2/20] Who founded Rome according to tradition?
  Retrieval: pass  |  Answer score: 4/5
[3/20] What government system replaced the Roman Kingdom around 509 BC?
  Retrieval: pass  |  Answer score: 4/5
[4/20] What were the Punic Wars?
  Retrieval: pass  |  Answer score: 5/5
[5/20] What did Julius Caesar do after conquering Gaul?
  Retrieval: pass  |  Answer score: 5/5
[6/20] What is the primary cause of modern climate change described in the document?
  Retrieval: pass  |  Answer score: 4/5
[7/20] How much have average global temperatures risen since the Industrial Revolution?
  Retrieval: pass  |  Answer score: 5/5
[8/20] How fast is the Arctic warming compared with the rest of the planet?
  Retrieval: pass  |  Answer score: 5/5
[9/20] What brain areas activate when someone listens to music?
  Retrieval: pass  |  Answer score: 4/5
[10/20] Why can music be intensely pleasurable?
  Retrieval: pass  |  Answer score: 4/5
[11/20] Why is music therapy useful for dementia and Alzheimer's disease?
  Retrieval: pass  |  Answer score: 5/5
[12/20] What are macronutrients and what do they provide?
  Retrieval: pass  |  Answer score: 5/5
[13/20] Which plant proteins can be combined to provide all essential amino acids?
  Retrieval: pass  |  Answer score: 5/5
[14/20] Why is hydration important for the body?
  Retrieval: pass  |  Answer score: 5/5
[15/20] Who became the first human in space and when?
  Retrieval: pass  |  Answer score: 4/5
[16/20] How did the Roman Republic become the Roman Empire, and who became the first emperor?
  Retrieval: pass  |  Answer score: 5/5
[17/20] How does climate change threaten both coastal cities and marine biodiversity?
  Retrieval: pass  |  Answer score: 4/5
[18/20] What are two examples of human efforts to explore or live beyond Earth after the Apollo era?
  Retrieval: pass  |  Answer score: 4/5
[19/20] What is the capital city of France?
  Retrieval: MISS  |  Answer score: 3/5
[20/20] Who won the 2022 FIFA World Cup?
  Retrieval: MISS  |  Answer score: 3/5

--- Evaluation Results ---
Retrieval recall:   18/20 (90%)
Answer correctness: 4.4 / 5.0 average
```

---

## Observations

Retrieval recall didn't change at all across chunk sizes -- 18/20 every time. The 2 misses are the unanswerable questions which have no source document, so that's expected, not a failure.

Where chunk size did matter was answer quality. Small chunks (150) came out on top at 4.5/5.0. The intuition makes sense -- tighter chunks give the model a focused piece of context rather than a wall of text to sift through, so the answers are more precise.

Large chunks (600) were interesting. Most documents got collapsed into a single chunk, and that actually hurt the unanswerable questions -- Q19 and Q20 both dropped to 3/5. When the model has a lot of context, it seems more likely to find something to latch onto and generate a plausible-sounding answer even when it shouldn't. Q20 at baseline (300) was even worse at 2/5 for the same reason.

The honest caveat here is that the corpus is tiny -- 5 short documents. Chunk size would matter a lot more for retrieval recall on a larger dataset where the right chunk could easily fall outside the top-K if chunking is too coarse.

## Decision

Going with `CHUNK_SIZE_SMALL (150)` and `CHUNK_OVERLAP_SMALL (25)` as the active config. Best answer correctness, cleaner no-answer behaviour.
