import os
from dotenv import load_dotenv
from uuid import uuid4
from typing import List, Optional
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker
from memory.init_database import Chat, ChatMessage, create_tables
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def create_chat(username : str, title : str):
    create_tables()
    thread_id = str(uuid4())

    with SessionLocal() as session:
        chat = Chat(
            username=username,
            thread_id=thread_id,
            title=title
        )
        try:
            session.add(chat)
            session.commit()
            session.refresh(chat)
        except Exception as e:
            raise ValueError(f"Unable to CREATE a new chat for User : {username} with title : {title}")

        print(f"User : {username} created a new chat with id : {thread_id}\n\n")

        return chat

def get_chat(username : str, thread_id : str):
    create_tables()
    with SessionLocal() as session:
        chat = session.get(Chat, thread_id)
        
        if chat is None:
            raise ValueError("Chat not found.")
        
        if chat.username!=username:
            raise PermissionError("You don't have permission to access this chat.")
        
        print(f"User : {username} queried chat with id : {thread_id}\n\n")

        return chat

def update_chat(username : str, thread_id : str, title : str):
    with SessionLocal() as session:
        chat = session.get(Chat, thread_id)

        if chat is None:
            raise ValueError("Chat not found.")

        if chat.username!=username:
            raise PermissionError("You don't have permission to access this chat.")
        
        old_title = chat.title
        chat.title = title
        try:
            session.commit()
            session.refresh(chat)
        except Exception as e:
            raise ValueError(f"Unable to update the chat title with id : {thread_id} for the User : {username}")

        print(f"User : {username} changed the title from {old_title} to {title}\n\n")

        return chat

def delete_chat(username : str, thread_id : str):
    with SessionLocal() as session:
        chat = session.get(Chat, thread_id)

        if chat is None:
            raise ValueError("Chat not found.")
        
        if chat.username!=username:
            raise PermissionError("You don't have permission to access this chat.")

        try:
            # Delete messages first
            session.execute(delete(ChatMessage).where(ChatMessage.thread_id == thread_id))
            session.delete(chat)
            session.commit()
        except Exception as e:
            raise ValueError(f"Unable to DELETE chat with id : {thread_id}: {str(e)}")

        try:
            with PostgresSaver.from_conn_string(DB_URL) as checkpoint:
                checkpoint.delete_thread(thread_id)
        except Exception as cp_err:
            print(f"Warning: could not delete LangGraph checkpoint thread: {cp_err}")

        print(f"User : {username} deleted the chat with id : {thread_id}\n\n")

        return chat


def get_all_chats(username : str):
    create_tables()
    with SessionLocal() as session:
        stmt = select(Chat).where(Chat.username==username).order_by(Chat.updated_at.desc())
        chats = session.scalars(stmt).all()

        print(f"User : {username} retrived total {len(chats)} chats.\n\n")

        return chats

def delete_all_chats(username : str):
    with SessionLocal() as session:
        stmt = select(Chat).where(Chat.username==username)
        chats = session.scalars(stmt).all()
        try:
            for chat in chats:
                session.execute(delete(ChatMessage).where(ChatMessage.thread_id == chat.thread_id))
            session.execute(delete(Chat).where(Chat.username==username))
            session.commit()
        except Exception as e:
            raise ValueError(f"Unable to DELETE all chat for the User : {username}")

        try:
            with PostgresSaver.from_conn_string(DB_URL) as checkpoint:
                for chat in chats:
                    checkpoint.delete_thread(chat.thread_id)
        except Exception as cp_err:
            print(f"Warning: could not delete LangGraph checkpoints: {cp_err}")


def save_chat_message(thread_id: str, role: str, text: str, source: Optional[str] = None, model: Optional[str] = None):
    """Persists an individual user or agent message into the database."""
    create_tables()
    with SessionLocal() as session:
        msg = ChatMessage(
            thread_id=thread_id,
            role=role,
            text=text,
            source=source,
            model=model,
        )
        try:
            session.add(msg)
            session.commit()
            session.refresh(msg)
            return msg
        except Exception as e:
            print(f"Warning: Failed to persist chat message: {e}")
            return None


def get_chat_messages(thread_id: str):
    """Retrieves all message history for a specific conversation thread."""
    create_tables()
    with SessionLocal() as session:
        stmt = select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.created_at.asc())
        return session.scalars(stmt).all()
