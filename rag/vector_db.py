from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import time
import os
from dotenv import load_dotenv
from rag.embeddings import load_embedding_model

load_dotenv()

INDEX_NAME = "agentic-rag-kb"
NAMESPACE = "agentic-rag-"

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )

    while not pc.describe_index(INDEX_NAME).status["ready"]:
        time.sleep(1)



embeddings = load_embedding_model()



def load_vector_store(username : str):
    namespace = f"{NAMESPACE}{username}"
    index = pc.Index(INDEX_NAME)
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace=namespace,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k" : 3,
            "namespace" : namespace,
        }
    )

    return [vector_store, retriever]

