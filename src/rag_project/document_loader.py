from pandas.core.reshape import encoding
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from typing import Any
from typing import List
import asyncio

async def load_documents(docs : List[Any]) -> List[Document]:
    all_documents = List[Document] = []

    async def load_single_document(doc : Any) -> List[Document]:
        file_path = Path(doc)
        extension = file_path.suffix.lower()

        if extension==".pdf":
            loader = PyPDFLoader(str(file_path))
        elif extension==".docx":
            loader = Docx2txtLoader(str(file_path))
        elif extension in {".md", ".txt"}:
            loader = TextLoader(str(file_path), encoding="utf-8", autodetect_encoding=True,)
        else:
            raise ValueError(f"Unsupported file format : {extension}")
        
        return await asyncio.to_thread(loader.load)
    
    results = await asyncio.gather(
        *(load_single_document(doc) for doc in docs)
    )

    for documents in results:
        all_documents.extend(documents)
    
    return all_documents