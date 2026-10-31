from langchain_core.messages import AIMessage
from states.agent_state import AgentState
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.rag_agent import load_model


def generate_from_tools(state : AgentState):
    model = load_model(state["model_name"] if state.get("model_name") is not None else None)

    question = state.get("question", "")
    kb_docs = state.get("kb_docs", []) or []

    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'Web URL')}]\n{doc.page_content}"
        for doc in kb_docs
    )

    if not context.strip():
        context = "No content could be retrieved from the specified URL."

    answer = model.invoke(f"""
    You are a technical instructor and helpful assistant.

    Answer the user request using ONLY the web URL context provided below.

    Rules:
    - If the user asked a specific question, answer it clearly and thoroughly using the context.
    - If the user submitted a URL or asked for a summary, provide a comprehensive, well-structured summary of the webpage including its main concepts, key features, and practical takeaways.
    - Format your answer in clean GitHub Markdown with clear sections, bullet points, and code snippets where relevant.
    - Do not invent unsupported details.
    - At the end, include the Source URL(s) cited.

    User Question / Intent:
    {question}

    Web URL Context:
    {context}
    """).content

    print("---ANSWERING FROM TOOLS---")

    return {
        "answer" : answer,
        "source_used" : "tools",
        "messages" : [AIMessage(answer)],
    }
