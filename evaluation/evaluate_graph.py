import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "rag_project"))

from dotenv import load_dotenv
from build_graph import build_graph
from langchain.messages import HumanMessage
from agentevals.graph_trajectory.utils import extract_langgraph_trajectory_from_thread
from agentevals.graph_trajectory.llm import create_graph_trajectory_llm_as_judge
from langgraph.checkpoint.memory import InMemorySaver
from langsmith import evaluate
from evaluation.evaluate_rag import target, clean_text

load_dotenv()

eval_llm = "google_genai:gemini-3.1-flash-lite"

checkpointer = InMemorySaver()

graph = build_graph(include_summarizer=False)

config = {
    "configurable" : {
        "thread_id" : "trajectory-test-1"
    }
}

question = "tell me about the management of checkpoints."

# initial_state = {
#         "question": question,
#         "current_query": question,
#         "username": "tester1",
#         "messages": [HumanMessage(content=question)],
#         "kb_docs": [],
#         "web_results": "",
#         "kb_grade": "",
#         "web_grade": "",
#         "answer": "",
#         "source_used": "",
#         "retry_count": 0,
#     }

# results = graph.invoke(initial_state, config)

# trajectory = extract_langgraph_trajectory_from_thread(
#     graph,
#     config
# )

# def serialize_for_eval(obj):
#     if isinstance(obj, dict):
#         return {k: serialize_for_eval(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [serialize_for_eval(item) for item in obj]
#     elif hasattr(obj, "content"):  
#         return {"role": getattr(obj, "type", "message"), "content": obj.content}
#     elif hasattr(obj, "page_content"): 
#         return {"content": obj.page_content, "metadata": getattr(obj, "metadata", {})}
#     return obj

# trajectory_judge = create_graph_trajectory_llm_as_judge(
#     model=eval_llm,
# )

# evaluation = trajectory_judge(
#     inputs=serialize_for_eval(trajectory["inputs"]),
#     outputs=serialize_for_eval(trajectory["outputs"]),
# )

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
    }, config)


    answer = clean_text(result.get("answer",""))
    docs = result.get("kb_docs",[])

    context = [
        doc.page_content if hasattr(doc, "page_content")
        else str(doc)
        for doc in docs
    ]

    return {
        "answer" : answer,
        "context" : context,
        "route" : result.get("source_used", ""),
    }

def routing_evaluator(outputs : dict, reference_outputs : dict) -> dict:
    predicted_route = outputs.get("route", "")
    expected_route = reference_outputs.get("route", "")

    return {
        "key" : "routing_accuracy",
        "score" : predicted_route==expected_route,
    }

results = evaluate(
    target,
    data="agentic-rag-system-test-trajectory-v3",
    evaluators=[routing_evaluator],
    experiment_prefix="agentic-rag-routing-v1",
    description="Evaluate KB, web, and direct routing",
    max_concurrency=1,
)

print("\n\nEvaluation done")