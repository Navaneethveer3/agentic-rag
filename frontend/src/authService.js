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
        navigateToLoginRequestUrl: false, // Critical for popups: prevents popup from navigating to home page
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
 * Login: Opens Microsoft Entra ID popup. User enters their Microsoft credentials.
 * Returns { username, displayName, token } on success.
 * Falls back to redirect if popups are blocked.
 */
export async function loginWithMicrosoft(loginHint = "") {
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
  if (loginHint) request.loginHint = loginHint;

  try {
    const response = await instance.loginPopup(request);
    return extractAccountInfo(response);
  } catch (err) {
    if (
      err.errorCode === "user_cancelled" ||
      err.name === "BrowserAuthError" && err.message?.includes("user_cancelled")
    ) {
      throw new Error("Microsoft sign-in was cancelled.");
    }
    console.warn("Popup blocked or failed, using redirect fallback:", err.errorCode || err.message);
    await instance.loginRedirect(request);
    return null; // Page will redirect
  }
}

/**
 * Check if the user is returning from a redirect login or has an existing session.
 * Call once on app mount. Returns account info or null.
 */
export async function checkExistingSession() {
  const instance = await initMsal();

  // 1. Check if returning from a full-page redirect
  try {
    const redirectResponse = await instance.handleRedirectPromise();
    if (redirectResponse && redirectResponse.account) {
      return extractAccountInfo(redirectResponse);
    }
  } catch (err) {
    console.warn("Redirect processing notice:", err);
  }

  // 2. Check active cached accounts
  const accounts = instance.getAllAccounts();
  if (accounts.length > 0) {
    try {
      const response = await instance.acquireTokenSilent({
        scopes: SCOPES,
        account: accounts[0],
      });
      return extractAccountInfo(response);
    } catch {
      const acc = accounts[0];
      return {
        username: acc.username || acc.name,
        displayName: acc.name || acc.username,
        token: localStorage.getItem("atlas_token") || null,
      };
    }
  }
  return null;
}

/**
 * Logout: Clears MSAL session and local storage.
 */
export async function logoutFromMicrosoft() {
  try {
    const instance = await initMsal();
    const accounts = instance.getAllAccounts();
    if (accounts.length > 0) {
      await instance.logoutPopup({
        account: accounts[0],
        mainWindowRedirectUri: window.location.origin,
      });
    }
  } catch (err) {
    console.warn("Logout notice:", err.message);
  } finally {
    localStorage.removeItem("atlas_token");
    localStorage.removeItem("atlas_username");
    sessionStorage.clear();
  }
}

/**
 * Extract standardized user info from an MSAL auth response.
 */
function extractAccountInfo(response) {
  const account = response.account;
  const token = response.idToken || response.accessToken || null;
  const username = account.username || account.name || "authenticated_user";
  const displayName = account.name || username;
  return { username, displayName, token };
}
