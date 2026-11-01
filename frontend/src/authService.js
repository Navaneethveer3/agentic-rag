import { PublicClientApplication } from "@azure/msal-browser";

// Azure App Registration: Agentic-RAG-System
const CLIENT_ID = import.meta.env.VITE_AZURE_CLIENT_ID || "7374bd15-ba19-4a5b-982e-c5eb3de952de";
const TENANT_ID = import.meta.env.VITE_AZURE_TENANT_ID || "30804f70-e0ed-4f10-ba63-19d50fb0c227";

const SCOPES = ["User.Read"];

let msalInstance = null;
let msalInitPromise = null;

/**
 * Initialize and return the singleton MSAL instance.
 */
export async function initMsal() {
  if (msalInstance) return msalInstance;
  if (msalInitPromise) return msalInitPromise;

  msalInitPromise = (async () => {
    const config = {
      auth: {
        clientId: CLIENT_ID,
        authority: `https://login.microsoftonline.com/${TENANT_ID}`,
        redirectUri: window.location.origin,
        postLogoutRedirectUri: window.location.origin,
        navigateToLoginRequestUrl: false,
      },
      cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false,
      },
    };

    const instance = new PublicClientApplication(config);
    await instance.initialize();
    msalInstance = instance;
    return instance;
  })();

  return msalInitPromise;
}

/**
 * Handles the return from Microsoft Entra ID redirect in the same tab.
 * Extracts tokens and user profile without opening any popups or new windows.
 */
export async function handleRedirectAuth() {
  const instance = await initMsal();

  try {
    const response = await instance.handleRedirectPromise();
    if (response && response.account) {
      return extractAccountInfo(response);
    }
  } catch (err) {
    console.error("handleRedirectPromise error:", err);
  }

  // Check cached accounts if already logged in
  const accounts = instance.getAllAccounts();
  if (accounts.length > 0) {
    const acc = accounts[0];
    return {
      username: acc.username || acc.name,
      displayName: acc.name || acc.username,
      token: localStorage.getItem("atlas_token") || null,
    };
  }

  return null;
}

/**
 * Single-page redirect login: Current tab navigates to Microsoft Entra ID.
 * ZERO popups, ZERO new tabs.
 */
export async function loginWithMicrosoftRedirect(loginHint = "") {
  try {
    sessionStorage.removeItem("msal.interaction.status");
    localStorage.removeItem("msal.interaction.status");
  } catch (_) {}

  const instance = await initMsal();

  const request = {
    scopes: SCOPES,
    prompt: "select_account",
    redirectUri: window.location.origin,
  };
  if (loginHint && loginHint.trim()) {
    request.loginHint = loginHint.trim();
  }

  // Navigates the current page to Microsoft Entra ID
  return instance.loginRedirect(request);
}

/**
 * Clean logout: clears MSAL accounts and local storage.
 * Stays on the same page in the current tab.
 */
export async function logoutUser() {
  try {
    const instance = await initMsal();
    const accounts = instance.getAllAccounts();
    for (const acc of accounts) {
      await instance.clearCache({ account: acc }).catch(() => {});
    }
  } catch (err) {
    console.warn("Logout notice:", err);
  } finally {
    localStorage.removeItem("atlas_token");
    localStorage.removeItem("atlas_username");
    sessionStorage.clear();
  }
}

function extractAccountInfo(response) {
  const account = response.account;
  const token = response.idToken || response.accessToken || null;
  const username = account.username || account.name || "authenticated_user";
  const displayName = account.name || username;
  return { username, displayName, token };
}
