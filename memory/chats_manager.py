from sympy.combinatorics.permutations import Perm
from langgraph.channels.base import Value
from numpy.f2py.auxfuncs import throw_error
import os
from dotenv import load_dotenv
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from init_database import Chat

load_dotenv()

DB_URL = os.getenv("DB_URL")


engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

def create_chat(username : str, title : str):

    thread_id = str(uuid4())

    with SessionLocal() as session:
        chat = Chat(
            username=username,
            thread_id=thread_id,
            title=title
        )

        session.add(chat)
        session.commit()
        session.refresh(chat)

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

        session.commit()
        session.refresh(chat)

        print(f"User : {username} changed the title from {old_title} to {title}\n\n")

        return chat

def delete_chat(username : str, thread_id : str):

    with SessionLocal() as session:
        chat = session.get(Chat, thread_id)

        if chat is None:
            raise ValueError("Chat not found.")
        
        if chat.username!=username:
            raise PermissionError("You don't have permission to access this chat.")

        session.delete(chat)
        session.commit()

        print(f"User : {username} deleted the chat with id : {thread_id}\n\n")

        return chat


def get_all_chats(username : str):

    with SessionLocal() as session:
        stmt = select(Chat).where(Chat.username==username)
        chats = session.scalars(stmt).all()

        print(f"User : {username} retrived total {len(chats)} chats.")

        return chats


username = "tester1"
title = "Updated RAG Systems"

get_all_chats(username)