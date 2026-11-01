import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { handleRedirectAuth } from './authService.js'
import { loginWithBackend } from './api.js'

async function bootstrap() {
  // If returning from Microsoft redirect in this same tab, process it BEFORE mounting App
  try {
    const authResult = await handleRedirectAuth();
    if (authResult && authResult.username) {
      localStorage.setItem("atlas_username", authResult.username);
      if (authResult.token) {
        localStorage.setItem("atlas_token", authResult.token);
      }
      // Register verified session with backend
      loginWithBackend(authResult.username, authResult.token).catch((e) =>
        console.warn("Backend session record notice:", e)
      );
      // Clean up the authorization code hash from the address bar
      if (window.location.hash) {
        window.history.replaceState(null, "", window.location.pathname);
      }
    }
  } catch (err) {
    console.warn("Auth initialization notice:", err);
  }

  // Mount the React application
  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
}

bootstrap();
