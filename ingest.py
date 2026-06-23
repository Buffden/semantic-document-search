import sys
from pathlib import Path
import chromadb
from utils import chunk_text
from embed import embed_chunks
from ingest.router import parse, SUPPORTED_EXTENSIONS

client = chromadb.PersistentClient(path = "./chroma_db")


def ingest_file(collection, filepath: str):
	filename = Path(filepath).name
	text = parse(filepath)
	chunks = chunk_text(text)
	embedded = embed_chunks(chunks)

	if collection.count() > 0:
		collection.delete(where = {"source": filename})

	collection.upsert(
		ids = [f"{filename}_{i}" for i in range(len(chunks))],
		embeddings = [e["embedding"] for e in embedded],
		documents = chunks,
		metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))],
	)

	print(f"Ingested {len(chunks)} chunks from {filename}")


def main():
	if len(sys.argv) < 2:
		print("Usage: python ingest.py <file_or_directory>")
		sys.exit(1)

	target = Path(sys.argv[1])
	collection = client.get_or_create_collection(name = "documents")

	if target.is_file():
		ingest_file(collection, str(target))
	elif target.is_dir():
		files = [f for f in target.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]
		if not files:
			print(f"No supported files found in {target}")
			sys.exit(0)
		for f in files:
			ingest_file(collection, str(f))
	else:
		print(f"Path not found: {target}")
		sys.exit(1)

	print(f"\nTotal vectors in collection: {collection.count()}")

if __name__ == '__main__':
	main()
