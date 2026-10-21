from langchain_core.documents import Document
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.text_splitter import text_splitter
from rag.vector_db import load_vector_store

def embed_documents(username : str, documents : List[Document]):
    splitter = text_splitter()
    
    chunks = splitter.split_documents(documents)

    vector_store = load_vector_store(username)[0]

    vector_store.add_documents(documents=chunks)

    print("Documents chunked successfully\n\n")

    return chunks