import json
import os
import sys

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search import search
from generate import generate_answer, NO_ANSWER_PHRASE

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATASET_PATH = os.path.join(os.path.dirname(__file__), "golden_dataset.json")
TOP_K = 5


def load_dataset() -> list[dict]:
    with open(DATASET_PATH) as f:
        return json.load(f)


def score_retrieval(chunks: list[dict], source: str) -> int:
    return 1 if source in [chunk["source"] for chunk in chunks] else 0


def score_answer(question: str, expected: str, actual: str) -> int:
    if expected == NO_ANSWER_PHRASE:
        return 5 if actual.strip() == NO_ANSWER_PHRASE else 1

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are evaluating a question-answering system.\n\n"
                    f"Question: {question}\n"
                    f"Expected answer: {expected}\n"
                    f"Actual answer: {actual}\n\n"
                    f"Score the actual answer from 1 to 5:\n"
                    f"5 = correct and complete\n"
                    f"4 = mostly correct, minor omission\n"
                    f"3 = partially correct\n"
                    f"2 = mostly wrong but touches the right topic\n"
                    f"1 = wrong or hallucinated\n\n"
                    f"Return only the integer score. No explanation."
                )
            }
        ]
    )

    return int(response.choices[0].message.content.strip())


def run_eval() -> None:
    dataset = load_dataset()

    retrieval_scores = []
    answer_scores = []

    for i, entry in enumerate(dataset, start=1):
        question = entry["question"]
        expected = entry["expected_answer"]
        source = entry["source"]

        print(f"[{i}/{len(dataset)}] {question}")

        chunks = search(question, top_k=TOP_K)
        result = generate_answer(question, chunks)
        actual = result["answer"].strip()

        r_score = score_retrieval(chunks, source)
        a_score = score_answer(question, expected, actual)

        retrieval_scores.append(r_score)
        answer_scores.append(a_score)

        print(f"  Retrieval: {'pass' if r_score else 'MISS'}  |  Answer score: {a_score}/5")

    total = len(dataset)
    retrieval_recall = sum(retrieval_scores)
    avg_answer = sum(answer_scores) / total

    print("\nEvaluation Results ---")
    print(f"Retrieval recall:   {retrieval_recall}/{total} ({100 * retrieval_recall // total}%)")
    print(f"Answer correctness: {avg_answer:.1f} / 5.0 average")


if __name__ == "__main__":
    run_eval()
