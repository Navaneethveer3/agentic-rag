import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from agents.rag_agent import load_model

model = load_model()

def direct_answer(state : AgentState):
    question = state["question"]

    answer = model.invoke(f"""
    Respond briefly and naturally.

    Message:
    {question}
    """).content

    print("---ANSWERING DIRECTLY---")

    return {
        "answer" : answer,
        "source_used" : "direct"
    }