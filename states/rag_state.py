from typing_extensions import TypedDict
from typing import List, Annotated
from langchain_core.documents import Document


class RagState(TypedDict):
    username : str
    question : str
    current_query : str
    kb_docs : List[Document]
    answer : str