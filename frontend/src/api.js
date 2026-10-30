const API_BASE = "http://localhost:8000";

function getHeaders(username, token = null) {
  const headers = {
    "Content-Type": "application/json",
  };
  const activeToken = token || localStorage.getItem("atlas_token");
  if (activeToken) {
    headers["Authorization"] = `Bearer ${activeToken}`;
  }
  const activeUser = username || localStorage.getItem("atlas_username");
  if (activeUser) {
    headers["X-Username"] = activeUser;
  }
  return headers;
}

export async function loginWithBackend(username) {
  const res = await fetch(`${API_BASE}/api/auth/entra/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(username ? { "X-Username": username } : {}),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Microsoft Entra ID authentication failed on backend");
  }
  return res.json();
}

export async function healthCheck() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error("API unreachable");
  return res.json();
}

export async function getAuthConfig() {
  const res = await fetch(`${API_BASE}/api/auth/config`);
  if (!res.ok) throw new Error("Failed to fetch auth config");
  return res.json();
}



export async function createChat(username, title = "New Chat") {
  const res = await fetch(`${API_BASE}/api/chats`, {
    method: "POST",
    headers: getHeaders(username),
    body: JSON.stringify({ title }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to create chat");
  }
  return res.json();
}

export async function getAllChats(username) {
  const res = await fetch(`${API_BASE}/api/chats`, {
    headers: getHeaders(username),
  });
  if (!res.ok) throw new Error("Failed to load chats");
  return res.json();
}

export async function getChat(username, threadId) {
  const res = await fetch(`${API_BASE}/api/chats/${threadId}`, {
    headers: getHeaders(username),
  });
  if (!res.ok) throw new Error("Failed to load chat");
  return res.json();
}

export async function getChatMessages(username, threadId) {
  const res = await fetch(`${API_BASE}/api/chats/${threadId}/messages`, {
    headers: getHeaders(username),
  });
  if (!res.ok) throw new Error("Failed to load chat messages");
  return res.json();
}

export async function updateChat(username, threadId, title) {
  const res = await fetch(`${API_BASE}/api/chats/${threadId}`, {
    method: "PATCH",
    headers: getHeaders(username),
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error("Failed to update chat");
  return res.json();
}

export async function deleteChat(username, threadId) {
  const res = await fetch(`${API_BASE}/api/chats/${threadId}`, {
    method: "DELETE",
    headers: getHeaders(username),
  });
  if (!res.ok) throw new Error("Failed to delete chat");
  return res.json();
}

export async function deleteAllChats(username) {
  const res = await fetch(`${API_BASE}/api/chats`, {
    method: "DELETE",
    headers: getHeaders(username),
  });
  if (!res.ok) throw new Error("Failed to delete all chats");
  return res.json();
}

export async function sendMessage(username, threadId, query, modelName = null) {
  const body = { query };
  if (modelName) body.model_name = modelName;

  const res = await fetch(`${API_BASE}/api/chats/${threadId}/messages`, {
    method: "POST",
    headers: getHeaders(username),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Agent execution failed");
  }
  return res.json();
}

export async function parseDocuments(username, files) {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  const headers = {};
  const activeToken = localStorage.getItem("atlas_token");
  if (activeToken) {
    headers["Authorization"] = `Bearer ${activeToken}`;
  }
  const activeUser = username || localStorage.getItem("atlas_username");
  if (activeUser) {
    headers["X-Username"] = activeUser;
  }

  const res = await fetch(`${API_BASE}/api/documents/parse`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Document parsing failed");
  }
  return res.json();
}
