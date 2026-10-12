import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.tools import tool

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

search = TavilySearch(max_results=3,
include_answer=True,
include_raw_content=False,
)

# @tool
def web_search(query : str):
    """search web without url"""

    response = search.invoke({"query" : query})

    return str(response)