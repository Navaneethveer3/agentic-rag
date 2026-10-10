import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.vector_db import load_vector_store
from langchain.tools import tool

@tool
def search_knowledge_base(username : str, query : str):
    """search information from the database"""
    retriever = load_vector_store(username)[1]

    docs = retriever.invoke(query)
    return docs


# docs = search_knowledge_base("common solutions in short term memory")

# for doc in docs:
#     print("\n\n")
#     print(doc.page_content)