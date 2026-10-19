import os
from dotenv import load_dotenv
from uuid import uuid4
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker
from memory.init_database import Chat
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URL = os.getenv("DB_URL")


engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def create_chat(username : str, title : str):

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
            session.delete(chat)
            session.commit()
        except Exception as e:
            raise ValueError(f"Unable to DELETE chat with id : {thread_id}")

        with PostgresSaver.from_conn_string(DB_URL) as checkpoint:
            checkpoint.setup()

            checkpoint.delete_thread(thread_id)

        print(f"User : {username} deleted the chat with id : {thread_id}\n\n")

        return chat


def get_all_chats(username : str):

    with SessionLocal() as session:
        stmt = select(Chat).where(Chat.username==username)
        chats = session.scalars(stmt).all()

        print(f"User : {username} retrived total {len(chats)} chats.\n\n")

        return chats

def delete_all_chats(username : str):

    with SessionLocal() as session:
        stmt = select(Chat).where(Chat.username==username)
        chats = session.scalars(stmt).all()
        stmt = delete(Chat).where(Chat.username==username)
        try:
            with PostgresSaver.from_conn_string(DB_URL) as checkpoint:
                checkpoint.setup()
                for chat in chats:
                    thread_id = chat.thread_id
                    try:
                        checkpoint.delete_thread(thread_id)
                    except Exception as e:
                        raise ValueError(f"Unable to delete the chat with id : {thread_id} for the User : {username}")
            session.execute(stmt)
            session.commit()
        except Exception as e:
            raise ValueError(f"Unable to DELETE all chat for the User : {username}")
