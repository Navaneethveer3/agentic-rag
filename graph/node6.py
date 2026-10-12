import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from agents.rag_agent import load_model

model = load_model()

def rewrite_query(state : AgentState):
    question = state["question"]
    retry_count = state["retry_count"]+1

    rewritten = model.invoke(f"""
    Rewrite the question for better retrieval and web search.

    Rules:
    - Preserve original intent.
    - Make it specific and search-friendly.
    - Do not answer.
    - Return only the rewritten query.

    Original question:
    {question}
    """).content.strip()

    print("---QUERY REWRITTEN---")

    return {
        "current_query" : rewritten,
        "retry_count" : retry_count
    }
