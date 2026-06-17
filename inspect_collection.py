import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


def main():
    collection = client.get_or_create_collection(name="documents")

    print(f"Total vectors in collection: {collection.count()}\n")

    sample = collection.get(
        limit = 1,
        include = ["documents", "metadatas", "embeddings"]
    )

    print("Sample entry:")
    print(f"  id:          {sample['ids'][0]}")
    print(f"  source:      {sample['metadatas'][0]['source']}")
    print(f"  chunk_index: {sample['metadatas'][0]['chunk_index']}")
    print(f"  text:        {sample['documents'][0][:120]}...")
    print(f"  embedding:   [{sample['embeddings'][0][0]:.6f}, {sample['embeddings'][0][1]:.6f}, ...] ({len(sample['embeddings'][0])} dims)")


if __name__ == '__main__':
    main()
