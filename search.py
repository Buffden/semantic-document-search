import json
from utils import chunk_text, cosine_similarity
from embed import embed_chunks, embed_query

def load_embedded_response() -> list[dict]:
    try:
        with open('embeddings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found") 

def search(query: str, top_k: int = 3) -> list[dict]:
    embedded_response = load_embedded_response()
    query_vector = embed_query(query)

    scored = [
        {"text": chunk["text"], "score": cosine_similarity(query_vector, chunk["embedding"])}
        for chunk in embedded_response
    ]

    return sorted(scored, key = lambda x: x["score"], reverse = True)[:top_k]

def main():
    results = search("what foods are good for the heart")
    for i, result in enumerate(results):
        print(f"Result {i + 1} (score: {result['score']:.4f})")
        print(result["text"])
        print()

if __name__ == '__main__':
    main()
