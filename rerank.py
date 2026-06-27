from sentence_transformers import CrossEncoder

_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(question: str, chunks: list[dict], top_n: int = 5) -> list[dict]:
    pairs = [(question, chunk["text"]) for chunk in chunks]
    scores = _model.predict(pairs)

    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)

    return [chunk for _, chunk in ranked[:top_n]]
