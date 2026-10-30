from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import time
import os
from dotenv import load_dotenv
from rag.embeddings import load_embedding_model

load_dotenv()

INDEX_NAME = "agentic-rag-kb"
NAMESPACE = "agentic-rag-"

_pc = None
_embeddings = None
_index_ensured = False

def get_pc():
    global _pc
    if _pc is None:
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set")
        _pc = Pinecone(api_key=api_key)
    return _pc

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = load_embedding_model()
    return _embeddings

def ensure_index():
    global _index_ensured
    if _index_ensured:
        return
    pc = get_pc()
    try:
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
        _index_ensured = True
    except Exception as e:
        print(f"Warning: Could not verify Pinecone index: {e}")

def load_vector_store(username: str):
    ensure_index()
    pc = get_pc()
    embeddings = get_embeddings()
    namespace = f"{NAMESPACE}{username}"
    index = pc.Index(INDEX_NAME)
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace=namespace,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 10,
            "namespace": namespace,
        }
    )

    return [vector_store, retriever]
