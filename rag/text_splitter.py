from langchain_text_splitters import RecursiveCharacterTextSplitter

def text_splitter():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    )
    return splitter