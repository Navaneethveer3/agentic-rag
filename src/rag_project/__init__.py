import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from agents.rag_agent import load_agent
from states.agent_state import AgentState
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from build_graph import build_graph
from memory.chat_manager import *
from langgraph.checkpoint.postgres import PostgresSaver
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

def main() -> None:
    print("Hello from rag-project!")


agent = load_agent()

@contextmanager
def load_connection():
    with PostgresSaver.from_conn_string(DB_URL) as checkpoint:
        checkpoint.setup()
        yield checkpoint



    
def ask_agent(username : str, query : str, config : dict):
    initial_state : AgentState = {
        "username" : username,
        "question" : query,
        "current_query" : query,
        "messages" : [HumanMessage(query)],
        "kb_docs" : [],
        "web_results" : "",
        "kb_grade" : "",
        "web_grade" : "",
        "answer" : "",
        "source_used" : "",
        "retry_count" : 0,
    }

    with load_connection() as checkpoint:
        graph = build_graph(checkpoint)

        response = graph.invoke(initial_state, config=config)

        print("\n"+"="*100)

        print(f"\nQuestion : {query}")
        print(f"\nSource used : {response["source_used"]}")
        print(f"\nAnswer : {response["answer"]}")

        print("\n"+"="*100)

        print("\n\n\n")

        context = response.get("context", {})
        running_summary = context.get("running_summary") if context else None

        if running_summary:
            print(f"Summary : {running_summary.summary}")
        else:
            print("Summary : not yet generated")

        return response


username = "tester1"
title = "Peronal idea imporvements"

thread_id = "67c1d7fa-3857-480b-ae14-6611ed3fee8d"

config = {
    "configurable" : {
        "thread_id" : thread_id
    }
}

query = "greet me"

result = ask_agent(username, query, config=config)