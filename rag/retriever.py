import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.vector_db import load_vector_store

retriever = load_vector_store("tester1")[1]

question = (
                "Rhodium prices are influenced by its limited supply, "
                "automotive industry demand, mining production, recycling, "
                "and emissions regulations. These factors can cause "
                "significant price fluctuations."
            )

docs = retriever.invoke(question)

for i, doc in enumerate(docs, start=1):
    print(f"\n--- Document {i} ---")
    print("Document Id : ", doc.id)
    print("\nPage content : ", doc.page_content)