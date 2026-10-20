import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "rag_project"))


from dotenv import load_dotenv
from build_graph import build_graph
from langsmith.evaluation import evaluate
from langchain.messages import HumanMessage
from agents.rag_agent import load_model


load_dotenv()

eval_llm = load_model()

graph = build_graph()


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
        "messages": [HumanMessage(content=question)],
        "kb_docs": [],
        "web_results": "",
        "kb_grade": "",
        "web_grade": "",
        "answer": "",
        "source_used": "",
        "retry_count": 0,
    })

    answer = result.get("answer","")

    return {
        "answer" : answer
    }


def qa_correctness_evaluator(run, example) -> dict:
    """
    LLM-as-a-judge: Evaluates if the predicted answer is factually
    consistent and conveys the key points of the reference answer.
    """
    question = example.inputs.get("question", "")
    expected = example.outputs.get("answer", "")
    predicted = run.outputs.get("answer", "")
    prompt = f"""You are an expert evaluator assessing a RAG system's response.
    Question: {question}
    Expected Reference Answer: {expected}
    Agent Predicted Answer: {predicted}
    Does the Agent Predicted Answer accurately cover the factual points from the Expected Answer?
    Answer with ONLY:
    SCORE: 1 (if correct and factually accurate)
    or
    SCORE: 0 (if incorrect, incomplete, or contradicts reference)
    REASON: <1 sentence rationale>
    """
    response = eval_llm.invoke(prompt).content
    response_text = clean_text(response)
    score = 1 if "SCORE: 1" in response_text else 0
    return {
        "key": "correctness",
        "score": score,
        "comment": response_text
    }



if __name__=="__main__":
    results = evaluate(
        target,
        data="agentic-rag-system-test-v1",
        evaluators=[qa_correctness_evaluator],
        experiment_prefix="agentic-rag-system-baseline",
        description=(
            "Baseline evaluation of my Gemini-powered "
            "LangGraph Agentic RAG."
        ),
        max_concurrency=1,
    )

    print("Experiment done.")
    print(results)