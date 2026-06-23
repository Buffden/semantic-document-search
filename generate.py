from openai import OpenAI
from dotenv import load_dotenv
import tiktoken
import os

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

GENERATION_MODEL = os.getenv("GENERATION_MODEL", "gpt-4o-mini")
TOKEN_BUDGET = int(os.getenv("TOKEN_BUDGET", "2000"))
NO_ANSWER_PHRASE = "I don't know based on the provided documents."

_PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


def _load_prompt(filename: str) -> str:
	path = os.path.join(_PROMPTS_DIR, filename)
	with open(path) as f:
		return f.read().strip()


_SYSTEM_PROMPT = _load_prompt("system_prompt.txt")


def _count_tokens(text: str) -> int:
	enc = tiktoken.get_encoding("cl100k_base")
	return len(enc.encode(text))


def _select_chunks_within_budget(chunks: list[dict], budget: int) -> list[dict]:
	selected = []
	tokens_used = 0

	for chunk in chunks:
		chunk_tokens = _count_tokens(chunk["text"])
		if tokens_used + chunk_tokens > budget:
			continue
		selected.append(chunk)
		tokens_used += chunk_tokens

	return selected


def _build_context_block(chunks: list[dict]) -> str:
	lines = []
	for i, chunk in enumerate(chunks, start = 1):
		lines.append(f"[{i}] Source: {chunk['source']} (chunk {chunk['chunk_index']})")
		lines.append(chunk["text"])
		lines.append("")
	return "\n".join(lines)


def generate_answer(question: str, chunks: list[dict]) -> dict:
	selected_chunks = _select_chunks_within_budget(chunks, TOKEN_BUDGET)

	if not selected_chunks:
		return {
			"answer": NO_ANSWER_PHRASE,
			"sources": []
		}

	context_block = _build_context_block(selected_chunks)
	user_message = f"Context:\n{context_block}\nQuestion: {question}"

	response = client.chat.completions.create(
		model = GENERATION_MODEL,
		messages = [
			{"role": "system", "content": _SYSTEM_PROMPT},
			{"role": "user", "content": user_message}
		],
		temperature = 0.0
	)

	answer = response.choices[0].message.content.strip()

	sources = [
		{
			"index": i + 1,
			"source": chunk["source"],
			"chunk_index": chunk["chunk_index"],
			"text": chunk["text"]
		}
		for i, chunk in enumerate(selected_chunks)
	]

	return {
		"answer": answer,
		"sources": sources
	}
