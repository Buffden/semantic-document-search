from embed import embed_query
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


def _query(collection, query_vector: list[float], top_k: int, filters: dict | None) -> list[dict]:
    kwargs = {
        "query_embeddings": [query_vector],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if filters:
        kwargs["where"] = filters

    results = collection.query(**kwargs)

    return [
        {
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i]
        }
        for i in range(len(results["documents"][0]))
    ]


def search(query: str, top_k: int = 3, filters: dict | None = None) -> list[dict]:
    collection = client.get_or_create_collection(name="documents")
    query_vector = embed_query(query)

    chunks = _query(collection, query_vector, top_k, filters)

    if filters and len(chunks) < 2:
        print(f"[search] filtered results too few ({len(chunks)}), retrying without filter")
        chunks = _query(collection, query_vector, top_k, filters=None)

    return chunks


def main():
    query = "what foods are good for the heart"
    results = search(query)

    print(f"Query: \"{query}\"\n")
    for i, result in enumerate(results):
        print(f"Result {i + 1} (distance: {result['distance']:.4f}) — {result['source']} [chunk {result['chunk_index']}]")
        print(result["text"])
        print()


if __name__ == '__main__':
    main()
