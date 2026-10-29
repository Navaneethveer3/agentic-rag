import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_PATH = PROJECT_ROOT / "src" / "rag_project"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from datetime import datetime
from typing import List
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from memory.chat_manager import (
    create_chat,
    get_chat,
    get_all_chats,
    update_chat,
    delete_chat,
    delete_all_chats,
)
from src.rag_project import ask_agent
from backend.response_schemas import (
    CreateChatRequest, 
    UpdateChatRequest, 
    ChatResponse, 
    MessageRequest, 
    MessageResponse)
from backend.get_user import get_current_user

load_dotenv()


app = FastAPI(
    title="Agentic RAG API",
    description="Production-grade API for Agentic RAG with Azure PostgreSQL and Microsoft Entra ID authentication",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)







@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify API and DB connectivity."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/chats", response_model=ChatResponse, tags=["Chats"])
def api_create_chat(
    req: CreateChatRequest,
    username: str = Depends(get_current_user),
):
    """Creates a new conversation thread for the authenticated user."""
    try:
        chat = create_chat(username=username, title=req.title)
        return ChatResponse(
            thread_id=chat.thread_id,
            username=chat.username,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/chats", response_model=List[ChatResponse], tags=["Chats"])
def api_get_all_chats(
    username: str = Depends(get_current_user),
):
    """Retrieves all conversation threads belonging to the authenticated user."""
    chats = get_all_chats(username=username)
    return [
        ChatResponse(
            thread_id=c.thread_id,
            username=c.username,
            title=c.title,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in chats
    ]


@app.get("/api/chats/{thread_id}", response_model=ChatResponse, tags=["Chats"])
def api_get_chat(
    thread_id: str,
    username: str = Depends(get_current_user),
):
    """Retrieves details of a specific conversation thread."""
    try:
        chat = get_chat(username=username, thread_id=thread_id)
        return ChatResponse(
            thread_id=chat.thread_id,
            username=chat.username,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.patch("/api/chats/{thread_id}", response_model=ChatResponse, tags=["Chats"])
def api_update_chat(
    thread_id: str,
    req: UpdateChatRequest,
    username: str = Depends(get_current_user),
):
    """Updates the title of an existing conversation thread."""
    try:
        chat = update_chat(username=username, thread_id=thread_id, title=req.title)
        return ChatResponse(
            thread_id=chat.thread_id,
            username=chat.username,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.delete("/api/chats/{thread_id}", tags=["Chats"])
def api_delete_chat(
    thread_id: str,
    username: str = Depends(get_current_user),
):
    """Deletes a conversation thread and its associated LangGraph checkpoints."""
    try:
        delete_chat(username=username, thread_id=thread_id)
        return {"message": f"Chat {thread_id} deleted successfully"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

def api_delete_all_chats(username : str = Depends(get_current_user)):
    """Delete all the chats for a user"""
    try:
        delete_all_chats(username)
    except Exception as e:
        raise Exception(e)

@app.post("/api/chats/{thread_id}/messages", response_model=MessageResponse, tags=["Agent"])
def api_send_message(
    thread_id: str,
    req: MessageRequest,
    username: str = Depends(get_current_user),
):
    """
    Sends a question to the Agentic RAG graph within a specific conversation thread.
    Persists history to Azure PostgreSQL checkpointer.
    """
    # Verify ownership of the chat
    try:
        get_chat(username=username, thread_id=thread_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        response = ask_agent(
            username=username,
            query=req.query,
            config=config,
            model_name=req.model_name,
        )

        context = response.get("context", {})
        running_summary = context.get("running_summary") if context else None
        summary_text = running_summary.summary if running_summary else None

        # Clean answer string if it comes as a list/dict
        raw_answer = response.get("answer", "")
        if isinstance(raw_answer, list) and len(raw_answer) > 0 and isinstance(raw_answer[0], dict):
            answer_text = raw_answer[0].get("text", str(raw_answer))
        else:
            answer_text = str(raw_answer)

        return MessageResponse(
            thread_id=thread_id,
            question=response.get("question", req.query),
            source_used=response.get("source_used", "unknown"),
            answer=answer_text,
            summary=summary_text,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Agent execution failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
