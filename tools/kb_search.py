import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.vector_db import load_vector_store
from langchain.tools import tool


def search_knowledge_base(query : str):
    retriever = load_vector_store("tester1")[1]

    docs = retriever.invoke(query)
    return docs


docs = search_knowledge_base("common solutions in short term memory")

for doc in docs:
    print("\n\n")
    print(doc.page_content)