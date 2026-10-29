import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools.web_base import search_web_url
from tools.kb_search import search_knowledge_base
from tools.tavily_web_search import web_search

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

DEFAULT_MODEL_NAME = "gemini-3-flash-preview"


tools = [
    search_web_url,
    search_knowledge_base,
    web_search
]

agent = create_agent(
    model="google_genai:"+DEFAULT_MODEL_NAME,
    tools=tools
)

def load_agent():
    return agent

def load_model(model_name : str = None):
    model = ChatGoogleGenerativeAI(
        model=DEFAULT_MODEL_NAME if model_name is None else model_name,
        thinking_level="low",
        max_retries=2,
    )
    return model