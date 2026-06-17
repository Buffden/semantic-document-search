from openai import OpenAI
from dotenv import load_dotenv
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
