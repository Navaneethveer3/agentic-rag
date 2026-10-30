import { PublicClientApplication } from "@azure/msal-browser";
import { getAuthConfig } from "./api";

const API_BASE = "http://localhost:8000";

// Fallback configuration if backend config is unavailable
const FALLBACK_CLIENT_ID = "7374bd15-ba19-4a5b-982e-c5eb3de952de";
const FALLBACK_TENANT_ID = "30804f70-e0ed-4f10-ba63-19d50fb0c227";

let msalInstance = null;

export async function initMsal() {
  if (msalInstance) return msalInstance;

  let clientId = FALLBACK_CLIENT_ID;
  let tenantId = FALLBACK_TENANT_ID;

  try {
    const config = await getAuthConfig();
    if (config?.client_id) clientId = config.client_id;
    if (config?.tenant_id) tenantId = config.tenant_id;
  } catch (err) {
    console.warn("Could not fetch remote auth config, using defaults:", err);
  }

  // Clear any hung interaction state from previous sessions
  try {
    sessionStorage.removeItem("msal.interaction.status");
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i);
      if (key && key.includes("interaction.status")) {
        sessionStorage.removeItem(key);
      }
    }
  } catch (_) {}

  const msalConfig = {
    auth: {
      clientId: clientId,
      authority: `https://login.microsoftonline.com/${tenantId}`,
      redirectUri: window.location.origin,
    },
    cache: {
      cacheLocation: "localStorage",
      storeAuthStateInCookie: false,
    },
    system: {
      windowHashTimeout: 9000,
      iframeHashTimeout: 9000,
      loadFrameTimeout: 9000,
    },
  };

  msalInstance = new PublicClientApplication(msalConfig);
  await msalInstance.initialize();
  return msalInstance;
}

// Scopes matching auth/entra_auth.py
export const LOGIN_REQUEST = {
  scopes: ["User.Read"],
};

/**
 * Full page redirect to Microsoft Entra ID login page.
 * Passes the entered username as loginHint so Microsoft pre-fills it.
 */
export async function loginWithMicrosoftRedirect(loginHint = "") {
  try {
    sessionStorage.removeItem("msal.interaction.status");
  } catch (_) {}

  const instance = await initMsal();
  const request = {
    scopes: ["User.Read"],
  };
  if (loginHint && loginHint.trim()) {
    request.loginHint = loginHint.trim();
  }
  return instance.loginRedirect(request);
}

/**
 * Handles the return from Microsoft Entra ID redirect.
 * Returns the user profile if redirected back from Microsoft, or null if normal page load.
 */
export async function handleRedirectAuth() {
  try {
    const instance = await initMsal();
    const response = await instance.handleRedirectPromise();
    if (response && response.account) {
      const username = response.account.username || response.account.name || "authenticated_user";
      const displayName = response.account.name || username;
      const token = response.idToken || response.accessToken;
      return {
        username,
        displayName,
        token,
      };
    }
  } catch (err) {
    console.error("handleRedirectAuth error:", err);
    throw err;
  }
  return null;
}

/**
 * Backend interactive SSO fallback (uses system browser loopback).
 */
export async function loginWithEntraBackend() {
  const res = await fetch(`${API_BASE}/api/auth/entra/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Backend Microsoft Entra login failed");
  }
  return res.json();
}

/**
 * Popup login fallback.
 */
export async function loginWithMicrosoftSSO(loginHint = "") {
  try {
    sessionStorage.removeItem("msal.interaction.status");
  } catch (_) {}

  let instance;
  try {
    instance = await initMsal();
  } catch (initErr) {
    console.warn("MSAL initialization failed, using backend SSO fallback:", initErr);
    return await loginWithEntraBackend();
  }

  return new Promise(async (resolve, reject) => {
    let completed = false;

    const timer = setTimeout(() => {
      if (!completed) {
        completed = true;
        reject(new Error("Login timed out or was closed. Please try again."));
      }
    }, 45000);

    try {
      const request = { ...LOGIN_REQUEST };
      if (loginHint) request.loginHint = loginHint;

      const popupPromise = instance.loginPopup(request);

      popupPromise
        .then((response) => {
          if (completed) return;
          completed = true;
          clearTimeout(timer);

          const account = response.account;
          const token = response.idToken || response.accessToken;
          const username = account.username || account.name || "authenticated_user";
          const displayName = account.name || username;

          resolve({
            username,
            displayName,
            token,
          });
        })
        .catch(async (popupErr) => {
          if (completed) return;
          console.warn("Browser MSAL popup encountered an error:", popupErr);

          if (
            popupErr.errorCode === "user_cancelled" ||
            (popupErr.name === "BrowserAuthError" && popupErr.message?.includes("user_cancelled"))
          ) {
            completed = true;
            clearTimeout(timer);
            return reject(new Error("Login was cancelled."));
          }

          try {
            console.log("Attempting backend Entra ID login fallback...");
            const backendUser = await loginWithEntraBackend();
            completed = true;
            clearTimeout(timer);
            resolve({
              username: backendUser.username,
              displayName: backendUser.name || backendUser.username,
              token: null,
            });
          } catch (backendErr) {
            completed = true;
            clearTimeout(timer);
            reject(
              new Error(
                popupErr.message || backendErr.message || "Microsoft SSO authentication failed. Please try again."
              )
            );
          }
        });
    } catch (err) {
      if (!completed) {
        completed = true;
        clearTimeout(timer);
        reject(err);
      }
    }
  });
}

export async function logoutMicrosoftSSO() {
  try {
    const instance = await initMsal();
    const accounts = instance.getAllAccounts();
    if (accounts.length > 0) {
      await instance.logoutPopup({
        account: accounts[0],
      });
    }
  } catch (err) {
    console.warn("SSO popup logout error (local session will still be cleared):", err);
  } finally {
    try {
      localStorage.removeItem("atlas_token");
      localStorage.removeItem("atlas_username");
      localStorage.removeItem("atlas_display_name");
      sessionStorage.clear();
    } catch (_) {}
  }
}
