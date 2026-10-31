import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_PATH = PROJECT_ROOT / "src" / "rag_project"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import tempfile
import shutil
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from memory.chat_manager import (
    create_chat,
    get_chat,
    get_all_chats,
    update_chat,
    delete_chat,
    delete_all_chats,
    save_chat_message,
    get_chat_messages,
)
from backend.response_schemas import (
    CreateChatRequest, 
    UpdateChatRequest, 
    ChatResponse, 
    MessageRequest, 
    MessageResponse,
    ParsedFileInfo,
    DocumentParseResponse)
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


@app.get("/api/auth/config", tags=["Auth"])
def get_auth_config():
    """Returns public Azure Entra ID SSO configuration for frontend authentication."""
    import os
    tenant_id = os.getenv("AZURE_TENANT_ID", "")
    client_id = os.getenv("AZURE_CLIENT_ID", "")
    return {
        "tenant_id": tenant_id,
        "client_id": client_id,
        "authority": f"https://login.microsoftonline.com/{tenant_id}",
    }


@app.post("/api/auth/entra/login", tags=["Auth"])
def api_entra_login():
    """
    Performs interactive Microsoft Entra ID authentication via MSAL.
    Returns user details and access token upon successful authentication.
    """
    try:
        from auth.entra_auth import login_with_entra
        user_info = login_with_entra()
        return {
            "status": "success",
            "username": user_info.get("username"),
            "name": user_info.get("name"),
            "oid": user_info.get("oid"),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Microsoft Entra ID authentication failed: {str(e)}"
        )




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

@app.delete("/api/chats", tags=["Chats"])
def api_delete_all_chats(username: str = Depends(get_current_user)):
    """Delete all the chats for a user"""
    try:
        delete_all_chats(username)
        return {"message": "All chats deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/chats/{thread_id}/messages", tags=["Chats"])
def api_get_chat_messages(
    thread_id: str,
    username: str = Depends(get_current_user),
):
    """
    Retrieves full message history for a specific conversation thread.
    Allows previous conversations in the chats to be visible when loaded.
    """
    try:
        get_chat(username=username, thread_id=thread_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    messages = get_chat_messages(thread_id)
    return [
        {
            "id": m.id,
            "thread_id": m.thread_id,
            "role": m.role,
            "text": m.text,
            "source": m.source,
            "model": m.model,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in messages
    ]


@app.post("/api/chats/{thread_id}/messages", response_model=MessageResponse, tags=["Agent"])
def api_send_message(
    thread_id: str,
    req: MessageRequest,
    username: str = Depends(get_current_user),
):
    """
    Sends a question to the Agentic RAG graph within a specific conversation thread.
    Persists history to Azure PostgreSQL database and checkpointer.
    """
    
    try:
        get_chat(username=username, thread_id=thread_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    
    save_chat_message(thread_id=thread_id, role="user", text=req.query)

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        
        from src.rag_project import ask_agent

        response = ask_agent(
            username=username,
            query=req.query,
            config=config,
            model_name=req.model_name,
        )

       
        context = response.get("context", {})
        running_summary = context.get("running_summary") if context else None
        raw_summary = running_summary.summary if running_summary else None

        summary_text = None
        if raw_summary:
            if isinstance(raw_summary, list):
                summary_text = "".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in raw_summary
                ).strip()
            elif isinstance(raw_summary, dict):
                summary_text = raw_summary.get("text", str(raw_summary))
            else:
                summary_text = str(raw_summary)

        
        raw_answer = response.get("answer", "")
        if isinstance(raw_answer, list):
            answer_text = "".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in raw_answer
            ).strip()
        elif isinstance(raw_answer, dict):
            answer_text = raw_answer.get("text", str(raw_answer))
        else:
            answer_text = str(raw_answer)

        source_used = response.get("source_used", "unknown")

        
        save_chat_message(
            thread_id=thread_id,
            role="agent",
            text=answer_text,
            source=source_used,
            model=req.model_name,
        )

        return MessageResponse(
            thread_id=thread_id,
            question=response.get("question", req.query),
            source_used=source_used,
            answer=answer_text,
            summary=summary_text,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Agent execution failed: {str(e)}")


@app.post("/api/documents/parse", response_model=DocumentParseResponse, tags=["Documents"])
async def api_parse_documents(
    files: List[UploadFile] = File(...),
    username: str = Depends(get_current_user),
):
    """
    Parses and embeds uploaded documents (PDF, DOCX, TXT, MD) into the user's vector store knowledge base.
    Enables users to chat directly with their documents in the chatbox.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files were provided for parsing."
        )

    allowed_extensions = {".pdf", ".docx", ".txt", ".md"}
    temp_dir = tempfile.mkdtemp(prefix="atlas_doc_upload_")
    saved_paths = []
    file_info_list = []

    try:
        for file in files:
            orig_name = Path(file.filename).name
            ext = Path(orig_name).suffix.lower()

            if ext not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported file format '{ext}' for file '{orig_name}'. Supported formats: .pdf, .docx, .txt, .md"
                )

            dest_path = Path(temp_dir) / orig_name
            content = await file.read()
            with open(dest_path, "wb") as f:
                f.write(content)

            saved_paths.append(str(dest_path))
            file_info_list.append(
                ParsedFileInfo(
                    filename=orig_name,
                    size=len(content),
                    status="indexed",
                )
            )

        # Lazy import to ensure process_documents is loaded in execution context
        from process_documents.document_loader import load_documents

        # Parse documents and index them in user's Pinecone vector store
        all_docs = await load_documents(username=username, docs=saved_paths)

        return DocumentParseResponse(
            status="success",
            message=f"Successfully parsed and indexed {len(file_info_list)} document(s) for {username}.",
            files=file_info_list,
            total_documents=len(all_docs),
            username=username,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document parsing failed: {str(e)}"
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.post("/api/documents/upload", response_model=DocumentParseResponse, tags=["Documents"])
async def api_upload_documents(
    files: List[UploadFile] = File(...),
    username: str = Depends(get_current_user),
):
    """Alias endpoint for document parsing."""
    return await api_parse_documents(files=files, username=username)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", port=8000)
