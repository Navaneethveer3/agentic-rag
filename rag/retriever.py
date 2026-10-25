import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.vector_db import load_vector_store

retriever = load_vector_store("tester1")[1]

question = (
                "Deep-ocean exploration helps scientists discover "
                "unknown marine species, study underwater ecosystems, "
                "understand geological processes, and learn more "
                "about Earth's oceans."
            )

docs = retriever.invoke(question)

for i, doc in enumerate(docs, start=1):
    print(f"\n--- Document {i} ---")
    print("Document Id : ", doc.id)
    print("\nPage content : ", doc.page_content)