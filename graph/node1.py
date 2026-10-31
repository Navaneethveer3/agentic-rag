import sys
import re
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.route_decision import RouteDecision
from states.agent_state import AgentState
from agents.rag_agent import load_model



def route_question(state : AgentState):
    question = state["question"]

    # Deterministic check: If the message contains a web URL, immediately route to tools
    url_pattern = r"https?://[^\s]+"
    if re.search(url_pattern, question):
        print("URL detected in question -> Routing directly to TOOLS\n\n")
        return {
            "current_query": question,
            "source_used": "tools",
        }

    model = load_model(state["model_name"] if state["model_name"]!=None else None)

    router_model = model.with_structured_output(RouteDecision, method="json_mode")

    decision = router_model.invoke(f"""
    You are a router for an Agentic RAG pipeline.
    - Route to "direct" for greetings, chitchat, or simple general logic.
    - Route to "kb" for questions about our private knowledge base, internal docs, or any document kind of information.
    - Route to "web" for real-time info, current events, market statistics, startup valuation data, or general web topics.
    - Route to "tools" if the user has given web url or set of urls.
    Question: {question}
    Return response as valid JSON:
    Example: {{"route": "web"}}
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
    elif state["source_used"]=="web":
        print("Decision routed : WEB\n\n")
        return "search_web"
    elif state["source_used"]=="tools":
        print("Decision routed : TOOLS\n\n")
        return "use_tools"
    else:
        print("Decision routed : DIRECT\n\n")
        return "direct_answer"
