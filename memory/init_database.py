import os
from dotenv import load_dotenv
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, String, DateTime, Index, func
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

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()
