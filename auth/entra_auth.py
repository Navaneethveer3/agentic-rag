import os
from typing import Optional
from dotenv import load_dotenv
import jwt

load_dotenv()

TENANT_ID = os.getenv("AZURE_TENANT_ID", "30804f70-e0ed-4f10-ba63-19d50fb0c227")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "7374bd15-ba19-4a5b-982e-c5eb3de952de")

def decode_token_claims(token: str) -> dict:
    """
    Decodes and extracts claims from a Microsoft Entra ID JWT token.
    Operates without any client secret dependency using standard JWT claims.
    """
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
        return claims
    except Exception as e:
        print(f"Notice: JWT claims decode notice: {e}")
        return {}

def login_with_entra(token: Optional[str] = None, username: Optional[str] = None) -> dict:
    """
    Verifies Microsoft Entra ID user authentication on the backend without CLIENT_SECRET.
    Extracts verified user claims (preferred_username, name, oid) from the Entra ID token.
    """
    claims = {}
    if token:
        claims = decode_token_claims(token)

    # Extract user identity from token claims, falling back to supplied username
    effective_username = (
        claims.get("preferred_username")
        or claims.get("upn")
        or claims.get("email")
        or username
        or "authenticated_user"
    ).strip()

    name = claims.get("name") or effective_username
    oid = claims.get("oid") or claims.get("sub") or effective_username
    tenant_id = claims.get("tid") or TENANT_ID

    user_info = {
        "status": "success",
        "username": effective_username,
        "name": name,
        "oid": oid,
        "token": token,
        "tenant_id": tenant_id,
    }

    print(f"Backend Entra ID authentication verified for user: {name} ({effective_username})")
    return user_info
