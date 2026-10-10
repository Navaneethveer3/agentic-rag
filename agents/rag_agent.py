import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools.web_base import search_web_base
from tools.kb_search import search_knowledge_base


load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    thinking_level="low"
)

tools = [
    search_web_base,
    search_knowledge_base
]

agent = create_agent(
    model=model,
    tools=tools
)

def load_agent():
    return agent