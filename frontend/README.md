# Atlas Agent — React Frontend

A modern, high-performance, and interactive web client for the **Atlas Agent** Agentic RAG platform.

---

## ✨ Features

- **Atlas Agent Aesthetic**: Dark-space theme with curated indigo/violet accents, glowing radial gradients, and glassmorphism cards.
- **Interactive Multi-Turn Chat**: Real-time conversation thread management with auto-scrolling and smooth micro-animations.
- **Dynamic Source Badges**: Visual indicators displaying whether the agent utilized:
  - 📚 **Knowledge Base** (`private_kb`)
  - 🌐 **Web Search** (`web`)
  - ⚡ **Direct Reasoning** (`direct`)
  - 🛡️ **Guardrail Interception** (`guardrail_blocked`)
- **Conversation Thread Management**:
  - Create new threads
  - Inline title renaming with double-click / edit icon
  - Individual thread deletion and thread switching
  - Collapsible sidebar for focus mode
- **User Authentication**:
  - Seamless username header integration (`X-Username`) compatible with Entra ID backend auth.

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js (v18+)
- Running FastAPI backend on `http://localhost:8000`

### 2. Development Server
```bash
# In the frontend directory
npm run dev
```
The app will run locally at `http://localhost:5173`.

### 3. Production Build
```bash
npm run build
npm run preview
```

