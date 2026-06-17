from utils import chunk_text, load_documents
from embed import embed_chunks
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


def main():
    collection = client.get_or_create_collection(name="documents")

    for doc in load_documents("documents/"):
        chunks = chunk_text(doc["text"])
        embedded = embed_chunks(chunks)

        # Delete existing chunks for this source before re-ingesting
        if collection.count() > 0:
            collection.delete(where={"source": doc["filename"]})

        collection.upsert(
            ids = [f"{doc['filename']}_{i}" for i in range(len(chunks))],
            embeddings = [e["embedding"] for e in embedded],
            documents = chunks,
            metadatas = [{"source": doc["filename"], "chunk_index": i} for i in range(len(chunks))]
        )

        print(f"Ingested {len(chunks)} chunks from {doc['filename']}")

    print(f"\nTotal vectors in collection: {collection.count()}")

if __name__ == '__main__':
    main()
