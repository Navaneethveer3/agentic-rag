import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from agents.rag_agent import load_agent
from states.agent_state import AgentState
from langchain.messages import HumanMessage
from build_graph import build_graph
from memory.chat_manager import *
from langgraph.checkpoint.postgres import PostgresSaver
from contextlib import contextmanager
from auth.entra_auth import login_with_entra
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

def main() -> None:
    print("Hello from rag-project!")

_checkpoint_setup_done = False

@contextmanager
def load_connection():
    global _checkpoint_setup_done
    with PostgresSaver.from_conn_string(DB_URL) as checkpoint:
        if not _checkpoint_setup_done:
            try:
                checkpoint.setup()
                _checkpoint_setup_done = True
            except Exception as e:
                print(f"Checkpoint setup notice: {e}")
        yield checkpoint


def ask_agent(username : str, query : str, config : dict, model_name : str = None):
    initial_state : AgentState = {
        "model_name" : model_name,
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

        print(f"\nQuestion : {response['question']}")
        print(f"\nSource used : {response['source_used']}")
        print(f"\nAnswer : {response['answer']}")

        print("\n"+"="*100)

        print("\n\n\n")

        context = response.get("context", {})
        running_summary = context.get("running_summary") if context else None

        if running_summary:
            print(f"Summary : {running_summary.summary}")
        else:
            print("Summary : not yet generated")

        return response


if __name__=="__main__":
    user = login_with_entra()
