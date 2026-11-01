import { PublicClientApplication } from "@azure/msal-browser";
import { getAuthConfig } from "./api";

// Fallback configuration from Azure App Registration: Agentic-RAG-System
const FALLBACK_CLIENT_ID = "7374bd15-ba19-4a5b-982e-c5eb3de952de";
const FALLBACK_TENANT_ID = "30804f70-e0ed-4f10-ba63-19d50fb0c227";

let msalInstance = null;
let msalInitPromise = null;

export async function initMsal() {
  if (msalInstance) return msalInstance;
  if (msalInitPromise) return msalInitPromise;

  msalInitPromise = (async () => {
    let clientId = import.meta.env.VITE_AZURE_CLIENT_ID || FALLBACK_CLIENT_ID;
    let tenantId = import.meta.env.VITE_AZURE_TENANT_ID || FALLBACK_TENANT_ID;

    try {
      const config = await getAuthConfig();
      if (config?.client_id) clientId = config.client_id;
      if (config?.tenant_id) tenantId = config.tenant_id;
    } catch (err) {
      console.warn("Using default Azure Entra ID configuration:", err);
    }

    const msalConfig = {
      auth: {
        clientId: clientId,
        authority: `https://login.microsoftonline.com/${tenantId}`,
        redirectUri: window.location.origin,
        postLogoutRedirectUri: window.location.origin,
        navigateToLoginRequestUrl: false,
      },
      cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false, // Prevents cross-site cookie restrictions in modern browsers
      },
      system: {
        windowHashTimeout: 9000,
        iframeHashTimeout: 9000,
        loadFrameTimeout: 9000,
      },
    };

    const instance = new PublicClientApplication(msalConfig);
    await instance.initialize();
    msalInstance = instance;
    return instance;
  })();

  return msalInitPromise;
}

export const LOGIN_REQUEST = {
  scopes: ["User.Read"],
};

/**
 * Cleanly authenticates user with Microsoft Entra ID.
 * Attempts a popup window first (retains SPA state with zero page reloads).
 * Falls back to full-page redirect if the browser blocks popups.
 */
export async function loginWithMicrosoft(loginHint = "") {
  try {
    sessionStorage.removeItem("msal.interaction.status");
  } catch (_) {}

  const instance = await initMsal();
  const request = {
    scopes: ["User.Read"],
    prompt: "select_account",
  };
  if (loginHint && loginHint.trim()) {
    request.loginHint = loginHint.trim();
  }

  try {
    const response = await instance.loginPopup(request);
    const account = response.account;
    const token = response.idToken || response.accessToken;
    const username = account.username || account.name || "authenticated_user";
    const displayName = account.name || username;

    return {
      username,
      displayName,
      token,
    };
  } catch (popupErr) {
    console.warn("Popup authentication notice:", popupErr);

    // If user explicitly closed or cancelled the popup, do not force a redirect
    if (
      popupErr.errorCode === "user_cancelled" ||
      popupErr.name === "BrowserAuthError" && popupErr.message?.includes("user_cancelled")
    ) {
      throw new Error("Microsoft sign-in was cancelled.");
    }

    // If popup was blocked by browser or failed, fallback to redirect
    console.log("Falling back to Microsoft redirect authentication...");
    await instance.loginRedirect(request);
    return null;
  }
}

/**
 * Handles the return from Microsoft Entra ID redirect (if redirect was used).
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

    // Check if account already cached
    const accounts = instance.getAllAccounts();
    if (accounts && accounts.length > 0) {
      const account = accounts[0];
      const username = account.username || account.name || "authenticated_user";
      const displayName = account.name || username;
      return {
        username,
        displayName,
        token: null,
      };
    }
  } catch (err) {
    console.error("handleRedirectAuth error:", err);
  }
  return null;
}

/**
 * Logs out user and cleans up auth storage.
 */
export async function logoutFromMicrosoft() {
  try {
    const instance = await initMsal();
    const accounts = instance.getAllAccounts();
    if (accounts.length > 0) {
      await instance.logoutPopup({
        account: accounts[0],
      });
    }
  } catch (err) {
    console.warn("SSO logout notice:", err);
  } finally {
    try {
      localStorage.removeItem("atlas_token");
      localStorage.removeItem("atlas_username");
      localStorage.removeItem("atlas_display_name");
      sessionStorage.clear();
    } catch (_) {}
  }
}
