import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import tool
from rag.vector_db import load_vector_store
from rag.text_splitter import text_splitter
import asyncio


load_dotenv()

@tool
def search_web_base(url : list[str]):
    """web url search to retrieve data"""
    loader = WebBaseLoader(
        web_paths=tuple(url),
        requests_kwargs = {
            "headers" :{
                "User-Agent" : "Mozilla/5.0 Agentic-RAG-Industry-Demo"
            }
        },
    )
    raw_docs = loader.load()
    raw_data = [doc.page_content for doc in raw_docs]

    # splitter = text_splitter()

    # chunks = splitter.split_documents(raw_docs)

    # vector_store = load_vector_store("tester1")[0]

    # vector_store.add_documents(documents=chunks)

    print("chunks loaded successfully")

    return raw_data

urls = ["https://docs.langchain.com/oss/python/langgraph/overview", 
        "https://docs.langchain.com/oss/python/langgraph/add-memory",
        "https://docs.langchain.com/oss/python/langgraph/use-subgraphs"]


search_web_base(urls)