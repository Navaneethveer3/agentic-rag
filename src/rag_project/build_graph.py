import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from langgraph.graph import StateGraph, START, END
from memory.summarizer import load_summarizer
from states.agent_state import AgentState
from graph.node1 import route_question, route_after_decision
from graph.node2 import retrieve_kb
from graph.node3 import grade_kb_evidence, decide_after_kb_grade
from graph.node4 import search_web
from graph.node5 import grade_web_evidence, decide_after_web_grade
from graph.node6 import rewrite_query
from graph.node7 import generate_from_kb
from graph.node8 import generate_from_web
from graph.node9 import direct_answer
from graph.node10 import answer_insufficient


def build_graph(checkpointer=None):

    summarizer = load_summarizer()

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("summarizer", summarizer)
    workflow.add_node("route_question", route_question)
    workflow.add_node("retrieve_kb", retrieve_kb)
    workflow.add_node("grade_kb_evidence", grade_kb_evidence)
    workflow.add_node("search_web", search_web)
    workflow.add_node("grade_web_evidence", grade_web_evidence)
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("direct_answer", direct_answer)
    workflow.add_node("answer_insufficient", answer_insufficient)
    workflow.add_node("generate_from_kb", generate_from_kb)
    workflow.add_node("generate_from_web", generate_from_web)

    # Edges
    workflow.add_edge(START, "summarizer")
    workflow.add_edge("summarizer", "route_question")
    
    workflow.add_conditional_edges("route_question", route_after_decision,{
        "retrieve_kb" : "retrieve_kb",
        "direct_answer" : "direct_answer",
        "search_web" : "search_web"
    })

    workflow.add_edge("retrieve_kb", "grade_kb_evidence")

    workflow.add_conditional_edges("grade_kb_evidence", decide_after_kb_grade, {
        "generate_from_kb" : "generate_from_kb",
        "search_web" : "search_web"
    })

    workflow.add_edge("search_web", "grade_web_evidence")

    workflow.add_conditional_edges("grade_web_evidence", decide_after_web_grade, {
        "generate_from_web" : "generate_from_web",
        "rewrite_query" : "rewrite_query",
        "answer_insufficient" : "answer_insufficient"
    })

    workflow.add_edge("rewrite_query", "retrieve_kb")

    workflow.add_edge("generate_from_kb", END)
    workflow.add_edge("generate_from_web", END)
    workflow.add_edge("direct_answer", END)
    workflow.add_edge("answer_insufficient", END)

    graph = workflow.compile(checkpointer=checkpointer)

    return graph
