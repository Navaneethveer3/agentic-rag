import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import tool

load_dotenv()

@tool
async def search_web_base(url : list[str]):
    """web url search to retrieve data"""
    loader = WebBaseLoader(
        web_paths=tuple(url),
        requests_kwargs = {
            "headers" :{
                "User-Agent" : "Mozilla/5.0 Agentic-RAG-Industry-Demo"
            }
        },
    )
    raw_docs = await loader.aload()
    data = [doc.page_content for doc in raw_docs]
    return data