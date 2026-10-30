import ModelSelector from "./ModelSelector";
import "./WelcomeScreen.css";

export default function WelcomeScreen({ onNewChat, selectedModel, onSelectModel }) {
  return (
    <div className="welcome-container">
      <div className="welcome-glow" />
      <div className="welcome-content fade-in">
        <div className="welcome-logo">
          <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="url(#welcomeGrad)" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round">
            <defs>
              <linearGradient id="welcomeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#6366f1" />
                <stop offset="100%" stopColor="#a78bfa" />
              </linearGradient>
            </defs>
            <circle cx="12" cy="12" r="10" />
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
            <line x1="2" y1="12" x2="22" y2="12" />
          </svg>
        </div>
        <h1 className="welcome-title">Atlas Agent</h1>
        <p className="welcome-subtitle">
          Your intelligent RAG-powered assistant with knowledge base retrieval, web search, and conversational memory.
        </p>

        {selectedModel && onSelectModel && (
          <div className="welcome-model-bar">
            <span className="welcome-model-label">Engine:</span>
            <ModelSelector
              selectedModel={selectedModel}
              onSelectModel={onSelectModel}
            />
          </div>
        )}

        <div className="welcome-capabilities">
          <div className="capability-card">
            <div className="capability-icon cap-kb">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
              </svg>
            </div>
            <h3>Knowledge Base</h3>
            <p>Search your uploaded documents and PDFs with semantic retrieval and reranking</p>
          </div>

          <div className="capability-card">
            <div className="capability-icon cap-web">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="2" y1="12" x2="22" y2="12" />
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1 4-10z" />
              </svg>
            </div>
            <h3>Web Search</h3>
            <p>Real-time web search and URL scraping for up-to-date information</p>
          </div>

          <div className="capability-card">
            <div className="capability-icon cap-mem">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20z" />
                <path d="M12 8v4l3 3" />
              </svg>
            </div>
            <h3>Memory</h3>
            <p>Persistent conversation history with automatic summarization</p>
          </div>
        </div>

        <button className="welcome-start-btn" onClick={onNewChat}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Start a Conversation
        </button>
      </div>
    </div>
  );
}
