import { useState, useRef, useEffect } from "react";
import ModelSelector from "./ModelSelector";
import "./ChatInput.css";

const SEND_ICON = (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);

const ATTACH_ICON = (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48" />
  </svg>
);

const FILE_ICON = (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
    <polyline points="14 2 14 8 20 8" />
  </svg>
);

const CLOSE_ICON = (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt", ".md"];

function formatFileSize(bytes) {
  if (!bytes) return "0 B";
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

export default function ChatInput({
  onSend,
  disabled,
  selectedModel,
  onSelectModel,
  isParsing = false,
  parsingStatus = "",
}) {
  const [value, setValue] = useState("");
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 160) + "px";
    }
  }, [value]);

  function handleFileSelect(files) {
    if (!files || files.length === 0) return;
    const newFiles = Array.from(files).filter((file) => {
      const ext = "." + file.name.split(".").pop().toLowerCase();
      return ALLOWED_EXTENSIONS.includes(ext);
    });

    if (newFiles.length === 0) {
      alert("Please upload supported documents: PDF, DOCX, TXT, or MD.");
      return;
    }

    setAttachedFiles((prev) => {
      const existingNames = new Set(prev.map((f) => f.name));
      const filtered = newFiles.filter((f) => !existingNames.has(f.name));
      return [...prev, ...filtered];
    });
  }

  function handleRemoveFile(fileName) {
    setAttachedFiles((prev) => prev.filter((f) => f.name !== fileName));
  }

  function handleSubmit(e) {
    e?.preventDefault();
    const trimmed = value.trim();
    if ((!trimmed && attachedFiles.length === 0) || disabled || isParsing) return;

    onSend(trimmed, attachedFiles);
    setValue("");
    setAttachedFiles([]);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }

  function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer?.files) {
      handleFileSelect(e.dataTransfer.files);
    }
  }

  const hasContent = value.trim().length > 0 || attachedFiles.length > 0;

  return (
    <form
      className={`chat-input-form ${isDragging ? "dragging" : ""}`}
      onSubmit={handleSubmit}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        multiple
        accept=".pdf,.docx,.txt,.md"
        onChange={(e) => {
          handleFileSelect(e.target.files);
        }}
      />

      <div className="chat-input-toolbar">
        <div className="chat-input-toolbar-left">
          {selectedModel && onSelectModel && (
            <ModelSelector
              compact
              direction="up"
              selectedModel={selectedModel}
              onSelectModel={onSelectModel}
            />
          )}
          <button
            type="button"
            className={`chat-attach-btn ${attachedFiles.length > 0 ? "has-files" : ""}`}
            onClick={() => fileInputRef.current?.click()}
            title="Attach documents to parse and chat with (.pdf, .docx, .txt, .md)"
            disabled={disabled || isParsing}
          >
            {ATTACH_ICON}
            <span className="attach-btn-label">
              {attachedFiles.length > 0 ? `${attachedFiles.length} doc(s)` : "Attach doc"}
            </span>
          </button>
        </div>

        <span className="chat-input-hint">
          {isParsing
            ? (parsingStatus || "Parsing documents...")
            : "Enter ↵ to send • Shift+Enter for new line"}
        </span>
      </div>

      {attachedFiles.length > 0 && (
        <div className="chat-attached-files-bar">
          {attachedFiles.map((file) => (
            <div key={file.name} className="attached-file-pill">
              <span className="attached-file-icon">{FILE_ICON}</span>
              <span className="attached-file-name" title={file.name}>
                {file.name}
              </span>
              <span className="attached-file-size">
                ({formatFileSize(file.size)})
              </span>
              <button
                type="button"
                className="attached-file-remove"
                onClick={() => handleRemoveFile(file.name)}
                title="Remove file"
              >
                {CLOSE_ICON}
              </button>
            </div>
          ))}
        </div>
      )}

      {isParsing && (
        <div className="chat-parsing-indicator">
          <div className="parsing-spinner" />
          <span>{parsingStatus || "Parsing document(s) and indexing into knowledge base..."}</span>
        </div>
      )}

      <div className="chat-input-container">
        <textarea
          ref={textareaRef}
          className="chat-input-textarea"
          placeholder={
            attachedFiles.length > 0
              ? "Ask questions about the attached document(s), or press send to analyze..."
              : "Ask Atlas Agent anything, or attach documents to chat with them..."
          }
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled || isParsing}
          rows={1}
        />
        <button
          type="submit"
          className={`chat-input-send ${hasContent && !disabled && !isParsing ? "active" : ""}`}
          disabled={!hasContent || disabled || isParsing}
          aria-label="Send message"
        >
          {SEND_ICON}
        </button>
      </div>
    </form>
  );
}
