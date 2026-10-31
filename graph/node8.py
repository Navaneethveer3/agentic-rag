import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from agents.rag_agent import load_model
from langchain.messages import AIMessage


def generate_from_web(state : AgentState):
    model = load_model(state["model_name"] if state["model_name"] is not None else None)

    question = state["question"]
    web_context = state["web_results"]

    answer = model.invoke(f"""
    You are a technical instructor.

    The private KB was insufficient, so web search was used.

    Answer using ONLY the web search context.

    Rules:
    - Beginner-friendly explanation.
    - Do not invent unsupported details.
    - Mention that the answer is based on Tavily web search.
    - Include source type: Web Search.
    - If URLs are present in context, include the most useful URLs.

    Question:
    {question}

    Web search context:
    {web_context}
    """).content

    print("---ANSWERING FROM WEB---")

    return {
        "answer" : answer,
        "source_used" : "web_search",
        "messages" : [AIMessage(answer)]
    }

