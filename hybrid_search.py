import chromadb
from rank_bm25 import BM25Okapi
from embed import embed_query
from config import RERANKER_CANDIDATE_K, RRF_K

client = chromadb.PersistentClient(path="./chroma_db")


def _get_all_chunks() -> list[dict]:
    collection = client.get_or_create_collection(name="documents")
    results = collection.get(include=["documents", "metadatas"])
    return [
        {
            "text": results["documents"][i],
            "source": results["metadatas"][i]["source"],
            "chunk_index": results["metadatas"][i]["chunk_index"],
        }
        for i in range(len(results["documents"]))
    ]


def _vector_search(query: str, top_k: int) -> list[dict]:
    collection = client.get_or_create_collection(name="documents")
    query_vector = embed_query(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["documents"][0]))
    ]


def _bm25_search(query: str, all_chunks: list[dict], top_k: int) -> list[dict]:
    tokenized_corpus = [chunk["text"].lower().split() for chunk in all_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(query.lower().split())
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [all_chunks[i] for i in ranked_indices[:top_k]]


def _rrf(vector_results: list[dict], bm25_results: list[dict], top_n: int) -> list[dict]:
    scores: dict[str, float] = {}
    chunk_map: dict[str, dict] = {}

    for rank, chunk in enumerate(vector_results, start=1):
        key = f"{chunk['source']}_{chunk['chunk_index']}"
        scores[key] = scores.get(key, 0) + 1 / (RRF_K + rank)
        chunk_map[key] = chunk

    for rank, chunk in enumerate(bm25_results, start=1):
        key = f"{chunk['source']}_{chunk['chunk_index']}"
        scores[key] = scores.get(key, 0) + 1 / (RRF_K + rank)
        chunk_map[key] = chunk

    ranked_keys = sorted(scores, key=lambda k: scores[k], reverse=True)
    return [chunk_map[k] for k in ranked_keys[:top_n]]


def hybrid_search(query: str, top_n: int = 5) -> list[dict]:
    all_chunks = _get_all_chunks()
    candidate_k = min(RERANKER_CANDIDATE_K, len(all_chunks))

    vector_results = _vector_search(query, top_k=candidate_k)
    bm25_results = _bm25_search(query, all_chunks, top_k=candidate_k)

    return _rrf(vector_results, bm25_results, top_n=top_n)
