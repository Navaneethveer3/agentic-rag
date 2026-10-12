import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from rag.vector_db import load_vector_store


def retrieve_kb(state : AgentState):

    retriever = load_vector_store(state["username"])[1]
    query = state["current_query"]
    docs = retriever.invoke(query)

    print("---DOCUMENTS RETRIEVED---\n\n")
    return {"kb_docs" : docs}