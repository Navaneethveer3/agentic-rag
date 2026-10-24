import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.vector_db import load_vector_store

retriever = load_vector_store("tester1")[1]

question = (
                "How does international cooperation help address climate "
                "change, and how does the Paris Agreement contribute "
                "to this effort?"
            )

docs = retriever.invoke(question)

for i, doc in enumerate(docs, start=1):
    print(f"\n--- Document {i} ---")
    print("Document Id : ", doc.id)
    print("\nPage content : ", doc.page_content)