import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.route_decision import RouteDecision
from states.agent_state import AgentState
from agents.rag_agent import load_model


model = load_model()

router_model = model.with_structured_output(RouteDecision, method="json_mode")

def route_question(state : AgentState):
    question = state["question"]

    decision = router_model.invoke(f"""
    you are a router for an Agentic RAG pipeline.

    if the question is simple/general/regular route to "direct"
    else route to "kb"

    question : {question}

    return response as valid JSON.
    Example :
    {{"route" : "kb"}}

    """
    )

    print("LLM STARTED\n\n")

    return {
        "current_query" : question,
        "source_used" : decision.route
    }


def route_after_decision(state : AgentState):
    if state["source_used"]=="kb":
        print("Decision routed : KB\n\n")
        return "retrieve_kb"
    else:
        print("Decision routed : DIRECT\n\n")
        return "direct_answer"