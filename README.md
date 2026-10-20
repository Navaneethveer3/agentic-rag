# Atlas Agent
> An agentic Retrieval-Augmented Generation (RAG) system designed to improve the accuracy and relevance of information retrieval and responses.

## Overview
> Atlas Agent is an agentic RAG application that helps users retrieve information and get answers from multiple sources. It supports document-based querying, web searches, and querying specific web URLs. Using an agent-based architecture, Atlas Agent simplifies information discovery and enables users to interact with their data and online content through natural language conversations.

## Features
- **Document-Based Querying:** Ask questions and retrieve relevant information from uploaded documents.
- **Web Search:** Search the web for relevant information and generate answers based on search results.
- **URL-Based Querying:** Query specific web pages to retrieve and understand their content.
- **Conversational Interface:** Interact with documents and web content through natural language conversations.
- **Conversation Memory:** Maintains separate conversation histories for individual users to support context-aware interactions across chats.
- **Agentic Architecture:** Uses an agent-based approach to determine and execute the appropriate steps to answer user queries.
- **Retrieval Quality Evaluation:** Evaluates the relevance and sufficiency of retrieved information from the knowledge base and web search results before generating an answer.
- **Automatic Retry Mechanism:** Retries information retrieval up to two times when the retrieved information is insufficient to answer the user's query.
- **Context-Aware Responses:** Generates relevant answers using retrieved information and available conversation context.
- **Unified Information Retrieval:** Access information from documents, web search results, and specific URLs through a single interface.
- **Message Summarization:** Older messages are summarized into a concise representation that preserves important context, key information, and relevant conversation details.
- **Context Management:** The conversation state is updated with the summary and the necessary recent messages, reducing the amount of history passed to the language model.
- **Conversation Continuity:** The model uses the summary and recent conversation messages to maintain continuity across longer interactions.

## Tech Stack
- **Frontend:** React
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Vector DB:** Pinecone
- **AI/ML:** LangChain, LangGraph
- **LLM Models used:** Gemini-3.6-flash(major model), all-MiniLM-L6-v2(chunking)

## Architecture/Workflow :
<img width="1691" height="2056" alt="agentic_rag_architecture" src="https://github.com/user-attachments/assets/d92eef10-58e0-4262-953c-ab61a7471b90" />

