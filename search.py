from embed import embed_query
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


def search(query: str, top_k: int = 3) -> list[dict]:
    collection = client.get_or_create_collection(name="documents")
    query_vector = embed_query(query)

    results = collection.query(
        query_embeddings = [query_vector],
        n_results = top_k,
        include = ["documents", "metadatas", "distances"]
    )

    return [
        {
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i]
        }
        for i in range(len(results["documents"][0]))
    ]


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
