from pydantic import BaseModel, Field
from typing import Literal

class RouteDecision(BaseModel):
    route : Literal["kb", "direct", "web", "tools"] = Field("Route to 'kb' for private docs; 'web' for current events/market data/external info; 'direct' for greetings/general chat.")

