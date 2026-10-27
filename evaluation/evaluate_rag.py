from langchain_core.prompts import prompt
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "rag_project"))


from dotenv import load_dotenv
from build_graph import build_graph
from graph.rag_test_graph import build_rag_graph
from langsmith.evaluation import evaluate
from langchain.messages import HumanMessage, SystemMessage
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT


load_dotenv()

eval_llm = "google_genai:gemini-3.1-flash-lite"

graph = build_rag_graph()

FAITHFULNESS_PROMPT = """
You are evaluating the faithfulness of an answer produced by a
Retrieval-Augmented Generation (RAG) system.

You will receive:
- The user's question
- The generated answer
- The actual retrieved context used by the application

Determine whether the factual claims in the answer are supported
by the retrieved context.

Scoring rules:
- Pass if all material factual claims are supported by the context.
- Fail if any material factual claim contradicts the context or
  introduces unsupported factual information.
- If the context is empty or insufficient to support the answer,
  do not assume that the answer is grounded.
- Judge the evidence in the context, not whether the answer
  sounds plausible from general knowledge.

Question and answer data:
{inputs}
{outputs}
"""

CONTEXT_RELEVANCE_PROMPT = """
You are evaluating the relevance of documents retrieved by a
Retrieval-Augmented Generation system.

You will receive a user question and retrieved context.

Determine whether the retrieved context contains information
that is meaningfully relevant to answering the question.

Pass if the context contains useful evidence or information
that helps answer the question.

Fail if the context is empty, entirely irrelevant, or unrelated
to the question.

Do not judge the generated answer.
Do not use outside knowledge to assume that retrieval succeeded.

Question:
{question}

Retrieved context:
{context}
"""

IMPROVED_PROMPT = """
Answer the question using the retrieved context.

- Use evidence from the context.
- Do not invent unsupported facts.
- If the context is insufficient, say so clearly.
- Answer the question directly.
"""

correctness_judge = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    model=eval_llm,
    feedback_key="answer_correctness",
)

faithfulness_judge = create_llm_as_judge(
    prompt=FAITHFULNESS_PROMPT,
    model=eval_llm,
    feedback_key="faithfulness",
)

context_relevance_judge = create_llm_as_judge(
    prompt=CONTEXT_RELEVANCE_PROMPT,
    model=eval_llm,
    feedback_key="context_relevance",
)


def clean_text(content) -> str:
    """Extracts pure text from string, list of dicts, or message objects."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    return str(content).strip() if content is not None else ""



def target(inputs : dict)->dict:
    
    question = inputs["question"]

    result = graph.invoke({
        "question": question,
        "current_query": question,
        "username": "tester1",
        # "messages": [SystemMessage(IMPROVED_PROMPT),
        # HumanMessage(content=question)],
        "kb_docs": [],
        # "web_results": "",
        # "kb_grade": "",
        # "web_grade": "",
        "answer": "",
        # "source_used": "",
        # "retry_count": 0,
    })


    answer = clean_text(result.get("answer",""))
    docs = result.get("kb_docs",[])

    context = [
        doc.page_content if hasattr(doc, "page_content")
        else str(doc)
        for doc in docs
    ]

    retrieved_doc_ids = [
        doc.id for doc in docs if hasattr(doc, "id") and doc.id is not None
    ]

    return {
        "answer" : answer,
        "context" : context,
        "retrieved_doc_ids" : retrieved_doc_ids,
    }


def correctness_evaluator(inputs : dict, outputs : dict, reference_outputs : dict) -> dict:
    """
    LLM-as-a-judge: Evaluates if the predicted answer is factually
    consistent and conveys the key points of the reference answer.
    """
    return correctness_judge(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs,
    )


def faithfulness_evaluator(inputs : dict, outputs : dict) -> dict:
    return faithfulness_judge(
        inputs=inputs,
        outputs=outputs,
    )


def context_relevance_evaluator(inputs : dict, outputs : dict) -> dict:
    return context_relevance_judge(
        question = inputs.get("question",""),
        context = "\n\n".join(outputs.get("context",[])) or "No context retrieved.",
    )

def retrieval_metrics_evaluator(outputs : dict, reference_outputs : dict) -> dict:
    retrieved = set(outputs.get("retrieved_doc_ids", []))
    expected = set(reference_outputs.get("retrieved_doc_ids", []))

    if not expected:
        return [
            {
                "key" : "precision", "score" : 1.0 if not retrieved else 0.0
            },
            {
                "key" : "recall", "score" : 1.0 if not retrieved else 0.0
            },
            {
                "key" : "f1-score", "score" : 1.0 if not expected else 0.0
            }
        ]
    
    true_positives = len(retrieved & expected)

    precision = true_positives/len(retrieved) if retrieved else 0.0
    recall = true_positives/len(expected) if expected else 0.0
    f1_score = (2*precision*recall/(precision+recall)) if (precision+recall)>0 else 0.0

    return [
        {
            "key" : "precision", "score" : round(precision,4)
        },
        {
            "key" : "recall", "score" : round(recall, 4)
        },
        {
            "key" : "f1-score", "score" : round(f1_score, 4)
        },
    ]


if __name__=="__main__":
    results = evaluate(
        target,
        data="agentic-rag-system-retrieval-metrics-v5",
        evaluators=[retrieval_metrics_evaluator],
        experiment_prefix="agentic-rag-system-retrieval-metrics-v5",
        description=(
            "Testing the retrieval metrics of RAG system with "
            "the version-5 dataset. Metrics include "
            "precision, recall, and f1-score."
        ),
        max_concurrency=1,
    )

    print("Evaluation done.")
    print(results)