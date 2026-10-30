import os
from dotenv import load_dotenv
import msal

load_dotenv()

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

SUCCESS_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Authentication Successful</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0B1220;
      color: #F8FAFC;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      text-align: center;
    }}
    .box {{
      background: #111827;
      border: 1px solid #1E293B;
      padding: 36px 48px;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      max-width: 420px;
    }}
    .check {{
      font-size: 36px;
      color: #38BDF8;
      margin-bottom: 12px;
    }}
    h1 {{ color: #F8FAFC; font-size: 22px; margin: 0 0 8px 0; }}
    p {{ color: #94A3B8; font-size: 14px; margin: 0; }}
  </style>
</head>
<body>
  <div class="box">
    <div class="check">&#10004;</div>
    <h1>Authentication Successful</h1>
    <p>Closing login tab and returning to the homepage...</p>
  </div>
  <script>
    try {{
      window.opener = null;
      window.open('', '_self', '');
      window.close();
    }} catch (e) {{}}
    setTimeout(function() {{
      window.location.href = "{FRONTEND_URL}";
    }}, 400);
  </script>
</body>
</html>
"""

def login_with_entra() -> dict:
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )

    accounts = app.get_accounts()

    result = None
    
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if not result:
        print("\nOpening browser for Microsoft Entra ID login...")
        result = app.acquire_token_interactive(
            scopes=SCOPES,
            success_template=SUCCESS_HTML,
        )
    
    if "access_token" in result:
        claims = result.get("id_token_claims", {})
        user_info = {
            "username": claims.get("preferred_username") or claims.get("upn") or claims.get("sub"),
            "name" : claims.get("name"),
            "oid" : claims.get("oid"),
        }

        print(f"Successfully authenticated as : {user_info['name']}({user_info['username']})")
        return user_info
    else:
        error = result.get("error_description") or result.get("error")
        raise PermissionError(f"Authentication failed : {error}")
