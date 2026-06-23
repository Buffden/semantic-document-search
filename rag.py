import sys
from search import search
from generate import generate_answer, NO_ANSWER_PHRASE

TOP_K = 5


def _print_result(result: dict) -> None:
	print("\nAnswer:")
	print(result["answer"])

	if result["sources"]:
		print("\nSources:")
		for source in result["sources"]:
			preview = source["text"][:120].replace("\n", " ")
			print(f"  [{source['index']}] {source['source']} (chunk {source['chunk_index']}): \"{preview}...\"")


def run(question: str) -> None:
	chunks = search(question, top_k = TOP_K)

	if not chunks:
		print("No documents found in the collection. Run ingest.py first.")
		return

	result = generate_answer(question, chunks)

	if result["answer"].strip() == NO_ANSWER_PHRASE:
		print("\nNo answer found in the documents.")
		return

	_print_result(result)


def main():
	if len(sys.argv) > 1:
		question = " ".join(sys.argv[1:])
	else:
		question = input("Enter your question: ").strip()

	if not question:
		print("Error: question cannot be empty.")
		sys.exit(1)

	run(question)


if __name__ == "__main__":
	main()
