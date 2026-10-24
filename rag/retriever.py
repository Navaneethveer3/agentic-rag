import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.vector_db import load_vector_store

retriever = load_vector_store("tester1")[1]

question = (
                "How can semantic search be used to retrieve relevant memories from a LangGraph store, "
                "and what role do embeddings and similarity search play in finding those memories?"
            )

docs = retriever.invoke(question)

for i, doc in enumerate(docs, start=1):
    print(f"\n--- Document {i} ---")
    print("Document Id : ", doc.id)
    print("\nPage content : ", doc.page_content)