# 🧭 Atlas Agent

> An agentic Retrieval-Augmented Generation (RAG) system that retrieves, reranks, and grades information from documents, the web, and specific URLs before answering, so responses stay accurate and grounded.

## 📖 Overview

Atlas Agent is an agentic RAG application that helps users get answers from multiple sources through natural language conversation. It supports querying uploaded documents, searching the web, and reading specific URLs. An agent decides which sources to use, evaluates the quality of what it retrieves, and retries when the information is insufficient.

## ✨ Key Highlights

- 📄 **Multi-document ingestion** (`.pdf`, `.docx`, `.txt`, `.md`) with per-user vector namespaces for privacy
- 🎯 **Reranking layer** that filters weak documents before they reach the LLM
- 🧠 **Chat summarization** that cuts token consumption by up to **80%** in long conversations
- 🔁 **Self-correcting retrieval** with relevance grading and up to 2 automatic retries
- 📊 **Systematically evaluated** with LangSmith: RAG metrics, retriever metrics, routing tests, and human evaluation

## 🚀 Features

### Retrieval & Querying
- **Document-Based Querying:** Ask questions over uploaded documents.
- **Web Search:** Generate answers from live web search results.
- **URL-Based Querying:** Query the content of specific web pages.
- **Unified Information Retrieval:** Documents, web search, and URLs are accessible through a single interface.

### Document Ingestion
- **Multi-File Upload:** Upload multiple documents at once in `.pdf`, `.docx`, `.txt`, and `.md` formats.
- **Instant Indexing:** Documents are chunked immediately and their embeddings stored in the vector store, ready for queries.
- **User Isolation:** Each user's embeddings live in a dedicated namespace, keeping data private and separated.

### Retrieval Quality
- **Reranking:** A reranker sits between the knowledge-base node and the grading node, removing weak documents so only strong context is passed to the LLM.
- **Retrieval Quality Evaluation:** Grades the relevance and sufficiency of retrieved knowledge-base and web results before answer generation.
- **Automatic Retry Mechanism:** Retries retrieval up to two times when the information is insufficient.

### Conversation & Memory
- **Conversational Interface:** Natural language chat over documents and web content.
- **Per-User Conversation Memory:** Separate histories for individual users, supporting context-aware interactions across chats.
- **Message Summarization:** Older messages are condensed into a summary that preserves key context and details.
- **Context Management:** Conversation state holds the summary plus recent messages, reducing history passed to the model by up to **80%** in long conversations.
- **Conversation Continuity:** The model uses the summary and recent messages to stay coherent over long interactions.

### Agentic Architecture
- **Agent-Based Routing:** The agent decides which steps and sources to use for each query.
- **Context-Aware Responses:** Answers are generated from retrieved information and conversation context.
## Architecture/Workflow :
<img width="1691" height="2056" alt="agentic_rag_architecture" src="https://github.com/user-attachments/assets/d92eef10-58e0-4262-953c-ab61a7471b90" />


## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Database | PostgreSQL |
| Vector DB | Pinecone |
| Orchestration | LangChain, LangGraph |
| Evaluation & Tracing | LangSmith |
| LLM | Gemini-3.6-flash (primary) |
| Embeddings / Chunking | all-MiniLM-L6-v2 |

## 🧪 Evaluation & Testing

Every component was tested separately against its own dataset, with traces captured in **LangSmith** for human review.

| Test | What it measures | Method |
|---|---|---|
| RAG quality | Answer correctness, faithfulness, retrieval relevance | LangSmith evaluators |
| Retriever quality | Precision, recall, F1-score | LangSmith evaluators |
| Human evaluation | Overall answer quality | Manual review of LangSmith traces |
| Routing | Correct node selection across varied queries | Multi-query test set |

### 📊 Results

> Replace the placeholders below with the numbers from your CSV reports.

| Metric | Score |
|---|---|
| Answer correctness | `XX%` |
| Faithfulness | `XX%` |
| Retrieval relevance | `XX%` |
| Retriever precision | `XX` |
| Retriever recall | `XX` |
| Retriever F1-score | `XX` |
| Routing accuracy | `XX%` |


