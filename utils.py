import numpy as np


def load_document(filepath: str) -> str:
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Document not found: {filepath}: {e}")


def load_documents(directory: str) -> list[dict]:
    import os
    documents = []
    for filename in filter(lambda f: f.endswith('.txt'), os.listdir(directory)):
        filepath = os.path.join(directory, filename)
        documents.append({"filename": filename, "text": load_document(filepath)})
    return documents

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    step = chunk_size - overlap
    chunks = []

    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        chunks.append(" ".join(chunk_words))
    
    return chunks

def cosine_similarity(a: list[float], b: list[float]) -> float: 
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
