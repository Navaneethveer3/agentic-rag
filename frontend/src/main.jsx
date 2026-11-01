import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { initMsal } from './authService.js'

// Detect if this window is an MSAL authentication popup
const isMsalPopup = typeof window !== "undefined" && window.opener && window.opener !== window;

if (isMsalPopup) {
  // We are inside the MSAL authentication popup window.
  // DO NOT mount the React application here!
  // Simply process the token hash and close this popup window immediately.
  document.body.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:center;height:100vh;background:#0B1220;color:#38BDF8;font-family:system-ui,-apple-system,sans-serif;">
      <div style="text-align:center;">
        <div style="width:36px;height:36px;border:3px solid #38BDF8;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 16px;"></div>
        <p style="font-size:15px;margin:0;color:#94A3B8;">Completing Microsoft authentication...</p>
      </div>
      <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
    </div>
  `;

  initMsal()
    .then((instance) => instance.handleRedirectPromise())
    .then(() => {
      setTimeout(() => {
        try {
          window.close();
        } catch (_) {}
      }, 100);
    })
    .catch((err) => {
      console.warn("Popup redirect promise notice:", err);
      try {
        window.close();
      } catch (_) {}
    });
} else {
  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
}
