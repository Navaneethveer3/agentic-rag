import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from agents.rag_agent import load_model
from langchain.messages import AIMessage, SystemMessage

model = load_model()

def direct_answer(state : AgentState):
    conversation = state.get("summarized_messages", state.get("messages",[]))

    system_prompt = SystemMessage("Response briefly and naturally\n")

    full_conversation = [system_prompt] + conversation

    answer = model.invoke(full_conversation).content

    print("---ANSWERING DIRECTLY---")

    return {
        "answer" : answer,
        "source_used" : "direct",
        "messages" : [AIMessage(answer)]
    }