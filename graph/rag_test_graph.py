import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from graph.node2 import retrieve_kb
from graph.node7 import generate_from_kb
from langgraph.graph import StateGraph, START, END
from states.rag_state import RagState

def build_rag_graph():

    workflow = StateGraph(RagState)

    workflow.add_node("retrieve_kb", retrieve_kb)
    workflow.add_node("generate_from_kb", generate_from_kb)

    workflow.add_edge(START, "retrieve_kb")
    workflow.add_edge("retrieve_kb", "generate_from_kb")
    workflow.add_edge("generate_from_kb", END)

    graph = workflow.compile()

    return graph

# query = "How to manage short-term memory?"

# initial_state = {
#     "question" : query,
#     "current_query" : query,
#     "username" : "tester1",
#     "answer" : "",
# }

# graph = build_rag_graph()

# graph.invoke(initial_state)