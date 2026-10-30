import "./TypingIndicator.css";

export default function TypingIndicator() {
  return (
    <div className="msg-row msg-agent fade-in">
      <div className="msg-avatar agent-avatar">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
          <line x1="2" y1="12" x2="22" y2="12" />
        </svg>
      </div>
      <div className="typing-bubble">
        <div className="typing-dots">
          <span className="typing-dot" style={{ animationDelay: "0ms" }} />
          <span className="typing-dot" style={{ animationDelay: "160ms" }} />
          <span className="typing-dot" style={{ animationDelay: "320ms" }} />
        </div>
        <span className="typing-label">Atlas Agent is thinking...</span>
      </div>
    </div>
  );
}
