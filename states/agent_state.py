from typing_extensions import TypedDict
from typing import List, Annotated, Any
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    model_name : str
    messages : Annotated[List[BaseMessage], add_messages]
    summarized_messages : List[BaseMessage]
    context : dict[str, Any]
    username : str
    question : str
    current_query : str
    kb_docs : List[Document]
    web_results : str
    kb_grade : str
    web_grade : str
    answer : str
    source_used : str
    retry_count : int