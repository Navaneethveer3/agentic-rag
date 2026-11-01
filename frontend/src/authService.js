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
        navigateToLoginRequestUrl: true,
      },
      cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false,
      },
    };

    const instance = new PublicClientApplication(config);
    await instance.initialize();

    // Process any pending redirect response (in case redirect flow was used)
    await instance.handleRedirectPromise().catch(() => {});

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
  const instance = await initMsal();

  const request = { scopes: SCOPES, prompt: "select_account" };
  if (loginHint) request.loginHint = loginHint;

  try {
    // Try popup first — keeps SPA state, no page reload
    const response = await instance.loginPopup(request);
    return extractAccountInfo(response);
  } catch (err) {
    // User explicitly cancelled → re-throw
    if (err.errorCode === "user_cancelled") {
      throw new Error("Sign-in was cancelled.");
    }
    // Popup blocked → fall back to full-page redirect
    console.warn("Popup blocked, using redirect:", err.errorCode || err.message);
    await instance.loginRedirect(request);
    return null; // page will redirect; caller should exit
  }
}

/**
 * Check if the user is returning from a redirect login.
 * Call once on app mount. Returns account info or null.
 */
export async function checkExistingSession() {
  const instance = await initMsal();

  // Check MSAL cache for already-signed-in accounts
  const accounts = instance.getAllAccounts();
  if (accounts.length > 0) {
    try {
      // Silently acquire a fresh token to verify the session is still valid
      const response = await instance.acquireTokenSilent({
        scopes: SCOPES,
        account: accounts[0],
      });
      return extractAccountInfo(response);
    } catch {
      // Silent token failed → session expired, user needs to login again
      return null;
    }
  }
  return null;
}

/**
 * Logout: Clears MSAL session and local storage.
 * Uses account.logoutHint to skip Microsoft's "which account?" screen.
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
