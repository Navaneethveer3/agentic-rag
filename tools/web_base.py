from states.agent_state import AgentState
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from rag.vector_db import load_vector_store
from rag.text_splitter import text_splitter


load_dotenv()


def search_web_url(state : AgentState):
    """Web url search to retrieve data.
       This tool retrieves the information from the web and stores it in database.
    """

    question = state["question"]

    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, question)

    # If no URLs detected, return gracefully
    if not urls:
        return {
            "question": question,
            "current_query": question,
            "kb_docs": [],
            "source_used": "tools",
        }

    # Remove the URLs from the question to get the user's actual question / intent
    clean_question = re.sub(url_pattern, "", question).strip()
    rewritten_question = re.sub(r"\s+", " ", clean_question).strip()

    # If the user only provided a URL with no question, set intent to summarizing the webpage
    if not rewritten_question:
        rewritten_question = "Summarize the key information, main concepts, and takeaways from this page."

    username = state["username"]

    loader = WebBaseLoader(
        web_paths=tuple(urls),
        requests_kwargs = {
            "headers" :{
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Agentic-RAG-Demo"
            }
        },
    )
    raw_docs = loader.load()

    splitter = text_splitter()
    chunks = splitter.split_documents(raw_docs)

    vector_store = load_vector_store(username)[0]
    vector_store.add_documents(documents=chunks)

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k" : 5,
            "filter": {
                "source" : {"$in": urls}
            }
        }
    )

    docs = retriever.invoke(rewritten_question)

    print("chunks loaded successfully\n\n")

    return {
        "question" : rewritten_question,
        "current_query" : rewritten_question,
        "kb_docs" : docs,
        "source_used" : "tools",
    }
