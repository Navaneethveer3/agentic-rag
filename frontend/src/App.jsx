import { useState, useEffect, useRef, useCallback } from "react";
import Sidebar from "./components/Sidebar";
import ChatInput from "./components/ChatInput";
import MessageBubble from "./components/MessageBubble";
import TypingIndicator from "./components/TypingIndicator";
import WelcomeScreen from "./components/WelcomeScreen";
import ThemeToggle from "./components/ThemeToggle";
import { DEFAULT_MODEL_ID } from "./models";
import {
  loginWithBackend,
  getAllChats,
  getChatMessages,
  createChat,
  deleteChat,
  updateChat,
  sendMessage,
  parseDocuments,
} from "./api";
import "./App.css";

const CHEVRON_DOWN_ICON = (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="6 9 12 15 18 9" />
  </svg>
);

export default function App() {
  // Theme state: dark / light
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("atlas_theme") || "dark";
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("atlas_theme", theme);
  }, [theme]);

  function handleToggleTheme() {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  }

  const [username, setUsername] = useState(() => {
    return localStorage.getItem("atlas_username") || "";
  });
  const [loggedIn, setLoggedIn] = useState(() => !!localStorage.getItem("atlas_username"));
  const [loginInput, setLoginInput] = useState("");

  const [selectedModel, setSelectedModel] = useState(() => {
    return localStorage.getItem("atlas_selected_model") || DEFAULT_MODEL_ID;
  });

  const [chats, setChats] = useState([]);
  const [activeThreadId, setActiveThreadId] = useState(null);
  const [messages, setMessages] = useState({});
  // Per-thread loading states so chatting in one chat does not block another chat
  const [loadingThreads, setLoadingThreads] = useState({});
  const [fetchingHistory, setFetchingHistory] = useState({});
  const [isParsing, setIsParsing] = useState(false);
  const [parsingStatus, setParsingStatus] = useState("");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Dynamic scrolling state
  const [showScrollBottom, setShowScrollBottom] = useState(false);
  const messagesAreaRef = useRef(null);
  const messagesEndRef = useRef(null);
  const isUserScrolledUp = useRef(false);

  function handleSelectModel(modelId) {
    setSelectedModel(modelId);
    localStorage.setItem("atlas_selected_model", modelId);
  }

  // Cross-tab login sync
  useEffect(() => {
    function handleStorageEvent(e) {
      if (e.key === "atlas_username" && e.newValue) {
        setUsername(e.newValue);
        setLoggedIn(true);
      }
    }
    window.addEventListener("storage", handleStorageEvent);
    return () => window.removeEventListener("storage", handleStorageEvent);
  }, []);

  // Check if page loaded from redirect login return
  useEffect(() => {
    async function checkRedirectReturn() {
      try {
        const { handleRedirectAuth } = await import("./authService");
        const res = await handleRedirectAuth();
        if (res && res.username) {
          localStorage.setItem("atlas_username", res.username);
          if (res.token) localStorage.setItem("atlas_token", res.token);
          setUsername(res.username);
          setLoggedIn(true);
          if (window.location.hash) {
            window.history.replaceState(null, "", window.location.pathname);
          }
        }
      } catch (err) {
        console.warn("Redirect check info:", err);
      }
    }
    checkRedirectReturn();
  }, []);

  // Handle dynamic scrolling
  const handleScroll = useCallback(() => {
    if (!messagesAreaRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = messagesAreaRef.current;
    const distanceFromBottom = scrollHeight - (scrollTop + clientHeight);
    const scrolledUp = distanceFromBottom > 100;
    isUserScrolledUp.current = scrolledUp;
    setShowScrollBottom(scrolledUp);
  }, []);

  const scrollToBottom = useCallback((smooth = true) => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: smooth ? "smooth" : "auto" });
      isUserScrolledUp.current = false;
      setShowScrollBottom(false);
    }
  }, []);

  // Auto-scroll when messages update, but only if user is not deliberately scrolled up
  useEffect(() => {
    if (!isUserScrolledUp.current) {
      scrollToBottom(true);
    }
  }, [messages, activeThreadId, loadingThreads, scrollToBottom]);

  // Load chats on login
  useEffect(() => {
    if (loggedIn && username) {
      loadChats();
    }
  }, [loggedIn, username]);

  async function loadChats() {
    try {
      const data = await getAllChats(username);
      data.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
      setChats(data);
    } catch (err) {
      console.error("Failed to load chats:", err);
    }
  }

  // Fetch previous messages for a chat from backend
  const loadChatMessages = useCallback(async (threadId) => {
    if (!threadId) return;
    setFetchingHistory((prev) => ({ ...prev, [threadId]: true }));
    try {
      const history = await getChatMessages(username, threadId);
      const formatted = history.map((m) => ({
        role: m.role,
        text: m.text,
        source: m.source,
        model: m.model,
      }));
      setMessages((prev) => ({ ...prev, [threadId]: formatted }));
      // Jump to bottom upon loading previous conversation
      setTimeout(() => {
        scrollToBottom(false);
      }, 50);
    } catch (err) {
      console.error(`Failed to load messages for thread ${threadId}:`, err);
    } finally {
      setFetchingHistory((prev) => ({ ...prev, [threadId]: false }));
    }
  }, [username, scrollToBottom]);

  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");

  // Authenticate user via backend Microsoft Entra ID
  async function handleLogin(e) {
    e.preventDefault();
    const name = loginInput.trim();
    if (!name || authLoading) return;

    setAuthLoading(true);
    setAuthError("");

    try {
      const result = await loginWithBackend(name);
      const authenticatedUser = result?.username || name;
      localStorage.setItem("atlas_username", authenticatedUser);
      setUsername(authenticatedUser);
      setLoggedIn(true);
    } catch (err) {
      console.error("Backend Entra authentication error:", err);
      setAuthError(err.message || "Microsoft Entra ID authentication failed on backend.");
    } finally {
      setAuthLoading(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem("atlas_username");
    localStorage.removeItem("atlas_token");
    setUsername("");
    setLoggedIn(false);
    setChats([]);
    setActiveThreadId(null);
    setMessages({});
    setLoadingThreads({});
  }

  async function handleNewChat() {
    try {
      const chat = await createChat(username, "New Chat");
      setChats((prev) => [chat, ...prev]);
      setActiveThreadId(chat.thread_id);
      setMessages((prev) => ({ ...prev, [chat.thread_id]: [] }));
    } catch (err) {
      console.error("Failed to create chat:", err);
    }
  }

  async function handleDeleteChat(threadId) {
    try {
      await deleteChat(username, threadId);
      setChats((prev) => prev.filter((c) => c.thread_id !== threadId));
      if (activeThreadId === threadId) {
        setActiveThreadId(null);
      }
      setMessages((prev) => {
        const copy = { ...prev };
        delete copy[threadId];
        return copy;
      });
      setLoadingThreads((prev) => {
        const copy = { ...prev };
        delete copy[threadId];
        return copy;
      });
    } catch (err) {
      console.error("Failed to delete chat:", err);
    }
  }

  async function handleRenameChat(threadId, newTitle) {
    try {
      const updated = await updateChat(username, threadId, newTitle);
      setChats((prev) =>
        prev.map((c) => (c.thread_id === threadId ? { ...c, title: updated.title } : c))
      );
    } catch (err) {
      console.error("Failed to rename chat:", err);
    }
  }

  function handleSelectChat(threadId) {
    setActiveThreadId(threadId);
    isUserScrolledUp.current = false;
    setShowScrollBottom(false);

    // If messages are not loaded yet or need refresh, fetch from backend
    if (!messages[threadId] || messages[threadId].length === 0) {
      loadChatMessages(threadId);
    } else {
      setTimeout(() => scrollToBottom(false), 30);
    }
  }

  async function handleSendMessage(query, attachedFiles = []) {
    let currentThreadId = activeThreadId;

    // Auto-create chat if on welcome screen without an active chat
    if (!currentThreadId) {
      try {
        const docName = attachedFiles[0]?.name;
        const initialTitle = docName
          ? `Doc: ${docName.slice(0, 30)}`
          : (query ? (query.length > 30 ? query.slice(0, 27) + "..." : query) : "New Chat");
        const newChat = await createChat(username, initialTitle);
        setChats((prev) => [newChat, ...prev]);
        setActiveThreadId(newChat.thread_id);
        currentThreadId = newChat.thread_id;
        setMessages((prev) => ({ ...prev, [newChat.thread_id]: [] }));
      } catch (err) {
        console.error("Failed to auto-create conversation thread:", err);
        return;
      }
    }

    // Only block if this specific thread is already running a query
    if (loadingThreads[currentThreadId] || isParsing) return;

    // Step 1: If documents are attached, parse & embed them via backend
    if (attachedFiles && attachedFiles.length > 0) {
      setIsParsing(true);
      setParsingStatus(`Parsing ${attachedFiles.length} document(s) & indexing into Knowledge Base...`);

      try {
        await parseDocuments(username, attachedFiles);
      } catch (err) {
        console.error("Document parsing error:", err);
        const errMsg = {
          role: "agent",
          text: `⚠️ Document parsing error: ${err.message}`,
          source: "guardrail_blocked",
        };
        setMessages((prev) => ({
          ...prev,
          [currentThreadId]: [...(prev[currentThreadId] || []), errMsg],
        }));
        setIsParsing(false);
        setParsingStatus("");
        return;
      } finally {
        setIsParsing(false);
        setParsingStatus("");
      }
    }

    // Determine query to send to agent
    let promptText = query;
    if (!promptText && attachedFiles && attachedFiles.length > 0) {
      const fileNames = attachedFiles.map((f) => f.name).join(", ");
      promptText = `I have uploaded the following document(s): ${fileNames}. Please give me an executive summary and explain the key findings.`;
    }

    if (!promptText) return;

    // Add user message with attached file badges
    const userMsg = {
      role: "user",
      text: promptText,
      files: attachedFiles.map((f) => ({ name: f.name, size: f.size })),
    };

    setMessages((prev) => ({
      ...prev,
      [currentThreadId]: [...(prev[currentThreadId] || []), userMsg],
    }));

    // Mark ONLY this specific thread as loading
    setLoadingThreads((prev) => ({ ...prev, [currentThreadId]: true }));
    isUserScrolledUp.current = false;
    setShowScrollBottom(false);
    scrollToBottom(true);

    try {
      const response = await sendMessage(username, currentThreadId, promptText, selectedModel);
      const agentMsg = {
        role: "agent",
        text: response.answer,
        source: response.source_used,
        model: selectedModel,
      };
      setMessages((prev) => ({
        ...prev,
        [currentThreadId]: [...(prev[currentThreadId] || []), agentMsg],
      }));

      // Auto-rename chat if it was the first message
      const threadMessages = messages[currentThreadId] || [];
      if (threadMessages.length === 0) {
        const title = promptText.length > 50 ? promptText.slice(0, 47) + "..." : promptText;
        handleRenameChat(currentThreadId, title);
      }
    } catch (err) {
      const errorMsg = {
        role: "agent",
        text: `⚠️ Error: ${err.message}`,
        source: "guardrail_blocked",
      };
      setMessages((prev) => ({
        ...prev,
        [currentThreadId]: [...(prev[currentThreadId] || []), errorMsg],
      }));
    } finally {
      // Clear loading state for this thread
      setLoadingThreads((prev) => ({ ...prev, [currentThreadId]: false }));
    }
  }

  const activeMessages = messages[activeThreadId] || [];
  const isCurrentThreadLoading = !!loadingThreads[activeThreadId];
  const isCurrentThreadFetching = !!fetchingHistory[activeThreadId];

  // Login Screen
  if (!loggedIn) {
    return (
      <div className="login-screen">
        <div className="login-top-bar">
          <ThemeToggle theme={theme} onToggle={handleToggleTheme} />
        </div>
        <div className="login-glow" />
        <div className="login-card fade-in">
          <div className="login-logo">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="url(#loginGrad)" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round">
              <defs>
                <linearGradient id="loginGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="var(--accent-start)" />
                  <stop offset="100%" stopColor="var(--accent-end)" />
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10" />
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
              <line x1="2" y1="12" x2="22" y2="12" />
            </svg>
          </div>
          <h1 className="login-title">Atlas Agent</h1>
          <p className="login-subtitle">Sign in to your conversation</p>

          <form className="login-manual-group" onSubmit={handleLogin}>
            <input
              className="login-input"
              type="text"
              placeholder="Enter your username (e.g. tester1)"
              value={loginInput}
              onChange={(e) => setLoginInput(e.target.value)}
              disabled={authLoading}
              autoFocus
            />
            <button className="login-btn" type="submit" disabled={!loginInput.trim() || authLoading}>
              {authLoading ? "Authenticating with Microsoft..." : "Sign In"}
            </button>
          </form>

          {authError && <div className="login-error-msg">{authError}</div>}
        </div>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <Sidebar
        chats={chats}
        activeThreadId={activeThreadId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
        onRenameChat={handleRenameChat}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        username={username}
        onLogout={handleLogout}
      />

      <main className="main-panel">
        {/* Top-right theme switcher bar */}
        <div className="main-panel-top-bar">
          <div className="top-bar-right">
            <ThemeToggle theme={theme} onToggle={handleToggleTheme} />
          </div>
        </div>

        {!activeThreadId ? (
          <div className="welcome-view-wrapper">
            <WelcomeScreen
              onNewChat={handleNewChat}
              selectedModel={selectedModel}
              onSelectModel={handleSelectModel}
            />
            <ChatInput
              onSend={handleSendMessage}
              disabled={isCurrentThreadLoading}
              selectedModel={selectedModel}
              onSelectModel={handleSelectModel}
              isParsing={isParsing}
              parsingStatus={parsingStatus}
            />
          </div>
        ) : (
          <>
            <div
              className="messages-area"
              ref={messagesAreaRef}
              onScroll={handleScroll}
            >
              {isCurrentThreadFetching && (
                <div className="messages-loading-hint fade-in">
                  <div className="parsing-spinner" />
                  <span>Loading previous conversation...</span>
                </div>
              )}

              {!isCurrentThreadFetching && activeMessages.length === 0 && !isCurrentThreadLoading && (
                <div className="empty-chat fade-in">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                  </svg>
                  <p>Send a message or attach documents to begin</p>
                </div>
              )}

              {activeMessages.map((msg, idx) => (
                <MessageBubble
                  key={idx}
                  role={msg.role}
                  text={msg.text}
                  files={msg.files}
                  source={msg.source}
                  model={msg.model}
                  animate={idx === activeMessages.length - 1}
                />
              ))}

              {isCurrentThreadLoading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </div>

            {showScrollBottom && (
              <button
                type="button"
                className="scroll-bottom-btn fade-in"
                onClick={() => scrollToBottom(true)}
                title="Scroll to latest messages"
              >
                {CHEVRON_DOWN_ICON}
              </button>
            )}

            <ChatInput
              onSend={handleSendMessage}
              disabled={isCurrentThreadLoading}
              selectedModel={selectedModel}
              onSelectModel={handleSelectModel}
              isParsing={isParsing}
              parsingStatus={parsingStatus}
            />
          </>
        )}
      </main>
    </div>
  );
}
