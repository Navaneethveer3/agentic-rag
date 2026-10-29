import os
from dotenv import load_dotenv
import msal

load_dotenv()

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = ["User.Read"]

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
        result = app.acquire_token_interactive(scopes=SCOPES)
    
    if "access_token" in result:
        claims = result.get("id_token_claims", {})
        user_info = {
            "username": claims.get("preferred_username") or claims.get("upn") or claims.get("sub"),
            "name" : claims.get("name"),
            "oid" : claims.get("oid"),
        }

        print(f"Successfully authenticated as : {user_info["name"]}({user_info["username"]})")
        return user_info
    else:
        error = result.get("error_description") or result.get("error")
        raise PermissionError(f"Authentication failed : {error}")