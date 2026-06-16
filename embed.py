from openai import OpenAI
from dotenv import load_dotenv
from utils import chunk_text
import json
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_chunks(chunks: list[str]) -> list[dict]:
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=chunks
    )

    return [{"text": chunk, "embedding": response.data[i].embedding} for i, chunk in enumerate(chunks)]

def embed_query(query: str) -> list[float]:
    return embed_chunks([query])[0]["embedding"]

def load_document(filepath: str) -> str:
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Document not found: {filepath}: {e}")

def response_write(filepath: str, embeddings: list[dict]) -> bool:
    try:
        with open(filepath, 'w') as f:
            json.dump(embeddings, f)
    except IOError as e:
        raise IOError(f"Failed to wrte embeddings: {e}")

def main():
    file_names = os.listdir("documents/")
    json_response = []
    for file_name in filter(lambda f: f.endswith('.txt'), file_names):
        json_response.extend(embed_chunks(chunk_text(load_document(f"documents/{file_name}"))))
    response_write("embeddings.json", json_response)

if __name__ == '__main__':
    main()