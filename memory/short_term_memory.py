import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.rag_agent import load_model
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.utils.uuid import uuid7
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    checkpointer.setup()

    model = load_model()

    def call_model(state : MessagesState):
        response = model.invoke(state["messages"])
        return {"messages" : [response]}

    workflow = StateGraph(MessagesState)

    workflow.add_node("model", call_model)
    workflow.add_edge(START, "model")
    workflow.add_edge("model", END)

    graph = workflow.compile(checkpointer=checkpointer)

    config = {
        "configurable" : {
            "thread_id" : "tester1"
        }
    }

    messages = [
        HumanMessage("Hi, my name is veer.")
    ]

    checkpointer.delete_thread("tester1")

    # response = graph.invoke({"messages" : messages}, config=config)
    # print("Turn 1 :\n")
    # print(response["messages"][-1].content)

    # response = graph.invoke({"messages":[HumanMessage("What is my name?")]}, config=config)
    # print("\nTurn 2 :\n")
    # print(response["messages"][-1].content)