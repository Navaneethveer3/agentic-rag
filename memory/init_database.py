import os
from dotenv import load_dotenv
from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlalchemy import create_engine, String, Text, DateTime, Index, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = "chats"
    
    thread_id : Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default = lambda : str(uuid4())
    )

    username : Mapped[str] = mapped_column(
        String(255),
        nullable = False,
        index = True
    )

    title : Mapped[str] = mapped_column(
        String(200),
        nullable = False,
        default = "New Chat"
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable = False,
        server_default = func.now()
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable = False,
        server_default = func.now(),
        onupdate = func.now()
    )

    __table_args__ = (
        Index(
            "idx_chats_username_updated",
            "username",
            updated_at.desc()
        ),
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thread_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # "user" or "agent"
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        Index("idx_messages_thread_created", "thread_id", created_at.asc()),
    )


_tables_created = False

def create_tables():
    global _tables_created
    if not _tables_created:
        try:
            Base.metadata.create_all(bind=engine)
            _tables_created = True
        except Exception as e:
            print(f"Warning: Failed to auto-create database tables: {e}")

if __name__ == "__main__":
    create_tables()
