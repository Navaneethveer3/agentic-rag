import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from agents.rag_agent import load_agent
from states.agent_state import AgentState
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from build_graph import build_graph


def main() -> None:
    print("Hello from rag-project!")


agent = load_agent()

graph = build_graph()

def chat_with_agent(username : str, query : str):

    system_prompt = f"""
                    You are a helpful helpdesk agent.
                    You have access to tools to retrieve information and answer user queries.
                    You have username : {username} to perform certain tools that require username.
                    Strictly answer with what information and tools you have.
                    Never try to answer on your own.
                    If you don't know the answer, just tell 'I don't have enough information'
                    """
    messages = [
        SystemMessage(system_prompt),
        HumanMessage(query)
    ]

    response = agent.invoke({"messages" : messages})

    final_response = response["messages"][-1]
    final_response.pretty_print()

    return final_response
    
def ask_agent(query : str):
    initial_state : AgentState = {
        "username" : "tester1",
        "question" : query,
        "current_query" : query,
        "kb_docs" : [],
        "web_results" : "",
        "kb_grade" : "",
        "web_grade" : "",
        "answer" : "",
        "source_used" : "",
        "retry_count" : 0,
    }

    response = graph.invoke(initial_state)

    print("\n"+"="*100)

    print(f"\nQuestion : {query}")
    print(f"\nSource used : {response["source_used"]}")
    print(f"\nAnswer : {response["answer"]}")

    print("\n"+"="*100)

    

    return response



result = ask_agent("Hi, how do I manage short term memory in LangGraph?")