import { useState } from "react";
import "./Sidebar.css";

const NEW_CHAT_ICON = (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 20h9" /><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z" />
  </svg>
);

const TRASH_ICON = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
  </svg>
);

const EDIT_ICON = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 20h9" /><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z" />
  </svg>
);

const LOGO_ICON = (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#logoGrad)" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
    <defs>
      <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#6366f1" />
        <stop offset="100%" stopColor="#a78bfa" />
      </linearGradient>
    </defs>
    <circle cx="12" cy="12" r="10" />
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
    <line x1="2" y1="12" x2="22" y2="12" />
  </svg>
);

export default function Sidebar({
  chats,
  activeThreadId,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  onRenameChat,
  collapsed,
  onToggleCollapse,
  username,
  onLogout,
}) {

  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");

  function startRename(chat) {
    setEditingId(chat.thread_id);
    setEditTitle(chat.title);
  }

  function commitRename(threadId) {
    if (editTitle.trim()) {
      onRenameChat(threadId, editTitle.trim());
    }
    setEditingId(null);
  }

  function formatDate(dateStr) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    const now = new Date();
    const diff = now - d;
    if (diff < 60000) return "Just now";
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  }

  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
      {/* Header */}
      <div className="sidebar-header">
        <div className="sidebar-brand" onClick={onToggleCollapse}>
          {LOGO_ICON}
          {!collapsed && <span className="sidebar-title">Atlas Agent</span>}
        </div>
        {!collapsed && (
          <button className="sidebar-new-btn" onClick={onNewChat} title="New chat">
            {NEW_CHAT_ICON}
          </button>
        )}
      </div>

      {/* Chat List */}
      {!collapsed && (
        <div className="sidebar-chats">
          <span className="sidebar-section-label">Recent Chats</span>
          <ul className="sidebar-chat-list">
            {chats.map((chat) => (
              <li
                key={chat.thread_id}
                className={`sidebar-chat-item ${chat.thread_id === activeThreadId ? "active" : ""}`}
                onClick={() => onSelectChat(chat.thread_id)}
              >
                {editingId === chat.thread_id ? (
                  <input
                    className="sidebar-rename-input"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    onBlur={() => commitRename(chat.thread_id)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") commitRename(chat.thread_id);
                      if (e.key === "Escape") setEditingId(null);
                    }}
                    autoFocus
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <>
                    <div className="sidebar-chat-info">
                      <span className="sidebar-chat-title">{chat.title}</span>
                      <span className="sidebar-chat-date">{formatDate(chat.updated_at)}</span>
                    </div>
                    <div className="sidebar-chat-actions">
                      <button
                        className="sidebar-action-btn"
                        onClick={(e) => { e.stopPropagation(); startRename(chat); }}
                        title="Rename"
                      >
                        {EDIT_ICON}
                      </button>
                      <button
                        className="sidebar-action-btn danger"
                        onClick={(e) => { e.stopPropagation(); onDeleteChat(chat.thread_id); }}
                        title="Delete"
                      >
                        {TRASH_ICON}
                      </button>
                    </div>
                  </>
                )}
              </li>
            ))}
          </ul>
          {chats.length === 0 && (
            <div className="sidebar-empty">
              <p>No conversations yet</p>
              <p className="sidebar-empty-hint">Start a new chat to begin</p>
            </div>
          )}
        </div>
      )}

      {/* Sidebar Footer with User Profile and Logout */}
      {!collapsed ? (
        <div className="sidebar-footer">
          <div className="sidebar-user-pill">
            <div className="sidebar-user-avatar">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.7 0 5-2.3 5-5s-2.3-5-5-5S7 4.3 7 7s2.3 5 5 5zm0 2c-3.3 0-10 1.7-10 5v2h20v-2c0-3.3-6.7-5-10-5z" />
              </svg>
            </div>
            <span className="sidebar-username" title={username || "User"}>
              {username || "User"}
            </span>
          </div>
          <button
            className="sidebar-logout-btn"
            onClick={onLogout}
            title="Log out of Atlas Agent"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            <span>Log out</span>
          </button>
        </div>
      ) : (
        <div className="sidebar-collapsed-footer">
          <button
            className="sidebar-action-btn danger"
            onClick={onLogout}
            title={`Log out (${username})`}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </button>
        </div>
      )}
    </aside>
  );
}

