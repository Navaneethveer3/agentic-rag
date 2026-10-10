import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from agents.rag_agent import load_agent
from langchain.messages import SystemMessage, HumanMessage, ToolMessage

def main() -> None:
    print("Hello from rag-project!")


agent = load_agent()

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
    


query = "can you tell me how to manage short term memory from this https://docs.langchain.com/oss/python/langgraph/add-memory"
chat_with_agent("tester1", query)