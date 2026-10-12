import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from rag.vector_db import load_vector_store

retriever = load_vector_store()[1]

def retrieve_kb(state : AgentState):
    query = state["current_query"]
    docs = retriever.invoke(query)

    return {"kb_docs" : docs}