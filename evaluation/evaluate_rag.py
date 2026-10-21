import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "rag_project"))


from dotenv import load_dotenv
from build_graph import build_graph
from langsmith.evaluation import evaluate
from langchain.messages import HumanMessage
from agents.rag_agent import load_model
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT


load_dotenv()

eval_llm = load_model()

graph = build_graph(include_summarizer=False)

correctness_judge = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    model="google_genai:gemini-3.1-flash-lite",
    feedback_key="answer_correctness",
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
        "messages": [HumanMessage(content=question)],
        "kb_docs": [],
        "web_results": "",
        "kb_grade": "",
        "web_grade": "",
        "answer": "",
        "source_used": "",
        "retry_count": 0,
    })

    time.sleep(2)

    answer = clean_text(result.get("answer",""))

    return {
        "answer" : answer
    }


def qa_correctness_evaluator(inputs : dict, outputs : dict, reference_outputs : dict) -> dict:
    """
    LLM-as-a-judge: Evaluates if the predicted answer is factually
    consistent and conveys the key points of the reference answer.
    """
    return correctness_judge(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs,
    )




if __name__=="__main__":
    results = evaluate(
        target,
        data="agentic-rag-system-test-v1",
        evaluators=[qa_correctness_evaluator],
        experiment_prefix="agentic-rag-system-baseline-v1",
        description=(
            "Baseline evaluation of my Gemini-powered LLM-as-a-Judge "
            "Semantic correctness"
        ),
        max_concurrency=1,
    )

    print("Evaluation done.")
    print(results)