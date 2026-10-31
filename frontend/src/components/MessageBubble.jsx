import { getModelById } from "../models";
import MarkdownRenderer from "./MarkdownRenderer";
import "./MessageBubble.css";

const SOURCE_LABELS = {
  private_kb: { label: "Knowledge Base", className: "source-kb" },
  web: { label: "Web Search", className: "source-web" },
  direct: { label: "Direct", className: "source-direct" },
  guardrail_blocked: { label: "Blocked", className: "source-blocked" },
  tools: { label: "Web URL", className: "source-web" },
};

const ATLAS_ICON = (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
    <line x1="2" y1="12" x2="22" y2="12" />
  </svg>
);

const DOC_ICON = (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
    <polyline points="14 2 14 8 20 8" />
  </svg>
);

export default function MessageBubble({ role, text, files, source, model, animate }) {
  const isUser = role === "user";
  const sourceInfo = SOURCE_LABELS[source] || null;
  const modelInfo = model ? getModelById(model) : null;

  return (
    <div className={`msg-row ${isUser ? "msg-user" : "msg-agent"} ${animate ? "fade-in" : ""}`}>
      {!isUser && (
        <div className="msg-avatar agent-avatar">{ATLAS_ICON}</div>
      )}
      <div className={`msg-bubble ${isUser ? "bubble-user" : "bubble-agent"}`}>
        {files && files.length > 0 && (
          <div className="msg-attached-files">
            {files.map((file, i) => (
              <span key={i} className="msg-file-badge">
                {DOC_ICON}
                <span>{typeof file === "string" ? file : file.name}</span>
              </span>
            ))}
          </div>
        )}
        
        {isUser ? (
          <div className="msg-text user-text">{text}</div>
        ) : (
          <MarkdownRenderer content={text} />
        )}

        {!isUser && (sourceInfo || modelInfo) && (
          <div className="msg-meta-row">
            {sourceInfo && (
              <span className={`msg-source-badge ${sourceInfo.className}`}>
                {sourceInfo.label}
              </span>
            )}
            {modelInfo && (
              <span className="msg-model-badge" title={`Model: ${modelInfo.id}`}>
                {modelInfo.label}
              </span>
            )}
          </div>
        )}
      </div>
      {isUser && (
        <div className="msg-avatar user-avatar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5S7 4.3 7 7s2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v2h20v-2c0-3.3-6.7-5-10-5z"/>
          </svg>
        </div>
      )}
    </div>
  );
}
