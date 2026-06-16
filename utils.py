import numpy as np

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
