import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.tools import tool

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

search = TavilySearch(max_results=3)

@tool
def search_web(query : str):
    """search web without url"""

    response = search.invoke({"query" : query})

    return str(response)