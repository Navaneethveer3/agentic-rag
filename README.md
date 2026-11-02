# 🧭 Atlas Agent

> A production-deployed agentic RAG system that retrieves, reranks, and grades information from documents, the web, and specific URLs before answering, so responses stay accurate and grounded. Secured with Microsoft Entra ID and hosted on Azure.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-000000)
![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?logo=microsoftazure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

## 📖 Overview

Atlas Agent is an agentic RAG application that helps users get answers from multiple sources through natural language conversation. It supports querying uploaded documents, searching the web, and reading specific URLs. An agent decides which sources to use, evaluates the quality of what it retrieves, and retries when the information is insufficient.

It is built end to end: ingestion pipeline, agent orchestration, authentication, evaluation, containerization, and cloud deployment.

## ✨ Key Highlights

- 📄 **Multi-document ingestion** (`.pdf`, `.docx`, `.txt`, `.md`) with per-user vector namespaces for privacy
- 🎯 **Reranking layer** that filters weak documents before they reach the LLM
- 🧠 **Chat summarization** that cuts token consumption by up to **80%** in long conversations
- 🔁 **Self-correcting retrieval** with relevance grading and up to 2 automatic retries
- 🔐 **Microsoft Entra ID authentication** for secure, per-user access
- ☁️ **Deployed on Azure**: backend on App Service (containerized via ACR), frontend on Static Web Apps, data on Azure PostgreSQL
- 📊 **Systematically evaluated** with LangSmith: RAG metrics, retriever metrics, routing tests, and human evaluation
- 🛡️ **Input guardrails** that detect sensitive data (emails, credit card numbers, API keys, and more) before it reaches the LLM

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

### Guardrails & Data Protection
- **Sensitive Data Detection:** User inputs are checked for emails, credit card numbers, API keys, and other sensitive patterns before being sent to the LLM.
- **Privacy by Design:** Sensitive information is handled at the input layer, so it is not passed to third-party model providers or stored in conversation history.
- **Defense in Depth:** Guardrails work alongside Entra ID authentication, per-user vector namespaces, and CORS controls.

### Security & Authentication
- **Microsoft Entra ID:** Users authenticate through Entra ID, and requests are tied to an authenticated identity.
- **Per-User Data Separation:** Vector namespaces and conversation histories are scoped to each user.
- **CORS Controls:** Allowed origins are configured through environment variables.
- 
## Architecture/Workflow :
<img width="1691" height="2056" alt="agentic_rag_architecture" src="https://github.com/user-attachments/assets/d92eef10-58e0-4262-953c-ab61a7471b90" />



### ☁️ Deployment Architecture

| Component | Azure Service |
|---|---|
| Backend (FastAPI) | Azure App Service (container) |
| Container image | Azure Container Registry (ACR) |
| Frontend (React) | Azure Static Web Apps |
| Database | Azure Database for PostgreSQL |
| Authentication | Microsoft Entra ID |

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Database | Azure Database for PostgreSQL |
| Vector DB | Pinecone |
| Orchestration | LangChain, LangGraph |
| Authentication | Microsoft Entra ID |
| Guardrails | PII Middleware |
| Evaluation & Tracing | LangSmith |
| LLM | Gemini-3.6-flash (primary) |
| Embeddings / Chunking | all-MiniLM-L6-v2 |
| Web Search | Tavily |
| Containerization | Docker |
| Cloud | Azure App Service, ACR, Static Web Apps |

## 🧪 Evaluation & Testing

Every component was tested separately against its own dataset, with traces captured in **LangSmith** for human review.

| Test | What it measures | Method |
|---|---|---|
| RAG quality | Answer correctness, faithfulness, retrieval relevance | LangSmith evaluators |
| Retriever quality | Precision, recall, F1-score | LangSmith evaluators |
| Human evaluation | Overall answer quality | Manual review of LangSmith traces |
| Routing | Correct node selection across varied queries | Multi-query test set |

### 📊 Results

| Metric | Score |
|---|---|
| Answer correctness | 95% |
| Faithfulness | 95% |
| Retrieval relevance | 90% |
| Retriever precision | 62% |
| Retriever recall | 65% |
| Retriever F1-score | 63% |
| Routing accuracy | 100% |

> Scores come from a curated evaluation set of **N** questions. Full datasets and reports are in [`/evaluation`](./evaluation).

## ⚙️ Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Docker (optional, for containerized runs)
- A PostgreSQL database (local or Azure PostgreSQL)
- A Microsoft Entra ID app registration
- API keys: Google (Gemini), Tavily, Pinecone, Hugging Face, LangSmith

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
PINECONE_API_KEY=your_pinecone_api_key
DB_URL=your_postgresql_connection_string
HF_TOKEN=your_huggingface_token
ALLOWED_ORIGINS=http://localhost:5173
FRONTEND_URL=http://localhost:5173
LANGCHAIN_API_KEY=your_langsmith_api_key
AZURE_TENANT_ID=your_entra_tenant_id
AZURE_CLIENT_ID=your_entra_client_id
```

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Gemini LLM access |
| `TAVILY_API_KEY` | Web search |
| `PINECONE_API_KEY` | Vector database |
| `DB_URL` | PostgreSQL connection string |
| `HF_TOKEN` | Hugging Face model downloads (embeddings) |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) |
| `FRONTEND_URL` | Frontend base URL |
| `LANGCHAIN_API_KEY` | LangSmith tracing and evaluation |
| `AZURE_TENANT_ID` | Microsoft Entra ID tenant |
| `AZURE_CLIENT_ID` | Microsoft Entra ID application (client) ID |

> **Important:** Never commit API keys, passwords, or other credentials to the repository. Add `.env` to `.gitignore`.

### 3. Run the Backend Locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 4. Run the Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

### 5. Run with Docker

```bash
docker build -t atlas-agent-backend .
docker run -p 8000:8000 --env-file .env atlas-agent-backend
```

<details>
<summary>View Dockerfile</summary>

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

</details>

## ☁️ Deploying to Azure

### Backend: Azure App Service (Container) + ACR

```bash
# Log in and create a registry
az login
az acr create --resource-group <resource-group> --name <acr-name> --sku Basic

# Build and push the image
az acr login --name <acr-name>
docker build -t <acr-name>.azurecr.io/atlas-agent-backend:latest .
docker push <acr-name>.azurecr.io/atlas-agent-backend:latest
```

Then create an App Service that pulls the image from ACR, and add all environment variables from the table above under **Settings → Environment variables**. Set `ALLOWED_ORIGINS` and `FRONTEND_URL` to your Static Web Apps URL, and set the container port to `8000` (`WEBSITES_PORT=8000`).

### Frontend: Azure Static Web Apps

1. Create a Static Web App and connect it to this repository.
2. Set the app location to `frontend` and the build output to `dist`.
3. Point the frontend's API base URL at your App Service URL.
4. Add the frontend URL as a redirect URI in your Entra ID app registration.

### Database: Azure Database for PostgreSQL

Create a PostgreSQL flexible server, allow access from your App Service, and set its connection string as `DB_URL`.

## 📂 Project Structure

```
atlas-agent/
├── backend/           # FastAPI app and LangGraph agent
├── frontend/          # React app
├── evaluation/        # Test datasets and result reports
│   ├── datasets.py
│   └── results/
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🔮 Future Improvements

- 📊 Application monitoring and alerting with Azure Monitor
- 🛡️ Rate limiting and API throttling
- 🧪 Larger, adversarial evaluation datasets
- 📡 Streaming responses for lower perceived latency

## 👤 Author

**Mamidi Navaneeth Veer**
[LinkedIn](https://linkedin.com/in/navaneethveer) · [GitHub](https://github.com/Navaneethveer3)
