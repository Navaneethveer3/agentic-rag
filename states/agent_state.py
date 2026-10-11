from typing_extensions import TypedDict
from typing import List
from langchain_core.documents import Document


class AgentState(TypedDict):
    question : str
    current_query : str
    kb_docs : List[Document]
    web_results : str
    kb_grade : str
    web_grade : str
    answer : str
    source_used : str
    retry_count : int