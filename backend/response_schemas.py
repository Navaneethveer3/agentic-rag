from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CreateChatRequest(BaseModel):
    title: str = Field(default="New Chat", description="Title of the new conversation")

class UpdateChatRequest(BaseModel):
    title: str = Field(..., description="Updated title for the conversation")

class ChatResponse(BaseModel):
    thread_id: str
    username: str
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MessageRequest(BaseModel):
    query: str = Field(..., description="User query / prompt for the agent")
    model_name: Optional[str] = Field(default=None, description="Optional override for LLM model")

class MessageResponse(BaseModel):
    thread_id: str
    question: str
    source_used: str
    answer: str
    summary: Optional[str] = None