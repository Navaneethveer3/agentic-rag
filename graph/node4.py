import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from tools.tavily_web_search import web_search


def search_web(state : AgentState):
    query = state["current_query"]

    result = web_search(query)

    print("---WEB SEARCH INVOKED---")

    return {
        "web_results" : result,
        "source_used" : "web"
    }