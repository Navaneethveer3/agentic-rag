import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.rag_agent import load_model
from states.agent_state import AgentState
from langchain.messages import AIMessage



def generate_from_kb(state : AgentState):
    model = load_model(state["model_name"] if state["model_name"] is not None else None)

    question = state["question"]

    context = "\n\n".join(
        f"[KB Source : {doc.metadata.get("source")}]\n{doc.page_content}"
        for doc in state["kb_docs"]
    )

    answer = model.invoke(f"""
    You are a technical instructor.

    Answer using ONLY the private KB context.

    Rules:
    - Beginner-friendly explanation.
    - Do not invent unsupported details.
    - Mention that the answer is based on the private KB.
    - Include source type: Private KB.

    Question:
    {question}

    Private KB context:
    {context}
    """).content

    print("---ANSWERING FROM KNOWLEDGE BASE---")

    return {
        "answer" : answer,
        "source_used" : "private_kb",
        "messages" : [AIMessage(answer)]
    }