from pydantic import BaseModel, Field
from typing import Literal

class RouteDecison(BaseModel):
    route : Literal["kb", "direct"] = Field("Use kb for questions needing Agentic RAG docs; direct for greetings/simple chat.")

