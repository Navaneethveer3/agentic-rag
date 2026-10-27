from states.rag_state import RagState
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from langchain_pinecone import PineconeRerank
from states.agent_state import AgentState
from rag.vector_db import load_vector_store
from dotenv import load_dotenv

load_dotenv()


reranker = PineconeRerank(
        model="bge-reranker-v2-m3",
        top_n=3,
    )

def retrieve_kb(state : AgentState | RagState):

    retriever = load_vector_store(state["username"])[1]
    query = state["current_query"]

    docs = retriever.invoke(query)

    print("---DOCUMENTS RETRIEVED---\n\n")

    print("Before Ranking : \n")

    for i, doc in enumerate(docs, start=1):
        print(f"Document {i} : {doc.id}\n")
    
    print("\n")

    if not docs:
        return {"kb_docs" : []}
    
    doc_id_map = {doc.page_content : doc.id for doc in docs}


    ranked_docs = reranker.compress_documents(
        documents=docs,
        query=query,
    )

    print("Docs after Reranking :\n")

    for i, doc in enumerate(ranked_docs, start=1):
        doc.id = doc_id_map.get(doc.page_content)
        print(f"Reranked document {i} : {doc.id}\n")
    
    print("\n")

    print("---DOCUMENTS RERANKED---\n\n")

    return {"kb_docs" : ranked_docs}